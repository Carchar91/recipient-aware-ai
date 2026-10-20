# Methodology

## The unit of work is an operation, not a personality

Recipient-Aware AI formalizes five independent operations from Eugene Prudchenko's approved article. They address different failure modes: confusing an observation with a motive; understanding without a usable request; attention without an answer; sender intent without recipient clarity; and an understandable message with an unfinished process.

Profiler builds an evidence-bounded map of a particular recipient’s decision criteria and possible barriers. Profiler Plus adapts the explanation of unchanged facts to those criteria. Dopamine Hooks develops attention and useful closure across the full text. Reverse follows the recipient’s reading using text plus explicitly shared context and inserts supported answers where questions arise. Rail prepares the execution kit, including available artifacts and calculations, while preserving human authority and judgment. The author’s rc.2 clarification sharpens these operations without rewriting the historical article.

The operational steps live in `protocols/`, not in five diverging hand-edited prompts. `tools/build_skills.py` generates the deployable copies and checks drift. An optional combination must be requested explicitly and reviewed as separate outputs; the runner intentionally accepts only one mode per request.

## What the formal contract adds

The article describes principles rather than a JSON API. This candidate adds engineering mechanisms:

- Evidence records have stable IDs and explicit kinds. None of the kinds asserts independent verification.
- Material conditions are identified up front and copied into a preservation ledger. When wording must survive verbatim, it is checked in the actual recipient-facing deliverable.
- Proceed, clarify and refuse are different outcomes. A refusal cannot carry an original-request draft in the result field.
- Hypotheses require alternative explanations and verification questions. This does not establish whether the hypothesis is plausible; that remains a human review question.
- Reverse findings must quote the supplied message, not an invented version. Recipient readback uses message content and explicitly recipient-known context, never private sender knowledge; semantic reviewers must check that it did not leak hidden sender context.
- Dopamine Hooks 1.1 retains operator summaries of promise and delivered value but removes the literal payoff gate. Whole-text development and fulfillment need semantic review. The 1.0 literal check remains unchanged for old results.
- Rail references real evidence IDs, orders dependencies and keeps several outcomes available. A graph can be structurally valid but coercive or impractical; the reviewer must examine the actions.

## Useful refusal, useful disagreement

Good faith is compatible with firm negotiation, a complaint, declining a proposal or contesting a charge. The prohibited mechanism is deception, coercion or exploitation, not having one's own interests.

A legitimate refusal is not a flaw to work around. A missing document is not a reason to invent a document. An authority question is not a reason to profile a clerk's character. A persuasive headline is not evidence of the truth of its promise.

## Provenance and author responsibility

The original article explains the development story in the author's own terms. This repository retains that source and labels added specifications as candidate implementation work. It does not independently verify the author's personal episodes or infer effect sizes from them.

The author retains editorial responsibility. The model provides assistance, not institutional authority, psychological diagnosis or the final right to decide.

## rc.2 author-intent revision

Readable results are mode-specific and deliverable-first; full JSON remains available with `render --audit`. The 1.1 perspective record separates operator evidence, recipient-known information, private sender evidence, stated recipient criteria and human authority; agent authority stays draft-only. These annotations do not prove the model respects the boundary. See `docs/CONTRACT_1_1.md` and `RC2_REVIEW_RU.md`.
