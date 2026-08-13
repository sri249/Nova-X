import asyncio
import logging

import httpx
import pytest

from app.main import app


@pytest.mark.asyncio
async def test_workflow():
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        print("1. Register User")
        # Try registering, ignore if already registered
        try:
            reg_res = await client.post("/auth/register", json={
                "email": "testuser_phase3@example.com",
                "password": "Password123!",
                "full_name": "Test User Phase 3"
            })
            print("Register:", reg_res.status_code)
        except httpx.RequestError as e:
            logger = logging.getLogger(__name__)
            logger.warning("Registration error: %s", e)

        print("2. Login User")
        login_res = await client.post("/auth/login", json={
            "email": "testuser_phase3@example.com",
            "password": "Password123!"
        })
        print("Login:", login_res.status_code)
        if login_res.status_code != 200:
            print(login_res.json())
            return
        token = login_res.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        print("3. Create Project")
        proj_res = await client.post("/projects", json={
            "name": "Phase 3 Test Project",
            "description": "Testing the AI Startup workflow end-to-end."
        }, headers=headers)
        print("Create Project:", proj_res.status_code)
        if proj_res.status_code not in (200, 201):
            print(proj_res.json())
            return
        project_id = proj_res.json()["id"]

        print("4. Problem Discovery")
        pd_res = await client.post(f"/projects/{project_id}/problem-discovery", json={
            "title": "Ocean Pollution",
            "description": "Too much plastic in the oceans.",
            "industry": "Environment",
            "country": "Global",
            "target_users": "Environmentalists",
            "existing_solutions": "Recycling",
            "pain_points": "High cost of collection"
        }, headers=headers)
        print("Problem Discovery:", pd_res.status_code)
        if pd_res.status_code != 200:
            print(pd_res.json())
            return

        print("5. Innovation DNA")
        dna_res = await client.post(f"/projects/{project_id}/innovation-dna", headers=headers)
        print("Innovation DNA:", dna_res.status_code)
        if dna_res.status_code != 200:
            print(dna_res.json())
            return

        print("6. Startup Formation")
        sf_res = await client.post(f"/projects/{project_id}/startup-formation", headers=headers)
        print("Startup Formation:", sf_res.status_code)
        if sf_res.status_code != 200:
            print(sf_res.json())
            return
        
        print("Workflow Completed Successfully! Data saved in DB.")
        print("Startup Generated:", sf_res.json()["profile"]["name"])

if __name__ == "__main__":
    asyncio.run(test_workflow())
