import re

with open("/Users/saikatghosh/.gemini/antigravity/scratch/unseencanada/webapp/index.html", "r") as f:
    content = f.read()

content = content.replace("</svg>", "</svg>\n                            <div id=\"map-labels\"></div>")

with open("/Users/saikatghosh/.gemini/antigravity/scratch/unseencanada/webapp/index.html", "w") as f:
    f.write(content)
