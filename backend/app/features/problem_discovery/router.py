import json
import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.api.dependencies import get_current_user
from app.core.database import get_db_session
from app.features.problem_discovery.models import ProblemAnalysis
from app.features.problem_discovery.schemas import (
    ProblemDiscoveryInput,
    ProblemDiscoveryResponse,
    SingleFieldRegenerateResponse,
    SingleFieldUpdate,
)
from app.features.projects.models import AIVersionHistory, Project
from app.features.projects.utils import recalculate_project_completion
from app.features.users.models import User
from app.services.ai import ContextManager, ai_service

router = APIRouter(prefix="/projects/{project_id}/problem-discovery", tags=["problem_discovery"])

@router.post("", response_model=ProblemDiscoveryResponse)
async def generate_problem_discovery(
    project_id: uuid.UUID,
    inputs: ProblemDiscoveryInput,
    current_user: User = Depends(get_current_user), 
    db: AsyncSession = Depends(get_db_session)
):
    # Verify project exists and belongs to user
    project_result = await db.execute(select(Project).where(Project.id == project_id, Project.owner_id == current_user.id))
    project = project_result.scalars().first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Generate via AI
    ai_output = await ai_service.generate_problem_discovery(inputs.dict())

    # Save to database
    # Check if already exists, if so update, else create
    existing_result = await db.execute(select(ProblemAnalysis).where(ProblemAnalysis.project_id == project_id))
    existing = existing_result.scalars().first()

    if existing:
        existing.core_problem = ai_output.problem_summary
        existing.problem_summary = ai_output.problem_summary
        existing.root_cause_analysis = ai_output.root_cause_analysis
        existing.stakeholders = ai_output.stakeholders
        existing.impact_analysis = ai_output.impact_analysis
        existing.opportunity_score = ai_output.opportunity_score
        existing.sdg_alignment = ai_output.sdg_alignment
        existing.key_insights = ai_output.key_insights
        analysis = existing
    else:
        analysis = ProblemAnalysis(
            project_id=project_id,
            core_problem=ai_output.problem_summary,
            problem_summary=ai_output.problem_summary,
            root_cause_analysis=ai_output.root_cause_analysis,
            stakeholders=ai_output.stakeholders,
            impact_analysis=ai_output.impact_analysis,
            opportunity_score=ai_output.opportunity_score,
            sdg_alignment=ai_output.sdg_alignment,
            key_insights=ai_output.key_insights
        )
        db.add(analysis)

    await db.commit()
    await db.refresh(analysis)
    await recalculate_project_completion(project_id, db)
    return analysis

@router.get("", response_model=ProblemDiscoveryResponse)
async def get_problem_discovery(
    project_id: uuid.UUID,
    current_user: User = Depends(get_current_user), 
    db: AsyncSession = Depends(get_db_session)
):
    project_result = await db.execute(select(Project).where(Project.id == project_id, Project.owner_id == current_user.id))
    if not project_result.scalars().first():
        raise HTTPException(status_code=404, detail="Project not found")

    existing_result = await db.execute(select(ProblemAnalysis).where(ProblemAnalysis.project_id == project_id))
    existing = existing_result.scalars().first()
    if not existing:
        raise HTTPException(status_code=404, detail="Problem analysis not found")
    
    return existing

@router.put("/{field_name}", response_model=ProblemDiscoveryResponse)
async def update_single_field(
    project_id: uuid.UUID,
    field_name: str,
    update_data: SingleFieldUpdate,
    current_user: User = Depends(get_current_user), 
    db: AsyncSession = Depends(get_db_session)
):
    project_result = await db.execute(select(Project).where(Project.id == project_id, Project.owner_id == current_user.id))
    if not project_result.scalars().first():
        raise HTTPException(status_code=404, detail="Project not found")

    existing_result = await db.execute(select(ProblemAnalysis).where(ProblemAnalysis.project_id == project_id))
    existing = existing_result.scalars().first()
    if not existing:
        raise HTTPException(status_code=404, detail="Problem analysis not found")
    
    if not hasattr(existing, field_name):
        raise HTTPException(status_code=400, detail=f"Field {field_name} does not exist")
        
    setattr(existing, field_name, update_data.content)
    await db.commit()
    await db.refresh(existing)
    return existing

@router.post("/{field_name}/regenerate", response_model=SingleFieldRegenerateResponse)
async def regenerate_single_field(
    project_id: uuid.UUID,
    field_name: str,
    current_user: User = Depends(get_current_user), 
    db: AsyncSession = Depends(get_db_session)
):
    project_result = await db.execute(select(Project).where(Project.id == project_id, Project.owner_id == current_user.id))
    if not project_result.scalars().first():
        raise HTTPException(status_code=404, detail="Project not found")

    existing_result = await db.execute(select(ProblemAnalysis).where(ProblemAnalysis.project_id == project_id))
    existing = existing_result.scalars().first()
    if not existing or not hasattr(existing, field_name):
        raise HTTPException(status_code=404, detail="Field or analysis not found")

    current_content = getattr(existing, field_name)
    # Save version history
    history = AIVersionHistory(
        project_id=project_id,
        module="problem_discovery",
        field_name=field_name,
        content={"data": current_content} if not isinstance(current_content, dict) else current_content
    )
    db.add(history)

    # Regenerate
    context_str = ContextManager.build_problem_context({
        "summary": existing.problem_summary,
        "root_causes": existing.root_cause_analysis
    })
    
    new_content = await ai_service.regenerate_single_field(context_str, field_name, str(current_content))
    
    # Simple hack to parse JSON if the field expects it
    if isinstance(current_content, (dict, list)):
        try:
            new_content = json.loads(new_content)
        except json.JSONDecodeError as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.warning("Failed to decode JSON: %s", e)

    setattr(existing, field_name, new_content)
    await db.commit()
    
    return SingleFieldRegenerateResponse(new_content=new_content)
