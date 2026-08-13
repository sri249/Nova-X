import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db_session
from app.features.investor_hub.models import InvestorHub
from app.features.projects.models import Project
from app.features.projects.utils import recalculate_project_completion
from app.features.users.models import User
from app.features.users.router import get_current_user
from app.services.ai.context_manager import ContextManager
from app.services.ai.service import ai_service

router = APIRouter(prefix="/projects/{project_id}/investor-hub", tags=["Investor Hub"])

@router.post("")
async def generate_investor_hub(
    project_id: uuid.UUID,
    current_user: User = Depends(get_current_user), 
    db: AsyncSession = Depends(get_db_session)
):
    try:
        project_result = await db.execute(select(Project).where(Project.id == project_id, Project.owner_id == current_user.id))
        project = project_result.scalars().first()
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")

        context = await ContextManager.build_full_project_context(project_id, db)
        
        generated = await ai_service.generate_investor_hub(context=context)

        # Check if exists
        result = await db.execute(select(InvestorHub).where(InvestorHub.project_id == project_id))
        existing = result.scalars().first()

        if existing:
            existing.executive_summary = generated.executive_summary
            existing.investment_memo = generated.investment_memo
            existing.funding_strategy = generated.funding_strategy
            existing.one_page_profile = generated.one_page_profile
            existing.due_diligence_checklist = generated.due_diligence_checklist
            existing.milestone_roadmap = generated.milestone_roadmap
            existing.pitch_deck = generated.pitch_deck
            existing.ai_metadata = generated.ai_metadata.model_dump()
        else:
            new_hub = InvestorHub(
                project_id=project_id,
                executive_summary=generated.executive_summary,
                investment_memo=generated.investment_memo,
                funding_strategy=generated.funding_strategy,
                one_page_profile=generated.one_page_profile,
                due_diligence_checklist=generated.due_diligence_checklist,
                milestone_roadmap=generated.milestone_roadmap,
                pitch_deck=generated.pitch_deck,
                ai_metadata=generated.ai_metadata.model_dump()
            )
            db.add(new_hub)

        await db.commit()
        await recalculate_project_completion(project_id, db)
        return {"status": "success", "message": "Investor Hub generated"}
    except HTTPException:
        raise
    except (ValueError, TypeError, KeyError, AttributeError, RuntimeError) as e:
        import traceback
        error_msg = "".join(traceback.format_exception(type(e), e, e.__traceback__))
        print(error_msg)
        return {"error": str(e), "traceback": error_msg}

@router.get("")
async def get_investor_hub(
    project_id: uuid.UUID,
    current_user: User = Depends(get_current_user), 
    db: AsyncSession = Depends(get_db_session)
):
    project_result = await db.execute(select(Project).where(Project.id == project_id, Project.owner_id == current_user.id))
    if not project_result.scalars().first():
        raise HTTPException(status_code=404, detail="Project not found")

    result = await db.execute(select(InvestorHub).where(InvestorHub.project_id == project_id))
    hub = result.scalars().first()
    if not hub:
        raise HTTPException(status_code=404, detail="Investor Hub not found")

    return hub
