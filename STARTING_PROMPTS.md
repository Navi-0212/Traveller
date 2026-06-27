# Antigravity Starting Prompts
## Sequential Prompts for 10 Sessions

Use the following prompts to start each new Antigravity session sequentially. Before starting a session, ensure the previous session has successfully completed and marked its tasks as completed in [ImplementationPlan.md](file:///c:/Projects/Ai%20travel%20agent/ImplementationPlan.md).

---

### Session 1: Project Setup & Backend API Base

**Prompt to copy/paste:**
```text
We are starting Sprint 1 of the Traveller project implementation. 

Please perform the following steps:
1. Read the PRD at c:/Projects/Ai travel agent/AI_Travel_Planner_PRD.md and the Implementation Plan at c:/Projects/Ai travel agent/ImplementationPlan.md to understand the project architecture.
2. Initialize the backend project structure:
   - Create directories: /app, /app/agents, /app/tests, /static
   - Create requirements.txt containing: fastapi, uvicorn, pydantic, google-genai, pytest, python-dotenv
   - Create app/main.py with a basic FastAPI server and a root health check endpoint (GET /health)
   - Create run.py or script to start the server locally
3. Write a test in app/tests/test_main.py to verify the health check endpoint returns 200.
4. Verify the setup runs correctly and tests pass.
5. Critical: Update the "Progress History" and "Sprint 1" sections in c:/Projects/Ai travel agent/ImplementationPlan.md to show Sprint 1 is completed. Add any technical notes for the next session under "Progress History". Stop when done. Do not write any AI agent code.
```

---

### Session 2: Orchestrator Agent & Core Models

**Prompt to copy/paste:**
```text
We are starting Sprint 2 of the Traveller project implementation.

Please perform the following steps:
1. Read the PRD and c:/Projects/Ai travel agent/ImplementationPlan.md to verify completed steps.
2. Create app/models.py to define the core Pydantic data schemas:
   - Activity (name, type, cost_usd, duration_hours, crowd_level, description)
   - DayItinerary (day_number, title, activities, transit_info)
   - BudgetBreakdown (category, estimated_cost, status)
   - TravelConstraints (destination, cities, duration_days, budget_usd, preferences, avoidances)
   - ItineraryPlan (days, budget_summary, validation_passed)
3. Create app/agents/orchestrator.py:
   - Implement the Orchestrator Agent using Gemini 2.5 Flash Lite
   - Write a system prompt enforcing constraint extraction to output JSON matching the TravelConstraints schema
4. Add unit tests in app/tests/test_orchestrator.py to assert correct parsing of 3 different natural-language requests.
5. Verify tests pass.
6. Critical: Update c:/Projects/Ai travel agent/ImplementationPlan.md. Mark Sprint 2 as completed and document what models/parsing schemas are ready for the downstream agents. Stop when done. Do not write code for downstream agents yet.
```

---

### Session 3: Destination Research & Logistics Agents

**Prompt to copy/paste:**
```text
We are starting Sprint 3 of the Traveller project implementation.

Please perform the following steps:
1. Read the PRD and c:/Projects/Ai travel agent/ImplementationPlan.md to verify previous work.
2. Implement the Destination Research Agent in app/agents/destination.py:
   - System prompt must take TravelConstraints and return curated attractions, sights, food, and neighborhood recommendations aligned with preferences (e.g. food) and avoidances (e.g. crowds).
3. Implement the Logistics Agent in app/agents/logistics.py:
   - System prompt must sequence recommended sights, allocate nights, determine transit times/costs, and organize days to avoid backtracking.
4. Create app/tests/test_dest_logistics.py to test outputs from both agents with mock constraints.
5. Verify tests pass.
6. Critical: Update c:/Projects/Ai travel agent/ImplementationPlan.md. Mark Sprint 3 as completed, document agent prompts, and describe how they hand data to the budget agent. Stop when done. Do not implement budget calculation code.
```

---

### Session 4: Budget & Review Agents

**Prompt to copy/paste:**
```text
We are starting Sprint 4 of the Traveller project implementation.

Please perform the following steps:
1. Read the PRD and c:/Projects/Ai travel agent/ImplementationPlan.md to verify completed steps.
2. Implement the Budget Agent in app/agents/budget.py:
   - System prompt must model cost categories (accommodation, transit, food, activities, buffer) based on constraints and logistics inputs, flagging category overruns.
3. Implement the Review Agent in app/agents/review.py:
   - System prompt must act as a quality gate, checking budget limits, day duration limits, preference compliance, and geographical consistency. It should output PASS or FAIL with explicit failure logs.
4. Create app/tests/test_budget_review.py to verify passing and failing cases.
5. Verify tests pass.
6. Critical: Update c:/Projects/Ai travel agent/ImplementationPlan.md. Mark Sprint 4 as completed, note how agent failures are logged, and hand over to the pipeline integration step. Stop when done. Do not build API endpoints.
```

---

### Session 5: Pipeline Integration & API Routes

**Prompt to copy/paste:**
```text
We are starting Sprint 5 of the Traveller project implementation.

Please perform the following steps:
1. Read the PRD and c:/Projects/Ai travel agent/ImplementationPlan.md to verify completed steps.
2. Create app/pipeline.py:
   - Build the agent orchestrator orchestrating: Orchestrator -> (Parallel Destination, Logistics, Budget) -> Review.
   - Implement retry feedback loops: if Review Agent returns FAIL, feed errors back to the Orchestrator/Logistics/Budget agents for correction (max 2 retries).
3. Update app/main.py to expose:
   - POST /api/plan: Accepts natural language prompt, runs pipeline, returns ItineraryPlan JSON.
   - POST /api/refine: Accepts existing ItineraryPlan + natural language instructions, returns updated ItineraryPlan JSON.
4. Add comprehensive integration tests in app/tests/test_pipeline.py.
5. Verify all tests pass. Make sure you can query endpoints via Swagger (/docs).
6. Critical: Update c:/Projects/Ai travel agent/ImplementationPlan.md. Mark Sprint 5 as completed, summarize backend endpoint URLs, and stop. Do not write frontend code.
```

---

### Session 6: Frontend Shell & Landing Page (Screen 1)

**Prompt to copy/paste:**
```text
We are starting Sprint 6 of the Traveller project implementation.

Please perform the following steps:
1. Read the PRD and c:/Projects/Ai travel agent/ImplementationPlan.md.
2. Configure app/main.py to serve static assets from the /static folder and serve index.html as the primary landing page.
3. Build the Frontend Shell:
   - Create /static/index.html and import Google Fonts (Plus Jakarta Sans, Outfit) and Material Icons.
   - Integrate Screen 1 styling and HTML layout from c:/Projects/Ai travel agent/stitch_aether_travel_landing_page/aether_travel_landing_page/code.html.
   - Wire up the conversational search bar and suggested prompt chips so clicking them or submitting a custom prompt captures the text.
   - Set up the transition logic to hide Screen 1 and show Screen 2 on submit.
4. Launch the local server and verify the landing page visual aesthetics, animations, and inputs.
5. Critical: Update c:/Projects/Ai travel agent/ImplementationPlan.md. Mark Sprint 6 as completed, state how user inputs are stored in frontend state, and stop. Do not implement the constraint editor fields.
```

---

### Session 7: Constraint Editor & Loading Page (Screen 2)

**Prompt to copy/paste:**
```text
We are starting Sprint 7 of the Traveller project implementation.

Please perform the following steps:
1. Read the PRD and c:/Projects/Ai travel agent/ImplementationPlan.md.
2. Integrate Screen 2 (Constraint Editor) using the HTML/CSS layout from c:/Projects/Ai travel agent/stitch_aether_travel_landing_page/traveller_constraint_editor_ai_pipeline/code.html:
   - On search submission from Screen 1, trigger a fast validation pass or mock call to backend to parse tags.
   - Display constraints as editable tags (destinations, preferences, avoidances), durational steppers, and budget sliders.
   - Clicking "Generate Itinerary" should trigger the full agent loading animation screen:
     - Render the 5 agent pipeline nodes (Orchestrator -> Research -> Logistics -> Budget -> Review) with active pulsing glows and loading indicators as each backend phase completes.
3. Verify transitions and interaction states.
4. Critical: Update c:/Projects/Ai travel agent/ImplementationPlan.md. Mark Sprint 7 as completed, specify how updated tags are packaged for the final generation payload, and stop. Do not write dashboard layouts yet.
```

---

### Session 8: Itinerary Dashboard & Map (Screen 3)

**Prompt to copy/paste:**
```text
We are starting Sprint 8 of the Traveller project implementation.

Please perform the following steps:
1. Read the PRD and c:/Projects/Ai travel agent/ImplementationPlan.md.
2. Integrate Screen 3 (Itinerary Dashboard) using the HTML/CSS from c:/Projects/Ai travel agent/stitch_aether_travel_landing_page/traveller_itinerary_dashboard/code.html:
   - Bind backend JSON response to day-by-day collapsible accordion timeline cards.
   - Render activities with color-coded category badges (Food = Coral, Sightseeing = Gold, Transit = Teal).
   - Integrate Leaflet.js on the right map viewport. For the active day, load coordinates, render custom markers matching activity types, and draw dashed route lines linking them.
   - Ensure clicking different days on the itinerary updates map coordinates and routes.
3. Test layout responsiveness and map drawing.
4. Critical: Update c:/Projects/Ai travel agent/ImplementationPlan.md. Mark Sprint 8 as completed, note the map integration details (libraries used, token configs if any), and stop. Do not wire budget dashboard metrics.
```

---

### Session 9: Budget & Co-Pilot Drawer (Screens 4 & 5)

**Prompt to copy/paste:**
```text
We are starting Sprint 9 of the Traveller project implementation.

Please perform the following steps:
1. Read the PRD and c:/Projects/Ai travel agent/ImplementationPlan.md.
2. Integrate Screen 4 (Budget Dashboard) using c:/Projects/Ai travel agent/stitch_aether_travel_landing_page/traveller_budget_analytics_financial_workspace/code.html:
   - Render the circular progress budget spent/remaining gauge and category bars.
   - Implement the "What-If" budget slider: when dragged, send a cost-reduction command to the backend.
3. Integrate Screen 5 (Co-Pilot Chat Drawer) using c:/Projects/Ai travel agent/stitch_aether_travel_landing_page/traveller_ai_co_pilot_collaboration_panel/code.html:
   - Open a side conversational drawer. Hook up message inputs to send text to POST /api/refine.
   - Render the AI response diff box showing added/removed activities, and click "Apply" to update the dashboard.
   - Mock a multiplayer presence with top avatar bubbles and cursor markers.
4. Verify budget updates and chat refinement work end-to-end.
5. Critical: Update c:/Projects/Ai travel agent/ImplementationPlan.md. Mark Sprint 9 as completed, document co-pilot refine prompt schema, and stop.
```

---

### Session 10: Integration, Edge Cases & Polish

**Prompt to copy/paste:**
```text
We are starting Sprint 10 of the Traveller project implementation.

Please perform the following steps:
1. Read the PRD and c:/Projects/Ai travel agent/ImplementationPlan.md.
2. Perform full integration:
   - Wire all screens together to form a seamless flow: Landing -> Constraint Editor -> Pipeline Loader -> Itinerary & Map Dashboard with Budget Panels and Co-Pilot Refinement.
3. Verify edge cases:
   - Handle network failures, Gemini timeouts, and Review Agent re-synthesis limits. Show helpful glassmorphic modal alerts.
   - Ensure clean responsive sizing on mobile viewports.
4. Polish visual design: refine glassmorphism shadows, scrollbar designs, and button click animations.
5. Create walkthrough.md summarizing features built, test reports, and instructions on running the complete Traveller app.
6. Critical: Update c:/Projects/Ai travel agent/ImplementationPlan.md. Mark Sprint 10 as completed, add final checkout notes, and stop.
```
