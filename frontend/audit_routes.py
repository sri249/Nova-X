import os

target_routes = [
    "/",
    "/login",
    "/register",
    "/dashboard",
    "/projects",
    "/projects/create",
    "/projects/[id]",
    "/projects/[id]/overview",
    "/projects/[id]/problem-discovery",
    "/projects/[id]/innovation-dna",
    "/projects/[id]/startup-formation",
    "/projects/[id]/market-intelligence",
    "/projects/[id]/financial-planner",
    "/projects/[id]/investor-hub",
    "/projects/[id]/risks-tasks",
    "/projects/[id]/chat",
    "/projects/[id]/settings",
    "/projects/[id]/export"
]

base_dir = r"c:\Users\SRI VIDHYA ALAPATI\OneDrive\Desktop\nova\frontend\src\app"

print("Route Audit:")
for route in target_routes:
    # Build possible file paths based on App Router rules (ignoring route groups)
    route_parts = [p for p in route.split("/") if p]
    
    # We will just do a simple search matching the route pattern in the directory tree
    found = False
    for root, dirs, files in os.walk(base_dir):
        rel_path = os.path.relpath(root, base_dir)
        # normalize to generic route format
        generic_route = "/" + rel_path.replace("\\", "/").replace("(auth)/", "").replace("(dashboard)/", "").replace(".", "")
        if generic_route == "/":
            generic_route = "/"
        elif generic_route.endswith("/"):
            generic_route = generic_route[:-1]
            
        if generic_route == route or (generic_route == "/" and route == "/"):
            if "page.tsx" in files:
                found = True
                break
                
    if found:
        print(f"[OK] {route}")
    else:
        print(f"[MISSING] {route}")
