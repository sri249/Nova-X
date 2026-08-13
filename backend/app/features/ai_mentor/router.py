import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db_session
from app.features.ai_mentor.models import AIMentorAnalysis
from app.features.projects.models import Project
from app.features.projects.utils import recalculate_project_completion
from app.features.users.models import User
from app.features.users.router import get_current_user
from app.services.ai.context_manager import ContextManager
from app.services.ai.service import ai_service

router = APIRouter(prefix="/projects/{project_id}/ai-mentor", tags=["AI Mentor"])

@router.post("")
async def generate_ai_mentor(
    project_id: uuid.UUID,
    current_user: User = Depends(get_current_user), 
    db: AsyncSession = Depends(get_db_session)
):
    project_result = await db.execute(select(Project).where(Project.id == project_id, Project.owner_id == current_user.id))
    project = project_result.scalars().first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    context = await ContextManager.build_full_project_context(project_id, db)
    generated = await ai_service.generate_ai_mentor(context=context)

    result = await db.execute(select(AIMentorAnalysis).where(AIMentorAnalysis.project_id == project_id))
    existing = result.scalars().first()

    if existing:
        existing.strengths = generated.strengths
        existing.weaknesses = generated.weaknesses
        existing.missing_information = generated.missing_information
        existing.risk_alerts = generated.risk_alerts
        existing.recommended_next_actions = generated.recommended_next_actions
        existing.weekly_priorities = generated.weekly_priorities
        existing.ai_metadata = generated.ai_metadata.model_dump()
    else:
        new_analysis = AIMentorAnalysis(
            project_id=project_id,
            strengths=generated.strengths,
            weaknesses=generated.weaknesses,
            missing_information=generated.missing_information,
            risk_alerts=generated.risk_alerts,
            recommended_next_actions=generated.recommended_next_actions,
            weekly_priorities=generated.weekly_priorities,
            ai_metadata=generated.ai_metadata.model_dump()
        )
        db.add(new_analysis)

    await db.commit()
    await recalculate_project_completion(project_id, db)
    return {"status": "success", "message": "AI Mentor generated"}

@router.get("")
async def get_ai_mentor(
    project_id: uuid.UUID,
    current_user: User = Depends(get_current_user), 
    db: AsyncSession = Depends(get_db_session)
):
    project_result = await db.execute(select(Project).where(Project.id == project_id, Project.owner_id == current_user.id))
    if not project_result.scalars().first():
        raise HTTPException(status_code=404, detail="Project not found")

    result = await db.execute(select(AIMentorAnalysis).where(AIMentorAnalysis.project_id == project_id))
    analysis = result.scalars().first()
    if not analysis:
        raise HTTPException(status_code=404, detail="AI Mentor Analysis not found")
    return analysis
