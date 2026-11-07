import re

with open("/Users/saikatghosh/.gemini/antigravity/scratch/unseencanada/webapp/style.css", "r") as f:
    content = f.read()

old_canvas_css = r"""\.map-canvas \{
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
\}"""

new_canvas_css = """.map-canvas {
  width: 100%;
  position: relative;
  display: block;
}"""

content = re.sub(old_canvas_css, new_canvas_css, content)

with open("/Users/saikatghosh/.gemini/antigravity/scratch/unseencanada/webapp/style.css", "w") as f:
    f.write(content)
