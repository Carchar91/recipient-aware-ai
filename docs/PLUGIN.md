# Skills-only plugin package

Recipient-Aware AI has a **local packaging candidate**, not a public ChatGPT
plugin listing. It targets the portable [Agent Plugins format](https://developers.openai.com/plugins/build/plugins)
with root `plugin.json`, five existing skills and no MCP server. There is no
account upload or public-directory submission in this work.

## Build and check

From a source checkout, using the environment described in [Installation](INSTALLATION.md):

```sh
python tools/build_plugin.py --output /tmp/recipient-aware-ai-plugin.zip
python tools/build_plugin.py --check /tmp/recipient-aware-ai-plugin.zip
```

The output must not already exist. Choose a fresh output filename to rebuild.
The builder uses an allowlist, rejects source symlinks and existing output paths,
checks generated skills against their canonical sources, and copies those skills
without editing them. The ZIP contains one `recipient-aware-ai/` directory, 30
files, all five skills, their reference schemas and invocation metadata,
onboarding, responsible use, limitations and licence notices. A small
`EVALUATION.md` pointer keeps the bundled limitations' evidence link usable
without pretending the complete evaluation archive is part of this plugin.

For JSON Schema validation, download the [official Agent Plugins schema](https://agent-plugins.org/schemas/1.0.0/plugin.schema.json)
as a local file, then use the pinned project dependencies:

```sh
python tools/build_plugin.py --check /tmp/recipient-aware-ai-plugin.zip \
  --schema /tmp/plugin.schema.json
```

The schema checks the portable manifest. The builder also checks this package's
expected components and presentation fields. These checks do not replace the
OpenAI submission portal's metadata and skill scans.

## Choose one mode

The [packaged onboarding](../plugin/README.md) gives a short chooser for Profiler,
Profiler Plus, Dopamine Hooks, Reverse and Rail. The three starter prompts in the
manifest select a specific mode. No sixth skill, automatic setup execution or
mode chaining is added. In a host that namespaces skills, select the installed
skill from its picker and name the corresponding mode in your prompt.

## Local installation test

Checked on 2026-10-21 with **Codex CLI 0.146.1**. To stage a new, local-only test
marketplace while building a new archive:

```sh
python tools/build_plugin.py --output /tmp/recipient-aware-ai-plugin-test.zip \
  --test-marketplace /tmp/recipient-aware-ai-plugin-test-marketplace
```

Both paths must be new. In the tested isolated Codex configuration, these CLI
commands succeeded:

```sh
codex plugin marketplace add /tmp/recipient-aware-ai-plugin-test-marketplace --json
codex plugin add recipient-aware-ai@recipient-aware-ai-local-test --json
codex plugin list --json --marketplace recipient-aware-ai-local-test
```

**Isolation matters:** these commands normally install into the user's Codex
configuration. Our test supplied a pre-created temporary directory using the
CLI's documented `CODEX_HOME` environment setting only for the test subprocess.
No credentials were copied; no account plugin was created. The real user's
configuration and plugin-cache inventory were unchanged before and after.
Do not run those commands against your normal configuration merely to repeat
the verification.

Codex `plugin/read` and `skills/list` then returned the correct display name,
version `0.1.0-rc.2`, and all five enabled namespaced skills:
`recipient-aware-ai:profiler`, `recipient-aware-ai:profiler-plus`,
`recipient-aware-ai:dopamine-hooks`, `recipient-aware-ai:reverse` and
`recipient-aware-ai:rail`. The runtime reported no MCP servers, hooks or apps.
Installed files matched the final ZIP byte-for-byte. The bundled Codex plugin
validator passed, using PyYAML 6.0.3 in a separate temporary validation environment;
PyYAML is not a new project or plugin dependency.

The initial portable-only trial discovered the skills but omitted the display
metadata and version in this older CLI. Therefore the builder generates a
`.codex-plugin/plugin.json` compatibility overlay from the portable manifest.
Identity and shared presentation stay synchronized; `supportURL` remains only
in the portable manifest because the older validator rejects that overlay field.
No duplicated hand-maintained skill content is added. Current portable clients
use the root manifest and inline OpenAI settings.

This is an installation, metadata and discovery check. **No plugin model turn,
ChatGPT web/mobile invocation, native application UI, public listing or review
approval was tested.** The separate [skills CLI smoke test](SKILLS_SH.md) must not
be described as a ChatGPT plugin evaluation.

## Permissions and data

The package adds no MCP server, hooks, executable scripts, account bindings,
telemetry, storage service or send action. Skills remain explicitly invoked and
do not grant host permissions. Existing host tools and permissions still apply;
instructions cannot enforce a sandbox. The selected AI host processes messages
under its own terms and privacy settings. User messages are not kept by a new
project-operated backend because this package has none.

The working SVG icon follows the author's site's paper/ink/brass palette. It is
an original local packaging asset, not an approved permanent project logo or a
claim of OpenAI endorsement. [Submission preparation](PLUGIN_SUBMISSION.md)
separates local validity from directory requirements.
