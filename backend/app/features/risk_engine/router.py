import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db_session
from app.features.projects.models import Project
from app.features.projects.utils import recalculate_project_completion
from app.features.risk_engine.models import RiskProfile
from app.features.users.models import User
from app.features.users.router import get_current_user
from app.services.ai.context_manager import ContextManager
from app.services.ai.service import ai_service

router = APIRouter(prefix="/projects/{project_id}/risk-engine", tags=["Risk Engine"])

@router.post("")
async def generate_risk_profile(
    project_id: uuid.UUID,
    current_user: User = Depends(get_current_user), 
    db: AsyncSession = Depends(get_db_session)
):
    project_result = await db.execute(select(Project).where(Project.id == project_id, Project.owner_id == current_user.id))
    project = project_result.scalars().first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    context = await ContextManager.build_full_project_context(project_id, db)
    generated = await ai_service.generate_risk_profile(context=context)

    result = await db.execute(select(RiskProfile).where(RiskProfile.project_id == project_id))
    existing = result.scalars().first()

    if existing:
        existing.technical_risks = generated.technical_risks
        existing.market_risks = generated.market_risks
        existing.financial_risks = generated.financial_risks
        existing.legal_risks = generated.legal_risks
        existing.execution_risks = generated.execution_risks
        existing.hiring_risks = generated.hiring_risks
        existing.ai_metadata = generated.ai_metadata.model_dump()
    else:
        new_risk = RiskProfile(
            project_id=project_id,
            technical_risks=generated.technical_risks,
            market_risks=generated.market_risks,
            financial_risks=generated.financial_risks,
            legal_risks=generated.legal_risks,
            execution_risks=generated.execution_risks,
            hiring_risks=generated.hiring_risks,
            ai_metadata=generated.ai_metadata.model_dump()
        )
        db.add(new_risk)

    await db.commit()
    await recalculate_project_completion(project_id, db)
    return {"status": "success", "message": "Risk Profile generated"}

@router.get("")
async def get_risk_profile(
    project_id: uuid.UUID,
    current_user: User = Depends(get_current_user), 
    db: AsyncSession = Depends(get_db_session)
):
    project_result = await db.execute(select(Project).where(Project.id == project_id, Project.owner_id == current_user.id))
    if not project_result.scalars().first():
        raise HTTPException(status_code=404, detail="Project not found")

    result = await db.execute(select(RiskProfile).where(RiskProfile.project_id == project_id))
    risk = result.scalars().first()
    if not risk:
        raise HTTPException(status_code=404, detail="Risk Profile not found")
    return risk
