import asyncio
import uuid

from sqlalchemy import select

from app.core.database import async_session_maker
from app.features.problem_discovery.models import ProblemAnalysis
from app.features.projects.models import Project


async def main():
    async with async_session_maker() as db:
        project_id = uuid.UUID('7aad881f-a0ba-46d3-8cd9-ae1a51c17062')
        proj = await db.execute(select(Project).where(Project.id == project_id))
        project_obj = proj.scalars().first()
        if project_obj:
            print(f'Project ID: {project_obj.id}')
            print(f'User ID: {project_obj.owner_id}')
            print(f'Status: {project_obj.status}')
            print(f'Created At: {project_obj.created_at}')
        else:
            print('Project not found!')
        
        pa = await db.execute(select(ProblemAnalysis).where(ProblemAnalysis.project_id == project_id))
        pa_obj = pa.scalars().first()
        if pa_obj:
            print(f'ProblemAnalysis found for project {project_id}')
            print(f'Core Problem: {pa_obj.core_problem}')
        else:
            print(f'ProblemAnalysis not found for project {project_id}')

if __name__ == "__main__":
    asyncio.run(main())
