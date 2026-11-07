with open("/Users/saikatghosh/.gemini/antigravity/scratch/unseencanada/webapp/app.js", "r") as f:
    content = f.read()

content = content.replace("const statProv = document.getElementById('stat-provinces');\n    if (statProv) statProv.textContent = visited;", "const statProv = document.getElementById('stat-provinces');\n    if (statProv) statProv.textContent = visited;\n    const heroCount = document.getElementById('hero-count');\n    if (heroCount) heroCount.textContent = visited;")

with open("/Users/saikatghosh/.gemini/antigravity/scratch/unseencanada/webapp/app.js", "w") as f:
    f.write(content)
