import re

with open("/Users/saikatghosh/.gemini/antigravity/scratch/unseencanada/webapp/index.html", "r") as f:
    content = f.read()

# Replace the stage-header and everything above the map-canvas
stage_replacement = """
                    <div class="map-stage card" id="map-stage-card">
                        <div class="stage-branding">
                            <div class="stage-user-info">
                                <img id="stage-avatar" src="" alt="Avatar" style="display:none;">
                                <h2 id="stage-name">My Canada</h2>
                            </div>
                            <div class="stage-score">
                                <span id="stage-count">0</span><span class="stage-total">/13</span>
                            </div>
                        </div>

                        <div class="map-controls">
                            <label class="toggle-checkbox">
                                <input type="checkbox" id="toggle-names" checked>
                                Show province names
                            </label>
                            <div class="theme-section">
                                <span class="theme-label">Theme</span>
                                <div class="theme-swatches" id="stage-themes">
                                    <!-- Populated by JS -->
                                </div>
                            </div>
                        </div>

                        <div class="map-canvas" id="map-wrapper" style="position: relative;">
"""

content = re.sub(r'<div class="map-stage card">.*?<div class="map-canvas" id="map-wrapper">', stage_replacement, content, flags=re.DOTALL)

with open("/Users/saikatghosh/.gemini/antigravity/scratch/unseencanada/webapp/index.html", "w") as f:
    f.write(content)
