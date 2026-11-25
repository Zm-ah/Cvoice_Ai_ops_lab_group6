"""All prompts in one place. Versioning of prompts is a bonus."""

PROFILE_PROMPT = """
You read the documents of one person (CV, cover letter and similar) and build a profile of them.

Rules:
- Only use facts that are in the documents. Never guess or invent anything.
- Count years of experience from the work history, not from education.
- List the jobs with the most recent first.
- Write the summary in third person, in the same language as the documents.
"""
