import asyncio
import uuid

from sqlalchemy import select

# Import main to register all models
from app.core.database import async_session_maker
from app.features.investor_hub.router import generate_investor_hub
from app.features.projects.models import Project
from app.features.risk_engine.router import generate_risk_profile
from app.features.task_planner.router import generate_task_planner
from app.features.users.models import User


async def run():
    project_id = uuid.UUID('7aad881f-a0ba-46d3-8cd9-ae1a51c17062')
    
    async with async_session_maker() as db:
        proj_result = await db.execute(select(Project).where(Project.id == project_id))
        project = proj_result.scalars().first()
        if not project:
            print("Project not found")
            return
            
        user_result = await db.execute(select(User).where(User.id == project.owner_id))
        user = user_result.scalars().first()
        
        # 1. Investor Hub
        print("Generating Investor Hub...")
        r1 = await generate_investor_hub(project_id, user, db)
        print("Investor Hub:", r1)
        
        # 2. Risk Engine
        print("Generating Risk Engine...")
        r2 = await generate_risk_profile(project_id, user, db)
        print("Risk Engine:", r2)

        # 3. Task Planner
        print("Generating Task Planner...")
        r3 = await generate_task_planner(project_id, user, db)
        print("Task Planner:", r3)

if __name__ == "__main__":
    asyncio.run(run())
