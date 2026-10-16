# Rail

Turn an unfinished request into a usable path of actions while preserving independent judgment.

## Use and do not use
Use when the recipient would otherwise need to assemble files, calculate, identify owners or invent a workflow. Do not turn the workflow into a forced route to agreement. Rail reduces organizational effort, not independent thinking.

## Inputs
Read the task, available evidence, roles, permissions, dependencies, required result and unknowns. A named person or contact cannot be invented to complete the route.

## Procedure
1. Identify work hidden in the request: locating evidence, selecting a version, identifying the decision owner, finding missing facts and reporting the result.
2. Separate fact gathering, checking, recommendation and authorization. Gathering supplier data is not approval to order; compiling bank documents is not permission to submit them.
3. Prepare ordered steps with an actor, exact action, evidence reference, expected output and dependencies. Use only supplied information; leave an explicit clarification step where information is missing.
4. Keep the path minimal and executable. Do not add empty table columns or speculative process branches merely to appear systematic.
5. Provide appropriate branches for confirmation, clarification, refusal and escalation. Their wording must respect real existing obligations, not invent a right to disregard them.
6. State what the recipient must not decide or do without authority. Identify the actual decision owner or flag that the owner is unknown.
7. Ensure the deliverable exposes consequences and choices instead of making refusal practically inaccessible.

## Readable result
A short instruction or task table; the decision owner; what the recipient should not decide; clarification/refusal/escalation paths. No external action is performed.

## Machine result
steps with id, actor, action, evidence_refs, output and depends_on; decision_owner; branches with when, action and outcome; message; do_not_decide.
Dependencies must reference an earlier step. Every branch action must be non-empty. Structural checks cannot prove that a branch is fair in real life.

## Stop and failure conditions
Clarify material authority or dependency contradictions. Refuse designs that hide refusal, exploit exhaustion or move forward without informed agreement.
FAIL: a forced confirmation funnel; invented responsible roles; automatic submission or purchase; treating a missing response as approval.
