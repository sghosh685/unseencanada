import re

with open("/Users/saikatghosh/.gemini/antigravity/scratch/unseencanada/webapp/app.js", "r") as f:
    content = f.read()

# Fix the missing width/height on clonedSvg which causes canvas to render it as 0x0
svg_old = r"""    clonedSvg\.insertBefore\(style, clonedSvg\.firstChild\);

    const canvas = document\.createElement\('canvas'\);"""

svg_new = """    clonedSvg.insertBefore(style, clonedSvg.firstChild);

    // Safari/Chrome canvas rendering requires explicit pixel width/height on the SVG
    clonedSvg.setAttribute('width', '629');
    clonedSvg.setAttribute('height', '609');

    const canvas = document.createElement('canvas');"""

content = re.sub(svg_old, svg_new, content)

with open("/Users/saikatghosh/.gemini/antigravity/scratch/unseencanada/webapp/app.js", "w") as f:
    f.write(content)
