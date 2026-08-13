import datetime
import json
import uuid
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db_session
from app.features.financial_planner.models import FinancialPlan
from app.features.projects.models import AIVersionHistory, Project
from app.features.projects.utils import recalculate_project_completion
from app.features.users.models import User
from app.features.users.router import get_current_user
from app.services.ai.service import ai_service

router = APIRouter(prefix="/projects/{project_id}/financial-planner", tags=["Financial Planner"])

class SingleFieldUpdate(BaseModel):
    content: Any

@router.post("")
async def generate_financial_planner(
    project_id: uuid.UUID,
    current_user: User = Depends(get_current_user), 
    db: AsyncSession = Depends(get_db_session)
):
    project_result = await db.execute(select(Project).where(Project.id == project_id, Project.owner_id == current_user.id))
    project = project_result.scalars().first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    context = f"Project: {project.name}. Description: {project.description}"
    market_data = "Market data provided here."
    
    ai_output = await ai_service.generate_financial_planner(context, market_data)

    existing_result = await db.execute(select(FinancialPlan).where(FinancialPlan.project_id == project_id))
    existing = existing_result.scalars().first()

    metadata_dict = ai_output.ai_metadata.model_dump()
    metadata_dict["generated_at"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    metadata_dict["model_version"] = "gpt-4o-mini"

    if existing:
        existing.startup_costs = ai_output.startup_costs
        existing.monthly_operating_costs = ai_output.monthly_operating_costs
        existing.hiring_costs = ai_output.hiring_costs
        existing.marketing_budget = ai_output.marketing_budget
        existing.infrastructure_cost = ai_output.infrastructure_cost
        existing.revenue_forecast = ai_output.revenue_forecast
        existing.cash_flow = ai_output.cash_flow
        existing.burn_rate = ai_output.burn_rate
        existing.runway = ai_output.runway
        existing.break_even_month = ai_output.break_even_month
        existing.funding_requirement = ai_output.funding_requirement
        existing.funding_recommendation = ai_output.funding_recommendation
        existing.roi_projection = ai_output.roi_projection
        existing.ai_metadata = metadata_dict
    else:
        new_fp = FinancialPlan(
            project_id=project_id,
            startup_costs=ai_output.startup_costs,
            monthly_operating_costs=ai_output.monthly_operating_costs,
            hiring_costs=ai_output.hiring_costs,
            marketing_budget=ai_output.marketing_budget,
            infrastructure_cost=ai_output.infrastructure_cost,
            revenue_forecast=ai_output.revenue_forecast,
            cash_flow=ai_output.cash_flow,
            burn_rate=ai_output.burn_rate,
            runway=ai_output.runway,
            break_even_month=ai_output.break_even_month,
            funding_requirement=ai_output.funding_requirement,
            funding_recommendation=ai_output.funding_recommendation,
            roi_projection=ai_output.roi_projection,
            ai_metadata=metadata_dict
        )
        db.add(new_fp)

    await db.commit()
    await recalculate_project_completion(project_id, db)
    return {"message": "Financial Planner generated", "status": "success"}

@router.get("")
async def get_financial_planner(
    project_id: uuid.UUID,
    current_user: User = Depends(get_current_user), 
    db: AsyncSession = Depends(get_db_session)
):
    project_result = await db.execute(select(Project).where(Project.id == project_id, Project.owner_id == current_user.id))
    if not project_result.scalars().first():
        raise HTTPException(status_code=404, detail="Project not found")

    result = await db.execute(select(FinancialPlan).where(FinancialPlan.project_id == project_id))
    data = result.scalars().first()
    if not data:
        raise HTTPException(status_code=404, detail="Financial Planner not found")
    
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

    result = await db.execute(select(FinancialPlan).where(FinancialPlan.project_id == project_id))
    existing = result.scalars().first()
    
    if not existing:
        raise HTTPException(status_code=404, detail="Financial Planner not found")

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

    result = await db.execute(select(FinancialPlan).where(FinancialPlan.project_id == project_id))
    existing = result.scalars().first()
    
    if not existing:
        raise HTTPException(status_code=404, detail="Financial Planner not found")

    if not hasattr(existing, field_name):
        raise HTTPException(status_code=400, detail="Invalid field name")

    current_content = getattr(existing, field_name)

    history = AIVersionHistory(
        project_id=project_id,
        module="financial_planner",
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
