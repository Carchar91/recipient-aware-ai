# Worked example: rail

Status: synthetic, assistant-authored reference fixture. NOT an independently executed model result.

# rail

Decision: proceed

The known division of responsibility supports a conditional fact-gathering workflow; missing contacts are handled by a clarification branch.

## Workflow
S1. Operations assistant: Confirm that the supplied records contain the actual contact routes for Vendor A and Vendor B. Ask the owner if those routes are missing. Expected output: Confirmed supplier contact routes or a focused clarification request.
S2. Operations assistant: Collect compatibility information and a quote from each supplier using the confirmed contact routes. Do not place an order. Expected output: Two supplier responses, each identifying what is confirmed and what is still unknown.
S3. Technical lead: Review the gathered information and decide compatibility, or request missing technical facts. Expected output: Compatibility decision or request for specific missing evidence.
S4. Owner: Review the quote and technical decision, then approve or decline the purchase separately. Expected output: Explicit purchase decision, with no order placed by this workflow.

Decision owner: The technical lead decides compatibility; the owner alone authorizes purchase.

## Branches
- confirm: The owner explicitly approves a suitable proposal. Record the authorized scope and use the normal separately authorized purchasing process.
- clarify: A contact, specification or quote is missing. Request only the missing information and keep authorization pending.
- decline: The proposal is unsuitable or the owner does not approve it. Record the decision and do not order.
- escalate: The operator is asked to decide compatibility or authorize payment. Refer to the technical lead or owner as appropriate.

## Do not decide
- The operations assistant must not approve compatibility.
- The operations assistant must not place an order or authorize payment.

## Recipient-facing instruction
Please collect compatibility information and quotes from Vendor A and Vendor B using the supplied contacts. Ask me if a contact is missing. Send the factual responses to the technical lead for compatibility review. Only the owner may authorize a purchase. Do not place an order or commit payment. If anything is missing or outside your authority, ask for clarification or refer it to the responsible role.

## Uncertainties
- Supplied facts have not been independently verified.

For understanding and good-faith communication. Never for deception, coercion, or exploiting vulnerabilities. Respect the other person's right to disagree.

*Structural validation does not establish truth, effectiveness or safety.*
