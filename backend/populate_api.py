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
        
        print(f"User email: {user.email}")
        from app.core.security import get_password_hash
        user.hashed_password = get_password_hash("password123")
        await db.commit()
        print("Password reset to password123")
        
    # Now we can log in and generate
    async with httpx.AsyncClient(base_url="http://localhost:8000", timeout=120.0) as client:
        resp = await client.post("/auth/login", json={"email": user.email, "password": "password123"})
        token = resp.json().get("access_token")
        headers = {"Authorization": f"Bearer {token}"}
        
        # 1. Problem Discovery
        print("Generating Problem Discovery...")
        r1 = await client.post(f"/projects/{project_id}/problem-discovery", json={
            "title": project.name,
            "description": project.description or "A cool project",
            "industry": "Tech",
            "country": "USA",
            "target_users": "Everyone",
            "existing_solutions": "None",
            "pain_points": "Many"
        }, headers=headers)
        print("Problem Discovery:", r1.status_code)
        
        # 2. Innovation DNA
        print("Generating Innovation DNA...")
        r2 = await client.post(f"/projects/{project_id}/innovation-dna", json={
            "problem_summary": "Summary",
            "target_audience": ["Users"],
            "innovation_focus": "Tech"
        }, headers=headers)
        print("Innovation DNA:", r2.status_code)

        # 3. Startup Formation
        print("Generating Startup Formation...")
        r3 = await client.post(f"/projects/{project_id}/startup-formation", json={
            "value_proposition": "Value",
            "business_model_canvas": {"key": "value"}
        }, headers=headers)
        print("Startup Formation:", r3.status_code)

        # 4. Market Intelligence
        print("Generating Market Intelligence...")
        r4 = await client.post(f"/projects/{project_id}/market-intelligence", json={
            "startup_name": "Test Startup",
            "industry": "Tech",
            "value_proposition": "Value"
        }, headers=headers)
        print("Market Intelligence:", r4.status_code)
        
        # 5. Financial Planner
        print("Generating Financial Planner...")
        r5 = await client.post(f"/projects/{project_id}/financial-planner", json={
            "startup_name": "Test Startup",
            "business_model": "SaaS"
        }, headers=headers)
        print("Financial Planner:", r5.status_code)
        
        # 6. Startup Health
        print("Generating Startup Health...")
        r6 = await client.post(f"/projects/{project_id}/startup-health", json={
            "startup_name": "Test Startup"
        }, headers=headers)
        print("Startup Health:", r6.status_code)

if __name__ == "__main__":
    asyncio.run(run())
