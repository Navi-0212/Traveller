# Traveller — Multi-Agent Travel Planner Walkthrough

Welcome to **Traveller**, a high-fidelity, multi-agent travel itinerary generation and optimization system. This document outlines the architecture, features built, test coverage, local execution steps, and deployment readiness status.

---

## 1. Project Architecture

Traveller utilizes a decoupled FastAPI backend and a single-page static HTML/JS frontend styled with glassmorphic Tailwind CSS and Leaflet.js maps.

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

### The 5-Agent Pipeline
1. **Orchestrator Agent (`app/agents/orchestrator.py`)**: Uses `gemini-2.5-flash-lite` to extract structured `TravelConstraints` from the user's natural language inputs.
2. **Destination Research Agent (`app/agents/destination.py`)**: Suggests key attractions, dining, and accommodations based on preferences and avoidances.
3. **Logistics Agent (`app/agents/logistics.py`)**: Sequences attractions day-by-day, grouping them by neighborhood to minimize geographical backtracking.
4. **Budget Agent (`app/agents/budget.py`)**: Models costs across categories (flights, accommodation, transit, food, activities, buffer) and flags overruns.
5. **Review Agent (`app/agents/review.py`)**: Acts as a quality gate checking budget compliance, duration, travel load, and consistency.
6. **Refiner Agent (`app/agents/refiner.py`)**: Supports conversational updates and edits on existing itineraries via the co-pilot chat drawer.

---

## 2. Features Built

- **Conversational Search Bar & Suggestion Chips**: Quick entry of travel prompts with dynamic chip filling.
- **Interactive Constraint Editor**: Edit extracted cities, customize travel style, steppers for duration, and sliders for budget ceilings.
- **Pipeline Loading Visualizer**: A live node-based loading UI displaying real-time agent completion status.
- **Split-Screen Dashboard**: 
  - Day-by-day accordion cards displaying food, sightseeing, and transit.
  - Interactive **Leaflet.js map** plotting Circular Glowing Markers and dashed route lines matching the day's timeline.
- **Budget Workspace**: Spent vs. remaining gauges, progress indicators, daily cost sparklines, and target budget sliders.
- **Co-Pilot Side Drawer**: Conversational chat interface executing `POST /api/refine` with a visual additions/removals diff check box and hot-reload.
- **Multiplayer Cursor Simulation**: Live mock status showing active cursor movements from other users (Priya & Sam) for co-planning.

---

## 3. Local Execution

### Prerequisites
- Python 3.10+
- A Google Gemini API Key

### Installation
1. Clone the project and navigate to the directory:
   ```bash
   cd "c:/Projects/Ai travel agent"
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set your API Key in the `.env` file:
   ```env
   GEMINI_API_KEY=your_actual_gemini_api_key
   ```

### Running the App
1. Start the FastAPI server:
   ```bash
   python run.py
   ```
2. Open your browser and navigate to:
   `http://localhost:8000`

---

## 4. Automated Tests

The backend is covered by comprehensive unit and integration tests under `app/tests/`:
- `test_main.py`: Health check assertions.
- `test_orchestrator.py`: Asserts constraint parsing and extraction.
- `test_dest_logistics.py`: Verifies places curation and logistics arrangement.
- `test_budget_review.py`: Validates budget allocations and Review Agent gate.
- `test_pipeline.py`: Tests the full pipeline flow, including retries on failure.

Run tests using:
```bash
pytest
```

---

## 5. Deployment Readiness Checklist

To transition the project from local development to production deployment, check the following items:

- [ ] **Configure the Gemini API Key**: Ensure `GEMINI_API_KEY` is injected as a secure environment variable in your production hosting platform (e.g., Render, Fly.io, Railway, AWS, GCP).
- [ ] **Restrict CORS Settings**: In `app/main.py`, replace `allow_origins=["*"]` with your specific production frontend domains to prevent cross-origin resource sharing vulnerabilities.
- [ ] **Configure Production Host/Port**: Ensure that Uvicorn binds to `0.0.0.0` instead of `127.0.0.1` and reads the port dynamically from the environment `PORT` (e.g. using `os.environ.get("PORT", 8000)`) so the cloud service router can route requests to the container.
- [ ] **Disable Reload/Debug Flags**: For production execution, run uvicorn with `reload=False` and adjust logging levels appropriately.
- [ ] **API Endpoint Protocol**: Ensure the frontend calls are relative (e.g., `/api/plan`), which is already implemented and supports automatic routing over HTTPS.
