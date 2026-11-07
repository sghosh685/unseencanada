import re

with open("/Users/saikatghosh/.gemini/antigravity/scratch/unseencanada/webapp/index.html", "r") as f:
    html = f.read()

# 1. Add the view-province skeleton
province_view = """
        <!-- ═══════════ PHASE 2: PROVINCE DRILL-DOWN VIEW ═══════════ -->
        <div id="view-province" class="view">
            <div class="province-drilldown-layout">
                <header class="drilldown-header">
                    <button class="btn btn-outline" onclick="window.location.hash='#map'">
                        ← Back to Canada
                    </button>
                    <div class="drilldown-title">
                        <h1 id="drilldown-name">Province Name</h1>
                        <span class="badge" id="drilldown-region">Region</span>
                    </div>
                    <div class="drilldown-progress">
                        <div class="progress-text">Explored: <b id="drilldown-score">0 / 0</b> places</div>
                        <div class="progress-bar"><div class="progress-fill" id="drilldown-progress-fill"></div></div>
                    </div>
                </header>

                <div class="drilldown-content">
                    <aside class="drilldown-sidebar card">
                        <div class="map-placeholder" id="drilldown-map-container">
                            <!-- We will clone the province SVG path here for visual flair -->
                        </div>
                        <p id="drilldown-desc" class="muted-text"></p>
                    </aside>

                    <div class="drilldown-grids">
                        <section class="place-section">
                            <h3>Cities & Regions</h3>
                            <div class="place-grid" id="grid-cities"></div>
                        </section>
                        <section class="place-section">
                            <h3>National & Provincial Parks</h3>
                            <div class="place-grid" id="grid-parks"></div>
                        </section>
                        <section class="place-section">
                            <h3>Hidden Gems</h3>
                            <div class="place-grid" id="grid-gems"></div>
                        </section>
                    </div>
                </div>
            </div>
        </div>
"""

# Insert it before view-explore
html = html.replace('<!-- ═══════════ EXPLORE VIEW', province_view + '\n        <!-- ═══════════ EXPLORE VIEW')

with open("/Users/saikatghosh/.gemini/antigravity/scratch/unseencanada/webapp/index.html", "w") as f:
    f.write(html)

with open("/Users/saikatghosh/.gemini/antigravity/scratch/unseencanada/webapp/style.css", "a") as f:
    f.write("""
/* Phase 2 Drilldown Styles */
.province-drilldown-layout {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.drilldown-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  background: var(--surface);
  padding: 1.5rem 2rem;
  border-radius: var(--radius);
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--line);
}

.drilldown-title h1 {
  margin: 0;
  font-size: 2rem;
  font-weight: 800;
  color: var(--ink);
}

.drilldown-progress {
  width: 200px;
}

.drilldown-content {
  display: grid;
  grid-template-columns: 350px 1fr;
  gap: 2rem;
}

@media (max-width: 900px) {
  .drilldown-content {
    grid-template-columns: 1fr;
  }
  .drilldown-header {
    flex-direction: column;
    align-items: flex-start;
  }
}

.map-placeholder {
  background: var(--brand-bg);
  border-radius: var(--radius-sm);
  padding: 2rem;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 1.5rem;
  min-height: 250px;
}

.map-placeholder svg {
  max-width: 100%;
  max-height: 200px;
  filter: drop-shadow(0 4px 6px rgba(0,0,0,0.1));
}

.place-section {
  margin-bottom: 2.5rem;
}

.place-section h3 {
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid var(--line);
}

.place-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 1rem;
}

.place-card {
  background: var(--surface);
  border: 1px solid var(--line);
  padding: 1rem;
  border-radius: var(--radius-sm);
  cursor: pointer;
  transition: var(--transition);
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
}

.place-card:hover {
  border-color: var(--brand);
  transform: translateY(-2px);
  box-shadow: var(--shadow);
}

.place-card.visited {
  background: var(--brand-bg);
  border-color: var(--brand);
}

.place-checkbox {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  border: 2px solid var(--muted);
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
}

.place-card.visited .place-checkbox {
  background: var(--brand);
  border-color: var(--brand);
}

.place-card.visited .place-checkbox::after {
  content: '✓';
  color: white;
  font-size: 12px;
  font-weight: bold;
}

.place-info b {
  display: block;
  font-size: 0.95rem;
  color: var(--ink);
  margin-bottom: 0.25rem;
}

.place-info small {
  display: block;
  font-size: 0.8rem;
  color: var(--muted);
  line-height: 1.3;
}
""")
