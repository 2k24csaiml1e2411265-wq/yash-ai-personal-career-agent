from __future__ import annotations

from fastapi import APIRouter

from app.agent.orchestrator import _TOOL_FUNCS
from app.config import settings
from app.models.schemas import DiagnosticsResponse
from app.services.knowledge_base import knowledge_base

router = APIRouter(prefix="/api", tags=["diagnostics"])


@router.get("/diagnostics", response_model=DiagnosticsResponse)
def diagnostics() -> DiagnosticsResponse:
    sections = sorted({d.section for d in knowledge_base.documents})
    return DiagnosticsResponse(
        status="ok" if knowledge_base.documents else "empty_knowledge_base",
        document_count=len(knowledge_base.documents),
        sections_indexed=sections,
        available_tools=sorted(_TOOL_FUNCS.keys()),
        llm_configured=settings.llm_configured,
        llm_provider=settings.llm_provider,
        model_name=settings.llm_model_name,
        retrieval_backend="TF-IDF (scikit-learn) cosine similarity",
    )
