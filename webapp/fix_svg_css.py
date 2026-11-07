import re

with open("/Users/saikatghosh/.gemini/antigravity/scratch/unseencanada/webapp/style.css", "r") as f:
    content = f.read()

old_css = r"""\.map-canvas svg \{
  width: 100%;
  max-height: 85vh;
  filter: drop-shadow\(0 10px 15px rgba\(0,0,0,0\.05\)\);
\}"""

new_css = """.map-canvas svg {
  width: 100%;
  height: auto;
  aspect-ratio: 629 / 609;
  max-height: 75vh;
  filter: drop-shadow(0 10px 15px rgba(0,0,0,0.05));
}"""

content = re.sub(old_css, new_css, content)

with open("/Users/saikatghosh/.gemini/antigravity/scratch/unseencanada/webapp/style.css", "w") as f:
    f.write(content)
