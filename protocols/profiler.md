# Profiler

Separate observations, plausible explanations and role constraints before choosing a communication strategy.

## Use and do not use
Use for an explicitly requested contextual analysis of supplied interaction. It is not a diagnostic profile, a face analysis, or a ready-to-send message generator.

## Inputs
Read the sender's legitimate objective, the recipient's known role and authority, actual words/actions, and supplied evidence. Absence of evidence is not evidence of an ulterior motive.

## Procedure
1. Restate the real decision or misunderstanding in neutral terms. Check whether the sender's interpretation is already an unsupported accusation.
2. Extract observations with evidence IDs. Keep “the employee said the rule exists” separate from “the rule exists.”
3. Identify confirmed role constraints and distinguish them from possibilities: authority, process, missing information, conflicting incentives or competing commitments.
4. Where motive interpretation is useful, offer multiple plausible explanations, including an ordinary procedural explanation when supported. Each hypothesis needs an alternative and a question that could disconfirm it. Do not manufacture motives merely to fill a template.
5. Identify likely objections as possibilities anchored in facts, not as fixed personality traits or vulnerabilities to target.
6. Recommend the smallest good-faith verification or communication move. The recommendation may be to change the sender's request rather than intensify persuasion.

## Readable result
Facts and sources; possible explanations and alternatives; important unknowns; role constraints; a concrete next action. Keep the sections proportional to the task. Do not append other protocol analyses automatically.

## Machine result
observations: items containing evidence_id and observation.
role_constraints: strings that distinguish known facts from unverified constraints.
likely_objections: tentative, evidence-aware objections.
recommended_action: one executable, good-faith next move.
Put explicit alternative motive explanations in the shared hypotheses field.

## Stop and failure conditions
Clarify if the actual interaction or required decision is missing. Refuse diagnosis, vulnerability exploitation or group-based character judgments.
FAIL examples: “He is dishonest”; “her silence means she agreed”; “the bank legally forbids this” when the only input is an employee's assertion.
A valid success may be discovering that authority, not attitude, explains the obstacle.
