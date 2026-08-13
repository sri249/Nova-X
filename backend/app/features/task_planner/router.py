import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db_session
from app.features.projects.models import Project
from app.features.projects.utils import recalculate_project_completion
from app.features.task_planner.models import TaskPlanner
from app.features.users.models import User
from app.features.users.router import get_current_user
from app.services.ai.context_manager import ContextManager
from app.services.ai.service import ai_service

router = APIRouter(prefix="/projects/{project_id}/task-planner", tags=["Task Planner"])

@router.post("")
async def generate_task_planner(
    project_id: uuid.UUID,
    current_user: User = Depends(get_current_user), 
    db: AsyncSession = Depends(get_db_session)
):
    project_result = await db.execute(select(Project).where(Project.id == project_id, Project.owner_id == current_user.id))
    project = project_result.scalars().first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    context = await ContextManager.build_full_project_context(project_id, db)
    generated = await ai_service.generate_task_planner(context=context)

    result = await db.execute(select(TaskPlanner).where(TaskPlanner.project_id == project_id))
    existing = result.scalars().first()

    if existing:
        existing.immediate_tasks = generated.immediate_tasks
        existing.day_30_plan = generated.day_30_plan
        existing.day_90_plan = generated.day_90_plan
        existing.month_6_plan = generated.month_6_plan
        existing.fundraising_timeline = generated.fundraising_timeline
        existing.product_timeline = generated.product_timeline
        existing.ai_metadata = generated.ai_metadata.model_dump()
    else:
        new_plan = TaskPlanner(
            project_id=project_id,
            immediate_tasks=generated.immediate_tasks,
            day_30_plan=generated.day_30_plan,
            day_90_plan=generated.day_90_plan,
            month_6_plan=generated.month_6_plan,
            fundraising_timeline=generated.fundraising_timeline,
            product_timeline=generated.product_timeline,
            ai_metadata=generated.ai_metadata.model_dump()
        )
        db.add(new_plan)

    await db.commit()
    await recalculate_project_completion(project_id, db)
    return {"status": "success", "message": "Task Planner generated"}

@router.get("")
async def get_task_planner(
    project_id: uuid.UUID,
    current_user: User = Depends(get_current_user), 
    db: AsyncSession = Depends(get_db_session)
):
    project_result = await db.execute(select(Project).where(Project.id == project_id, Project.owner_id == current_user.id))
    if not project_result.scalars().first():
        raise HTTPException(status_code=404, detail="Project not found")

    result = await db.execute(select(TaskPlanner).where(TaskPlanner.project_id == project_id))
    plan = result.scalars().first()
    if not plan:
        raise HTTPException(status_code=404, detail="Task Planner not found")
    return plan
