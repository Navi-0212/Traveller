# Traveller — Multi-Agent AI Travel Planner

Welcome to **Traveller**, a premium, multi-agent AI travel itinerary planner. Built using a robust FastAPI backend orchestration pipeline, Gemini 2.5 Flash Lite, and a high-fidelity glassmorphic HTML/JS/Tailwind frontend.

---

## 🚀 Key Features

* **Conversational Parsing**: Type your dream trip in natural language, and the orchestrator automatically extracts destinations, budget, duration, and vibes.
* **Tag-Based Constraint Editor**: Fine-tune travel days, budgets, preferences, and avoidances using an intuitive tag manager.
* **5-Agent Pipeline Visualizer**: Watch in real-time as specialized agents (Orchestrator ➔ Curation ➔ Logistics ➔ Budget ➔ Review) build your trip.
* **Split-Screen Map Timeline**: Interactive Leaflet.js map plotting circular glowing markers and route lines synchronized with your day-by-day itineraries.
* **Financial Workspace**: Track spent vs. remaining budgets with SVG gauges, daily cost sparklines, and cost-reduction target sliders.
* **AI Co-Pilot Drawer**: Conversational chat that calculates edits, shows a visual diff check box, and hot-reloads adjustments instantly.
* **Multiplayer Presence**: Implements mock cursors and online avatars for collaborative planning.

---

## 🛠️ Tech Stack

* **Backend**: FastAPI (Python 3.10+), Pydantic v2, Google GenAI SDK
* **Frontend**: HTML5, Vanilla JavaScript, Tailwind CSS (CDN), Leaflet.js
* **AI Engine**: Gemini 2.5 Flash Lite (`gemini-2.5-flash-lite`)

---

## ⚙️ Quick Start

### 1. Prerequisites
Ensure you have **Python 3.10+** installed on your system.

### 2. Installation
Clone the repository and install the dependencies:
```bash
pip install -r requirements.txt
```

### 3. API Key Setup
Create a `.env` file in the project root (or update the existing one) and add your Gemini API Key:
```env
GEMINI_API_KEY=your_actual_gemini_api_key
```
*(Get your free key from [Google AI Studio](https://aistudio.google.com/))*

### 4. Run the Server
Launch the application locally:
```bash
python run.py
```
Open your browser and navigate to: **`http://localhost:8000`**

---

## 🧪 Testing

The backend is backed by offline unit tests and live integration suites under `app/tests/`. To run the tests:

```bash
# Run mock-based offline tests (instantly passes)
python -m pytest -k "mocked"

# Run all tests (requires GEMINI_API_KEY)
python -m pytest
```

---

## 🌐 Deployment Reference

* For details on deploying the static frontend to **Vercel** and the backend API to **Railway**, refer to the [deployment.md](deployment.md) guide.
* For features documentation and design specifications, refer to [walkthrough.md](walkthrough.md).
