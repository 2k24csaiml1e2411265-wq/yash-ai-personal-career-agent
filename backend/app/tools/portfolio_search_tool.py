"""
Portfolio Search Tool
---------------------
Purpose: the general-purpose fallback tool. Runs the TF-IDF retriever
across every section of the knowledge base (profile, education,
experience, projects, skills, links) and returns the top matching
chunks. Used when the intent router can't confidently map a query to one
specific tool, or as a second pass when a specific tool finds nothing.

Input:  free-text query
Output: ToolResult with concatenated top-k chunks and one Source per chunk
"""
from __future__ import annotations

from app.rag.retriever import retriever
from app.models.schemas import Source
from app.tools.base import ToolResult
from app.config import settings

TOOL_NAME = "portfolio_search"


def run(query: str, top_k: int = None, min_score: float = None) -> ToolResult:
    try:
        top_k = top_k or settings.retrieval_top_k
        min_score = settings.retrieval_min_score if min_score is None else min_score

        chunks = retriever.search(query, top_k=top_k, min_score=min_score)
        if not chunks:
            return ToolResult(found=False, content="", tool_name=TOOL_NAME)

        content = "\n\n---\n\n".join(f"[{c.document.title}] {c.document.text}" for c in chunks)
        sources = [
            Source(
                label=c.document.source_label,
                section=c.document.section,
                ref_id=c.document.ref_id,
                url=c.document.url,
            )
            for c in chunks
        ]
        return ToolResult(found=True, content=content, sources=sources, tool_name=TOOL_NAME)
    except Exception:
        return ToolResult(found=False, content="", tool_name=TOOL_NAME)
