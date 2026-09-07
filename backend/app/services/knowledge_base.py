"""
Loads the verified knowledge base from /data/*.json and exposes it in two
shapes:

1. Raw, typed access for the tools (get_project(id), list_experience(), ...)
2. A flat list of `Document` chunks for the retriever, each tagged with the
   section/id it came from so answers can always cite a real source.

This module is the ONLY place that reads the JSON files. Everything else —
tools, retriever, API routers — goes through it, so there is exactly one
source of truth (matching the "Data Editability" requirement in the spec).
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

from app.config import settings


@dataclass
class Document:
    """A single retrievable chunk of verified personal knowledge."""
    id: str
    section: str  # profile | education | experience | projects | skills | certifications | links
    title: str
    text: str
    ref_id: Optional[str] = None
    url: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def source_label(self) -> str:
        section_title = self.section.replace("_", " ").title()
        return f"{section_title} → {self.title}"


def _load_json(filename: str) -> Any:
    path = settings.data_dir / filename
    if not path.exists():
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


class KnowledgeBase:
    def __init__(self) -> None:
        self.profile: Dict[str, Any] = _load_json("profile.json") or {}
        self.education: List[Dict[str, Any]] = _load_json("education.json") or []
        self.links: Dict[str, Any] = _load_json("links.json") or {}
        self.experience: List[Dict[str, Any]] = _load_json("experience.json") or []
        self.skills: Dict[str, List[str]] = _load_json("skills.json") or {}
        self.projects: List[Dict[str, Any]] = _load_json("projects.json") or []
        self.certifications: List[Dict[str, Any]] = _load_json("certifications.json") or []
        self.achievements: List[Dict[str, Any]] = _load_json("achievements.json") or []
        self.documents: List[Document] = self._build_documents()

    # ------------------------------------------------------------------ #
    # Typed lookups used by tools
    # ------------------------------------------------------------------ #
    def get_project(self, project_id: str) -> Optional[Dict[str, Any]]:
        query = project_id.strip().lower()
        needle = query.replace(" ", "-")
        for p in self.projects:
            if p["id"] == needle or p["name"].strip().lower() == query:
                return p
        # loose match, either direction, so this also handles a full
        # sentence query like "Explain ExamLens AI." that merely mentions
        # the project name rather than being only the name.
        for p in self.projects:
            name_l = p["name"].strip().lower()
            id_as_words = p["id"].replace("-", " ")
            if (
                needle in p["id"]
                or query in name_l
                or name_l in query
                or id_as_words in query
            ):
                return p
        return None

    def find_projects_by_technology(self, tech: str) -> List[Dict[str, Any]]:
        tech_l = tech.strip().lower()
        return [
            p for p in self.projects
            if any(tech_l in t.lower() for t in p.get("technologies", []))
        ]

    def find_projects_by_category(self, category: str) -> List[Dict[str, Any]]:
        cat_l = category.strip().lower()
        return [
            p for p in self.projects
            if any(cat_l in c.lower() for c in p.get("category", []))
        ]

    # ------------------------------------------------------------------ #
    # Document index for retrieval
    # ------------------------------------------------------------------ #
    def _build_documents(self) -> List[Document]:
        docs: List[Document] = []

        if self.profile:
            docs.append(Document(
                id="profile-about",
                section="profile",
                title=self.profile.get("name", "Profile"),
                text=" ".join(filter(None, [
                    self.profile.get("tagline", ""),
                    self.profile.get("positioning_statement", ""),
                    self.profile.get("about", ""),
                    self.profile.get("career_direction", ""),
                ])),
            ))
            if self.profile.get("currently_learning"):
                docs.append(Document(
                    id="profile-learning",
                    section="profile",
                    title="Currently Learning",
                    text=self.profile["currently_learning"],
                ))

        for edu in self.education:
            docs.append(Document(
                id=f"education-{edu.get('institution', 'edu')}",
                section="education",
                title=edu.get("institution", "Education"),
                text=" ".join(filter(None, [
                    edu.get("degree", ""),
                    edu.get("duration", ""),
                    edu.get("status", ""),
                    " ".join(edu.get("highlights", [])),
                ])),
            ))

        for exp in self.experience:
            docs.append(Document(
                id=f"experience-{exp['id']}",
                section="experience",
                title=f"{exp['role']} at {exp['organization']}",
                ref_id=exp["id"],
                text=" ".join(filter(None, [
                    exp.get("role", ""),
                    exp.get("organization", ""),
                    exp.get("duration", ""),
                    exp.get("description", ""),
                    " ".join(exp.get("technologies", [])),
                    " ".join(exp.get("highlights", [])),
                ])),
                metadata={"technologies": exp.get("technologies", [])},
            ))

        for proj in self.projects:
            docs.append(Document(
                id=f"project-{proj['id']}",
                section="projects",
                title=proj["name"],
                ref_id=proj["id"],
                url=f"/projects/{proj['id']}",
                text=" ".join(filter(None, [
                    proj.get("tagline", ""),
                    proj.get("short_description", ""),
                    proj.get("problem", ""),
                    proj.get("solution", ""),
                    " ".join(proj.get("features", [])),
                    " ".join(proj.get("technologies", [])),
                    " ".join(proj.get("category", [])),
                ])),
                metadata={"technologies": proj.get("technologies", []), "category": proj.get("category", [])},
            ))

        if self.skills:
            for category, items in self.skills.items():
                docs.append(Document(
                    id=f"skills-{category}",
                    section="skills",
                    title=category.replace("_", " ").title(),
                    text=f"{category.replace('_', ' ')}: " + ", ".join(items),
                    metadata={"items": items},
                ))

        for cert in self.certifications:
            cert_name = cert.get("name", "")
            issuer = cert.get("issuer", "")
            date = cert.get("date", "")
            description = cert.get("description", "")

            docs.append(Document(
                id=f"cert-{cert_name or 'cert'}",
                section="certifications",
                title=cert_name or "Certification",
                text=" ".join(filter(None, [
                    cert_name,
                    f"certification {cert_name}",
                    f"certificate {cert_name}",
                    f"credential {cert_name}",
                    f"issued by {issuer}",
                    issuer,
                    date,
                    description,
                ])),
                metadata={
                    "issuer": issuer,
                    "date": date,
                    "credential_url": cert.get("credential_url", ""),
                },
            ))
        if self.links:
            docs.append(Document(
                id="links",
                section="links",
                title="Contact & Profiles",
                text=f"GitHub {self.links.get('github', '')} LinkedIn {self.links.get('linkedin', '')} "
                     f"Email {self.links.get('email', '')} Resume {self.links.get('resume', '')}",
                metadata=dict(self.links),
            ))

        return docs


# Module-level singleton — the JSON files are small and static per process.
knowledge_base = KnowledgeBase()
