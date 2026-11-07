with open("/Users/saikatghosh/.gemini/antigravity/scratch/unseencanada/webapp/app.js", "r") as f:
    content = f.read()

region_logic = """
    const regionsContainer = document.getElementById('regions-grid');
    if (regionsContainer && window.CANADA_DATA && window.CANADA_DATA.regions) {
      let html = '';
      window.CANADA_DATA.regions.forEach(reg => {
        const visitedInRegion = reg.provinceIds.filter(id => state.visitedProvinces.includes(id)).length;
        const total = reg.provinceIds.length;
        const isComplete = visitedInRegion === total;
        html += `
          <div class="region-card ${isComplete ? 'complete' : ''}">
            <div class="region-icon">${reg.icon || '🗺️'}</div>
            <div class="region-info">
              <h4>${reg.name}</h4>
              <span>${visitedInRegion} / ${total} provinces</span>
            </div>
          </div>
        `;
      });
      regionsContainer.innerHTML = html;
    }
  }

  function checkAchievements() {
"""

content = content.replace("  }\n\n  function checkAchievements() {", region_logic)

with open("/Users/saikatghosh/.gemini/antigravity/scratch/unseencanada/webapp/app.js", "w") as f:
    f.write(content)
