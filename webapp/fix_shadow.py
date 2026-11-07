import re

with open("/Users/saikatghosh/.gemini/antigravity/scratch/unseencanada/webapp/style.css", "r") as f:
    css = f.read()

old_svg_cont = r"""\.svg-container \{
  position: relative;
  height: 100%;
  aspect-ratio: 629 / 609;
  max-width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
\}"""

new_svg_cont = """.svg-container {
  position: relative;
  height: 100%;
  aspect-ratio: 629 / 609;
  max-width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  filter: drop-shadow(0 10px 15px rgba(0,0,0,0.05));
}"""

css = re.sub(old_svg_cont, new_svg_cont, css)

with open("/Users/saikatghosh/.gemini/antigravity/scratch/unseencanada/webapp/style.css", "w") as f:
    f.write(css)
