# Install through the skills CLI

Checked on 2026-10-21. The existing `skills/` layout is discoverable by the Vercel-maintained `skills` CLI. Installing directly from GitHub works independently of a skills.sh directory listing. This check establishes one Codex installation and one synthetic use; [compatibility and the first result](COMPATIBILITY.md) state the limits.

## Install one operation in Codex

Use Node.js 22.20.0 or later, as required by `skills@1.7.4`. The check used Node.js 25.9.0 on macOS ARM64. Run from the intended project root. Stop if `.agents/skills/profiler-plus` already exists; use a new empty project for a first trial.

```sh
DISABLE_TELEMETRY=1 DO_NOT_TRACK=1 npx --yes skills@1.7.4 add https://github.com/Carchar91/recipient-aware-ai/tree/v0.1.0-rc.2 --skill profiler-plus --agent codex --yes
```

This exact command succeeded once in an empty temporary project. It installed only `profiler-plus`, copied its four files into `.agents/skills/profiler-plus/`, and created the project's `skills-lock.json` with `ref: v0.1.0-rc.2`. The tag resolved to commit `8817f78999e413f9da60d90e66882b474fc6de37`; all four installed files matched that public commit byte-for-byte. No global install was performed.

The single-skill copy does not include the repository-root [LICENSE](../LICENSE), [NOTICE](../NOTICE) or [third-party notices](../THIRD_PARTY_NOTICES.md). Retain those upstream notices when redistributing an installed skill. The release ZIP and plugin package include them.

To inspect available names without installing:

```sh
DISABLE_TELEMETRY=1 DO_NOT_TRACK=1 npx --yes skills@1.7.4 add https://github.com/Carchar91/recipient-aware-ai/tree/v0.1.0-rc.2 --list
```

Both the public tag and `main` returned exactly five names: `profiler`, `profiler-plus`, `dopamine-hooks`, `reverse`, `rail`. Both resolved to the same commit on the check date. Select one operation; installing a skill does not authorize chaining the others.

After installation, this command lists the project installation:

```sh
DISABLE_TELEMETRY=1 DO_NOT_TRACK=1 npx --yes skills@1.7.4 list --agent codex --json
```

Start a new Codex session in the project and explicitly invoke the selected skill, for example:

```text
Use $profiler-plus on the synthetic material below. Draft only; do not send.
```

Ordinary readable use needs no Python or JSON. `agents/openai.yaml` requests explicit invocation. Review the recipient-facing draft separately from operator notes before using it.

## Directory presence is a separate state

On 2026-10-21, read-only skills.sh search returned no results for `recipient-aware-ai` or `profiler-plus` scoped to owner `carchar91`. The repository directory URL returned HTTP 404. The direct skill URL returned HTTP 200 but displayed a 404 message saying the skill was unavailable. The successful GitHub install therefore does **not** establish a directory listing, leaderboard position, or security-audit result.

The [official FAQ](https://skills.sh/docs/faq) describes automatic leaderboard inclusion through installation telemetry. Every CLI check here set both opt-out variables. These tests were not used to seed a listing or manufacture installation counts. No pack, public submission, plugin listing, or marketplace publication was created.

## Mechanism and primary references

The CLI searches supported repository containers including `skills/`; a skill's `SKILL.md` must have `name` and `description` frontmatter. `--list` discovers candidates, `--skill` selects the named operation, and `--agent codex` selects the project destination. These are installer behaviours; host execution must be checked separately.

- [Official CLI installation options, pinned to 1.7.4](https://github.com/vercel-labs/skills/blob/a80e4c9d12d607631249d4d7d059f835d4b2f13a/docs/commands.md#skills-add)
- [Official skill format and discovery rules, pinned to 1.7.4](https://github.com/vercel-labs/skills/blob/a80e4c9d12d607631249d4d7d059f835d4b2f13a/docs/creating-skills.md)
- [Official telemetry opt-out implementation, pinned to 1.7.4](https://github.com/vercel-labs/skills/blob/a80e4c9d12d607631249d4d7d059f835d4b2f13a/src/telemetry.ts) — either variable disables CLI telemetry and security-audit requests; both were set here. This does not claim to disable ordinary host/service logging.
- [Official skills.sh documentation](https://skills.sh/docs)

The local audit retains exact commands, stdout/stderr, public refs, installed-file hashes, and the unchanged first Codex transcript. The public [compatibility record](COMPATIBILITY.md#single-codex-smoke-2026-10-21) contains the synthetic task, first answer and hashes. No protocol or generated skill content was changed for this integration.
