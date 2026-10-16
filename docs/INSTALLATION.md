# Installation and invocation

## Source harness

Use Python 3.11+ from the repository root. Install `requirements.lock` in an isolated environment. Run `python tools/verify.py` before use. The exact pinned dependencies were also installed successfully in a clean macOS ARM64 environment with Python 3.14.4 during handoff. Other Python/platform combinations remain unverified.

`python -m rai list` prints the five IDs. `compile` creates instructions only. `run` calls one model only with both network and cost opt-in flags. No feature sends the resulting message to another person.

## Skills

The `skills/` folders conform to the Agent Skills directory/frontmatter design and include their schema references. They are generated from `protocols/`; do not edit generated copies independently.

For repository-scoped Codex use, copy the selected folders into `.agents/skills` in the intended methodology/testing repository. Check for an existing skill of the same name before copying and do not overwrite it silently. Do not install globally or into the website repo merely because it is open in the editor.

Invoke a selected mode explicitly, for example `$reverse` with the target message and known facts. The instructions allow readable responses in ordinary chat; machine JSON is used only when requested by the harness or caller.

`agents/openai.yaml` sets `allow_implicit_invocation: false`. This is a host setting, not a universal safety guarantee. Other clients may ignore it. The plain Python harness always takes one explicit mode from the validated input.

No plugin manifest or marketplace publication is asserted in this candidate. Packaging these same generated skills into a plugin is a separate integration and validation task. Do not invent a catalog listing, installation link or platform certification.

References: https://agentskills.io/specification and https://learn.chatgpt.com/docs/build-skills
