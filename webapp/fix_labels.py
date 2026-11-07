import re

with open("/Users/saikatghosh/.gemini/antigravity/scratch/unseencanada/webapp/index.html", "r") as f:
    content = f.read()

# First remove ALL instances
content = content.replace("<div id=\"map-labels\"></div>", "")
content = content.replace("                            \n", "") # cleanup empty lines

# Now carefully put it only after the canada-map SVG
content = content.replace('<svg id="canada-map"', 'PLACEHOLDER_CANADA_MAP')
content = content.replace('</svg>', '</svg>\n')
content = content.replace('PLACEHOLDER_CANADA_MAP', '<svg id="canada-map"')

# Find the canada-map SVG end
def replace_func(m):
    return m.group(0) + '\n                            <div id="map-labels"></div>\n'

content = re.sub(r'(<svg id="canada-map".*?</svg>)', replace_func, content, flags=re.DOTALL)

with open("/Users/saikatghosh/.gemini/antigravity/scratch/unseencanada/webapp/index.html", "w") as f:
    f.write(content)
