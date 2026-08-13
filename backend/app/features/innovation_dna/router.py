import json
import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.api.dependencies import get_current_user
from app.core.database import get_db_session
from app.features.innovation_dna.models import InnovationDNA
from app.features.innovation_dna.schemas import (
    InnovationDNAResponse,
    SingleFieldRegenerateResponse,
    SingleFieldUpdate,
)
from app.features.problem_discovery.models import ProblemAnalysis
from app.features.projects.models import AIVersionHistory, Project
from app.features.projects.utils import recalculate_project_completion
from app.features.users.models import User
from app.services.ai import ContextManager, ai_service

router = APIRouter(prefix="/projects/{project_id}/innovation-dna", tags=["innovation_dna"])

@router.post("", response_model=InnovationDNAResponse)
async def generate_innovation_dna(
    project_id: uuid.UUID,
    current_user: User = Depends(get_current_user), 
    db: AsyncSession = Depends(get_db_session)
):
    project_result = await db.execute(select(Project).where(Project.id == project_id, Project.owner_id == current_user.id))
    if not project_result.scalars().first():
        raise HTTPException(status_code=404, detail="Project not found")

    problem_result = await db.execute(select(ProblemAnalysis).where(ProblemAnalysis.project_id == project_id))
    problem = problem_result.scalars().first()
    if not problem:
        raise HTTPException(status_code=400, detail="Problem Discovery must be completed first")

    # Generate via AI
    ai_output = await ai_service.generate_innovation_dna(problem.core_problem, problem.root_cause_analysis)

    existing_result = await db.execute(select(InnovationDNA).where(InnovationDNA.project_id == project_id))
    existing = existing_result.scalars().first()

    if existing:
        existing.unique_value_proposition = ai_output.differentiation[0] if ai_output.differentiation else "N/A"
        existing.unfair_advantage = ai_output.market_gap
        existing.innovation_score = ai_output.innovation_score
        existing.originality_score = ai_output.originality_score
        existing.competitor_overview = ai_output.competitor_overview
        existing.market_gap = ai_output.market_gap
        existing.novelty_analysis = ai_output.novelty_analysis
        existing.differentiation = ai_output.differentiation
        existing.patent_potential_indicator = ai_output.patent_potential_indicator
        existing.innovation_radar_visualization = ai_output.innovation_radar_visualization
        dna = existing
    else:
        dna = InnovationDNA(
            project_id=project_id,
            unique_value_proposition=ai_output.differentiation[0] if ai_output.differentiation else "N/A",
            unfair_advantage=ai_output.market_gap,
            innovation_score=ai_output.innovation_score,
            originality_score=ai_output.originality_score,
            competitor_overview=ai_output.competitor_overview,
            market_gap=ai_output.market_gap,
            novelty_analysis=ai_output.novelty_analysis,
            differentiation=ai_output.differentiation,
            patent_potential_indicator=ai_output.patent_potential_indicator,
            innovation_radar_visualization=ai_output.innovation_radar_visualization
        )
        db.add(dna)

    await db.commit()
    await db.refresh(dna)
    await recalculate_project_completion(project_id, db)
    return dna

@router.get("", response_model=InnovationDNAResponse)
async def get_innovation_dna(
    project_id: uuid.UUID,
    current_user: User = Depends(get_current_user), 
    db: AsyncSession = Depends(get_db_session)
):
    project_result = await db.execute(select(Project).where(Project.id == project_id, Project.owner_id == current_user.id))
    if not project_result.scalars().first():
        raise HTTPException(status_code=404, detail="Project not found")

    existing_result = await db.execute(select(InnovationDNA).where(InnovationDNA.project_id == project_id))
    existing = existing_result.scalars().first()
    if not existing:
        raise HTTPException(status_code=404, detail="Innovation DNA not found")
    
    return existing

@router.put("/{field_name}", response_model=InnovationDNAResponse)
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

    existing_result = await db.execute(select(InnovationDNA).where(InnovationDNA.project_id == project_id))
    existing = existing_result.scalars().first()
    if not existing:
        raise HTTPException(status_code=404, detail="Innovation DNA not found")
    
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

    existing_result = await db.execute(select(InnovationDNA).where(InnovationDNA.project_id == project_id))
    existing = existing_result.scalars().first()
    if not existing or not hasattr(existing, field_name):
        raise HTTPException(status_code=404, detail="Field or DNA not found")

    current_content = getattr(existing, field_name)
    
    # Save version history
    history = AIVersionHistory(
        project_id=project_id,
        module="innovation_dna",
        field_name=field_name,
        content={"data": current_content} if not isinstance(current_content, dict) else current_content
    )
    db.add(history)

    # Regenerate
    problem_result = await db.execute(select(ProblemAnalysis).where(ProblemAnalysis.project_id == project_id))
    problem = problem_result.scalars().first()
    
    context_str = ContextManager.build_innovation_context({
        "problem_summary": problem.problem_summary if problem else "",
        "root_causes": problem.root_cause_analysis if problem else {},
        "current_dna": {
             "value_prop": existing.unique_value_proposition,
             "market_gap": existing.market_gap
        }
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
