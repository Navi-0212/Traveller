# Traveller — Distributed Multi-Agent Collaborative Travel Orchestrator

[![FastAPI](https://img.shields.io/badge/API-FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Gemini](https://img.shields.io/badge/AI-Gemini%202.5%20Flash%20Lite-0D9488?style=for-the-badge&logo=google-gemini&logoColor=white)](https://ai.google.dev/)
[![Vercel](https://img.shields.io/badge/Frontend-Vercel-000000?style=for-the-badge&logo=vercel&logoColor=white)](https://vercel.com)
[![Railway](https://img.shields.io/badge/Hosting-Railway-130f40?style=for-the-badge&logo=railway&logoColor=white)](https://railway.app)

Traveller is an enterprise-grade, distributed multi-agent system designed to automatically synthesize, budget-model, and geographically optimize multi-day travel itineraries. 

By leveraging a custom **5-Agent Pipeline with State Feedback and Self-Correction Loops** built on **FastAPI (Python)** and **Gemini 2.5 Flash Lite**, Traveller resolves the NP-hard constraints of itinerary generation—minimizing geographic backtracking, enforcing strict budget caps, adhering to positive/negative preferences, and optimizing daily travel load.

---

## 🏛️ System Architecture

Traveller implements a decoupled, modern architecture: a high-performance ASGI FastAPI backend and a responsive, glassmorphic Single Page Application (SPA) frontend.

```
       ┌─────────────────────────────────────────────────────────────┐
       │                 FRONTEND SPA (Vercel Edge)                  │
       │   - Screen 1: NL Conversational Prompt Capture              │
       │   - Screen 2: Dynamic Constraint Tag Editor & Pipeline UI   │
       │   - Screen 3: Leaflet.js Map Timeline (Sequenced Pins)      │
       │   - Screen 4: Budget Dashboard & What-If Ceilings           │
       │   - Screen 5: Real-Time Diff Refiner (Co-Pilot Drawer)      │
       └──────────────────────────────┬──────────────────────────────┘
                                      │
                        HTTP requests │ Proxied via Vercel Rewrite
                        (JSON Payload)│ to bypass CORS pre-flights
                                      ▼
       ┌─────────────────────────────────────────────────────────────┐
       │               FASTAPI ASGI BACKEND (Railway)                │
       │   [Uvicorn / ASGI Server - Port 8080 - 0.0.0.0 Binding]     │
       │                                                             │
       │   /api/extract ──➔ Parses prompts into TravelConstraints     │
       │   /api/plan    ──➔ Executes Multi-Agent Pipeline E2E        │
       │   /api/refine  ──➔ Evaluates conversational diff edits      │
       └──────────────────────────────┬──────────────────────────────┘
                                      │
                        google-genai  │ Structured Outputs
                        SDK Calls     │ (JSON Schema Enforcement)
                                      ▼
       ┌─────────────────────────────────────────────────────────────┐
       │                    GOOGLE GEMINI ENGINE                     │
       │                 - Model: gemini-2.5-flash-lite              │
       │                 - Context: 1M tokens                        │
       └─────────────────────────────────────────────────────────────┘
```

---

## 🤖 The Multi-Agent Pipeline & State Machine

The core of Traveller is its execution pipeline. Rather than relying on a single, massive prompt (which often leads to hallucinations, constraint violations, and formatting errors), Traveller divides the task among five specialized micro-agents:

```
               [ User Input ]
                      │
                      ▼
            ┌───────────────────┐
            │ 1. Orchestrator   │ (Extracts TravelConstraints, Temp: 0.3)
            └─────────┬─────────┘
                      │
                      ├──────────────────────────┐
                      ▼                          ▼
            ┌───────────────────┐      ┌───────────────────┐
            │ 2. Destination    │      │ 4. Budget Agent   │
            │    Research       │      │    (Cost Model)   │ (Temp: 0.3)
            └─────────┬─────────┘      └─────────┬─────────┘
                      │                          │
                      ▼                          │
            ┌───────────────────┐                │
            │ 3. Logistics      │                │
            │    Coordinator    │ (Temp: 0.3)    │
            └─────────┬─────────┘                │
                      │                          │
                      ▼                          ▼
                   [Itinerary Output]  [Budget Breakdown]
                      │                          │
                      └────────────┬─────────────┘
                                   ▼
                         ┌───────────────────┐
                         │ 5. Review Agent   │ (Temp: 0.3)
                         └─────────┬─────────┘
                                   │
                                   ├───────────────┐
                              FAIL │ (Max 2 Retries)│ PASS
                                   ▼               ▼
                           [Feedback Loop]   [Return 200 OK]
                                   │           ItineraryPlan
                                   ▼
                         (Re-run Research &
                          Logistics with logs)
```

### 1. Master Orchestrator Agent (`app/agents/orchestrator.py`)
* **Objective**: Translate natural language prompts into a structured schema of constraints.
* **LLM Config**: Temperature `0.3` (minimizes creative drift to enforce strict extraction).
* **Behavior**: Parses destination, cities, duration (days), total budget (USD), preferences (e.g., food, history), and avoidances (e.g., crowds, long walks). If parameters are missing, it applies sensible defaults (e.g., $2000 USD, 7 days, mid-range accommodation).

### 2. Destination Research Agent (`app/agents/destination.py`)
* **Objective**: Curate places, experiences, and accommodations that align with constraints.
* **LLM Config**: Temperature `0.7` (higher creativity for diverse recommendations).
* **Behavior**: Recommends locations, neighborhoods, entry fees, and average durations. It filters out crowded sights if the user specified an avoidance of crowds (e.g., recommending Nezu Shrine instead of Meiji Jingu in Tokyo).

### 3. Logistics Coordinator Agent (`app/agents/logistics.py`)
* **Objective**: Sequence activities day-by-day to form a logical timeline.
* **LLM Config**: Temperature `0.3`.
* **Behavior**: Organizes activities into `Morning`, `Afternoon`, and `Evening` slots. It groups activities by neighborhood to minimize transit times and avoid geographic backtracking.

### 4. Budget Agent (`app/agents/budget.py`)
* **Objective**: Construct a financial model of the trip.
* **LLM Config**: Temperature `0.3`.
* **Behavior**: Evaluates costs across six categories (`flights`, `accommodation`, `transit`, `food`, `activities`, and `buffer`). It calculates estimated costs, compares them against target category limits, and flags category overruns with an `Exceeded` status.

### 5. Review Agent (`app/agents/review.py`)
* **Objective**: Serve as the quality gate (Verification Phase).
* **LLM Config**: Temperature `0.3`.
* **Behavior**: Evaluates the plan against six criteria: `duration_fit`, `city_coverage`, `budget_compliance`, `preference_alignment`, `avoidance_compliance`, and `logistics_realism`. If any check fails, it outputs `status="FAIL"` along with detailed feedback logs.

### 🔁 Self-Correction & Feedback Loop
If the **Review Agent** fails a plan, the pipeline triggers a retry loop (capped at **2 retries**). The failure log is fed back to the **Destination Research** and **Logistics** agents as a system message. The agents adapt their output based on the failure logs. If the checks still fail after 2 retries, a fallback check returns the best-effort plan with `validation_passed=False` and a list of warnings.

---

## 📋 API Specifications

Traveller enforces strict Pydantic models for request/response serialization. 

### 1. Extract Constraints
* **Endpoint**: `POST /api/extract`
* **Request Payload**:
  ```json
  { "prompt": "Plan a 3-day trip to Japan. Tokyo only. Budget $1500. Love ramen, hate long walks." }
  ```
* **Response Payload (`TravelConstraints`)**:
  ```json
  {
    "destination": "Japan",
    "cities": ["Tokyo"],
    "duration_days": 3,
    "budget_usd": 1500.0,
    "preferences": ["Ramen", "Food"],
    "avoidances": ["Long walks"],
    "travel_style": "independent",
    "accommodation_preference": "mid-range"
  }
  ```

### 2. Generate Plan
* **Endpoint**: `POST /api/plan`
* **Request Payload**: Contains either `prompt` (E2E run) or a structured `constraints` object (running from the constraint editor).
* **Response Payload (`ItineraryPlan`)**:
  ```json
  {
    "destination": "Japan",
    "duration_days": 3,
    "days": [
      {
        "day_number": 1,
        "title": "Ramen Discovery & Historic Walk",
        "activities": [
          {
            "name": "Nezu Shrine",
            "type": "temple",
            "time_slot": "Morning",
            "cost_usd": 0.0,
            "duration_hours": 1.5,
            "crowd_level": "low",
            "description": "Quiet shrine, avoiding Meiji Jingu crowds."
          }
        ],
        "transit_info": "Metro (15 mins, $2)"
      }
    ],
    "budget_summary": [
      {
        "category": "accommodation",
        "allocated_usd": 500.0,
        "estimated_cost_usd": 450.0,
        "status": "Within"
      }
    ],
    "validation_passed": true,
    "validation_notes": "Successfully validated by Review Agent."
  }
  ```

### 3. Refine Plan
* **Endpoint**: `POST /api/refine`
* **Request Payload**: Receives the `existing_plan` and the user's conversational `instructions`.
* **Response Payload**: An updated `ItineraryPlan` with recalculated budget and validation states.

---

## 🛠️ Local Development & Installation

### Setup Environment
1. Ensure **Python 3.10+** is installed on your local machine.
2. Clone the repository and navigate into the root directory:
   ```bash
   git clone https://github.com/Navi-0212/Traveller.git
   cd Traveller
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file in the project root:
   ```env
   GEMINI_API_KEY=AIzaSyYourGeminiApiKeyHere
   ALLOWED_ORIGINS=*
   ```
   *(Get your API key from [Google AI Studio](https://aistudio.google.com/))*

### Run the Dev Server
```bash
python run.py
```
The server will start on `http://127.0.0.1:8000`. You can visit this URL in your browser to interact with the frontend, or visit `http://127.0.0.1:8000/docs` to view the interactive Swagger API documentation.

---

## 🧪 Verification & Test Suite

Traveller includes a test suite covering unit operations and integration flows under `app/tests/`. 

To accommodate developer key limits (Free Tier API quotas), the test suite segregates **offline mock tests** from **live integration tests**.

```bash
# Run only mock-based offline tests (zero API calls, runs instantly)
python -m pytest -k "mocked"

# Run the complete test suite (Requires a valid GEMINI_API_KEY env variable)
python -m pytest
```

---

## 🌐 Production Deployment Engineering

Traveller is configured for rapid, seamless deployment using a decoupled structure.

### Backend Hosting (Railway)
* **Start Command**: Railway detects the root `Procfile` and runs `web: python run.py`.
* **Port Mapping**: The backend automatically binds to `0.0.0.0` and listens to the port injected dynamically by Railway via `os.environ.get("PORT")`.
* **CORS Security**: You can lock down API access by passing a comma-separated list of your Vercel domains into the `ALLOWED_ORIGINS` environment variable in Railway.

### Frontend Hosting (Vercel)
* **Asset Routing**: Vercel reads `vercel.json` to route root `/` traffic directly to serve the static dashboard at `static/index.html`.
* **API Rewrite Proxy**: `vercel.json` maps `/api/:path*` to your Railway URL. This routes API requests on Vercel through a server-side proxy, bypassing CORS pre-flight steps and protecting client-side requests from cross-origin blocking.
