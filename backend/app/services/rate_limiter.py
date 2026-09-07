"""
A deliberately simple in-memory rate limiter.

Good enough for a single-process portfolio API to avoid casual abuse of
the (potentially paid) LLM endpoint. Not a substitute for a real
distributed limiter if this were a multi-instance production service —
that trade-off is documented in docs/deployment.md.
"""
from __future__ import annotations

import time
from collections import defaultdict, deque
from typing import Deque, Dict

from app.config import settings

_hits: Dict[str, Deque[float]] = defaultdict(deque)


def is_allowed(client_id: str) -> bool:
    if not settings.rate_limit_enabled:
        return True

    now = time.time()
    window_start = now - settings.rate_limit_window_seconds
    hits = _hits[client_id]

    while hits and hits[0] < window_start:
        hits.popleft()

    if len(hits) >= settings.rate_limit_requests:
        return False

    hits.append(now)
    return True
