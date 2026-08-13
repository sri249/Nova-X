import os

base_dir = r"c:\Users\SRI VIDHYA ALAPATI\OneDrive\Desktop\nova\frontend\src\app\(dashboard)\projects\[id]"

for root, _, files in os.walk(base_dir):
    for filename in files:
        if filename == "page.tsx":
            file = os.path.join(root, filename)
            with open(file, "r", encoding="utf-8") as f:
                content = f.read()
                
            if "console.error(err);" in content:
                new_content = content.replace("console.error(err);", "if (err?.response?.status !== 404) console.error(err);")
                with open(file, "w", encoding="utf-8") as f:
                    f.write(new_content)
                print(f"Patched: {file}")
