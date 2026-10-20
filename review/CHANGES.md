# Minimal local delivery change

Baseline: accepted targeted-review source archive, SHA-256 `9fbf956793b7d74e60cf5dd0538102f4190b33bd5cb47658b1b2b275f15f5db4`.

[changes.patch](changes.patch) contains the complete diff for the three modified pre-existing content files:

- `README.md`: audience-facing entry, saved Plus demonstration, Codex path and explicit evidence limits.
- `protocols/rail.md`: two existing procedure steps; actual file creation/readability, fallback, and internal deadline boundary.
- `skills/rail/SKILL.md`: generated counterpart of that canonical change.

No implementation, renderer, schema, other protocol or original report change. `MANIFEST.json` is regenerated for the new complete package; it is packaging metadata, not a methodology change.

New files, deliberately separate from the patch to avoid treating binary workbooks and copied evidence as source rewrites:

- `editorial/rail-kits/07-kits/`: one XLSX, two recipient TXT drafts, one handoff template and one operator instruction.
- `editorial/rail-kits/08-delivery/`: one XLSX, four recipient TXT drafts, one handoff template and one operator instruction.
- `evidence/rc2-eight-runs/`: the 18 unchanged members of the saved readable evidence archive, seven unchanged Rail input files and a new provenance note.
- `reports/RC2_DELIVERY_VERIFICATION.json` and `.log`: actual offline engineering results for this pass.
- `review/`: this change note, the patch, the Russian delivery report and focused file-check results.

Every packaged file is listed with size and SHA-256 in the root manifest. Applying the text patch alone does not recreate the added workbooks or evidence; the single review archive carries those files. Previous source archives, source trees, pilot and saved model outputs remain untouched.
