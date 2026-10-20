# Recipient-Aware AI

Five independent operations for using AI to understand a person's decision criteria, write a grounded message, develop a complete text, read it from the recipient's side, or prepare the work someone needs to execute.

Use them when the bottleneck is an unclear decision, a message that assumes too much, or a handoff that leaves someone else to finish the preparation. Choose one operation for the task. These are not five AI personas or a mandatory pipeline.

**AI should challenge assumptions, not merely strengthen persuasion.**

Try a standalone skill in **Codex**, the environment used for the saved eight-run check: [quick start below](#try-one-operation-in-codex). You get a decision map, a usable text, or a prepared execution kit, depending on the operation. Results still need human review.

**[Get v0.1.0-rc.2 — experimental prerelease](https://github.com/Carchar91/recipient-aware-ai/releases/tag/v0.1.0-rc.2)** · [Apache-2.0](LICENSE) for author-owned materials; [third-party terms retained](THIRD_PARTY_NOTICES.md).

## One proposal. Two readers. Same terms. Different explanation.

Two saved **Profiler Plus** runs used the same synthetic museum-training offer. Olga, the finance recipient, asked for the full cost and equipment requirements first. Sofya, the programme recipient, prioritised accuracy and the author's voice.

**Olga — editorial English translation excerpt:**

> Please approve an order for three in-person sessions on editing exhibition labels. The total fixed price is 54,000 roubles: preparation, all three sessions and a PDF of exercises are included, with no additional materials charges. The museum provides the room and screen.

[Full unchanged Russian first response](evidence/rc2-eight-runs/first-responses/03-plus-budget.md) · [task and original assessment](evidence/rc2-eight-runs/readable-results/03-plus-budget.md)

**Sofya — editorial English translation excerpt:**

> I propose approving an order for three in-person sessions on editing exhibition labels. The work centres on accuracy and preserving the author's voice while making the text clearer.

[Full unchanged Russian first response](evidence/rc2-eight-runs/first-responses/04-plus-curation.md) · [task and original assessment](evidence/rc2-eight-runs/readable-results/04-plus-curation.md)

The terms stay the same: three sessions on 5, 12 and 19 November 2026, 14:00–15:30; one group of up to 24 employees; 54,000 roubles including preparation, delivery and exercise PDFs; no materials surcharge; museum-provided room, screen and six anonymised labels; no recording; six months of internal materials use without public redistribution. Neither letter promises increased attendance or a measured training effect. The openings change to address evidenced priorities; the proposal and the recipient's right to decline remain intact. The excerpts are translations for this README, not new model results.

**[Read both complete letters in English, then see Reverse before/after and a Rail kit](SHOWCASE_EN.md).** These are explicitly labelled editorial translations linked to the unchanged Russian originals.

## See the next two kinds of result

- **Reverse:** [a complete revised invitation and compact question/answer map](evidence/rc2-eight-runs/first-responses/06-reverse-invitation.md), with [its task and assessment](evidence/rc2-eight-runs/readable-results/06-reverse-invitation.md). Supported answers are placed where the reader needs them. Unknown TIFF compatibility stays unknown.
- **Rail:** [branch-supplies kit](editorial/rail-kits/07-kits/START_HERE_RU.md) and [poster-delivery kit](editorial/rail-kits/08-delivery/START_HERE_RU.md), each with editable formula-based XLSX and separate ready-to-use messages. The delivery kit keeps the missing receiving window visible while preparing the work that can proceed.

**Evidence boundary:** the Rail files are labelled **editorial derivatives of saved answers**. The original two model sessions produced text and created **zero files**. This review creates the files and strengthens Rail's file-delivery rule. It does not demonstrate that a future model session will follow that rule. [Provenance](evidence/rc2-eight-runs/SOURCE.md) · [this review and actual checks](review/DELIVERY_REVIEW_RU.md)

## Choose the operation

| Operation | Use it to | Expected result |
| --- | --- | --- |
| **Profiler** | Understand evidenced reasoning, criteria, trusted grounds and possible barriers. | A substantive opening conclusion, decision map, alternatives and a useful next move. Not a personality diagnosis or mind reading. |
| **Profiler Plus** | Explain an unchanged proposal through the recipient's known priorities. | The ready message first; adaptation notes separately; material terms preserved. |
| **Dopamine Hooks** | Develop interest and understanding from paragraph to paragraph. | A complete connected text that answers the questions it raises. No claim about brain chemistry or observed retention. |
| **Reverse** | Read a draft using only what the recipient can know. | Revised text with supported answers at their point of need, then a compact map of consequential questions. |
| **Rail** | Remove avoidable preparation from a handoff. | Necessary working files when tools and permission allow; short instructions, explicit unknowns and human decision limits. |

Each has a [canonical specification](protocols/), a self-contained [skill folder](skills/), examples and engineering checks. Invoking one does not activate the others.

## Try one operation in Codex

Download the [skills-only release asset](https://github.com/Carchar91/recipient-aware-ai/releases/download/v0.1.0-rc.2/recipient-aware-ai-skills-0.1.0-rc.2.zip) and [SHA256SUMS.txt](https://github.com/Carchar91/recipient-aware-ai/releases/download/v0.1.0-rc.2/SHA256SUMS.txt). Verify its checksum, then extract into a **new, empty folder**. You get five independent skill folders plus licence and installation notices. For macOS/Linux, from the download directory:

```bash
grep -F '  recipient-aware-ai-skills-0.1.0-rc.2.zip' SHA256SUMS.txt | shasum -a 256 -c
mkdir recipient-aware-ai-skills-0.1.0-rc.2 && \
  unzip recipient-aware-ai-skills-0.1.0-rc.2.zip -d recipient-aware-ai-skills-0.1.0-rc.2
```

After successful verification and extraction, copy the **selected** folder into a project you control:

```bash
mkdir -p /path/to/your-project/.agents/skills
test ! -e /path/to/your-project/.agents/skills/profiler-plus && \
  cp -R recipient-aware-ai-skills-0.1.0-rc.2/profiler-plus /path/to/your-project/.agents/skills/
```

If that skill folder already exists, review it rather than overwriting it. Open that project in Codex and explicitly select `$profiler-plus`. Supply the proposal, all material terms, the recipient's directly known priorities, and what you are authorised to request. For example:

> Use $profiler-plus. Draft the message first. Here are the fixed offer terms, the recipient's stated priorities and the requested decision: [provide your facts]. Keep unsupported assumptions visible; put operator notes outside the recipient's message.

For another operation, copy and explicitly select that skill instead. From the full source package, the same folders live under `skills/`. **Ordinary skill use does not require Python, schemas or JSON.** This README does not install anything. Use synthetic or appropriately authorised material; do not paste confidential correspondence without permission. [Installation details](docs/INSTALLATION.md)

The saved check used Codex CLI **0.163.0-alpha.10.2**, existing ChatGPT sign-in, requested model alias **gpt-6-astra**, reasoning **medium**, and eight fresh task contexts. No separate API billing was used. The backend snapshot was not exposed; global Seraphim instructions remained present, and memory/history were disabled. Each trace showed the selected full skill was read. [Original environment and limitations report](evidence/rc2-eight-runs/REPORT_RU.md)

This is the tested route described here. ChatGPT plugin installation or compatibility was **not tested**. The new file-delivery rule has not had a new model trial.

## Developer path

Use a Python 3.11+ source checkout with pinned dependencies. After dependency installation, the verification tools run offline and make no model calls:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.lock
python tools/verify_manifest.py
python tools/build_skills.py --check
python tools/verify.py --report reports/YOUR_LOCAL_VERIFICATION.json
```

Dependency installation needs package access. The reported checks cover the recorded local interpreter, not every supported Python version. [Current engineering report](reports/PUBLIC_RC2_VERIFICATION.json) · [public release checks and rights scope](reports/PUBLIC_RELEASE_REVIEW.md) · [preserved delivery checks](review/FILE_CHECKS.json) · [earlier minimal delivery patch](review/CHANGES.md)

The reference harness compiles prompts and validates/renders structured results. It is a developer tool; ordinary skill use does not require a JSON response. To inspect an **authored development fixture**, without calling a model:

```bash
python -m rai compile --input development/rc2/dev-rv-sequence/input.json
python -m rai render \
  --input development/rc2/dev-rv-sequence/input.json \
  --output development/rc2/dev-rv-sequence/authored-output.json
```

Canonical rules live in `protocols/`; rebuild generated skills with `python tools/build_skills.py`. The API adapter and comparison tooling are separate, explicitly opt-in operations described in [evaluation documentation](EVALUATION.md). No API calls are needed to review this package.

## What this evidence establishes

All eight situations are synthetic. The full first answers and primary agent assessments are preserved unchanged. They illustrate distinct operations; they are not client implementations, independent studies or controlled evidence of superiority. The [earlier pilot and its unchanged answers](evidence/rc1-pilot/SOURCE.md) retain their failures and partially contaminated control; they established no comparative advantage. [Give practical feedback](https://github.com/Carchar91/recipient-aware-ai/issues/new?template=feedback.yml): the task, selected operation and environment, what helped, and what you had to correct. Do not publish private documents or correspondence.

Engineering checks test software behaviour, provenance handling, generated-source consistency and file integrity. They do **not** measure usefulness to people, semantic truth or general safety. This review ran no new models. Repeated model sessions for this revised delivery rule, real reader reactions, controlled comparisons and safety across scenarios remain untested. The XLSX checks distinguish library recalculation and reopening from untested native Excel/LibreOffice behaviour.

## Author, source and boundaries

**Eugene Prudchenko** is the author. **Seraphim** is his personal AI assistant, not a separate foundation model. [The author's original article](https://prudchenko.com/writing/five-communication-protocols) provides the historical account; [the approved snapshot](docs/source/article.approved.en.md) and [source map](SOURCE_MAP.md) distinguish that account from this package's engineering implementation. [Citation](CITATION.cff)

**For understanding and good-faith communication. Never for deception, coercion, or exploiting vulnerabilities. Respect the other person's right to disagree.**

[Methodology](METHODOLOGY.md) · [Responsible use](RESPONSIBLE_USE.md) · [Limitations](LIMITATIONS.md) · [Licence](LICENSE) · [Licensing decision record](LICENSE_PENDING.md)

The ethical principles describe intended use and the behaviour of the official skills; they do not add restrictions to Apache-2.0 or guarantee control of third-party copies.
