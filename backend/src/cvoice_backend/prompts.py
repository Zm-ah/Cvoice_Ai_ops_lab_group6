"""System prompts, fetched from Logfire with a local fallback."""

# Claude is used for this.

import logfire

# Local fallback, is used if Logfire can not be reached
PERSONA_CHAT_PROMPT_DEFAULT = (
    "You are the person described in the uploaded CV. "
    "Answer in first person, based only on the CV content. "
    "If the CV does not contain the answer, say so."
)

persona_chat_prompt = logfire.var(
    name="prompt__persona_chat", type=str, default=PERSONA_CHAT_PROMPT_DEFAULT
)


def get_persona_chat_prompt() -> str:
    """Return the version of the persona chat prompt that the production label points to."""

    with persona_chat_prompt.get(label="production") as resolved:
        return resolved.value
