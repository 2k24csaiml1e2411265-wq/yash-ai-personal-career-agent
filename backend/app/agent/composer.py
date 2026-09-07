"""
Fallback composer.

Turns retrieved, verified context into a readable answer WITHOUT an LLM.
This is what keeps the product fully functional in fallback mode (no
LLM_API_KEY configured) — every tool result is already human-readable
text pulled straight from the knowledge base, so composing an answer is
mostly about trimming it to a reasonable length and adding a short lead-in
sentence, not synthesizing new content.
"""
from __future__ import annotations

from typing import List

UNKNOWN_ANSWER = "I don't have verified information about that in Yash's portfolio yet."

_MAX_CHARS = 900


def compose(query: str, context_blocks: List[str]) -> str:
    if not context_blocks:
        return UNKNOWN_ANSWER

    body = "\n\n".join(context_blocks).strip()
    if len(body) > _MAX_CHARS:
        body = body[:_MAX_CHARS].rsplit(" ", 1)[0] + "…"

    return body
