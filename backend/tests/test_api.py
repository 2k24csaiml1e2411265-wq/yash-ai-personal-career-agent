from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_endpoint():
    res = client.get("/api/health")
    assert res.status_code == 200
    assert res.json() == {"status": "ok"}


def test_diagnostics_endpoint_reports_healthy_knowledge_base():
    res = client.get("/api/diagnostics")
    assert res.status_code == 200
    body = res.json()
    assert body["status"] == "ok"
    assert body["document_count"] > 0
    assert "projects" in body["sections_indexed"]


def test_projects_endpoint_returns_list_without_dataanalystenv():
    res = client.get("/api/projects")
    assert res.status_code == 200
    projects = res.json()
    assert len(projects) >= 1
    ids = [p["id"] for p in projects]
    names = [p["name"].lower() for p in projects]
    assert "openenv-data-analyst-environment" not in ids
    assert not any("dataanalyst" in n or "openenv" in n for n in names)


def test_single_project_endpoint():
    res = client.get("/api/projects/examlens-ai")
    assert res.status_code == 200
    assert res.json()["name"] == "ExamLens AI"


def test_single_project_endpoint_404_for_unknown_id():
    res = client.get("/api/projects/does-not-exist")
    assert res.status_code == 404


def test_chat_endpoint_grounded_answer():
    res = client.post("/api/chat", json={"message": "Explain ExamLens AI.", "mode": "project"})
    assert res.status_code == 200
    body = res.json()
    assert body["grounded"] is True
    assert "project_tool" in body["tools_used"]
    assert len(body["sources"]) > 0
    assert len(body["trace"]) == 5  # intent, tool_selection, retrieval, grounding, generation


def test_chat_endpoint_unknown_question_is_not_fabricated():
    res = client.post(
        "/api/chat", json={"message": "What is Yash's annual salary?", "mode": "recruiter"}
    )
    assert res.status_code == 200
    body = res.json()
    assert body["grounded"] is False
    assert "don't have verified information" in body["answer"].lower()
    assert body["sources"] == []


def test_chat_endpoint_rejects_empty_message():
    res = client.post("/api/chat", json={"message": "", "mode": "recruiter"})
    assert res.status_code == 422  # pydantic min_length validation


def test_chat_endpoint_rejects_invalid_mode():
    res = client.post("/api/chat", json={"message": "Hello", "mode": "not-a-real-mode"})
    assert res.status_code == 422


def test_chat_endpoint_defaults_mode_when_omitted():
    res = client.post("/api/chat", json={"message": "What internships has Yash completed?"})
    assert res.status_code == 200
    assert res.json()["grounded"] is True
