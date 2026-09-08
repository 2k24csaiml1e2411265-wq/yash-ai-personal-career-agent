# Yash AI — Personal AI Career Agent

> A grounded AI career agent that answers questions about my education, experience, projects, skills, certifications, and GitHub activity using retrieval, typed tools, and LLM generation.

[![Python](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18-61DAFB.svg)](https://react.dev/)
[![TypeScript](https://img.shields.io/badge/TypeScript-Frontend-3178C6.svg)](https://www.typescriptlang.org/)
[![Tests](https://img.shields.io/badge/Tests-17%20Passing-success.svg)](#testing)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## Overview

**Yash AI** is my personal AI career agent and portfolio website.

Instead of connecting a language model directly to a portfolio and allowing it to answer anything, the system first identifies the user's intent, selects the appropriate tool, retrieves verified information from my portfolio knowledge base, checks whether the answer is grounded, and only then generates a response.

The result is a portfolio assistant designed around one core principle:

> **If the information is not verified, the agent should say so instead of guessing.**

The system can answer questions about:

- 👤 Personal profile
- 🎓 Education
- 💼 Experience
- 🚀 Projects
- 🧠 Technical skills
- 📜 Certifications
- 🏆 Achievements
- 🐙 Live GitHub activity
- 🔗 Verified portfolio links
- 🤖 Career-oriented questions

---

# Why I Built This

Most AI portfolio websites are essentially:

```text
User → LLM → Answer
