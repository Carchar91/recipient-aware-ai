#!/usr/bin/env python3
"""Build/check a deterministic skills-only plugin; never installs or uploads it."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys
import zipfile
from xml.etree import ElementTree

from build_skills import products
from package_release import archive

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = 'https://agent-plugins.org/schemas/1.0.0/plugin.schema.json'
NAMES = ('profiler', 'profiler-plus', 'dopamine-hooks', 'reverse', 'rail')
NOTICES = ('LICENSE', 'NOTICE', 'THIRD_PARTY_NOTICES.md', 'RESPONSIBLE_USE.md', 'LIMITATIONS.md')


def entries():
    """Allowlist components; copy existing skills byte-for-byte, never regenerate."""
    generated = dict(products())
    files = {}
    for name, expected in generated.items():
        path = ROOT / name
        if path.is_symlink() or path.read_text() != expected:
            raise ValueError(f'Canonical skill drift or symlink: {name}')
        files[name] = path.read_bytes()
    for name in ('plugin.json', 'README.md', 'EVALUATION.md', 'assets/icon.svg'):
        path = ROOT / 'plugin' / name
        if path.is_symlink():
            raise ValueError(f'Symlink: {path}')
        files[name] = path.read_bytes()
    for name in NOTICES:
        path = ROOT / name
        if path.is_symlink():
            raise ValueError(f'Symlink: {path}')
        files[name] = path.read_bytes()
    manifest = json.loads(files['plugin.json'])
    compatibility = {key: value for key, value in manifest.items() if key not in ('$schema', 'extensions')}
    compatibility['skills'] = './skills/'
    # CLI 0.146.1 needs an overlay; supportURL is not accepted by its validator.
    compatibility['interface'] = {key: value for key, value in manifest['extensions']['com.openai']['interface'].items() if key != 'supportURL'}
    files['.codex-plugin/plugin.json'] = (json.dumps(compatibility, indent=2) + '\n').encode()
    return files


def require(condition, message):
    if not condition:
        raise ValueError(message)


def validate(files, schema_path=None):
    manifest = json.loads(files['plugin.json'])
    require(manifest['$schema'] == SCHEMA, "Invalid plugin metadata: manifest['$schema'] == SCHEMA")
    require(manifest['name'] == 'recipient-aware-ai', "Invalid plugin metadata: manifest['name'] == 'recipient-aware-ai'")
    require(manifest['version'] == (ROOT / 'VERSION').read_text().strip(), "Invalid plugin metadata: manifest['version'] == (ROOT / 'VERSION').read_text().strip()")
    require(re.fullmatch('\\d+\\.\\d+\\.\\d+(?:-[0-9A-Za-z.-]+)?(?:\\+[0-9A-Za-z.-]+)?', manifest['version']), "Invalid plugin metadata: re.fullmatch('\\\\d+\\\\.\\\\d+\\\\.\\\\d+(?:-[0-9A-Za-z.-]+)?(?:\\\\+[0-9A-Za-z.-]+)?', manifest['version'])")
    require(manifest['author']['name'] == 'Eugene Prudchenko', "Invalid plugin metadata: manifest['author']['name'] == 'Eugene Prudchenko'")
    require(manifest['license'] == 'Apache-2.0', "Invalid plugin metadata: manifest['license'] == 'Apache-2.0'")
    require(set(manifest) <= {'$schema', 'name', 'version', 'description', 'author', 'homepage', 'repository', 'license', 'keywords', 'extensions'}, "Invalid plugin metadata: set(manifest) <= {'$schema', 'name', 'version', 'description', 'author', 'homepage', 'repository', 'license', 'keywords', 'extensions'}")
    settings = manifest['extensions']['com.openai']
    require(set(settings) == {'interface', 'review', 'publication'}, "Invalid plugin metadata: set(settings) == {'interface', 'review', 'publication'}")
    interface = settings['interface']
    for key, limit in [('displayName', 30), ('shortDescription', 30), ('longDescription', 4000), ('developerName', 80)]:
        require(isinstance(interface[key], str) and 0 < len(interface[key]) <= limit, key)
    require(interface['category'] == 'Communication', "Invalid plugin metadata: interface['category'] == 'Communication'")
    require(interface['capabilities'] == [], "Invalid plugin metadata: interface['capabilities'] == []")
    prompts = interface['defaultPrompt']
    require(len(prompts) <= 3 and len(set(prompts)) == len(prompts), 'Invalid plugin metadata: len(prompts) <= 3 and len(set(prompts)) == len(prompts)')
    require(all((isinstance(p, str) and 0 < len(p) <= 128 and ('\n' not in p) for p in prompts)), "Invalid plugin metadata: all((isinstance(p, str) and 0 < len(p) <= 128 and ('\\n' not in p) for p in prompts))")
    require(0 < len(settings['review']['prompts']) <= 20, "Invalid plugin metadata: 0 < len(settings['review']['prompts']) <= 20")
    require(all((isinstance(p, str) and 0 < len(p) <= 4000 for p in settings['review']['prompts'])), "Invalid plugin metadata: all((isinstance(p, str) and 0 < len(p) <= 4000 for p in settings['review']['prompts']))")
    for key in ('websiteURL', 'supportURL'):
        require(interface[key].startswith('https://') and len(interface[key]) <= 1024, "Invalid plugin metadata: interface[key].startswith('https://') and len(interface[key]) <= 1024")
    for key in ('logo', 'composerIcon'):
        require(interface[key] == './assets/icon.svg', "Invalid plugin metadata: interface[key] == './assets/icon.svg'")
        require(interface[key][2:] in files, 'Invalid plugin metadata: interface[key][2:] in files')
    svg = ElementTree.fromstring(files['assets/icon.svg'])
    require(svg.attrib['width'] == svg.attrib['height'] == '256', "Invalid plugin metadata: svg.attrib['width'] == svg.attrib['height'] == '256'")
    require(len(files['assets/icon.svg']) <= 5 * 1024 * 1024, "Invalid plugin metadata: len(files['assets/icon.svg']) <= 5 * 1024 * 1024")
    require(sorted((p.split('/')[1] for p in files if p.endswith('/SKILL.md'))) == sorted(NAMES), "Invalid plugin metadata: sorted((p.split('/')[1] for p in files if p.endswith('/SKILL.md'))) == sorted(NAMES)")
    require(not any((p.startswith(('.app', 'mcp.', '.mcp', 'hooks/', 'scripts/')) for p in files)), "Invalid plugin metadata: not any((p.startswith(('.app', 'mcp.', '.mcp', 'hooks/', 'scripts/')) for p in files))")
    for name in NAMES:
        require(f'name: {name}\n' in files[f'skills/{name}/SKILL.md'].decode(), "Invalid plugin metadata: f'name: {name}\\n' in files[f'skills/{name}/SKILL.md'].decode()")
        require('allow_implicit_invocation: false' in files[f'skills/{name}/agents/openai.yaml'].decode(), "Invalid plugin metadata: 'allow_implicit_invocation: false' in files[f'skills/{name}/agents/openai.yaml'].decode()")
        for filename in ('input.schema.json', 'output.schema.json'):
            json.loads(files[f'skills/{name}/references/{filename}'])
    compatibility = json.loads(files['.codex-plugin/plugin.json'])
    require(compatibility['skills'] == './skills/', "Invalid plugin metadata: compatibility['skills'] == './skills/'")
    for key in ('name', 'version', 'description', 'author', 'homepage', 'repository', 'license', 'keywords'):
        require(compatibility[key] == manifest[key], key)
    require(compatibility['interface'] == {key: value for key, value in interface.items() if key != 'supportURL'}, "Invalid plugin metadata: compatibility['interface'] == {key: value for key, value in interface.items() if key != 'supportURL'}")
    if schema_path:
        import jsonschema
        jsonschema.Draft202012Validator(json.loads(schema_path.read_text())).validate(manifest)
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    choice = parser.add_mutually_exclusive_group(required=True)
    choice.add_argument('--output', type=Path, help='ZIP path; existing files are not overwritten')
    choice.add_argument('--check', type=Path, help='Check an existing ZIP against the current allowed source files')
    parser.add_argument('--schema', type=Path, help='Locally downloaded official Agent Plugins schema for JSON Schema validation')
    parser.add_argument('--test-marketplace', type=Path, help='Also stage a new local-only test marketplace; never registers or installs it')
    args = parser.parse_args()
    files = entries()
    manifest = validate(files, args.schema)
    prefix = manifest['name'] + '/'
    expected = {prefix + name: blob for name, blob in files.items()}
    target = args.output or args.check
    if args.output:
        if target.exists() or target.is_symlink():
            parser.error(f'Output already exists: {target}')
        target.parent.mkdir(parents=True, exist_ok=True)
        archive(target, list(expected.items()))
    with zipfile.ZipFile(target) as bundle:
        if len(bundle.namelist()) != len(expected) or set(bundle.namelist()) != set(expected):
            raise ValueError('Archive inventory differs from the skills-only allowlist')
        if bundle.testzip() is not None:
            raise ValueError('Archive CRC error')
        for name, blob in expected.items():
            if bundle.read(name) != blob:
                raise ValueError(f'Archive source mismatch: {name}')
    if args.test_marketplace:
        market = args.test_marketplace
        market.mkdir(parents=True, exist_ok=False)
        for name, blob in files.items():
            path = market / 'plugins' / manifest['name'] / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(blob)
        catalog = {
            'name': 'recipient-aware-ai-local-test',
            'interface': {'displayName': 'Recipient-Aware AI Local Test'},
            'plugins': [{
                'name': manifest['name'],
                'source': {'source': 'local', 'path': './plugins/' + manifest['name']},
                'policy': {'installation': 'AVAILABLE', 'authentication': 'ON_INSTALL'},
                'category': 'Communication',
            }],
        }
        path = market / '.agents/plugins/marketplace.json'
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(catalog, indent=2) + '\n')
    print(json.dumps({
        'status': 'PASS', 'archive': str(target),
        'sha256': hashlib.sha256(target.read_bytes()).hexdigest(),
        'files': len(expected), 'skills': list(NAMES),
        'skills_and_notices': 'byte-identical to current repository sources',
        'official_schema_validation': 'PASS' if args.schema else 'NOT_RUN; use --schema with a downloaded official schema',
        'installation': 'NOT_PERFORMED_BY_THIS_COMMAND',
        'publication': 'NOT_PERFORMED',
    }, indent=2))
    return 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (AssertionError, KeyError, ValueError, OSError, zipfile.BadZipFile) as error:
        print(f'Plugin validation failed: {error}', file=sys.stderr)
        raise SystemExit(1)
