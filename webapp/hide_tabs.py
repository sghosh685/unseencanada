import re

with open("/Users/saikatghosh/.gemini/antigravity/scratch/unseencanada/webapp/index.html", "r") as f:
    content = f.read()

# Hide the tabs
content = content.replace('<button class="nav-tab" data-view="explore">Explore</button>', '<!-- <button class="nav-tab" data-view="explore">Explore</button> -->')
content = content.replace('<button class="nav-tab" data-view="stats">Stats</button>', '<!-- <button class="nav-tab" data-view="stats">Stats</button> -->')

with open("/Users/saikatghosh/.gemini/antigravity/scratch/unseencanada/webapp/index.html", "w") as f:
    f.write(content)
