import re

with open("/Users/saikatghosh/.gemini/antigravity/scratch/unseencanada/webapp/app.js", "r") as f:
    js = f.read()

# In generateImage, it uses: const el = clonedSvg.querySelector(`#${p.id}`);
# We should change it to use the real DOM element!
old_query = r"""const el = clonedSvg\.querySelector\(`#\$\{p\.id\}`\);"""
new_query = """const el = document.getElementById(p.id); // Use real DOM element for accurate getBBox"""

js = re.sub(old_query, new_query, js)

with open("/Users/saikatghosh/.gemini/antigravity/scratch/unseencanada/webapp/app.js", "w") as f:
    f.write(js)
