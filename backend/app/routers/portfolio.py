from __future__ import annotations

from typing import Any, Dict, List

from fastapi import APIRouter, HTTPException

from app.agent.modes import MODES
from app.services.knowledge_base import knowledge_base

router = APIRouter(prefix="/api", tags=["portfolio"])


@router.get("/profile")
def get_profile() -> Dict[str, Any]:
    return knowledge_base.profile


@router.get("/education")
def get_education() -> List[Dict[str, Any]]:
    return knowledge_base.education


@router.get("/links")
def get_links() -> Dict[str, Any]:
    return knowledge_base.links


@router.get("/experience")
def get_experience() -> List[Dict[str, Any]]:
    return knowledge_base.experience


@router.get("/skills")
def get_skills() -> Dict[str, List[str]]:
    return knowledge_base.skills


@router.get("/certifications")
def get_certifications() -> List[Dict[str, Any]]:
    return knowledge_base.certifications


@router.get("/achievements")
def get_achievements() -> List[Dict[str, Any]]:
    return knowledge_base.achievements


@router.get("/projects")
def get_projects() -> List[Dict[str, Any]]:
    return knowledge_base.projects


@router.get("/projects/{project_id}")
def get_project(project_id: str) -> Dict[str, Any]:
    project = knowledge_base.get_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail=f"No project found with id '{project_id}'")
    return project


@router.get("/modes")
def get_modes() -> Dict[str, Any]:
    return {
        key: {
            "label": cfg.label,
            "description": cfg.description,
            "suggested_questions": cfg.suggested_questions,
        }
        for key, cfg in MODES.items()
    }
