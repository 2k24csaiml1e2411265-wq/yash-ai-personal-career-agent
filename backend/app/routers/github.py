from __future__ import annotations

from typing import Any, Dict

from fastapi import APIRouter

from app.tools import github_tool

router = APIRouter(prefix="/api", tags=["github"])


@router.get("/github")
def get_github_activity() -> Dict[str, Any]:
    result = github_tool.run("")
    return {
        "available": result.found,
        "summary": result.content if result.found else None,
        "note": None if result.found else (
            "Live GitHub data is unavailable right now (no network access, no username "
            "configured, or the API rate-limited this request). No fabricated data is shown."
        ),
    }
