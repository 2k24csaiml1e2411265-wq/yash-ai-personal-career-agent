from app.services.knowledge_base import knowledge_base


def test_knowledge_base_loads_all_sections():
    assert knowledge_base.profile, "profile.json should load"
    assert knowledge_base.education, "education.json should load"
    assert knowledge_base.experience, "experience.json should load"
    assert knowledge_base.skills, "skills.json should load"
    assert knowledge_base.projects, "projects.json should load"
    assert knowledge_base.links, "links.json should load"


def test_documents_are_indexed_for_every_section():
    sections = {d.section for d in knowledge_base.documents}
    assert "profile" in sections
    assert "experience" in sections
    assert "projects" in sections
    assert "skills" in sections
    assert "links" in sections


def test_get_project_exact_id():
    project = knowledge_base.get_project("examlens-ai")
    assert project is not None
    assert project["name"] == "ExamLens AI"


def test_get_project_from_full_sentence():
    project = knowledge_base.get_project("Explain ExamLens AI in detail.")
    assert project is not None
    assert project["id"] == "examlens-ai"


def test_get_project_unknown_returns_none():
    assert knowledge_base.get_project("some project that does not exist") is None


def test_find_projects_by_technology():
    matches = knowledge_base.find_projects_by_technology("Prophet")
    assert any(p["id"] == "smart-campus-sustainability-dashboard" for p in matches)


def test_no_fabricated_certifications_or_achievements():
    # Certifications and achievements should contain only explicitly
    # provided portfolio data. The loader must not invent placeholder entries.

    assert isinstance(knowledge_base.certifications, list)
    assert isinstance(knowledge_base.achievements, list)

    for cert in knowledge_base.certifications:
        assert cert.get("name")
        assert cert.get("issuer")

    for achievement in knowledge_base.achievements:
        assert achievement.get("title")
