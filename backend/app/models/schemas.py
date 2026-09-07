"""Typed request/response models used across the API and agent."""
from __future__ import annotations

from typing import List, Literal, Optional

from pydantic import BaseModel, Field

AgentMode = Literal["recruiter", "technical", "project", "about"]


class ChatMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000)
    mode: AgentMode = "recruiter"
    history: List[ChatMessage] = Field(default_factory=list, max_length=20)


class Source(BaseModel):
    label: str  # e.g. "Projects → ExamLens AI"
    section: str  # e.g. "projects"
    ref_id: Optional[str] = None  # e.g. "examlens-ai"
    url: Optional[str] = None  # clickable link if one exists (e.g. /projects/:id)


class TraceStep(BaseModel):
    """One stage of the agent pipeline, surfaced to the UI as a live trace."""
    stage: Literal["intent", "tool_selection", "retrieval", "grounding", "generation"]
    label: str
    detail: str
    status: Literal["ok", "empty", "skipped"]


class ChatResponse(BaseModel):
    answer: str
    grounded: bool
    sources: List[Source] = Field(default_factory=list)
    suggested_followups: List[str] = Field(default_factory=list)
    tools_used: List[str] = Field(default_factory=list)
    trace: List[TraceStep] = Field(default_factory=list)
    latency_ms: float
    llm_used: bool


class DiagnosticsResponse(BaseModel):
    model_config = {"protected_namespaces": ()}

    status: str
    document_count: int
    sections_indexed: List[str]
    available_tools: List[str]
    llm_configured: bool
    llm_provider: str
    model_name: str
    retrieval_backend: str
