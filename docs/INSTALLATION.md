# Installation and invocation

## Source harness

Use Python 3.11+ from the repository root. Install `requirements.lock` in an isolated environment. Run `python tools/verify.py` before use. The exact pinned dependencies were also installed successfully in a clean macOS ARM64 environment with Python 3.14.4 during handoff. Other Python/platform combinations remain unverified.

`python -m rai list` prints the five IDs. `compile` creates instructions only. `run` calls one model only with both network and cost opt-in flags. No feature sends the resulting message to another person.

## Skills

For the experimental v0.1.0-rc.2 release, download the skills-only ZIP and SHA256SUMS from [the release](https://github.com/Carchar91/recipient-aware-ai/releases/tag/v0.1.0-rc.2). Verify the selected ZIP's checksum and extract into a new, empty folder. Each mode folder at the archive root is self-contained. Copy only the selected folder into the intended project's `.agents/skills`, and stop if a folder of that name already exists. The [README](https://github.com/Carchar91/recipient-aware-ai/blob/v0.1.0-rc.2/README.md#try-one-operation-in-codex) gives the complete file-based path. Ordinary skill use needs no Python or JSON.

The `skills/` folders conform to the Agent Skills directory/frontmatter design and include their schema references. They are generated from `protocols/`; do not edit generated copies independently.

For repository-scoped Codex use, copy the selected folders into `.agents/skills` in the intended methodology/testing repository. Check for an existing skill of the same name before copying and do not overwrite it silently. Do not install globally or into the website repo merely because it is open in the editor.

Invoke a selected mode explicitly, for example `$reverse` with the target message and known facts. The instructions allow readable responses in ordinary chat; machine JSON is used only when requested by the harness or caller.

`agents/openai.yaml` sets `allow_implicit_invocation: false`. This is a host setting, not a universal safety guarantee. Other clients may ignore it. The plain Python harness always takes one explicit mode from the validated input.

No plugin manifest or marketplace publication is asserted in this candidate. Packaging these same generated skills into a plugin is a separate integration and validation task. Do not invent a catalog listing, installation link or platform certification.

References: https://agentskills.io/specification and https://learn.chatgpt.com/docs/build-skills

## rc.2 evidence boundary

Current exported references are contract 1.1; the source harness can also validate preserved 1.0 artifacts. Read the full source package's `docs/CONTRACT_1_1.md` before mixing versions. Ordinary chat should produce the selected mode’s readable deliverable; machine mode is opt-in. `render --audit` exposes the full operator record separately.

Eight saved synthetic sessions used Codex CLI 0.163.0-alpha.10.2 with existing ChatGPT sign-in, requested alias gpt-6-astra and reasoning medium. The full selected skill was read in each recorded session. Global Seraphim instructions remained in the host; the backend snapshot was not exposed. See the full source package's `evidence/rc2-eight-runs/REPORT_RU.md`. Preparing this public release adds only file/instruction checks, not another model or host-integration trial. In particular, the new Rail file-delivery rule, ChatGPT plugin installation, native Excel/LibreOffice and other hosts remain untested.
