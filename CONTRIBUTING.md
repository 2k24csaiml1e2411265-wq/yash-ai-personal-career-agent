# Contributing

This is a personal portfolio project, but it's structured to be easy to extend.

## Editing personal data

All portfolio content lives in `data/*.json`. Update a project, add an
experience entry, or change a skill by editing the relevant file — nothing
else needs to change, since both the API and (eventually) the frontend read
from these files as the single source of truth.

**Anti-hallucination rule:** don't fill in a field with invented information.
Use `"TODO: ..."` as the value and it will pass through visibly rather than
silently.

## Backend development

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
pytest tests/ -v
```

New tools go in `backend/app/tools/`, following the `ToolResult` contract in
`app/tools/base.py`. New routing rules go in `backend/app/agent/intent.py`.

## Commit style

Small, focused commits with a clear message are preferred over large mixed
changes.
