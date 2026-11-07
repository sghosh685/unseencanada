import re

with open("/Users/saikatghosh/.gemini/antigravity/scratch/unseencanada/webapp/index.html", "r") as f:
    content = f.read()

# 1. Add Google Fonts (Inter)
if "fonts.googleapis.com" not in content:
    content = content.replace("</title>", "</title>\n    <link href=\"https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap\" rel=\"stylesheet\">")

# 2. Move Personalization to Top of Map
sidebar_personalize_regex = r'<div class="sidebar-personalize">.*?</div>\s*</div>\s*</aside>'
# We will just remove the whole sidebar-actions and personalize from sidebar,
# and put a new clean inputs row above the map.

def replace_sidebar(m):
    return "</aside>"

content = re.sub(r'<div class="sidebar-personalize">.*?</aside>', replace_sidebar, content, flags=re.DOTALL)

# Now, we rewrite the map column
map_column_old = r'<!-- Map Stage -->.*?<div class="map-stage card" id="map-stage-card">'

map_column_new = """<!-- Map Stage -->
                <div class="main-content">
                    <!-- Personalization Row -->
                    <div class="personalize-bar card">
                        <div class="input-group">
                            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
                            <input type="text" id="sidebar-name" placeholder="Your Name" value="">
                        </div>
                        <div class="input-group">
                            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"/><circle cx="8.5" cy="8.5" r="1.5"/><polyline points="21 15 16 10 5 21"/></svg>
                            <label for="sidebar-photo" class="photo-upload-label">Add Photo</label>
                            <input type="file" id="sidebar-photo" accept="image/*" style="display:none;">
                        </div>
                        <div class="input-group">
                            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>
                            <input type="text" id="sidebar-next-adventure" placeholder="Next Adventure?" value="">
                        </div>
                        <div class="theme-section">
                            <div class="theme-swatches" id="stage-themes">
                                <!-- Populated by JS -->
                            </div>
                        </div>
                    </div>

                    <!-- Map Card -->
                    <div class="map-stage card" id="map-stage-card">"""

content = re.sub(map_column_old, map_column_new, content, flags=re.DOTALL)

# 3. Add Download Buttons below the map wrapper
map_wrapper_regex = r'(<div class="map-canvas" id="map-wrapper" style="position: relative;">.*?</svg>\n                            <div id="map-labels"></div>\n\n\n                    </div>)'

map_wrapper_new = r"""\1
                    
                    <div class="card-footer-progress">
                        <div class="progress-bar-wrapper">
                            <div class="progress-info">
                                <span id="progress-text-card">0% of Canada explored</span>
                                <span class="brand-tag">MyCanada.com</span>
                            </div>
                            <div class="progress-bar"><div class="progress-fill" id="progress-fill-card"></div></div>
                        </div>
                    </div>
                </div> <!-- End Map Stage Card -->
                
                <div class="download-actions">
                    <h3>Download Your Map</h3>
                    <div class="download-buttons">
                        <button class="btn btn-outline" id="download-btn-png">↓ PNG</button>
                        <button class="btn btn-outline" id="download-btn-jpg">↓ JPG</button>
                        <button class="btn btn-outline" id="share-btn">Share Link</button>
                    </div>
                </div>
            </div> <!-- End Main Content -->"""

content = re.sub(map_wrapper_regex, map_wrapper_new, content, flags=re.DOTALL)


with open("/Users/saikatghosh/.gemini/antigravity/scratch/unseencanada/webapp/index.html", "w") as f:
    f.write(content)
