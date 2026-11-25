## Logfire (tracing and prompts)

We use [Logfire](https://logfire-eu.pydantic.dev) to trace requests and agent
calls, and to version the system prompts.

### Environment variables

Add both keys to your `.env`. Each person creates their own keys.

| Variable | What it does | How to create it |
|---|---|---|
| `LOGFIRE_TOKEN` | Sends traces from the backend to Logfire | Project settings, API keys, create a key with only **Send telemetry** |
| `LOGFIRE_API_KEY` | Fetches prompts from Logfire | Managed variables, **Create API key** (read variables only) |

Name your keys after yourself, for example `name_local_dev`, so a single key
can be revoked without affecting others.

Without `LOGFIRE_TOKEN` the app still runs, but no traces are sent.
Without `LOGFIRE_API_KEY` the agents use the local fallback prompts in `prompts.py`.

### Prompts

System prompts live in Logfire under **Prompts** and are fetched in
`backend/src/cvoice_backend/prompts.py`. The app always uses the version that
the `production` label points to.

To change a prompt:

1. Edit the prompt in Logfire and save a new version.
2. Move the `production` label to the new version (Managed variables, the prompt's variable).
3. Update the matching `*_PROMPT_DEFAULT` in `prompts.py` with the same text,
   so the local fallback stays in sync.