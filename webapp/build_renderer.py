with open("/Users/saikatghosh/.gemini/antigravity/scratch/unseencanada/webapp/app.js", "a") as f:
    f.write("""

  // ═══════════ PHASE 2: DRILLDOWN RENDERING ═══════════
  window.toggleMicroPlace = function(placeId) {
    if (state.visitedPlaces.includes(placeId)) {
        state.visitedPlaces = state.visitedPlaces.filter(id => id !== placeId);
    } else {
        state.visitedPlaces.push(placeId);
    }
    saveState();
    // Re-render current drilldown if active
    const hash = window.location.hash;
    if (hash.startsWith('#province/')) {
        renderProvinceDrilldown(hash.split('/')[1]);
    }
  };

  function renderProvinceDrilldown(provinceId) {
    const p = window.CANADA_DATA.provinces.find(prov => prov.id === provinceId);
    if (!p) return;

    document.getElementById('drilldown-name').textContent = p.name;
    document.getElementById('drilldown-region').textContent = p.region;
    document.getElementById('drilldown-desc').textContent = p.description;

    // Grab the SVG path from the main map to display as a header graphic!
    const svgEl = document.getElementById(p.id);
    const mapContainer = document.getElementById('drilldown-map-container');
    if (svgEl) {
        const bbox = svgEl.getBBox();
        const clone = svgEl.cloneNode(true);
        const theme = window.CANADA_DATA.themes[state.user.themeIndex] || window.CANADA_DATA.themes[0];
        
        // Remove classes and hardcode the fill
        clone.classList.remove('visited');
        clone.style.fill = state.visitedProvinces.includes(p.id) ? theme.primary : '#E5E7EB';
        clone.style.stroke = 'white';
        clone.style.strokeWidth = '2px';
        
        mapContainer.innerHTML = `
            <svg viewBox="${bbox.x - 10} ${bbox.y - 10} ${bbox.width + 20} ${bbox.height + 20}" xmlns="http://www.w3.org/2000/svg">
                ${clone.outerHTML}
            </svg>
        `;
    }

    const renderGrid = (containerId, items) => {
        const container = document.getElementById(containerId);
        if (!items || items.length === 0) {
            container.parentElement.style.display = 'none';
            return 0;
        }
        container.parentElement.style.display = 'block';
        let html = '';
        let visitedCount = 0;
        
        items.forEach(item => {
            const isVisited = state.visitedPlaces.includes(item.id);
            if (isVisited) visitedCount++;
            html += `
                <div class="place-card ${isVisited ? 'visited' : ''}" onclick="toggleMicroPlace('${item.id}')">
                    <div class="place-checkbox"></div>
                    <div class="place-info">
                        <b>${item.name}</b>
                        ${item.highlight ? `<small>${item.highlight}</small>` : ''}
                    </div>
                </div>
            `;
        });
        container.innerHTML = html;
        return { total: items.length, visited: visitedCount };
    };

    const citiesStats = renderGrid('grid-cities', p.cities);
    const parksStats = renderGrid('grid-parks', p.parks);
    const gemsStats = renderGrid('grid-gems', p.hiddenGems);

    const totalPlaces = (citiesStats.total || 0) + (parksStats.total || 0) + (gemsStats.total || 0);
    const totalVisited = (citiesStats.visited || 0) + (parksStats.visited || 0) + (gemsStats.visited || 0);
    
    document.getElementById('drilldown-score').textContent = `${totalVisited} / ${totalPlaces}`;
    
    const pct = totalPlaces === 0 ? 0 : Math.round((totalVisited / totalPlaces) * 100);
    document.getElementById('drilldown-progress-fill').style.width = `${pct}%`;
  }
""")
