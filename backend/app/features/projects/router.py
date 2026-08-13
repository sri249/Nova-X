import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.api.dependencies import get_current_user
from app.core.database import get_db_session
from app.features.ai_mentor.models import AIMentorAnalysis
from app.features.financial_planner.models import FinancialPlan
from app.features.innovation_dna.models import InnovationDNA
from app.features.investor_hub.models import InvestorHub
from app.features.market_intelligence.models import MarketIntelligence
from app.features.problem_discovery.models import ProblemAnalysis
from app.features.projects.models import Project, StartupScore
from app.features.projects.schemas import ProjectCreate, ProjectResponse, ProjectUpdate
from app.features.projects.utils import recalculate_project_completion
from app.features.risk_engine.models import RiskProfile
from app.features.startup_formation.models import (
    BusinessModel,
    CustomerPersona,
    StartupProfile,
)
from app.features.task_planner.models import TaskPlanner
from app.features.users.models import User
from app.services.ai.service import ai_service

router = APIRouter(prefix="/projects", tags=["projects"])

@router.post("", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(
    project_in: ProjectCreate, 
    current_user: User = Depends(get_current_user), 
    db: AsyncSession = Depends(get_db_session)
):
    new_project = Project(
        name=project_in.name,
        description=project_in.description,
        status=project_in.status,
        owner_id=current_user.id
    )
    db.add(new_project)
    await db.commit()
    await db.refresh(new_project)
    await recalculate_project_completion(new_project.id, db)
    return new_project

@router.get("", response_model=list[ProjectResponse])
async def read_projects(
    current_user: User = Depends(get_current_user), 
    db: AsyncSession = Depends(get_db_session)
):
    result = await db.execute(
        select(Project).where(Project.owner_id == current_user.id, Project.deleted_at == None)
    )
    return result.scalars().all()

@router.get("/{project_id}", response_model=ProjectResponse)
async def read_project(
    project_id: uuid.UUID,
    current_user: User = Depends(get_current_user), 
    db: AsyncSession = Depends(get_db_session)
):
    result = await db.execute(
        select(Project).where(Project.id == project_id, Project.owner_id == current_user.id, Project.deleted_at == None)
    )
    project = result.scalars().first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@router.put("/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: uuid.UUID,
    project_update: ProjectUpdate,
    current_user: User = Depends(get_current_user), 
    db: AsyncSession = Depends(get_db_session)
):
    result = await db.execute(
        select(Project).where(Project.id == project_id, Project.owner_id == current_user.id, Project.deleted_at == None)
    )
    project = result.scalars().first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    update_data = project_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(project, key, value)
        
    await db.commit()
    await db.refresh(project)
    return project

@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
    project_id: uuid.UUID,
    current_user: User = Depends(get_current_user), 
    db: AsyncSession = Depends(get_db_session)
):
    from datetime import datetime, timezone
    result = await db.execute(
        select(Project).where(Project.id == project_id, Project.owner_id == current_user.id, Project.deleted_at == None)
    )
    project = result.scalars().first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    project.deleted_at = datetime.now(timezone.utc)
    await db.commit()

@router.get("/{project_id}/export")
async def export_project_json(
    project_id: uuid.UUID,
    current_user: User = Depends(get_current_user), 
    db: AsyncSession = Depends(get_db_session)
):
    project_result = await db.execute(select(Project).where(Project.id == project_id, Project.owner_id == current_user.id))
    project = project_result.scalars().first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    problem = (await db.execute(select(ProblemAnalysis).where(ProblemAnalysis.project_id == project_id))).scalars().first()
    dna = (await db.execute(select(InnovationDNA).where(InnovationDNA.project_id == project_id))).scalars().first()
    profile = (await db.execute(select(StartupProfile).where(StartupProfile.project_id == project_id))).scalars().first()
    bm = (await db.execute(select(BusinessModel).where(BusinessModel.project_id == project_id))).scalars().first()
    persona = (await db.execute(select(CustomerPersona).where(CustomerPersona.project_id == project_id))).scalars().all()
    market = (await db.execute(select(MarketIntelligence).where(MarketIntelligence.project_id == project_id))).scalars().first()
    financials = (await db.execute(select(FinancialPlan).where(FinancialPlan.project_id == project_id))).scalars().first()
    scores = (await db.execute(select(StartupScore).where(StartupScore.project_id == project_id))).scalars().first()
    
    investor_hub = (await db.execute(select(InvestorHub).where(InvestorHub.project_id == project_id))).scalars().first()
    risk_profile = (await db.execute(select(RiskProfile).where(RiskProfile.project_id == project_id))).scalars().first()
    task_planner = (await db.execute(select(TaskPlanner).where(TaskPlanner.project_id == project_id))).scalars().first()
    ai_mentor = (await db.execute(select(AIMentorAnalysis).where(AIMentorAnalysis.project_id == project_id))).scalars().first()

    def to_dict(obj):
        if not obj: return None
        d = {k: v for k, v in obj.__dict__.items() if not k.startswith('_')}
        if 'id' in d: d['id'] = str(d['id'])
        if 'project_id' in d: d['project_id'] = str(d['project_id'])
        if 'created_at' in d: d['created_at'] = d['created_at'].isoformat()
        if 'updated_at' in d: d['updated_at'] = d['updated_at'].isoformat() if d['updated_at'] else None
        return d

    return {
        "project": to_dict(project),
        "problem_discovery": to_dict(problem),
        "innovation_dna": to_dict(dna),
        "startup_profile": to_dict(profile),
        "business_model": to_dict(bm),
        "customer_personas": [to_dict(p) for p in persona],
        "market_intelligence": to_dict(market),
        "financial_planner": to_dict(financials),
        "startup_score": to_dict(scores),
        "investor_hub": to_dict(investor_hub),
        "risk_profile": to_dict(risk_profile),
        "task_planner": to_dict(task_planner),
        "ai_mentor_analysis": to_dict(ai_mentor)
    }

@router.post("/{project_id}/generate-health-score")
async def generate_startup_health_score(
    project_id: uuid.UUID,
    current_user: User = Depends(get_current_user), 
    db: AsyncSession = Depends(get_db_session)
):
    project_result = await db.execute(select(Project).where(Project.id == project_id, Project.owner_id == current_user.id))
    project = project_result.scalars().first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Fetch context data
    financials = (await db.execute(select(FinancialPlan).where(FinancialPlan.project_id == project_id))).scalars().first()
    market = (await db.execute(select(MarketIntelligence).where(MarketIntelligence.project_id == project_id))).scalars().first()
    
    context = f"Project: {project.name}. Description: {project.description}"
    financial_data = str({k: v for k, v in financials.__dict__.items() if not k.startswith('_')}) if financials else "No financial data"
    market_data = str({k: v for k, v in market.__dict__.items() if not k.startswith('_')}) if market else "No market data"
    
    ai_output = await ai_service.generate_startup_health(context, financial_data, market_data)

    existing_score_result = await db.execute(select(StartupScore).where(StartupScore.project_id == project_id))
    existing_score = existing_score_result.scalars().first()

    if existing_score:
        existing_score.innovation_score = ai_output.innovation_score
        existing_score.business_score = ai_output.business_score
        existing_score.market_score = ai_output.market_score
        existing_score.technology_score = ai_output.technology_score
        existing_score.scalability_score = ai_output.scalability_score
        existing_score.execution_score = ai_output.execution_score
        existing_score.financial_score = ai_output.financial_score
        existing_score.investment_readiness = ai_output.investment_readiness
        existing_score.overall_score = ai_output.overall_health_score
        existing_score.ai_recommendations = ai_output.ai_recommendations
    else:
        new_score = StartupScore(
            project_id=project_id,
            innovation_score=ai_output.innovation_score,
            business_score=ai_output.business_score,
            market_score=ai_output.market_score,
            technology_score=ai_output.technology_score,
            scalability_score=ai_output.scalability_score,
            execution_score=ai_output.execution_score,
            financial_score=ai_output.financial_score,
            investment_readiness=ai_output.investment_readiness,
            overall_score=ai_output.overall_health_score,
            ai_recommendations=ai_output.ai_recommendations
        )
        db.add(new_score)

    await db.commit()
    return {"message": "Health Score Generated", "status": "success"}

@router.get("/{project_id}/health")
async def get_startup_health_score(
    project_id: uuid.UUID,
    current_user: User = Depends(get_current_user), 
    db: AsyncSession = Depends(get_db_session)
):
    project_result = await db.execute(select(Project).where(Project.id == project_id, Project.owner_id == current_user.id))
    project = project_result.scalars().first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    existing_score_result = await db.execute(select(StartupScore).where(StartupScore.project_id == project_id))
    existing_score = existing_score_result.scalars().first()
    if not existing_score:
        raise HTTPException(status_code=404, detail="Startup Score not found")
    return existing_score
