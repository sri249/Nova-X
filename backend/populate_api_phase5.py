import asyncio
import uuid

import httpx
from sqlalchemy import select

# Import main to register all models
from app.core.database import async_session_maker
from app.features.projects.models import Project
from app.features.users.models import User


async def run():
    project_id = '7aad881f-a0ba-46d3-8cd9-ae1a51c17062'
    
    async with async_session_maker() as db:
        proj_result = await db.execute(select(Project).where(Project.id == uuid.UUID(project_id)))
        project = proj_result.scalars().first()
        if not project:
            print("Project not found")
            return
            
        user_result = await db.execute(select(User).where(User.id == project.owner_id))
        user = user_result.scalars().first()
        
    # Now we can log in and generate
    async with httpx.AsyncClient(base_url="http://localhost:8000", timeout=120.0) as client:
        resp = await client.post("/auth/login", json={"email": user.email, "password": "password123"})
        token = resp.json().get("access_token")
        headers = {"Authorization": f"Bearer {token}"}
        
        # 1. Investor Hub
        print("Generating Investor Hub...")
        r1 = await client.post(f"/projects/{project_id}/investor-hub", json={}, headers=headers)
        print("Investor Hub:", r1.status_code, r1.text)
        
        # 2. Risk Engine
        print("Generating Risk Engine...")
        r2 = await client.post(f"/projects/{project_id}/risk-engine", json={}, headers=headers)
        print("Risk Engine:", r2.status_code, r2.text)

        # 3. Task Planner
        print("Generating Task Planner...")
        r3 = await client.post(f"/projects/{project_id}/task-planner", json={}, headers=headers)
        print("Task Planner:", r3.status_code, r3.text)

        # Also hit generate-health-score just in case
        print("Generating Health Score...")
        r4 = await client.post(f"/projects/{project_id}/generate-health-score", json={}, headers=headers)
        print("Health Score:", r4.status_code)

if __name__ == "__main__":
    asyncio.run(run())
