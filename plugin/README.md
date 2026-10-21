# Recipient-Aware AI — skills-only plugin

Local packaging candidate by Eugene Prudchenko, based on experimental prerelease
`v0.1.0-rc.2`. Not submitted to or available in the public plugin directory.

Choose **one** mode and name it explicitly in your request. Start with a synthetic
or shareable task, include the available facts, and review the result before use.

| Your task | Choose |
| --- | --- |
| Understand evidence about someone's reasoning and decision criteria | **Profiler** |
| Adapt a message to a particular recipient while preserving its terms | **Profiler Plus** |
| Develop interest through an entire text without false promises | **Dopamine Hooks** |
| Read material as its recipient and integrate supported answers | **Reverse** |
| Prepare work and handoff materials so an executor has less left to do | **Rail** |

Example: “Use Reverse on this synthetic draft. Read it as the recipient, place
supported answers where questions arise, and keep unknowns explicit.”

There are five independent protocols, not five personas or an automatic pipeline.
The onboarding is this chooser; no sixth protocol or automatic setup workflow is
added. If a host namespaces skill names, select the installed skill in that host's
picker, then ask for its corresponding mode. For ordinary chat, ask for readable
output; machine-mode JSON is optional.

**AI should challenge assumptions, not merely strengthen persuasion.**

For understanding and good-faith communication. Never for deception, coercion,
or exploiting vulnerabilities. Respect the other person's right to disagree.

This package contains instructions and references only: no MCP server, executable
hooks, telemetry, external storage, or sending capability. A host may already have
tools and permissions of its own. These instructions do not technically remove
those permissions; review the host and keep human approval for external actions.
Messages are still processed by your selected AI host under its terms and data
settings. Do not supply confidential material without authority to share it.

Engineering checks and synthetic examples do not demonstrate practical efficacy,
psychological accuracy, or superior model performance. Read [Responsible Use](https://github.com/Carchar91/recipient-aware-ai/blob/v0.1.0-rc.2/RESPONSIBLE_USE.md)
and [Limitations](https://github.com/Carchar91/recipient-aware-ai/blob/v0.1.0-rc.2/LIMITATIONS.md). Native file output depends on the host's tools;
Rail must distinguish files actually created from a plan or suggested filename.

Seraphim is Eugene's personal AI assistant, not a separate foundation model.

Author-owned materials: Apache-2.0; preserve [NOTICE](https://github.com/Carchar91/recipient-aware-ai/blob/v0.1.0-rc.2/NOTICE) and
[third-party terms](https://github.com/Carchar91/recipient-aware-ai/blob/v0.1.0-rc.2/THIRD_PARTY_NOTICES.md). The working icon is an original local
packaging asset; it is not a claim of an existing registered brand or approved
public-directory listing.
