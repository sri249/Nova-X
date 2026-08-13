import uuid

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.features.ai_mentor.models import AIMentorAnalysis
from app.features.financial_planner.models import FinancialPlan
from app.features.innovation_dna.models import InnovationDNA
from app.features.investor_hub.models import InvestorHub
from app.features.market_intelligence.models import MarketIntelligence
from app.features.problem_discovery.models import ProblemAnalysis
from app.features.projects.models import Project
from app.features.risk_engine.models import RiskProfile
from app.features.startup_formation.models import StartupProfile
from app.features.task_planner.models import TaskPlanner


async def recalculate_project_completion(project_id: uuid.UUID, db: AsyncSession) -> None:
    project_result = await db.execute(select(Project).where(Project.id == project_id))
    project = project_result.scalars().first()
    
    if not project:
        return

    # Count populated modules
    modules = [
        ProblemAnalysis,
        InnovationDNA,
        StartupProfile,
        MarketIntelligence,
        FinancialPlan,
        InvestorHub,
        RiskProfile,
        TaskPlanner,
        AIMentorAnalysis
    ]
    
    # We check 9 modules. BusinessModel is generated together with StartupProfile usually.
    completed = 0
    total = len(modules)
    
    for module_model in modules:
        result = await db.execute(select(module_model).where(module_model.project_id == project_id))
        if result.scalars().first():
            completed += 1
            
    percentage = int((completed / total) * 100)
    
    project.completion_percentage = percentage
    if percentage == 100:
        project.status = "Completed"
    elif percentage > 0 and project.status == "Draft":
        project.status = "Generating"
        
    await db.commit()
