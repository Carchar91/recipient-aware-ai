# Plugin submission preparation — not submitted

Prepared on 2026-10-21 from the [current OpenAI package guide](https://developers.openai.com/plugins/build/plugins),
[submission guide](https://developers.openai.com/plugins/deploy/submission) and
[submission error reference](https://developers.openai.com/plugins/deploy/submission-errors).
No portal upload, private account plugin, public submission or publication was
performed. Local package validation is described in [Plugin package](PLUGIN.md).

## Listing prepared in the package

- Name: **Recipient-Aware AI**.
- Subtitle: **Write for the reader's needs** (28 characters).
- Author and intended developer identity: **Eugene Prudchenko**.
- Category: **Communication**.
- Version: **0.1.0-rc.2**, a plugin packaging candidate based on the existing
  experimental prerelease; it does not replace the GitHub release.
- Description: five independent, explicitly selected protocols, supported tasks,
  synthetic-evidence limitations, ethical boundaries, and host data handling.
- Three starter prompts and five draft reviewer prompts are in
  [plugin.json](../plugin/plugin.json). The reviewer prompts are examples to try,
  not a claim that those cases were run.
- Working square SVG logo/composer icon, release notes, source, licence and
  correct author attribution are included. Review the provisional icon before
  choosing it for a public listing.

The package uses the verified public [repository](https://github.com/Carchar91/recipient-aware-ai)
for `websiteURL` and its [public issues page](https://github.com/Carchar91/recipient-aware-ai/issues)
for `supportURL`. Support issues must use synthetic or safely redacted examples.
No promise of response time or private support service is made.

No `privacyPolicyURL` or `termsOfServiceURL` is invented. The Apache-2.0 licence
is not a privacy policy or a general terms-of-service page.

## What the current rules actually require

The current official field reference says all four listing URLs (website,
support, privacy policy and terms) are required **for an attached MCP app that
needs public review**. It explicitly says skills-only metadata validation does
not require all four. This supersedes the stricter four-URL statement in the
cached preparation skill used during this task. If the selected portal version
requests additional fields for this package, resolve the actual finding rather
than inventing policy URLs or assuming the upload is ready.

Skills-only plugins do **not** require MCP app test cases, a demo recording or
reviewer credentials. They still need metadata checks, required skills scans and
the applicable review/attestation steps. The optional distribution-video concept
is not a mandatory MCP review demo and is not a recorded video.

MCP-domain verification is part of connecting an MCP server. This package has no
MCP endpoint, account integration, OAuth, remote server or local process to
connect; do not create any of these just to complete submission preparation.
There is no need for the local-MCP organization allowlist for this skills-only
package. Host and workspace policies may still limit installation or submission.

## Decisions and online checks left to the owner

1. Select the owning OpenAI organization/project and the intended **verified
   individual identity Eugene Prudchenko**, or explicitly choose a different
   legitimate business publisher. Package text cannot override the verified name
   shown by the portal. Account access and verification have not been inspected.
2. Confirm portal permissions. The official guide allows organization owners to
   submit; other members need **Apps Management Write**. Complete individual or
   business verification in organization settings as required.
3. Choose country targeting and any listing translations. These fields are
   intentionally absent; no all-countries declaration or legal attestation is
   inferred from the author's location. The package itself provides no checkout,
   subscriptions or purchases; confirm any portal commerce declaration against
   the final intended offering.
4. Approve the provisional icon or supply a final one. The current format allows
   a contained square SVG; the portal's actual icon checks remain unverified.
5. Give separate permission for the portal action. Then upload the exact checked
   ZIP as a draft, inspect its imported developer identity, listing and five
   skills, wait for metadata/skill scans, and resolve real findings. The owner
   must complete legal and policy attestations; this document does not accept
   them on the owner's behalf.
6. Review submission and publication are separate decisions. Uploading creates a
   draft, submission starts review, and an approved plugin must still be
   published. None of those states is implied by a local test or valid ZIP.

A successful public review is not guaranteed. Adding MCP capabilities later is
not a silent upgrade to this package: the current submission guide says adding
an MCP server to an existing skills-only plugin is not supported. That is a
future scope decision, not a reason to add tools now.
