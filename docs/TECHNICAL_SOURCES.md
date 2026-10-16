# Primary technical references

The implementation was checked against these primary sources during preparation. They inform format and API choices, not the author's historical claims or evidence of efficacy.

- Agent Skills specification: https://agentskills.io/specification
- OpenAI skill authoring, explicit invocation and host metadata: https://learn.chatgpt.com/docs/build-skills
- OpenAI Responses creation and Structured Outputs: https://developers.openai.com/api/reference/resources/responses/methods/create
- OpenAI Responses migration and store handling: https://developers.openai.com/api/docs/guides/migrate-to-responses
- GitHub CLI private repository creation: https://cli.github.com/manual/gh_repo_create
- GitHub CLI draft release creation and verify-tag: https://cli.github.com/manual/gh_release_create
- GitHub repository licensing: https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository

The local validator retains stricter JSON Schema constraints than the wire-format subset. Unsupported provider/model combinations are reported rather than retried with silently weakened settings.
