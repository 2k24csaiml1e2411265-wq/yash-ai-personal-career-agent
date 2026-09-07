from __future__ import annotations

from fastapi import APIRouter, HTTPException, Request

from app.agent.orchestrator import handle_chat
from app.models.schemas import ChatRequest, ChatResponse
from app.services.rate_limiter import is_allowed

router = APIRouter(prefix="/api", tags=["chat"])


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest, http_request: Request) -> ChatResponse:
    client_id = http_request.client.host if http_request.client else "unknown"
    if not is_allowed(client_id):
        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded — please wait a moment before asking another question.",
        )
    return handle_chat(request)
