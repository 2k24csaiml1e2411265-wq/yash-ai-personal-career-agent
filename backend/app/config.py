"""
Central configuration for the Yash AI backend.

All environment-driven behavior (which LLM provider to call, where the
knowledge base lives, which origins may call the API) is resolved here so
the rest of the app never reads os.environ directly. This makes the
"fallback mode" requirement easy to reason about: if LLM_API_KEY is unset,
`settings.llm_configured` is False and the agent knows to degrade
gracefully instead of crashing.
"""
from __future__ import annotations

import os
from pathlib import Path
from typing import List

from dotenv import load_dotenv

# Load a .env file if present. In production (Render/Railway/etc.) real
# environment variables are used instead and this is a no-op.
load_dotenv()

BACKEND_DIR = Path(__file__).resolve().parent.parent  # .../backend
REPO_ROOT = BACKEND_DIR.parent  # repo root


def _bool_env(name: str, default: bool) -> bool:
    val = os.getenv(name)
    if val is None:
        return default
    return val.strip().lower() in {"1", "true", "yes", "on"}


class Settings:
    # --- App metadata ---
    app_name: str = "Yash AI — Personal Career Agent API"
    app_version: str = "1.0.0"

    # --- Data ---
    # Single source of truth for portfolio content lives in /data at the
    # repo root. Both the agent's retriever and the REST endpoints read
    # from here — nothing is duplicated into the frontend.
    data_dir: Path = Path(os.getenv("DATA_DIR") or str(REPO_ROOT / "data"))

    # --- LLM configuration ---
    llm_provider: str = os.getenv("LLM_PROVIDER", "none").strip().lower()
    llm_api_key: str = os.getenv("LLM_API_KEY", "").strip()
    llm_model_name: str = os.getenv("MODEL_NAME", "openai/gpt-oss-120b")
    llm_base_url: str = os.getenv(
        "LLM_BASE_URL", "https://api.groq.com/openai/v1/chat/completions"
    )
    llm_timeout_seconds: float = float(os.getenv("LLM_TIMEOUT_SECONDS", "20"))

    @property
    def llm_configured(self) -> bool:
        """True only when a real provider + key are both present."""
        return bool(self.llm_api_key) and self.llm_provider not in {"", "none"}

    # --- GitHub (optional live data) ---
    github_username: str = os.getenv("GITHUB_USERNAME", "2k24csaiml1e2411265-wq")
    github_token: str = os.getenv("GITHUB_TOKEN", "")  # optional, raises rate limit

    # --- CORS ---
    cors_origins: List[str] = [
        o.strip()
        for o in os.getenv(
            "CORS_ORIGINS",
            "http://localhost:5173,http://127.0.0.1:5173",
        ).split(",")
        if o.strip()
    ]

    # --- Retrieval ---
    retrieval_top_k: int = int(os.getenv("RETRIEVAL_TOP_K", "4"))
    retrieval_min_score: float = float(os.getenv("RETRIEVAL_MIN_SCORE", "0.12"))

    # --- Rate limiting (very lightweight, in-memory) ---
    rate_limit_enabled: bool = _bool_env("RATE_LIMIT_ENABLED", True)
    rate_limit_requests: int = int(os.getenv("RATE_LIMIT_REQUESTS", "30"))
    rate_limit_window_seconds: int = int(os.getenv("RATE_LIMIT_WINDOW_SECONDS", "60"))


settings = Settings()
