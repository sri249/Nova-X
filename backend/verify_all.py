import asyncio
from datetime import timedelta

import httpx
from sqlalchemy import select

from app.core.database import async_session_maker

# Models to verify inserts
from app.core.security import create_access_token
from app.features.users.models import User


async def run_verification():
    print("Starting E2E Backend Verification...")
    
    async with async_session_maker() as db:
        user_result = await db.execute(select(User).limit(1))
        user = user_result.scalars().first()
        if not user:
            print("No user found")
            return
            
    # Create token manually
    token = create_access_token(subject=str(user.id), expires_delta=timedelta(hours=1))
    
    async with httpx.AsyncClient(base_url="http://localhost:8000", timeout=60.0) as client:
        headers = {"Authorization": f"Bearer {token}"}
        
        # 2. Create Project
        proj_resp = await client.post("/projects", json={
            "name": "E2E Verification Project",
            "description": "Testing everything",
            "status": "Generating"
        }, headers=headers)
        print(f"Project Creation Status: {proj_resp.status_code}")
        print(f"Project Creation Response: {proj_resp.text}")
        project_id = proj_resp.json()["id"]
        print(f"Created Project: {project_id}")
        
        # 3. Hit all endpoints
        endpoints = [
            ("Problem Discovery", f"/projects/{project_id}/problem-discovery", {
                "title": "E2E", 
                "description": "Desc",
                "industry": "Tech",
                "country": "USA",
                "target_users": "Developers",
                "existing_solutions": "None",
                "pain_points": "High cost"
            }),
            ("Innovation DNA", f"/projects/{project_id}/innovation-dna", {}),
            ("Startup Formation", f"/projects/{project_id}/startup-formation", {}),
            ("Market Intelligence", f"/projects/{project_id}/market-intelligence", {}),
            ("Financial Planner", f"/projects/{project_id}/financial-planner", {}),
            ("Startup Health", f"/projects/{project_id}/generate-health-score", {}),
            ("Investor Hub", f"/projects/{project_id}/investor-hub", {}),
            ("Risk Engine", f"/projects/{project_id}/risk-engine", {}),
            ("Task Planner", f"/projects/{project_id}/task-planner", {}),
            ("AI Mentor", f"/projects/{project_id}/ai-mentor", {})
        ]
        
        results = []
        
        for name, url, payload in endpoints:
            print(f"Testing {name}...")
            r = await client.post(url, json=payload, headers=headers)
            results.append((name, r.status_code))
            print(f"{name}: {r.status_code}")
            
        print("\n--- Verification Results ---")
        for name, code in results:
            print(f"{name}: {'PASS' if code == 200 else 'FAIL (' + str(code) + ')'}")
            
if __name__ == "__main__":
    asyncio.run(run_verification())
