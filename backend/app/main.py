"""
Yash AI — Personal Career Agent API.

Entrypoint that wires together CORS, routers, and a couple of
process-wide error handlers. Run with:

    uvicorn app.main:app --reload

See docs/development.md for the full local setup.
"""
from __future__ import annotations

import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import chat, diagnostics, github, portfolio

logging.basicConfig(level=logging.INFO)

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description=(
        "Backend for Yash Kushwaha's personal AI career agent — a grounded, "
        "tool-using assistant answering questions about his projects, skills, "
        "and experience from a verified knowledge base."
    ),
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

app.include_router(portfolio.router)
app.include_router(chat.router)
app.include_router(github.router)
app.include_router(diagnostics.router)


@app.get("/")
def root() -> dict:
    return {
        "service": settings.app_name,
        "version": settings.app_version,
        "status": "running",
        "docs": "/docs",
    }


@app.get("/api/health")
def health() -> dict:
    return {"status": "ok"}
