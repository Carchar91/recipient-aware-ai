# Contract 1.1 — local rc.2

The input and output `schema_version` must match. Current `schemas/*.json` and generated skills describe 1.1. `schemas/v1.0/*.json` preserve the six original schemas byte-for-byte. Validation and provider schema selection dispatch on the input version; old fixtures and results are not upgraded automatically. No rc.1 prompt hash or historical score is recomputed. Old inputs can be validated or compiled with their original schema, but compiling with the revised rc.2 procedures is a new prompt, not an rc.1 replay. Generated standalone skills export 1.1 only; use the preserved rc.1 package for old standalone instructions.

## Small additions

- Input: one `perspective` record with evidence-ID lists `recipient_known_evidence`, `sender_private_evidence`, `recipient_criteria`, `human_authority`, plus `agent_authority: draft_only`. Empty lists mean unknown/not supplied. All evidence is available to the operator. Unmarked facts are not assumed already known to the recipient; relevant nonprivate facts may be introduced as new information. A fact cannot be both private and recipient-known, nor can a material condition be hidden as private.
- Profiler: `decision_map` with supported signals and interpretations, `main_barrier`, `communication_frame`. Sparse evidence allows an empty map, not fabricated traits.
- Profiler Plus: no new result fields; the existing message and evidence placement can express recipient adaptation.
- Dopamine Hooks: no new fields. `body` is the full text including opening; `payoff` summarizes the delivered answer and need not be a literal substring. Headline/opening/CTA can be empty when not needed. Semantic fulfillment is unverified by this check. The historical 1.0 substring gate remains intact.
- Reverse: each finding adds `question`, `answer_evidence_refs`, `inserted_answer`. A supplied answer needs nonprivate evidence IDs and an exact excerpt in the revision. This reference check cannot detect every private paraphrase or undisclosed leak. Unknown answers use empty refs and excerpt, with the gap explained to the operator. Presence does not establish semantic correctness or appropriate placement.
- Rail: `artifacts` holds actual inline content with source IDs; `blockers` identifies missing input, its known source and the dependent step. Only applicable branches are needed in 1.1; the old four-branch gate remains for 1.0. Inline names do not assert physical attachments exist.
- The 1.1 preservation ledger includes exactly the declared material conditions and full original evidence text, including attribution. Other evidence belongs in evidence/observations, not an invented condition ledger.

## Readable output

`python -m rai render --input ... --output ...` puts the useful result first. `--audit` additionally shows the complete operator-only machine record. Ethical notice remains outside the recipient's message. Ordinary skill conversation uses its own readable format without mandatory JSON. No automatic mode chaining or external action was added.

## Limits

Reference existence, exact excerpts, schema validity and dependency order are machine-checkable. Accurate recipient adaptation, discretion, genuine answer quality, no covert pressure, complete practical preparation and correct interpretation of authority still need semantic review. These checks do not certify them. Both old and new model responses may fail even when all development fixtures pass.
