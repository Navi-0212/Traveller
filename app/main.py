from dotenv import load_dotenv
load_dotenv()

import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional
from app.models import ItineraryPlan, TravelConstraints
from app.pipeline import ItineraryPipeline

app = FastAPI(title="Traveller API", version="1.0")

# Read allowed CORS origins from env variable (comma-separated), default to "*" for development
allowed_origins_str = os.getenv("ALLOWED_ORIGINS", "*")
allowed_origins = [origin.strip() for origin in allowed_origins_str.split(",") if origin.strip()]

# Enable CORS for local and web frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PlanRequest(BaseModel):
    prompt: Optional[str] = None
    constraints: Optional[TravelConstraints] = None

class RefineRequest(BaseModel):
    existing_plan: ItineraryPlan
    instructions: str

# Instantiate the pipeline once at startup
pipeline = ItineraryPipeline()

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "Traveller API"}

@app.post("/api/extract", response_model=TravelConstraints)
async def extract_constraints(request: PlanRequest):
    if not request.prompt or not request.prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt is required for extraction.")
    try:
        constraints = pipeline.orchestrator.extract_constraints(request.prompt)
        return constraints
    except Exception as e:
        import traceback
        print("ERROR in /api/extract:")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Constraint extraction error: {str(e)}")

@app.post("/api/plan", response_model=ItineraryPlan)
async def generate_travel_plan(request: PlanRequest):
    if not request.prompt and not request.constraints:
        raise HTTPException(status_code=400, detail="Must provide either prompt or constraints.")
    try:
        plan = pipeline.generate_plan(user_prompt=request.prompt, constraints=request.constraints)
        return plan
    except Exception as e:
        import traceback
        print("ERROR in /api/plan:")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Generation pipeline error: {str(e)}")

@app.post("/api/refine", response_model=ItineraryPlan)
async def refine_travel_plan(request: RefineRequest):
    if not request.instructions.strip():
        raise HTTPException(status_code=400, detail="Refinement instructions cannot be empty.")
    try:
        updated_plan = pipeline.refine_plan(request.existing_plan, request.instructions)
        return updated_plan
    except Exception as e:
        import traceback
        print("ERROR in /api/refine:")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Refinement pipeline error: {str(e)}")

# Serve index.html at root if present (for local development), otherwise redirect to health check
@app.get("/")
async def serve_index():
    if os.path.exists("index.html"):
        return FileResponse("index.html")
    return {"status": "healthy", "message": "Traveller API is running. Access the frontend via Vercel."}
