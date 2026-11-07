import re

with open("/Users/saikatghosh/.gemini/antigravity/scratch/unseencanada/webapp/style.css", "r") as f:
    content = f.read()

old_canvas = r"""\.map-canvas \{
  width: 100%;
  position: relative;
  display: block;
\}"""

new_canvas = """.map-canvas {
  width: 100%;
  position: relative;
  display: block;
  padding-bottom: 96.82%; /* 609 / 629 * 100% */
}"""

content = re.sub(old_canvas, new_canvas, content)

old_svg = r"""\.map-canvas svg \{
  width: 100%;
  height: auto;
  aspect-ratio: 629 / 609;
  max-height: 75vh;
  filter: drop-shadow\(0 10px 15px rgba\(0,0,0,0\.05\)\);
\}"""

new_svg = """.map-canvas svg {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  filter: drop-shadow(0 10px 15px rgba(0,0,0,0.05));
}"""

content = re.sub(old_svg, new_svg, content)

with open("/Users/saikatghosh/.gemini/antigravity/scratch/unseencanada/webapp/style.css", "w") as f:
    f.write(content)

with open("/Users/saikatghosh/.gemini/antigravity/scratch/unseencanada/webapp/app.js", "r") as f:
    js_content = f.read()

# Fix BOTH getBBox calls
old_bbox = r"""                const bbox = el\.getBBox\(\);
                let cx = bbox\.x \+ bbox\.width / 2;
                let cy = bbox\.y \+ bbox\.height / 2;"""

new_bbox = """                const bbox = el.getBBox();
                if (bbox.width === 0 && bbox.height === 0) throw new Error("Zero BBox");
                let cx = bbox.x + bbox.width / 2;
                let cy = bbox.y + bbox.height / 2;"""

js_content = re.sub(old_bbox, new_bbox, js_content)

with open("/Users/saikatghosh/.gemini/antigravity/scratch/unseencanada/webapp/app.js", "w") as f:
    f.write(js_content)
