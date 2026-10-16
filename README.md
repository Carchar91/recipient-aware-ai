# Recipient-Aware AI

## AI can make you more persuasive. Even when you are wrong.

Five independent communication protocols by **Eugene Prudchenko**, developed through practical work with his AI assistant **Seraphim**.

The point is not to obtain agreement at any cost. It is to check assumptions, prepare grounded communication, make its relevance visible, review what the recipient can actually understand, and remove unnecessary work without removing choice.

**For understanding and good-faith communication. Never for deception, coercion, or exploiting vulnerabilities. Respect the other person's right to disagree.**

### Release status

`0.1.0-rc.1` is a **private-review release candidate**. It is not a public GitHub release, a scientifically validated method, or a marketplace plugin.
The original preparation report is [reports/LOCAL_VERIFICATION.json](reports/LOCAL_VERIFICATION.json); it is preserved as a historical snapshot. Current handoff checks and corrections are recorded in [RELEASE_NOTES.md](RELEASE_NOTES.md) and [CHANGELOG.md](CHANGELOG.md). Engineering verification is separate from live model evaluation.
**Live model evaluation and independent semantic review have not been performed. Public licensing has not been selected.** See [LICENSE_PENDING.md](LICENSE_PENDING.md).

### What is actually in the package?

| Protocol | Operation | Concrete result |
| --- | --- | --- |
| **Profiler** | Separate an observation from possible explanations and role constraints. | Evidence-linked observations, alternative hypotheses, unknowns and a verification move. |
| **Profiler Plus** | Turn understanding into a justified communication or institutional decision package. | Recipient-facing draft, requested decision, evidence placement and authority/escalation notes. |
| **Dopamine Hooks** | Make relevance visible and deliver the explanation promised by the opening. | Headline, opening, body and an explicit promise-to-payoff link. No neurochemical claims. |
| **Reverse** | Compare message-only understanding with the sender's actual objective and facts. | Exact-quote findings, possible readings, task correction and one revised message. |
| **Rail** | Make an unfinished assignment executable without transferring unauthorized decisions. | Actors, evidence, steps, dependencies and confirmation/clarification/refusal/escalation branches. |

Each protocol has an operational specification, a standalone `SKILL.md`, an input/output contract, an example and synthetic evaluation cases. No mode starts the other four automatically.

### Not just five descriptions

The reference implementation can:

* Compile the same versioned protocol and input into the same system/user prompt pair, with SHA-256 provenance.
* Validate structured results against a closed JSON Schema plus cross-field checks: real evidence IDs, exact quotations, preserved conditions, explicit choices and acyclic workflow dependencies.
* Render a validated output into a readable draft and separate operator notes.
* Prepare or run paired baseline/protocol evaluations with an explicit call cap, no tools, no automatic retries and opt-in model access.
* Export shuffled review samples without arm labels, while retaining a separate answer key.
* Build self-contained skills from one canonical source and fail if generated copies drift.

These checks make errors observable. They do **not** prove that a model's interpretation is true, non-manipulative or useful. One test deliberately shows that semantically bad prose can satisfy a structural contract. That boundary is part of the design, not a footnote.

## Start from a source checkout

Requires Python 3.11 or newer; the exact local test interpreter and dependency versions are recorded in the report. The test suite was executed in the supplied environment, not every supported Python version. Install the pinned dependencies in an isolated environment:

```bash
python -m venv .venv
# macOS / Linux
source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -r requirements.lock
python tools/verify.py
```

This candidate is a source-checkout package, not a published PyPI package. Run the following from the repository root.

### Compile a reproducible request without calling any model

```bash
python -m rai compile --input examples/reverse/input.json
```

The result contains the selected instructions and task data as separate fields. This is a prompt pair, **not a generated answer**. It can be used with a model environment that the operator is authorized to use. Only the explicit OpenAI adapter described below is implemented here; compatibility with other model APIs has not been tested.

### Inspect a worked example

```bash
python -m rai validate-output \
  --input examples/reverse/input.json \
  --output examples/reverse/reference-output.json

python -m rai render \
  --input examples/reverse/input.json \
  --output examples/reverse/reference-output.json
```

The reference output is clearly labeled as an **assistant-authored synthetic fixture**, not a measured model run. [Read the walkthrough](examples/reverse/walkthrough.md).

The matching `invalid-output.json` deliberately contains a false quotation. Passing it to `validate-output` must return a nonzero exit code. Other modes have their own failure examples.

### Live execution is explicit, optional and potentially paid

The adapter uses the OpenAI Responses API. Select a model available to your account that supports Structured Outputs. No default model is chosen and no benchmark result is prefilled.

```bash
# Set OPENAI_API_KEY securely in your environment. Never commit it.
python -m rai run \
  --input examples/reverse/input.json \
  --model YOUR_SUPPORTED_MODEL_ID \
  --allow-network --acknowledge-cost
```

`privacy_ok` must also be true in the input. This flag records operator permission; it does not independently verify consent or confidentiality. The adapter uses `store=false`, does not supply tools, does not follow links in material, and does not log credentials. Provider data-handling policies still apply; this is not a promise of zero retention.

Without both opt-in flags or without a key, the runner refuses before sending a request. Incomplete replies, provider refusals outside the schema, HTTP errors and contract failures are recorded, not silently rewritten into passes.

### Run a real comparison, not a prewritten success story

```bash
# Plan only. No network calls.
python tools/live_eval.py --model YOUR_SUPPORTED_MODEL_ID --case rv-01

# Executes two requests: common-safety baseline and detailed Reverse.
python tools/live_eval.py --model YOUR_SUPPORTED_MODEL_ID --case rv-01 \
  --execute --allow-network --acknowledge-cost --max-calls 2
```

Both arms receive identical input facts, the same output schema and common safety constraints. Only the detailed mode procedure differs. Model, prompt hashes, input hashes, returned model, usage and validation results are recorded. A repeated prompt is reproducible; stochastic model output is not guaranteed byte-identical.

The 30 included cases are transparent development fixtures, **not held-out evidence of generalization**. Human review is a separate operation. See [EVALUATION.md](EVALUATION.md) before interpreting any score.

## Use the independent skills

`skills/` contains five generated, self-contained skill folders. Each has the approved ethical notice and its own schema references. `agents/openai.yaml` sets `allow_implicit_invocation: false` for hosts that support that setting.

Follow [docs/INSTALLATION.md](docs/INSTALLATION.md). Installing or selecting a skill is not the same as proving it behaves correctly. Other hosts may ignore invocation metadata. The deterministic CLI also requires one explicit protocol ID.

## Read the methodology and its limits

[Methodology](METHODOLOGY.md) · [Source map](SOURCE_MAP.md) · [Responsible use](RESPONSIBLE_USE.md) · [Known limits](LIMITATIONS.md) · [Evaluation design](EVALUATION.md) · [Author's original article](https://prudchenko.com/writing/five-communication-protocols)

The approved article is preserved in `docs/source/article.approved.en.md`. The schemas, cases, validation rules and code are a new operationalization prepared for this candidate, not a claim to have recovered every historical prompt. The author's personal observations remain observations, not experiments.

The package contains no client correspondence, account details, real bank documents, user analytics, auto-send capability or credentials.

## Author and application

The methodology is attributed to Eugene Prudchenko. Seraphim is his personal AI assistant, not a proprietary foundation model. See [CITATION.cff](CITATION.cff) for candidate attribution. No repository URL or published-release date is asserted before actual publication.

For adaptation to a team's legitimate workflows, use the [author's contact page](https://prudchenko.com/contact). Send a general description, not confidential case files.

**Strong communication helps someone make a decision. It should never take that decision away from them.**
