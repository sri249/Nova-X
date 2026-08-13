import datetime
import json
import uuid
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db_session
from app.features.market_intelligence.models import MarketIntelligence
from app.features.projects.models import AIVersionHistory, Project
from app.features.projects.utils import recalculate_project_completion
from app.features.users.models import User
from app.features.users.router import get_current_user
from app.services.ai.service import ai_service

router = APIRouter(prefix="/projects/{project_id}/market-intelligence", tags=["Market Intelligence"])

class SingleFieldUpdate(BaseModel):
    content: Any

@router.post("")
async def generate_market_intelligence(
    project_id: uuid.UUID,
    current_user: User = Depends(get_current_user), 
    db: AsyncSession = Depends(get_db_session)
):
    project_result = await db.execute(select(Project).where(Project.id == project_id, Project.owner_id == current_user.id))
    project = project_result.scalars().first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    context = f"Project: {project.name}. Description: {project.description}"
    
    ai_output = await ai_service.generate_market_intelligence(context)

    existing_result = await db.execute(select(MarketIntelligence).where(MarketIntelligence.project_id == project_id))
    existing = existing_result.scalars().first()

    # Create metadata dict with generated_at and model_version
    metadata_dict = ai_output.ai_metadata.model_dump()
    metadata_dict["generated_at"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    metadata_dict["model_version"] = "gpt-4o-mini"

    if existing:
        existing.tam_sam_som = ai_output.tam_sam_som
        existing.industry_growth_rate = ai_output.industry_growth_rate
        existing.cagr = ai_output.cagr
        existing.market_maturity = ai_output.market_maturity
        existing.customer_personas = ai_output.customer_personas
        existing.adoption_curve = ai_output.adoption_curve
        existing.seasonal_trends = ai_output.seasonal_trends
        existing.market_trends = ai_output.market_trends
        existing.geographic_expansion = ai_output.geographic_expansion
        existing.regulatory_risks = ai_output.regulatory_risks
        existing.emerging_technologies = ai_output.emerging_technologies
        existing.swot_analysis = ai_output.swot_analysis
        existing.competitor_matrix = ai_output.competitor_matrix
        existing.market_gap_analysis = ai_output.market_gap_analysis
        existing.barriers_to_entry = ai_output.barriers_to_entry
        existing.market_readiness_score = ai_output.market_readiness_score
        existing.ai_metadata = metadata_dict
    else:
        new_market = MarketIntelligence(
            project_id=project_id,
            tam_sam_som=ai_output.tam_sam_som,
            industry_growth_rate=ai_output.industry_growth_rate,
            cagr=ai_output.cagr,
            market_maturity=ai_output.market_maturity,
            customer_personas=ai_output.customer_personas,
            adoption_curve=ai_output.adoption_curve,
            seasonal_trends=ai_output.seasonal_trends,
            market_trends=ai_output.market_trends,
            geographic_expansion=ai_output.geographic_expansion,
            regulatory_risks=ai_output.regulatory_risks,
            emerging_technologies=ai_output.emerging_technologies,
            swot_analysis=ai_output.swot_analysis,
            competitor_matrix=ai_output.competitor_matrix,
            market_gap_analysis=ai_output.market_gap_analysis,
            barriers_to_entry=ai_output.barriers_to_entry,
            market_readiness_score=ai_output.market_readiness_score,
            ai_metadata=metadata_dict
        )
        db.add(new_market)

    await db.commit()
    await recalculate_project_completion(project_id, db)
    return {"message": "Market Intelligence generated", "status": "success"}

@router.get("")
async def get_market_intelligence(
    project_id: uuid.UUID,
    current_user: User = Depends(get_current_user), 
    db: AsyncSession = Depends(get_db_session)
):
    project_result = await db.execute(select(Project).where(Project.id == project_id, Project.owner_id == current_user.id))
    if not project_result.scalars().first():
        raise HTTPException(status_code=404, detail="Project not found")

    result = await db.execute(select(MarketIntelligence).where(MarketIntelligence.project_id == project_id))
    data = result.scalars().first()
    if not data:
        raise HTTPException(status_code=404, detail="Market Intelligence not found")
    
    return data

@router.put("/{field_name}")
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

    result = await db.execute(select(MarketIntelligence).where(MarketIntelligence.project_id == project_id))
    existing = result.scalars().first()
    
    if not existing:
        raise HTTPException(status_code=404, detail="Market Intelligence not found")

    if not hasattr(existing, field_name):
        raise HTTPException(status_code=400, detail="Invalid field name")

    setattr(existing, field_name, update_data.content)
    await db.commit()
    return {"message": "Updated successfully"}

@router.post("/{field_name}/regenerate")
async def regenerate_single_field(
    project_id: uuid.UUID,
    field_name: str,
    current_user: User = Depends(get_current_user), 
    db: AsyncSession = Depends(get_db_session)
):
    project_result = await db.execute(select(Project).where(Project.id == project_id, Project.owner_id == current_user.id))
    project = project_result.scalars().first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    result = await db.execute(select(MarketIntelligence).where(MarketIntelligence.project_id == project_id))
    existing = result.scalars().first()
    
    if not existing:
        raise HTTPException(status_code=404, detail="Market Intelligence not found")

    if not hasattr(existing, field_name):
        raise HTTPException(status_code=400, detail="Invalid field name")

    current_content = getattr(existing, field_name)

    history = AIVersionHistory(
        project_id=project_id,
        module="market_intelligence",
        field_name=field_name,
        content=current_content if isinstance(current_content, (dict, list)) else {"text": current_content}
    )
    db.add(history)

    context = f"Project: {project.name}. Description: {project.description}"
    new_content = await ai_service.regenerate_single_field(context, field_name, str(current_content))

    if isinstance(current_content, (dict, list)):
        try:
            new_content = json.loads(new_content)
        except json.JSONDecodeError as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.warning("Failed to decode JSON: %s", e)

    setattr(existing, field_name, new_content)
    await db.commit()
    
    return {"message": "Regenerated successfully", "new_content": new_content}
