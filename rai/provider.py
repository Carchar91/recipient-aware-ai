"""Opt-in OpenAI Responses adapter; no implicit network calls, tools or retries."""
from __future__ import annotations
import json
import os
import urllib.request
import urllib.error
from typing import Any
from .core import compile_case, schema, strict_json, ContractError, validate_output, digest

ENDPOINT = 'https://api.openai.com/v1/responses'


def wire_schema(node: Any) -> Any:
    """Keep the basic structured-output subset; stricter constraints stay local."""
    if isinstance(node, list):
        return [wire_schema(x) for x in node]
    if isinstance(node, dict):
        return {k: wire_schema(v) for k,v in node.items()
                if k not in ('$schema','title','uniqueItems','minLength','minItems','maxItems','pattern')}
    return node


def make_payload(compiled: dict, model: str, max_output_tokens: int = 4096) -> dict:
    if not isinstance(model, str) or not model.strip():
        raise ContractError('Supply an explicit model ID; no model is chosen automatically.')
    if not 256 <= max_output_tokens <= 16384:
        raise ContractError('max_output_tokens must be between 256 and 16384.')
    return {'model':model,'instructions':compiled['system'],'input':compiled['user'],
            'store':False,'max_output_tokens':max_output_tokens,'truncation':'disabled',
            'text':{'format':{'type':'json_schema','name':'rai_'+compiled['protocol'].replace('-','_'),
                            'strict':True,'schema':wire_schema(schema(compiled['protocol']))}}}


def extract_answer(response: dict) -> str:
    if response.get('status') != 'completed':
        raise ContractError('Model response was not completed; do not treat partial output as valid.')
    chunks = []
    for item in response.get('output', []):
        if item.get('type') != 'message':
            continue
        for part in item.get('content', []):
            if part.get('type') == 'refusal':
                raise ContractError('Provider refusal outside the result schema; record and review it separately.')
            if part.get('type') == 'output_text':
                chunks.append(part.get('text', ''))
    if not chunks:
        raise ContractError('No assistant output_text was returned.')
    return ''.join(chunks)


def call_model(data: dict, model: str, *, arm: str = 'protocol', allow_network: bool = False,
               acknowledge_cost: bool = False, max_output_tokens: int = 4096, timeout: int = 120) -> dict:
    compiled = compile_case(data, arm)
    if not allow_network or not acknowledge_cost:
        raise ContractError('Live calls require --allow-network and --acknowledge-cost; no request sent.')
    if not data['privacy_ok']:
        raise ContractError('privacy_ok is false: this input is not authorized for model transmission.')
    key = os.environ.get('OPENAI_API_KEY', '')
    if not key:
        raise ContractError('OPENAI_API_KEY is not set; no request sent.')
    payload = make_payload(compiled, model, max_output_tokens)
    request = urllib.request.Request(ENDPOINT, data=json.dumps(payload).encode('utf-8'),
               headers={'Authorization':'Bearer '+key,'Content-Type':'application/json'}, method='POST')
    record = {'origin':'live_provider_response','provider':'OpenAI Responses API',
              'requested_model':model,'protocol':data['protocol'],'case_id':data['case_id'],'arm':arm,
              'protocol_version':compiled['protocol_version'],'input_sha256':compiled['input_sha256'],
              'prompt_sha256':compiled['prompt_sha256'],'output_schema_sha256':digest(schema(data['protocol'])),
              'max_output_tokens':max_output_tokens,'store':False,'automatic_retries':0,
              'semantic_verdict':'not_reviewed'}
    try:
        with urllib.request.urlopen(request, timeout=timeout) as reply:
            blob = reply.read(4_000_001)
        if len(blob) > 4_000_000:
            raise ContractError('Response exceeds the local size limit.')
        response = strict_json(blob.decode('utf-8'))
        record.update({'response_id':response.get('id'),'returned_model':response.get('model'),
                       'usage':response.get('usage', {})})
        answer = extract_answer(response)
        record['output_text'] = answer
        output = strict_json(answer)
        record['output'] = output
        record['contract_errors'] = validate_output(data, output)
        record['status'] = 'contract_pass' if not record['contract_errors'] else 'contract_fail'
    except urllib.error.HTTPError as exc:
        # No raw remote error body or headers: these may echo request content.
        record.update(status='transport_error',error=f'HTTP {exc.code}; no automatic retry.')
    except urllib.error.URLError:
        record.update(status='transport_error',error='Network/TLS error; no automatic retry.')
    except (TimeoutError, UnicodeDecodeError, ContractError, KeyError, TypeError, AttributeError):
        record.update(status='response_error',error='Incomplete, refused, malformed or unusable response; review local output if available. No automatic retry.')
    return record
