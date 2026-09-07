"""
Intent detection & tool routing.

This is deliberately a transparent, rule-based router rather than a second
LLM call: for a knowledge base this size the query vocabulary is small and
predictable (project names, tech names, "internship", "github", ...), so a
keyword/pattern router is both faster and easier to audit than an LLM
function-call step — and it still works with zero LLM configured, which
the fallback-mode requirement depends on.

`route()` returns an ordered list of tool names to try. The orchestrator
calls them in order and stops accumulating once it has enough grounded
context, but always falls back to `portfolio_search` if nothing more
specific matched.
"""
from __future__ import annotations

import re
from typing import List

from app.services.knowledge_base import knowledge_base

_LINK_PATTERNS = [r"\bgithub\b", r"\blinkedin\b", r"\bresume\b", r"\bcv\b", r"\bcontact\b", r"\bemail\b"]
_EXPERIENCE_PATTERNS = [
    r"\bintern(ship)?s?\b", r"\bexperience\b", r"\bwork(ed)?\b", r"\bemployer\b",
    r"\bflyrank\b", r"\b1m1b\b", r"\bedunet\b",
]
_SKILLS_PATTERNS = [
    r"\bskills?\b", r"\btech(nologies|nology)?\b", r"\bstack\b", r"\blanguages?\b",
    r"\bframeworks?\b", r"\btools?\b", r"\bprogramming\b",
]
_CERTIFICATION_PATTERNS = [
    r"\bcertifications?\b",
    r"\bcertificates?\b",
    r"\bcredentials?\b",
    r"\bcertified\b",
    r"\bcourses?\b",
]
_EDUCATION_PATTERNS = [
    r"\beducation\b",
    r"\beducational\b",
    r"\bdegree\b",
    r"\bcollege\b",
    r"\buniversity\b",
    r"\bstudying\b",
    r"\bstudies\b",
    r"\bacademic\b",
    r"\bqualification\b",
]
_PROFILE_PATTERNS = [
    r"\bwho is yash\b",
    r"\bwho is yash kushwaha\b",
    r"\btell me about yash\b",
    r"\babout yash\b",
    r"\byash's background\b",
    r"\byash kushwaha\b",
]
_PROJECT_PATTERNS = [
    r"\bprojects?\b", r"\bbuil(t|d)\b", r"\bexamlens\b", r"\bsustainability\b",
    r"\bdashboard\b",
]
_GITHUB_LIVE_PATTERNS = [r"\brepos(itories)?\b", r"\bgithub activity\b", r"\bcommits?\b"]
_ABOUT_PATTERNS = [
    r"\bwho is\b", r"\babout\b", r"\bcareer direction\b", r"\bcurrently learning\b",
     r"\bcollege\b", r"\bdegree\b", r"\bstudying\b", r"\bjourney\b",
    r"\bbackground\b",
]

_KNOWN_PROJECT_NAMES = [p["name"].lower() for p in knowledge_base.projects] + [
    p["id"].replace("-", " ") for p in knowledge_base.projects
]

_ALL_SKILL_ITEMS = sorted(
    {
        item.lower()
        for items in knowledge_base.skills.values()
        for item in items
        # "GitHub"/"Git" are also profile-link words handled by
        # _LINK_PATTERNS — excluding them here avoids a query like
        # "what is Yash's GitHub" being misrouted to the skills tool.
        if item.lower() not in {"github", "git"}
    },
    key=len,
    reverse=True,  # match longer names first, e.g. "machine learning" before "learning"
)


def _mentions_known_skill(text: str) -> bool:
    return any(re.search(rf"\b{re.escape(item)}\b", text) for item in _ALL_SKILL_ITEMS)


def _matches_any(patterns: List[str], text: str) -> bool:
    return any(re.search(p, text) for p in patterns)


def route(query: str) -> List[str]:
    q = query.lower().strip()
    tools: List[str] = []

    mentions_project_name = any(name in q for name in _KNOWN_PROJECT_NAMES)

    if mentions_project_name or _matches_any(_PROJECT_PATTERNS, q):
        tools.append("project_tool")
    if _matches_any(_SKILLS_PATTERNS, q):
        tools.append("skills_tool")
    if _mentions_known_skill(q) and "skills_tool" not in tools:
        tools.append("skills_tool")
    if _matches_any(_CERTIFICATION_PATTERNS, q):
        tools.append("certifications_tool")
    if _matches_any(_EXPERIENCE_PATTERNS, q):
        tools.append("experience_tool")
    if _matches_any(_GITHUB_LIVE_PATTERNS, q):
        tools.append("github_tool")
    if _matches_any(_EDUCATION_PATTERNS, q):
        tools.append("education_tool")
    if _matches_any(_PROFILE_PATTERNS, q):
        tools.append("profile_tool")
    if _matches_any(_LINK_PATTERNS, q):
        tools.append("links_tool")
    if _matches_any(_ABOUT_PATTERNS, q):
        # "about"/"background"/"journey" questions benefit from both a
        # broad profile search and real experience entries — this is
        # gated on the query's own wording, unlike a blanket mode fallback.
        tools.append("portfolio_search")
        tools.append("experience_tool")

    if not tools:
        tools.append("portfolio_search")

    # portfolio_search always runs last as a safety net if nothing else
    # produced grounded content — the orchestrator adds it if needed.
    return tools
