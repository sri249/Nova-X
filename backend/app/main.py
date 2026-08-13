from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="The AI Innovation & Startup Operating System API",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Update for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": settings.PROJECT_NAME}

# Include routers
from app.features.ai_mentor.router import router as ai_mentor_router
from app.features.chat.router import router as chat_router
from app.features.export.router import router as export_router
from app.features.financial_planner.router import router as financial_planner_router
from app.features.innovation_dna.router import router as innovation_router
from app.features.investor_hub.router import router as investor_hub_router
from app.features.market_intelligence.router import router as market_intelligence_router
from app.features.problem_discovery.router import router as problem_discovery_router
from app.features.projects.router import router as projects_router
from app.features.risk_engine.router import router as risk_engine_router
from app.features.startup_formation.router import router as startup_router
from app.features.task_planner.router import router as task_planner_router
from app.features.users.router import router as auth_router

app.include_router(auth_router)
app.include_router(projects_router)
app.include_router(problem_discovery_router)
app.include_router(innovation_router)
app.include_router(startup_router)
app.include_router(market_intelligence_router)
app.include_router(financial_planner_router)
app.include_router(investor_hub_router)
app.include_router(risk_engine_router)
app.include_router(task_planner_router)
app.include_router(ai_mentor_router)
app.include_router(chat_router)
app.include_router(export_router)
