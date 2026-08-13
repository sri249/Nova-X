import uuid

import httpx

API_URL = "http://localhost:8000"
client = httpx.Client(base_url=API_URL, timeout=30.0)

print("Starting E2E API Verification...")

# 1. Health Check
res = client.get("/health")
assert res.status_code == 200
print("✅ Backend Health Check")

# 2. Register User
unique_email = f"ecofarm_{uuid.uuid4().hex[:8]}@novax.ai"
res = client.post("/auth/register", json={
    "full_name": "EcoFarm Founder",
    "email": unique_email,
    "password": "Password123!"
})
if res.status_code != 200 and res.status_code != 201:
    print("❌ Registration Failed:", res.text)
else:
    print("✅ Registration")

# 3. Login
res = client.post("/auth/login", json={
    "email": unique_email,
    "password": "Password123!"
})
if res.status_code != 200:
    print("❌ Login Failed:", res.text)
    import sys
    sys.exit(1)
token = res.json()["access_token"]
print("✅ Login")
client.headers.update({"Authorization": f"Bearer {token}"})

# 4. Create Project
project_data = {
    "name": "EcoFarm AI",
    "description": "AI-powered precision agriculture platform helping farmers make better crop, soil, irrigation, disease, and market decisions.",
    "industry": "Agriculture",
    "country": "India",
    "target_users": "Small and medium-scale farmers",
    "problem": "Farmers often make crop, fertilizer, irrigation, and selling decisions without personalized agricultural insights.",
    "pain_points": "Unpredictable weather, rising input costs, lack of expert advice, poor market information, and late disease detection."
}
res = client.post("/projects", json=project_data)
if res.status_code not in (200, 201):
    print("❌ Project Creation Failed:", res.text)
    import sys
    sys.exit(1)
project_id = res.json()["id"]
print(f"✅ Project Creation (ID: {project_id})")

# Modules to test sequentially
modules = [
    ("problem-discovery", "/projects/{id}/problem-discovery"),
    ("innovation-dna", "/projects/{id}/innovation-dna"),
    ("startup-formation", "/projects/{id}/startup-formation"),
    ("market-intelligence", "/projects/{id}/market-intelligence"),
    ("financial-planner", "/projects/{id}/financial-planner"),
    ("investor-hub", "/projects/{id}/investor-hub"),
    ("risk-engine", "/projects/{id}/risk-engine"),
    ("task-planner", "/projects/{id}/task-planner")
]

for name, url_template in modules:
    url = url_template.format(id=project_id)
    print(f"Testing {name}...")
    # Generate
    payload = {}
    if name == "problem-discovery":
        payload = {
            "title": project_data["name"],
            "description": project_data["description"],
            "industry": project_data["industry"],
            "country": project_data["country"],
            "target_users": project_data["target_users"],
            "existing_solutions": "None currently",
            "pain_points": project_data["pain_points"]
        }
    res = client.post(url, json=payload)
    if res.status_code != 200:
        print(f"❌ {name} Generation Failed:", res.status_code, res.text)
        continue
    # Verify GET
    res = client.get(url)
    if res.status_code != 200:
        print(f"❌ {name} Fetch Failed:", res.status_code, res.text)
    else:
        print(f"✅ {name} Verified")

# Test AI Co-Founder Chat
res = client.post(f"/projects/{project_id}/chat", json={
    "message": "What are the biggest risks for EcoFarm AI?",
    "session_id": "demo-session-1"
})
if res.status_code == 200:
    print("✅ Chat API")
else:
    print("❌ Chat API Failed:", res.text)

# Project Health
res = client.post(f"/projects/{project_id}/generate-health-score")
if res.status_code == 200:
    res = client.get(f"/projects/{project_id}/health")
    if res.status_code == 200:
        print("✅ Startup Health API:", res.json())
    else:
        print("❌ Startup Health API Fetch Failed:", res.text)
else:
    print("❌ Startup Health API Generate Failed:", res.text)

print("E2E API Verification Complete.")
