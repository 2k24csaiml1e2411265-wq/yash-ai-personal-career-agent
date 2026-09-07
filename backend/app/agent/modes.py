"""
Career modes.

Each mode changes three things about how the agent behaves:
  - system_prompt_addendum: tone/priorities appended to the base system prompt
  - suggested_questions: shown in the UI for that mode
  - preferred_tools: tools tried first, before the generic router order
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class ModeConfig:
    label: str
    description: str
    system_prompt_addendum: str
    suggested_questions: List[str]
    preferred_tools: List[str]


MODES: Dict[str, ModeConfig] = {
    "recruiter": ModeConfig(
        label="Recruiter",
        description="Quick, outcome-focused answers about fit for a role.",
        system_prompt_addendum=(
            "Answer as if speaking to a recruiter or hiring manager who is short on time. "
            "Lead with the most relevant fact, keep answers tight, and connect skills/projects "
            "to real-world capability rather than listing buzzwords."
        ),
        suggested_questions=[
            "Why would Yash be a good ML intern?",
            "What are Yash's strongest AI/ML projects?",
            "What internships has Yash completed?",
        ],
        preferred_tools=["experience_tool", "project_tool", "skills_tool"],
    ),
    "technical": ModeConfig(
        label="Technical",
        description="Deeper answers about architecture, tools, and implementation.",
        system_prompt_addendum=(
            "Answer with technical precision. Reference specific technologies, architecture, "
            "and engineering decisions where they are available in the verified context. "
            "It's fine to be more detailed here than in other modes."
        ),
        suggested_questions=[
            "Explain the architecture of ExamLens AI.",
            "What technologies does Yash use?",
            "Which project demonstrates the most ML depth?",
        ],
        preferred_tools=["project_tool", "skills_tool"],
    ),
    "project": ModeConfig(
        label="Project",
        description="Focused on exploring Yash's built projects.",
        system_prompt_addendum=(
            "Focus on Yash's projects: what problem each one solves, how it works, and what "
            "was built. Prefer concrete project details over generic profile summary."
        ),
        suggested_questions=[
            "Show me Yash's strongest project.",
            "Which projects use machine learning?",
            "Explain ExamLens AI.",
        ],
        preferred_tools=["project_tool"],
    ),
    "about": ModeConfig(
        label="About",
        description="Yash's background, education, and technical journey.",
        system_prompt_addendum=(
            "Focus on Yash's background, education, and technical journey — how his interests "
            "and experience connect, not just a list of facts."
        ),
        suggested_questions=[
            "Tell me about Yash's technical journey.",
            "What is Yash currently learning?",
            "What is Yash's educational background?",
        ],
        preferred_tools=["portfolio_search", "experience_tool"],
    ),
}

DEFAULT_MODE = "recruiter"


def get_mode(mode: str) -> ModeConfig:
    return MODES.get(mode, MODES[DEFAULT_MODE])
