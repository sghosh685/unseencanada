import re

with open("/Users/saikatghosh/.gemini/antigravity/scratch/unseencanada/webapp/index.html", "r") as f:
    content = f.read()

m = re.search(r'(<svg id="canada-map".*?</svg>)', content, flags=re.DOTALL)
if m:
    with open("/Users/saikatghosh/.gemini/antigravity/scratch/unseencanada/webapp/extracted.svg", "w") as f:
        f.write(m.group(1))
    print(f"Extracted SVG, length: {len(m.group(1))}")
else:
    print("NO SVG FOUND!")
