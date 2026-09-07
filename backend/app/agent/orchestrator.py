"""
Agent Orchestrator.

This is the piece that turns "a chat message" into "a grounded answer",
following the pipeline described in docs/agent-design.md:

    query -> intent detection -> tool selection -> retrieval ->
    verified context -> LLM (or fallback composer) -> grounded answer -> sources

Every stage is recorded as a TraceStep and returned to the frontend, so
the chat UI can show — truthfully, because it's the real pipeline state,
not a fake animation — what the agent actually did to answer the question.
"""
from __future__ import annotations

import time
from typing import Dict, List

from app.agent import composer, intent, modes
from app.agent.prompts import BASE_SYSTEM_PROMPT
from app.models.schemas import ChatRequest, ChatResponse, Source, TraceStep
from app.services import llm_client
from app.tools import (
    certifications_tool,
    education_tool,
    experience_tool,
    github_tool,
    links_tool,
    portfolio_search_tool,
    profile_tool,
    project_tool,
    skills_tool,
)
from app.tools.base import ToolResult

_TOOL_FUNCS = {
    "project_tool": project_tool.run,
    "experience_tool": experience_tool.run,
    "skills_tool": skills_tool.run,
    "links_tool": links_tool.run,
    "github_tool": github_tool.run,
    "portfolio_search": portfolio_search_tool.run,
    "certifications_tool": certifications_tool.run,
    "education_tool": education_tool.run,
    "profile_tool": profile_tool.run,
}
_GENERIC_PROJECT_MARKERS = ["strongest", "best project", "show me", "favorite project", "favourite project"]


def _reorder_by_mode(tool_order: List[str], preferred: List[str]) -> List[str]:
    preferred_present = [t for t in preferred if t in tool_order]
    rest = [t for t in tool_order if t not in preferred_present]
    return preferred_present + rest


def _run_tools(query: str, tool_order: List[str]) -> Dict[str, ToolResult]:
    results: Dict[str, ToolResult] = {}
    for tool_name in tool_order:
        func = _TOOL_FUNCS.get(tool_name)
        if not func:
            continue
        result = func(query)

        # A "which project should I look at" style query won't name a
        # specific project — fall back to a full project summary instead
        # of reporting "not found".
        if (
            tool_name == "project_tool"
            and not result.found
            and any(marker in query.lower() for marker in _GENERIC_PROJECT_MARKERS)
        ):
            result = project_tool.run_list_all()

        results[tool_name] = result
    return results


def handle_chat(request: ChatRequest) -> ChatResponse:
    start = time.perf_counter()
    trace: List[TraceStep] = []
    query = request.message.strip()
    mode_config = modes.get_mode(request.mode)

    # 1. Intent detection
    routed_tools = intent.route(query)
    ordered_tools = _reorder_by_mode(routed_tools, mode_config.preferred_tools)
    trace.append(TraceStep(
        stage="intent",
        label="Intent detected",
        detail=f"Mode: {mode_config.label}. Candidate tools: {', '.join(ordered_tools)}",
        status="ok",
    ))

    # 2. Tool selection (recorded distinctly from execution for transparency)
    trace.append(TraceStep(
        stage="tool_selection",
        label="Tools selected",
        detail=", ".join(ordered_tools),
        status="ok" if ordered_tools else "empty",
    ))

    # 3. Retrieval — execute tools in priority order
    tool_results = _run_tools(query, ordered_tools)

    # Safety net: always fall back to the broad portfolio search if nothing
    # more specific matched. Note this deliberately does NOT fall through to
    # every mode-preferred tool for any unmatched query — several tools
    # (e.g. experience_tool) return a broad summary when nothing specific
    # matches, which is only appropriate when the query's own content put
    # them in the routed list, not as a blanket fallback for any question.
    if not any(r.found for r in tool_results.values()) and "portfolio_search" not in tool_results:
        tool_results["portfolio_search"] = portfolio_search_tool.run(query)

    found_results = [r for r in tool_results.values() if r.found]
    tools_used = [r.tool_name for r in found_results]

    context_blocks = [r.content for r in found_results if r.content]
    sources: List[Source] = []
    seen_labels = set()
    for r in found_results:
        for s in r.sources:
            if s.label not in seen_labels:
                sources.append(s)
                seen_labels.add(s.label)

    trace.append(TraceStep(
        stage="retrieval",
        label="Knowledge base retrieval",
        detail=f"{len(found_results)} tool(s) returned verified matches, {len(sources)} source(s)."
               if found_results else "No verified matches found in the knowledge base.",
        status="ok" if found_results else "empty",
    ))

    grounded = bool(context_blocks)
    trace.append(TraceStep(
        stage="grounding",
        label="Grounding check",
        detail="Verified context available — answer will be grounded."
               if grounded else "No verified context — refusing to speculate.",
        status="ok" if grounded else "empty",
    ))

    # 4. Generation
    if not grounded:
        answer = composer.UNKNOWN_ANSWER
        llm_used = False
        trace.append(TraceStep(
            stage="generation", label="Response generation",
            detail="Skipped generation — nothing grounded to answer from.", status="skipped",
        ))
    else:
        system_prompt = f"{BASE_SYSTEM_PROMPT} {mode_config.system_prompt_addendum}"
        llm_answer = llm_client.generate(system_prompt, query, context_blocks)
        if llm_answer:
            answer = llm_answer
            llm_used = True
            trace.append(TraceStep(
                stage="generation", label="LLM generation",
                detail="Answer generated by the configured LLM, grounded in verified context.",
                status="ok",
            ))
        else:
            answer = composer.compose(query, context_blocks)
            llm_used = False
            trace.append(TraceStep(
                stage="generation", label="Template composition (fallback mode)",
                detail="No LLM configured (or the call failed) — composed the answer directly "
                       "from verified context instead.",
                status="ok",
            ))

    suggested = [q for q in mode_config.suggested_questions if q.lower() != query.lower()][:3]

    latency_ms = round((time.perf_counter() - start) * 1000, 2)

    return ChatResponse(
        answer=answer,
        grounded=grounded,
        sources=sources,
        suggested_followups=suggested,
        tools_used=tools_used,
        trace=trace,
        latency_ms=latency_ms,
        llm_used=llm_used,
    )
