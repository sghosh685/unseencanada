import re

with open("/Users/saikatghosh/.gemini/antigravity/scratch/unseencanada/webapp/style.css", "r") as f:
    content = f.read()

old_canvas = r"""\.map-canvas \{
  width: 100%;
  position: relative;
  display: block;
  padding-bottom: 96\.82%; /\* 609 / 629 \* 100% \*/
\}"""

new_canvas = """.map-canvas {
  width: 100%;
  height: 500px;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
}"""

content = re.sub(old_canvas, new_canvas, content)

old_svg = r"""\.map-canvas svg \{
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  filter: drop-shadow\(0 10px 15px rgba\(0,0,0,0\.05\)\);
\}"""

new_svg = """.map-canvas svg {
  width: 100%;
  height: 100%;
  display: block;
  filter: drop-shadow(0 10px 15px rgba(0,0,0,0.05));
}"""

content = re.sub(old_svg, new_svg, content)

with open("/Users/saikatghosh/.gemini/antigravity/scratch/unseencanada/webapp/style.css", "w") as f:
    f.write(content)
