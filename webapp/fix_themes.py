import re

with open("/Users/saikatghosh/.gemini/antigravity/scratch/unseencanada/webapp/index.html", "r") as f:
    content = f.read()

# The one inside map-controls is inside `<div class="theme-section">`
map_controls_theme_regex = r'<div class="theme-section">\s*<span class="theme-label">Theme</span>\s*<div class="theme-swatches" id="stage-themes">\s*<!-- Populated by JS -->\s*</div>\s*</div>'

content = re.sub(map_controls_theme_regex, '', content)

with open("/Users/saikatghosh/.gemini/antigravity/scratch/unseencanada/webapp/index.html", "w") as f:
    f.write(content)
