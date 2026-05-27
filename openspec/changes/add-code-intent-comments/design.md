## Context

The MCP server is compact and mostly self-explanatory, but a few behaviors were introduced to handle LLM-specific failure modes. The most important example is preventing stale timezone arguments from overriding a newly geocoded location. Without comments, future edits may accidentally remove or weaken those safeguards.

## Goals / Non-Goals

**Goals:**

- Add comments that explain intent, policy, or LLM-specific failure modes.
- Keep comments close to the relevant code.
- Avoid restating simple mechanics that are already clear from names and types.

**Non-Goals:**

- Do not change behavior.
- Do not add broad file-level tutorials.
- Do not comment every function or every line.

## Decisions

- Use short inline or block comments only where intent is not obvious from code.
- Prefer comments for policy decisions in `service.py`, `resolver.py`, `open_meteo.py`, and `time_now.py`.
- Leave simple MCP wrapper functions in `tools.py` alone unless a specific non-obvious behavior is added later.

## Risks / Trade-offs

- Excess comments can become stale -> keep comments tied to stable intent rather than implementation details.
- Comment-only changes can feel cosmetic -> scope them to known confusing behavior and LLM-tool orchestration edge cases.
