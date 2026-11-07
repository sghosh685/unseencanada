import re

with open("/Users/saikatghosh/.gemini/antigravity/scratch/unseencanada/webapp/style.css", "r") as f:
    content = f.read()

old_svg = r"""\.map-canvas svg \{
  width: 100%;
  height: 100%;
  display: block;
  filter: drop-shadow\(0 10px 15px rgba\(0,0,0,0\.05\)\);
\}"""

new_svg = """.map-canvas svg {
  width: 100%;
  height: 100%;
  display: block;
  /* Safari bug: drop-shadow on SVG can cause it to disappear */
  /* filter: drop-shadow(0 10px 15px rgba(0,0,0,0.05)); */
}"""

content = re.sub(old_svg, new_svg, content)

with open("/Users/saikatghosh/.gemini/antigravity/scratch/unseencanada/webapp/style.css", "w") as f:
    f.write(content)
