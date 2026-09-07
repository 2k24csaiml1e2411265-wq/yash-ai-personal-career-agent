"""
LLM client.

Talks to any OpenAI-compatible chat-completions endpoint (Groq, OpenAI,
Together, etc.) based on LLM_PROVIDER / LLM_API_KEY / MODEL_NAME /
LLM_BASE_URL in the environment. If no key is configured, or the call
fails for any reason, `generate()` returns None — callers must treat that
as "use the fallback template", never raise it up as a hard error. This is
what keeps the app alive with zero configuration (see docs/deployment.md,
"Fallback mode").
"""
from __future__ import annotations

import logging
from typing import List, Optional

import httpx

from app.config import settings

logger = logging.getLogger("yash_ai.llm")


def generate(system_prompt: str, user_message: str, context_blocks: List[str]) -> Optional[str]:
    if not settings.llm_configured:
        return None

    context_text = "\n\n".join(context_blocks) if context_blocks else "(no verified context retrieved)"
    grounded_system_prompt = (
        f"{system_prompt}\n\n"
        "You must answer ONLY using the verified context below. Do not use outside knowledge "
        "about the person. If the context does not contain the answer, say so plainly instead "
        "of guessing.\n\n"
        f"VERIFIED CONTEXT:\n{context_text}"
    )

    payload = {
        "model": settings.llm_model_name,
        "messages": [
            {"role": "system", "content": grounded_system_prompt},
            {"role": "user", "content": user_message},
        ],
        "temperature": 0.3,
        "max_tokens": 500,
    }
    headers = {
        "Authorization": f"Bearer {settings.llm_api_key}",
        "Content-Type": "application/json",
    }

    try:
        with httpx.Client(timeout=settings.llm_timeout_seconds) as client:
            resp = client.post(settings.llm_base_url, json=payload, headers=headers)
            resp.raise_for_status()
            data = resp.json()
            return data["choices"][0]["message"]["content"].strip()
    except Exception as exc:  # network error, timeout, bad response shape, etc.
        logger.warning("LLM call failed, falling back to template response: %s", exc)
        return None
