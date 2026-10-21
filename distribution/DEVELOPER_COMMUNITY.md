# Developer-community post — draft, not published

## An AI-written request can be clear and still leave the wrong work to the reader

I built Recipient-Aware AI through practical work with my personal AI assistant, Seraphim. It is an Apache-2.0 project with five independent operations: Profiler, Profiler Plus, Dopamine Hooks, Reverse and Rail. Choose the operation your task needs; they do not activate one another.

One example is Reverse: check a message using what the recipient can actually know, then place supported answers in the message itself.

**Before — excerpt from a synthetic invitation:**

> Everything is already prepared; all we need from you are photographs and confirmation.

**After — two excerpts from its revision:**

> There is a projector in the room, but the ability to display the TIFF files you sent has not yet been checked.

> We will publish the announcement only after you explicitly agree to lead this meeting.

The complete revision also specifies the meeting, payment, photograph rights and responsibilities. It does not invent technical readiness or treat silence as consent. These are editorial English translations of saved Russian first responses, not new model results or a real recipient's reaction: [full before/after and provenance](https://github.com/Carchar91/recipient-aware-ai/blob/main/SHOWCASE_EN.md#2-reverse-an-invitation-before-and-after).

[Try one skill](https://github.com/Carchar91/recipient-aware-ai#try-one-operation-in-codex) on a synthetic task or material you are authorised to share. Ordinary skill use does not need Python or JSON. [Experimental rc.2 release](https://github.com/Carchar91/recipient-aware-ai/releases/tag/v0.1.0-rc.2).

The examples illustrate intended behavior. Engineering checks and synthetic sessions do not establish superiority over ordinary prompting. Human review remains necessary, and host data-handling rules still apply.

If you try it, report the task, selected operation, environment, what helped and what you had to correct. Please omit private documents and correspondence.

For understanding and good-faith communication. Never for deception, coercion, or exploiting vulnerabilities. Respect the other person's right to disagree.
