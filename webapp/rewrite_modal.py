import re

with open("/Users/saikatghosh/.gemini/antigravity/scratch/unseencanada/webapp/app.js", "r") as f:
    content = f.read()

new_modal_logic = """
    const modal = document.getElementById('province-modal');
    if (!modal) return;

    const isVisited = state.visitedProvinces.includes(id);
    
    // Header
    document.getElementById('modal-header').innerHTML = `
      <h2 id="modal-title">${p.name}</h2>
      <div class="modal-badges">
        <span class="badge region-badge">${p.region}</span>
      </div>
    `;
    
    // Format complex arrays
    const formatList = (arr) => arr ? arr.map(item => `
      <div class="list-item">
        <span class="list-bullet">•</span>
        <div class="list-text">
          <b>${item.name || item}</b>
          ${item.highlight ? `<span> - ${item.highlight}</span>` : ''}
        </div>
      </div>
    `).join('') : '';

    // Body
    document.getElementById('modal-body').innerHTML = `
      <div class="province-detail">
        <p class="desc-lead">${p.description}</p>
        
        <div class="detail-facts">
          <div class="fact-chip">🏛️ Capital: ${p.capital}</div>
          <div class="fact-chip">👥 Pop: ${p.population}</div>
          <div class="fact-chip">📏 Area: ${p.area}</div>
        </div>

        ${p.famousFor ? `
        <div class="detail-section">
          <h3>Famous For</h3>
          <div class="detail-tags">
            ${p.famousFor.map(f => `<span class="tag">${f}</span>`).join('')}
          </div>
        </div>
        ` : ''}
        
        ${p.cities && p.cities.length > 0 ? `
        <div class="detail-section">
          <h3>Top Cities to Visit</h3>
          <div class="detail-list">${formatList(p.cities)}</div>
        </div>
        ` : ''}
        
        ${p.parks && p.parks.length > 0 ? `
        <div class="detail-section">
          <h3>National Parks</h3>
          <div class="detail-list">${formatList(p.parks)}</div>
        </div>
        ` : ''}
        
        ${p.hiddenGems && p.hiddenGems.length > 0 ? `
        <div class="detail-section">
          <h3>Hidden Gems</h3>
          <div class="detail-list">${formatList(p.hiddenGems)}</div>
        </div>
        ` : ''}
      </div>
    `;

    // Footer
    document.getElementById('modal-footer').innerHTML = `
      <button class="btn ${isVisited ? 'btn-outline' : 'btn-primary'}" id="modal-toggle-visited" data-id="${p.id}">
        ${isVisited ? 'Mark as Unvisited' : 'Mark as Visited'}
      </button>
    `;

    // Re-bind click event for the dynamically created button
    document.getElementById('modal-toggle-visited').addEventListener('click', (e) => {
      toggleProvince(e.target.dataset.id);
      openProvinceModal(e.target.dataset.id); // Refresh modal to show updated state
    });

    modal.classList.add('show');
    modal.removeAttribute('hidden');
"""

# Replace from "const modal = document.getElementById('province-modal');" to "modal.removeAttribute('hidden');"
pattern = re.compile(r"const modal = document\.getElementById\('province-modal'\);.*?modal\.removeAttribute\('hidden'\);", re.DOTALL)
content = pattern.sub(new_modal_logic.strip(), content)

with open("/Users/saikatghosh/.gemini/antigravity/scratch/unseencanada/webapp/app.js", "w") as f:
    f.write(content)
