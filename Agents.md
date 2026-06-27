# Gemini Workspace Rules — Traveller

## 1. Project Overview
**Traveller** is a multi-agent travel itinerary generation system using a FastAPI backend and static HTML/JS/Tailwind frontend.
* **AI Backend**: Gemini 2.5 Flash Lite via `google-genai` SDK.
* **Orchestration**: Custom 5-agent pipeline (Orchestrator, Research, Logistics, Budget, Review).

## 2. Multi-Session Constraints (CRITICAL)
This project is implemented across 10 sequential sessions guided by [ImplementationPlan.md](file:///c:/Projects/Ai%20travel%20agent/ImplementationPlan.md).
* **Strict Scope Isolation**: Focus *only* on the current sprint described in the starter prompt. Do not write code or create files for future sprints.
* **Handover Protocol**: Before ending each session, you MUST:
  1. Check off completed checklist items in [ImplementationPlan.md](file:///c:/Projects/Ai%20travel%20agent/ImplementationPlan.md).
  2. Mark the current active sprint as `[x] Completed`.
  3. Write a brief technical summary under the "Progress History" section of that file.

## 3. Tech Stack & Standards
* **Backend**: FastAPI (Python 3.10+), Pydantic v2, `pytest` (tests in `app/tests/`).
* **Frontend**: Vanilla HTML/JS, CDN-loaded Tailwind CSS, Leaflet.js for maps. Code integrated from Stitch designs in `stitch_aether_travel_landing_page/`.
* **Design Guidelines**: Default to Obsidian Void background (#0B0F19), Slate Glass card containers, Aurora Teal (#0D9488) accents, and Outfit/Plus Jakarta Sans typography (see [DESIGN.md](file:///c:/Projects/Ai%20travel%20agent/DESIGN.md)).

## 4. Gemini SDK Integration
* **API SDK**: Use the official `google-genai` Python library.
* **Model**: Use `gemini-2.5-flash-lite`.
* **Parameters**: Temperature `0.3` for constraint extraction and orchestration; `0.7` for itinerary generation and agent prose.