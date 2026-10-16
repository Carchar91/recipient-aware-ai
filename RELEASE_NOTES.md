# Recipient-Aware AI 0.1.0-rc.1

Private-review release candidate for five independent communication protocols by Eugene Prudchenko, developed with his personal AI assistant Seraphim.

## Included

Operational specifications and standalone skills for Profiler, Profiler Plus, Dopamine Hooks, Reverse and Rail. A source-checkout Python harness compiles versioned requests, validates evidence/output contracts and renders readable results. An explicitly opt-in OpenAI Responses adapter and paired evaluation tools support real testing without fabricating results. Thirty synthetic development cases and five worked positive/negative pairs make expected behavior and common failures inspectable.

## Verification

The supplied reports/LOCAL_VERIFICATION.json and its log preserve the original 113-test preparation result. During handoff on 2026-10-16, all 113 original tests were reproduced in a clean macOS ARM64 environment with Python 3.14.4 and the unchanged requirements.lock pins. After the corrections below, the full suite passed **120 tests, with zero failures, errors or skips**. Fresh machine-readable logs were retained separately from the original report.

Additional checks passed: all five generated skills match their canonical sources; all five worked positive outputs validate and render; all five negative outputs are rejected; repeated compilation is byte-identical. All 110 normalized article blocks in the preserved source were found in the public article. This source comparison was AI-assisted, not independent human semantic evaluation. The original article SHA-256 remains `452a1bd0acf19cdb61381786f80dbaecb092c55317c4986aabe0d690da037b8d`.

The build archive has a file-level SHA-256 manifest and an adjacent archive checksum. Checksums establish byte integrity relative to the manifest, not an independently signed provenance attestation. Actual uploaded assets and remote release state require separate GitHub readback.

## Minimal handoff corrections

- Record non-object model responses as failed attempts without losing them from the evaluation denominator.
- Block blinded-review exports when the current input differs from its recorded hash.
- Block publication of unlisted source files and verify the exact private repository, draft/prerelease flags and release tag.
- Add seven offline regression tests and clarify historical preparation status notices.

The article, five protocols, skills, schemas, examples and dependency versions are unchanged. See CHANGELOG.md for details.

## Not claimed

No live provider evaluations or independent semantic-review results. No scientifically validated efficacy, universal safety, guaranteed recipient agreement, cross-model certification, marketplace listing or public open-source license. All worked examples are labeled synthetic authoring fixtures.

## Publication boundary

Keep this a draft prerelease in the owner's private methodology repository. Public licensing and public release require the owner's decision. Do not modify prudchenko.com or its repository.
