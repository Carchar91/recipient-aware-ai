# Changelog

## 0.1.0-rc.1

Prepared the first private-review implementation candidate: five independent operational specifications, generated self-contained skills, six JSON Schemas, a compiler/validator/renderer, an opt-in OpenAI Responses adapter, 30 synthetic cases, five worked outputs with invalid counterparts, offline tests, paired evaluation and blinded-review tools, provenance documentation and private-draft release support.

No live model efficacy evaluation, independent semantic review, public license selection or marketplace release is included. Original preparation reports retain their pre-handoff GitHub status; actual private draft availability must be checked in GitHub.

### Handoff corrections — 2026-10-16

- Preserve malformed non-object model responses in evaluation records and the failure denominator instead of crashing before writing the attempt.
- Refuse blinded-review export when current case input no longer matches the input hash recorded during the run.
- Refuse private publication if release-source inventory differs from the verified manifest, and validate the final repository identity, private visibility, draft/prerelease flags and tag.
- Add mocked regression coverage for these failure paths. No live model calls were used.
- Clarify historical status reports and record successful clean installation of the unchanged dependency pins on Python 3.14.4.

The source article, five protocols, generated skills, schemas and synthetic examples are unchanged. This remains the same private-review candidate version; it has not been publicly released.
