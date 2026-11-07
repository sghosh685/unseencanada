import re

with open("/Users/saikatghosh/.gemini/antigravity/scratch/unseencanada/webapp/index.html", "r") as f:
    content = f.read()

# Wrap svg and map-labels in a new relative container that scales
old_html = r"""<svg id="canada-map" width="100%" height="100%" viewBox="0 0 629 609" xmlns="http://www.w3.org/2000/svg">"""
new_html = """<div class="svg-container">
<svg id="canada-map" width="100%" height="100%" viewBox="0 0 629 609" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMidYMid meet">"""

content = content.replace(old_html, new_html)

old_html2 = r"""<div id="map-labels"></div>"""
new_html2 = """<div id="map-labels"></div>
</div>"""

content = content.replace(old_html2, new_html2)

with open("/Users/saikatghosh/.gemini/antigravity/scratch/unseencanada/webapp/index.html", "w") as f:
    f.write(content)

with open("/Users/saikatghosh/.gemini/antigravity/scratch/unseencanada/webapp/style.css", "r") as f:
    css = f.read()

# Update CSS for the new wrapper
old_canvas = r"""\.map-canvas \{
  width: 100%;
  height: 500px;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
\}"""

new_canvas = """.map-canvas {
  width: 100%;
  height: 500px; /* Force a robust height so it doesn't collapse in Safari */
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
}

.svg-container {
  position: relative;
  height: 100%;
  aspect-ratio: 629 / 609;
  max-width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}"""

css = re.sub(old_canvas, new_canvas, css)

# Make sure SVG and labels fill the new container exactly
old_svg = r"""\.map-canvas svg \{
  width: 100%;
  height: 100%;
  display: block;
  /\* Safari bug: drop-shadow on SVG can cause it to disappear \*/
  /\* filter: drop-shadow\(0 10px 15px rgba\(0,0,0,0\.05\)\); \*/
\}"""

new_svg = """.map-canvas svg {
  position: absolute;
  top: 0; left: 0;
  width: 100%;
  height: 100%;
  display: block;
}"""

css = re.sub(old_svg, new_svg, css)

with open("/Users/saikatghosh/.gemini/antigravity/scratch/unseencanada/webapp/style.css", "w") as f:
    f.write(css)
