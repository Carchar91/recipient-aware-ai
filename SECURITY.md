# Security and data handling

No credentials or real correspondence belong in this repository. The model runner obtains its key only from OPENAI_API_KEY and calls only the fixed OpenAI Responses endpoint. No credentials are written into reports. The compiler and validator do not execute user text or follow links. The runner supplies no browser, filesystem, account, send or purchase tool to the model.

Live calls require explicit network consent, cost acknowledgment and input privacy authorization. HTTP failures are not automatically retried. The command-line output and ignored runs/ folder may contain the submitted material and model text, so protect them as sensitive data.

Schemas, notices and explicit-invocation metadata do not make a language model a trusted decision maker. Malicious input can still affect model output. Human review is required before use. Do not pass private client documents without authority and an appropriate processing environment.

Do not publish secrets or sensitive examples in GitHub issues. For a security concern, start with a non-sensitive description through the author's established contact channel. Do not post live credentials even when demonstrating a bug.
