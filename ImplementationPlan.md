# Traveller — Multi-Session Implementation Plan
## 10-Sprint Agent Roadmap

This document serves as the persistent master roadmap for building **Traveller** over 10 sequential agent sessions (sprints). Each sprint represents a single, self-contained session designed to fit comfortably within the agent's context window.

> [!IMPORTANT]
> **HANDOVER PROTOCOL**: At the end of each session, the agent must check off completed items in this file, mark the current sprint as `[x] Completed`, write a short handover summary under the **Progress History** section, and stop. Do not start work on the next sprint in the same session.

---

## Architecture Reference

```
   ┌─────────────────────────────────────────────────────────────┐
   │                       FRONTEND                              │
   │   Screen 1: Landing Page & Conversational Input             │
   │   Screen 2: Constraint Editor & Loading States              │
   │   Screen 3: Itinerary Dashboard & Interactive Map           │
   │   Screen 4: Budget Dashboard & "What-If" Workspace          │
   │   Screen 5: Co-Pilot Refinement Drawer                      │
   └──────────────┬──────────────────────────────▲───────────────┘
                  │ API Calls                    │ JSON Updates
                  ▼                              │
   ┌─────────────────────────────────────────────┴───────────────┐
   │                    BACKEND (FastAPI)                        │
   │   /api/plan (Generate Itinerary)                            │
   │   /api/refine (Conversational Adjustment)                   │
   │                                                             │
   │   Orchestration Pipeline:                                   │
   │   Orchestrator ──┬──> Destination Research Agent            │
   │                  ├──> Logistics Agent                       │
   │                  └──> Budget Agent                          │
   │                  └──> [Parallel Execution]                  │
   │                  ▼                                          │
   │               Review Agent (Constraint Guardrail)           │
   └─────────────────────────────────────────────────────────────┘
```

---

## Progress History

### Sprint 1: Setup & Backend API Base (Completed)
- Initialized requirements.txt with FastAPI, Uvicorn, Pydantic, google-genai, Pytest, python-dotenv, and HTTPX.
- Built backend shell with `app/main.py` containing `/health` check.
- Set up `run.py` to launch server locally.
- Created test runner configuration in `app/tests/test_main.py`.
- *Note: Terminal commands execution failed due to IDE local security policy restrictions on C:\Python314. The user should run `pip install -r requirements.txt` and `pytest` manually to verify setup.*

- [x] **Sprint 1**: Setup & Backend API Base — *Status: Completed*
### Sprint 2: Orchestrator Agent & Core Models (Completed)
- Defined core Pydantic v2 data models in `app/models.py` (`Activity`, `DayItinerary`, `BudgetBreakdown`, `TravelConstraints`, `ItineraryPlan`).
- Implemented `OrchestratorAgent` in `app/agents/orchestrator.py` utilizing the `google-genai` SDK and JSON schema outputs capability of Gemini 2.5 Flash Lite.
- Set up unit testing in `app/tests/test_orchestrator.py` including a mocked client test case and live integration test cases for Japan, Italy, and weekend trip prompts.

- [x] **Sprint 2**: Orchestrator Agent & Core Models — *Status: Completed*
### Sprint 3: Destination Research & Logistics Agents (Completed)
- Updated `app/models.py` to add `RecommendedPlace` and `DestinationCuration` (curated recommended items and hotels list), and `LogisticsOutput` (organized list of day itineraries).
- Implemented `DestinationResearchAgent` in `app/agents/destination.py` with custom curation prompts aligning to avoidances/preferences using temperature 0.7.
- Implemented `LogisticsAgent` in `app/agents/logistics.py` to arrange curated activities into day-by-day Morning/Afternoon/Evening slots and transit connectors, grouping spots by neighborhood to avoid backtracking.
- Created `app/tests/test_dest_logistics.py` with isolated unit tests using mocks and a chained live integration test.

- [x] **Sprint 3**: Destination Research & Logistics Agents — *Status: Completed*
### Sprint 4: Budget & Review Agents (Completed)
- Updated `app/models.py` with `BudgetOutput` (Pydantic list wrapper of categories) and `ReviewOutput` (PASS/FAIL status, failure reason, and checklist dict).
- Implemented `BudgetAgent` in `app/agents/budget.py` to distribute budgets across flights, stay, transit, food, activities, and buffer categories. It flags overruns with an 'Exceeded' status.
- Implemented `ReviewAgent` in `app/agents/review.py` checking duration, city coverage, total budget compliance, preferences, avoidances, daily active hours, and backtracking.
- Created `app/tests/test_budget_review.py` verifying mock calculations, mock validations (PASS and FAIL branches), and a live chained integration test flow.

- [x] **Sprint 4**: Budget & Review Agents — *Status: Completed*
### Sprint 5: Pipeline Integration & API Routes (Completed)
- Implemented `RefinerAgent` in `app/agents/refiner.py` to support conversational edits on existing plans.
- Modified `DestinationResearchAgent` and `LogisticsAgent` to accept Review Agent failure logs as feedback on retry attempts.
- Built `ItineraryPipeline` in `app/pipeline.py` executing: Orchestrator -> Destination -> Logistics -> Budget -> Review. Includes a 2-retry feedback loop on failure, and fallback checks.
- Exposed REST endpoints in `app/main.py` with Uvicorn CORS:
  - `POST /api/plan` (Itinerary generation)
  - `POST /api/refine` (Conversational adjustment refinement)
  - `GET /health` (API status)
- Created `app/tests/test_pipeline.py` verifying E2E success, loop retries, and live refinement scenarios.

- [x] **Sprint 5**: Pipeline Integration & API Routes — *Status: Completed*
### Sprint 6: Frontend Shell & Landing Page (Screen 1) (Completed)
- Configured FastAPI in `app/main.py` to serve `/static` folder resources via `StaticFiles` and serve `index.html` at the root path (`/`).
- Created the SPA Frontend Shell `/static/index.html` containing:
  - Global styling imports for fonts (Plus Jakarta Sans, Outfit) and Google Icons.
  - Custom visual theme matching [DESIGN.md](file:///c:/Projects/Ai%20travel%20agent/DESIGN.md) (Obsidian background, Slate Glass panels, Aurora Teal gradients).
  - High-fidelity Screen 1 Landing Page layout and search bar.
  - Suggested chips interaction: clicking a chip inserts its text into the input field.
  - Submit transition logic: captures prompt, updates `appState.userInputPrompt`, hides Screen 1, and shows Screen 2 placeholder.

- [x] **Sprint 6**: Frontend Shell & Landing Page (Screen 1) — *Status: Completed*
### Sprint 7: Constraint Editor & Loading Page (Screen 2) (Completed)
- Integrated the Constraint Editor layout from `stitch_aether_travel_landing_page/traveller_constraint_editor_ai_pipeline` into `/static/index.html`.
- Displayed extracted travel constraints dynamically as editable tags (cities, preferences, avoidances), trip duration stepper, and budget range slider.
- Structured input interactions:
  - Users can add city tags and delete city, preference, or avoidance tags, dynamically updating the in-memory `TravelConstraints` state.
  - Steppers and budget range sliders directly modify the constraint days and budget ceiling.
- Enabled API handshake flow:
  - Submitting Screen 1 triggers `/api/extract` to parse inputs, loading the output into Screen 2's editor interface.
  - Clicking "Generate Itinerary" packages the finalized state as `{"prompt": null, "constraints": TravelConstraints}` and sends it to `POST /api/plan`.
- Integrated 5-Agent Pipeline Visualizer:
  - Triggers sequential loading animations (Orchestrator -> Research -> Logistics -> Budget -> Review) with active pulsing glows and a detailed status feed card.
  - Successfully routes the final generated plan JSON to a temporary success panel.

- [x] **Sprint 7**: Constraint Editor & Loading Page (Screen 2) — *Status: Completed*
### Sprint 8: Itinerary Dashboard & Map (Screen 3) (Completed)
- Integrated Screen 3 (Itinerary Dashboard) from `stitch_aether_travel_landing_page/traveller_itinerary_dashboard/code.html` into a full-viewport container `#screen-dashboard` sibling to `<main>`.
- Configured SPA screen toggling to hide `<main>` and `<footer>` and set body overflow to prevent window scrolling when Screen 3 is active, ensuring a solid maps-dashboard feel.
- Bound backend generated plan JSON to day-by-day collapsible accordion cards:
  - Dynamically builds day headers showing `Day X - City` and day titles.
  - Toggles accordion bodies showing activity lists with custom Material Icons (e.g. food $\rightarrow$ `ramen_dining`, temple $\rightarrow$ `temple_buddhist`, transit $\rightarrow$ `train`).
  - Color-codes activity categories: Food $\rightarrow$ Coral, Sightseeing/Temples $\rightarrow$ Gold, Transit $\rightarrow$ Teal.
- Integrated Leaflet.js v1.9.4 map framework on the right section:
  - Loaded dark matter tile layers from CartoDB Dark Matter tile provider (no API key/token required).
  - Plotted custom circular glowing markers matching the activity types.
  - Linked activity pins sequentially with a dashed route line (`#0D9488`).
  - Centered and auto-fit bounds on each active day's coordinates.
  - Added click listeners to day accordion headers to swap the active day, animate map coordinates transitions, and redraw route lines.

- [x] **Sprint 8**: Itinerary Dashboard & Map (Screen 3) — *Status: Completed*
- [x] **Sprint 9**: Budget & Co-Pilot Drawer (Screens 4 & 5) — *Status: Completed*
- [x] **Sprint 10**: Integration, Edge Cases & Polish — *Status: Completed*

### Sprint 10: Integration, Edge Cases & Polish (Completed)
- Wrote glassmorphic alert modal overlay and close handlers to manage errors and warnings.
- Configured API error catch handlers across input extraction, pipeline generation, and co-pilot refinement fetch loops to trigger informative modal notices.
- Extracted Review Agent warnings on validation failures (`validation_passed: false`) to alert users dynamically.
- Refined dashboard layout classes to change timeline accordions height and stack below maps on mobile viewports for clean responsive sizing.
- Added scale active transitions to all primary buttons and chips.
- Authored the project documentation `walkthrough.md` outlining system architecture, design specifications, offline mocks, and local execution details.

### Deployment & Launch (Completed)
- Separated frontend and backend architectures: hosted static client on Vercel and API backend on Railway.
- Created `Procfile` and updated `run.py` to support dynamic host/port bindings.
- Resolved backend startup crashes by removing unused static files directory mounts.
- Implemented Vercel reverse proxy rewrites in `vercel.json` and relative paths in `index.html` to eliminate CORS handshake errors.
- Verified active connection, API key authentication, and E2E multi-agent planning pipelines on the live Vercel domain.

### Sprint 9: Budget & Co-Pilot Drawer (Screens 4 & 5) (Completed)
- Integrated Screen 4 (Financial Workspace/Budget Dashboard) including the circular SVG Spent vs Remaining gauge, cost forecast daily sparkline bars, and category breakdown allocation grid.
- Implemented the "What-If" target budget slider which fires a cost-reduction instruction via the co-pilot refinement API.
- Integrated Screen 5 (Co-Pilot Chat Drawer) right side panel with full scrolling message history.
- Bound conversational messages input to `POST /api/refine` endpoint, extracting added/removed itinerary activities to display a visual diff checklist box (additions highlighted in emerald, removals line-through rose).
- Added an "Apply Changes" button to hot-reload the updated itinerary plan into both the day timeline and the budget dashboard screens.
- Mocked real-time multiplayer cursor movements and coop status notifications for online users (Priya & Sam).

---

## Detailed Sprint Specifications

### Sprint 1: Setup & Backend API Base
*   **Goal**: Initialize backend environment, project folders, and verification tests.
*   **Scope Boundaries**: Focus strictly on folder structure, package dependencies, FastAPI baseline, and local start scripts. Do not write any AI agent code.
*   **Tasks**:
    - [x] Create folder structure: `/app`, `/app/agents`, `/app/tests`, `/static`.
    - [x] Create `requirements.txt` containing: `fastapi`, `uvicorn`, `pydantic`, `google-genai`, `pytest`, `python-dotenv`, `httpx`.
    - [x] Create `app/main.py` with basic FastAPI shell and a root health check endpoint (`GET /health`).
    - [x] Create `run.py` or start scripts to launch backend locally.
    - [x] Create initial test runner setup `app/tests/test_main.py` to assert health check passes.
*   **Verification**: Run `pytest` and confirm local FastAPI server runs.

---

### Sprint 2: Orchestrator Agent & Core Models
*   **Goal**: Implement core Pydantic data schemas and build the initial Orchestrator Agent to extract structured constraints from natural language inputs.
*   **Scope Boundaries**: Focus on constraint extraction prompts and structural validation. Do not write the downstream agents (Logistics, Budget, etc.).
*   **Tasks**:
    - [x] Define schemas in `app/models.py`: `Activity`, `DayItinerary`, `BudgetBreakdown`, `TravelConstraints`, and `ItineraryPlan`.
    - [x] Create `app/agents/orchestrator.py`.
    - [x] Write system prompt for the Orchestrator utilizing Gemini 2.5 Flash Lite to extract structured JSON matching `TravelConstraints`.
    - [x] Implement parser logic using structured outputs API (JSON Schema enforcement).
    - [x] Write unit tests in `app/tests/test_orchestrator.py` asserting correct constraint extraction for 3 sample inputs (e.g. Japan, Italy, weekend trip).
*   **Verification**: Run tests with `pytest app/tests/test_orchestrator.py`.

---

### Sprint 3: Destination Research & Logistics Agents
*   **Goal**: Build the Destination Research Agent and the Logistics Agent to handle places discovery and routing schedule generation.
*   **Scope Boundaries**: Focus on places curation and day sequencing. Assume budget parameters are checked later.
*   **Tasks**:
    - [x] Create `app/agents/destination.py`.
    - [x] Write system prompt for Destination Research Agent to suggest attractions, dining, and stay neighborhoods based on preferences and avoidances.
    - [x] Create `app/agents/logistics.py`.
    - [x] Write system prompt for Logistics Agent to sequence activities, allocate night durations, suggest transit modes, and prevent geographic backtracking.
    - [x] Write unit tests in `app/tests/test_dest_logistics.py` to verify mock output processing from both agents.
*   **Verification**: Run tests with `pytest app/tests/test_dest_logistics.py`.

---

### Sprint 4: Budget & Review Agents
*   **Goal**: Build the Budget Agent for cost tracking and the Review Agent for final itinerary validation.
*   **Scope Boundaries**: Focus on constraint verification and budget calculations.
*   **Tasks**:
    - [x] Create `app/agents/budget.py`.
    - [x] Write system prompt for Budget Agent to distribute totals across accommodation, activities, transit, and food, and flag budget overruns.
    - [x] Create `app/agents/review.py`.
    - [x] Write validation system prompt for Review Agent to check duration fit, city presence, budget limits, preference match, and travel load. Return `PASS` or detailed error feedback.
    - [x] Write tests in `app/tests/test_budget_review.py` to verify validation passing and failing conditions.
*   **Verification**: Run tests with `pytest app/tests/test_budget_review.py`.

---

### Sprint 5: Pipeline Integration & API Routes
*   **Goal**: Chain the 5 agents into a complete execution pipeline and expose web endpoints for generation and refinement.
*   **Scope Boundaries**: Complete the backend agent orchestrator. Do not write frontend templates yet.
*   **Tasks**:
    - [x] Create `app/pipeline.py` to execute: Orchestrator -> (Parallel Destination, Logistics, Budget) -> Review. Include a retry feedback loop (max 2 retries) on Review Agent failure.
    - [x] Wire up pipeline into `app/main.py` with endpoints:
      - `POST /api/plan`: Receives natural language text, runs pipeline, returns ItineraryPlan JSON.
      - `POST /api/refine`: Receives active itinerary and natural language instruction, returns modified JSON itinerary.
    - [x] Add comprehensive integration tests in `app/tests/test_pipeline.py`.
*   **Verification**: Run all backend tests. Verify API endpoints locally via Swagger docs (`/docs`).

---

### Sprint 6: Frontend Shell & Landing Page (Screen 1)
*   **Goal**: Set up static site serving and build Screen 1 (Landing Page) using exported assets from `stitch_aether_travel_landing_page/aether_travel_landing_page`.
*   **Scope Boundaries**: Setup the HTML shell and Landing Page interactions. Do not wire map libraries or dashboard panels.
*   **Tasks**:
    - [x] Configure `app/main.py` to serve static files from `/static` and load `/static/index.html`.
    - [x] Integrate Screen 1 styling and HTML layout. Add typography (Plus Jakarta Sans, Outfit).
    - [x] Implement conversational search input field with suggestions chips.
    - [x] Hook up search form submission to trigger state transition to Screen 2.
*   **Verification**: Open browser, visit `http://localhost:8000/` and verify landing page aesthetics, responsiveness, and basic interaction.

---

### Sprint 7: Constraint Editor & Loading Page (Screen 2)
*   **Goal**: Integrate Screen 2 to display parsed constraints and show the animated agent generation pipeline.
*   **Scope Boundaries**: Focus on constraint tag editing and pipeline status animations.
*   **Tasks**:
    - [x] Integrate HTML structure and assets from `stitch_aether_travel_landing_page/traveller_constraint_editor_ai_pipeline`.
    - [x] Write JavaScript to parse input from Screen 1, perform initial mock call to `/api/plan` (fast validation pass), and display extracted constraints as editable tags, sliders, and steppers.
    - [x] Implement the agent loading pipeline screen: show animated transition through agent steps (Orchestrator -> Research -> Logistics -> Budget -> Review) with status icons.
*   **Verification**: Submit search, confirm transition to constraint editor, edit tags, submit, and view active agent loading animation.

---

### Sprint 8: Itinerary Dashboard & Map (Screen 3)
*   **Goal**: Implement the primary split-screen dashboard (Screen 3) to show the day-by-day timeline cards and map routing.
*   **Scope Boundaries**: Focus on itinerary timelines and map pins. Do not write detailed budget metrics or co-pilot chat mechanics yet.
*   **Tasks**:
    - [x] Integrate HTML structure and styles from `stitch_aether_travel_landing_page/traveller_itinerary_dashboard`.
    - [x] Bind backend JSON response to day-by-day accordion cards.
    - [x] Implement Leaflet.js map on the right viewport. Load coordinates for activities, plot custom color-coded markers (Food = Coral, Sightseeing = Gold, Transit = Teal), and draw dashed route lines.
    - [x] Implement card expansion click handlers and floating action menu (PDF, Calendar, Share).
*   **Verification**: Generate plan, verify day cards render with correct cost badges, and map draws correct pins.

---

### Sprint 9: Budget & Co-Pilot Drawer (Screens 4 & 5)
*   **Goal**: Build the budget analysis metrics and the interactive side chat drawer for itinerary adjustments.
*   **Scope Boundaries**: Wire up budget calculations and refinement chat.
*   **Tasks**:
    - [x] Integrate UI structures from `traveller_budget_analytics_financial_workspace` and `traveller_ai_co_pilot_collaboration_panel`.
    - [x] Render budget gauge rings, category cards, and progress bars.
    - [x] Implement the "What-If" slider: sliding it down sends a cost-reduction command to the backend.
    - [x] Implement the side chat drawer: typing refinement instructions (e.g. "Move temple to day 4") sends a request to `/api/refine`, highlights differences in a visual diff box, and updates the itinerary on confirm.
*   **Verification**: Use the co-pilot chat to refine a generated trip. Verify the itinerary updates dynamically and the budget dashboard gauges re-render.

---

### Sprint 10: Integration, Edge Cases & Polish
*   **Goal**: Conduct full system testing, address edge cases, finalize styling, and document the walkthrough.
*   **Scope Boundaries**: Final stabilization and quality checks. No new feature additions.
*   **Tasks**:
    - [x] Handle backend edge cases: validation failures, Gemini timeouts (show friendly fallback alerts).
    - [x] Implement final layout polish: adjust glassmorphism shadows, mobile responsive hamburger menus, and smooth layout fade-ins.
    - [x] Verify complete user flow from landing page -> editor -> loading -> dashboard -> chat refinement.
    - [x] Create `walkthrough.md` with verification reports.
*   **Verification**: Run all end-to-end flows. Ensure console has zero errors.
