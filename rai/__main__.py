from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path
from .core import ROOT, PROTOCOLS, ContractError, load_json, compile_case, validate_input, validate_output, render_output
from .provider import call_model


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description='Recipient-Aware AI: explicit single-protocol reference harness.')
    sub = parser.add_subparsers(dest='command', required=True)
    comp = sub.add_parser('compile', help='Print a reproducible system/user prompt pair; never calls a model.')
    comp.add_argument('--input', required=True)
    comp.add_argument('--arm', choices=('protocol','baseline'), default='protocol')
    vi = sub.add_parser('validate-input'); vi.add_argument('--input', required=True)
    vo = sub.add_parser('validate-output'); vo.add_argument('--input', required=True); vo.add_argument('--output', required=True)
    render = sub.add_parser('render'); render.add_argument('--input', required=True); render.add_argument('--output', required=True)
    render.add_argument('--audit', action='store_true', help='Append the full operator-only machine record.')
    live = sub.add_parser('run', help='One paid model request, only with both explicit opt-in flags.')
    live.add_argument('--input', required=True); live.add_argument('--model', required=True)
    live.add_argument('--arm', choices=('protocol','baseline'), default='protocol')
    live.add_argument('--allow-network', action='store_true'); live.add_argument('--acknowledge-cost', action='store_true')
    live.add_argument('--max-output-tokens', type=int, default=4096)
    sub.add_parser('list', help='List the five independent protocol IDs.')
    args = parser.parse_args(argv)
    try:
        if args.command == 'list':
            print('\n'.join(PROTOCOLS)); return 0
        data = load_json(args.input)
        if args.command == 'compile':
            print(json.dumps(compile_case(data, args.arm), ensure_ascii=False, indent=2)); return 0
        if args.command == 'validate-input':
            errors = validate_input(data)
        elif args.command == 'validate-output':
            errors = validate_output(data, load_json(args.output))
        elif args.command == 'render':
            print(render_output(data, load_json(args.output), audit=args.audit), end=''); return 0
        elif args.command == 'run':
            record = call_model(data,args.model,arm=args.arm,allow_network=args.allow_network,
                                acknowledge_cost=args.acknowledge_cost,max_output_tokens=args.max_output_tokens)
            print(json.dumps(record,ensure_ascii=False,indent=2))
            return 0 if record['status']=='contract_pass' else 1
        else:
            raise ContractError('Unknown command.')
        print(json.dumps({'contract_pass':not errors,'errors':errors,
                          'semantic_verdict':'not_assessed_by_this_validator'},ensure_ascii=False,indent=2))
        return 1 if errors else 0
    except (ContractError, OSError, ValueError) as exc:
        print(str(exc), file=sys.stderr); return 2

if __name__=='__main__':
    raise SystemExit(main())
