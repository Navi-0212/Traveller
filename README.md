# 🌌 Traveller — Distributed Multi-Agent Collaborative Travel Orchestrator

> A state-of-the-art AI Travel Agent that transforms conversational trip planning into optimized, budget-tracked, and geographically routed itineraries.

[![FastAPI](https://img.shields.io/badge/API-FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Gemini](https://img.shields.io/badge/AI-Gemini%202.5%20Flash%20Lite-0D9488?style=for-the-badge&logo=google-gemini&logoColor=white)](https://ai.google.dev/)
[![Vercel](https://img.shields.io/badge/Frontend-Vercel-000000?style=for-the-badge&logo=vercel&logoColor=white)](https://vercel.com)
[![Railway](https://img.shields.io/badge/Hosting-Railway-130f40?style=for-the-badge&logo=railway&logoColor=white)](https://railway.app)

---

## 🌟 The Core Vision

Planning a trip is traditionally fragmented. Travelers spend hours bouncing between flight aggregators, hotel search engines, local blogs, mapping software, and Excel spreadsheets. 

**Traveller** consolidates this entire workspace into a single interface. By combining a **premium glassmorphic SPA frontend** with a **5-agent self-correcting backend state machine** powered by **Gemini 2.5 Flash Lite**, Traveller automates the entire planning process from a single sentence.

---

## 🚀 How It Works (Step-by-Step)

```
 💬 1. Natural Language Prompt ──► 🏷️ 2. Constraint Tag Editor ──► 🤖 3. 5-Agent Pipeline
                                                                           │
 💬 5. Conversational Co-Pilot  ◄── 📊 4. Interactive Map & Budget  ◄──────┘
```

### 1️⃣ Prompt & Capture
Type your trip idea naturally: *"Plan a 5-day foodie trip to Japan. Tokyo and Kyoto. Under $3000. Love ramen, hate crowds."*

### 2️⃣ Edit & Tweak
The **Master Orchestrator** instantly extracts destination details, days, budget, and vibes, rendering them as interactive tags. Adjust days, add new cities, or change the budget slider before building.

### 3️⃣ Run the Pipeline
Watch the **Agent Pipeline Visualizer** pulse in real-time as specialized AI agents coordinate tasks, calculate budgets, and verify constraints.

### 4️⃣ Explore the Dashboard
Explore a split-screen dashboard:
* **Left**: A day-by-day accordion timeline categorized by activity type (Food, Sightseeing, Transit).
* **Right**: An interactive **Leaflet.js map** displaying sequenced activity pins connected by a dashed route.
* **Financials**: An SVG budget gauge with sparkline charts showing category allocations (accommodation, transit, buffer, etc.).

### 5️⃣ Chat with your Co-Pilot
Open the chat drawer to refine the itinerary: *"Add a ramen cooking class on Day 2"*. The co-pilot computes the change and presents a **visual diff box** showing additions and removals before hot-reloading the plan.

---

## 🤖 Meet the AI Agent Team

Behind the scenes, Traveller runs a distributed team of 5 specialized agents that work together to build, calculate, and audit your itinerary.

| Agent Persona | Role | Primary Objective | Temperature |
| :--- | :--- | :--- | :--- |
| **🕵️‍♂️ Master Orchestrator** | Director | Parses natural language inputs into structured constraints. | `0.3` (Strict) |
| **🎨 Vibe Curator (Research)** | Explorer | Recommends sights, restaurants, and hotels matching user vibes. | `0.7` (Creative) |
| **🗺️ Route Master (Logistics)** | Dispatcher | Arranges activities by neighborhood to minimize backtracking. | `0.3` (Strict) |
| **📈 CFO (Budget)** | Accountant | Builds a category cost breakdown and flags budget overruns. | `0.3` (Strict) |
| **⚖️ Quality Gatekeeper (Review)** | Auditor | Verifies itinerary details against all initial constraints. | `0.3` (Strict) |

### 🔄 The Self-Correction Feedback Loop
If the **Quality Gatekeeper** flags a constraint violation (e.g. daily budget exceeded or too many active hours), it outputs a failure report. The pipeline routes this feedback back to the **Curator** and **Route Master** agents to adjust their planning, running up to **2 automated retries** before delivering the final, audited itinerary.

---

## 💻 Tech Stack & Design Architecture

Traveller combines modern engineering paradigms with premium design systems:

### 🎨 Frontend (Client Shell)
* **Obsidian Void Theme**: A sleek `#0B0F19` slate-glass backdrop with vibrant Aurora Teal (`#0D9488`) highlights.
* **Leaflet.js**: Vector maps utilizing CartoDB Dark Matter tiles.
* **Dynamic Budget Gauges**: Inline SVG rings that calculate spent vs. remaining budgets on the fly.
* **Visual Diff Engine**: Red/green diff boxes highlighting co-pilot adjustments.
* **Co-op Presence Simulation**: Live cursors showing mock collaborative users (Priya & Sam).

### ⚙️ Backend (API Engine)
* **FastAPI**: Asynchronous Python web framework for clean API routes.
* **Pydantic v2**: Hard schema validation for data models.
* **Google GenAI SDK**: Direct integration with Gemini 2.5 Flash Lite.
* **Pytest**: Complete unit testing suite with offline mocks.
---


