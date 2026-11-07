import re

with open("/Users/saikatghosh/.gemini/antigravity/scratch/unseencanada/webapp/app.js", "r") as f:
    content = f.read()

# 1. Update updateMapUI to toggle label visibility
update_map_ui_old = """  function updateMapUI() {
    const svgMap = document.getElementById('canada-map');
    if (!svgMap) return;

    window.CANADA_DATA.provinces.forEach(p => {
      const el = document.getElementById(p.id);
      if (el) {
        if (state.visitedProvinces.includes(p.id)) {
          el.classList.add('visited');
        } else {
          el.classList.remove('visited');
        }
      }
    });
  }"""

update_map_ui_new = """  function updateMapUI() {
    const svgMap = document.getElementById('canada-map');
    if (!svgMap) return;

    const showNames = document.getElementById('toggle-names')?.checked !== false;

    window.CANADA_DATA.provinces.forEach(p => {
      const el = document.getElementById(p.id);
      const label = document.getElementById(`label-${p.id}`);
      
      if (el) {
        if (state.visitedProvinces.includes(p.id)) {
          el.classList.add('visited');
          if (label && showNames) label.classList.add('show');
          else if (label) label.classList.remove('show');
        } else {
          el.classList.remove('visited');
          if (label) label.classList.remove('show');
        }
      }
    });
  }"""

content = content.replace(update_map_ui_old, update_map_ui_new)

# 2. Add createLabels logic to setupMap
setup_map_old = """    svgMap.addEventListener('click', (e) => {"""

setup_map_new = """    // Create Labels
    const container = document.getElementById('map-labels');
    if (container) {
      container.innerHTML = '';
      const viewBoxStr = svgMap.getAttribute('viewBox') || "0 0 629 609";
      const [,,vw, vh] = viewBoxStr.split(' ').map(Number);

      window.CANADA_DATA.provinces.forEach(p => {
        const el = document.getElementById(p.id);
        if (!el) return;
        try {
            const bbox = el.getBBox();
            let cx = bbox.x + bbox.width / 2;
            let cy = bbox.y + bbox.height / 2;
            
            // Tweaks for visual center
            if (p.id === 'CA-NU') { cx -= 60; cy += 60; }
            if (p.id === 'CA-BC') { cx += 20; cy -= 20; }
            if (p.id === 'CA-ON') { cy += 50; cx += 10; }
            if (p.id === 'CA-QC') { cx -= 30; cy += 50; }
            if (p.id === 'CA-NL') { cx += 60; cy += 40; }
            if (p.id === 'CA-PE') { cy -= 5; cx += 15; }
            if (p.id === 'CA-NS') { cx += 20; cy += 10; }
            if (p.id === 'CA-NT') { cx += 20; cy -= 10; }

            const leftPct = (cx / vw) * 100;
            const topPct = (cy / vh) * 100;

            const label = document.createElement('div');
            label.className = 'province-label';
            label.id = `label-${p.id}`;
            label.style.left = `${leftPct}%`;
            label.style.top = `${topPct}%`;
            label.textContent = p.name;
            container.appendChild(label);
        } catch (e) {
            // getBBox might fail if svg is display:none
        }
      });
    }

    document.getElementById('toggle-names')?.addEventListener('change', updateMapUI);

    svgMap.addEventListener('click', (e) => {"""

content = content.replace(setup_map_old, setup_map_new)

# 3. Update renderAll to update stage branding
render_all_old = """    const nextAdvInput = document.getElementById('sidebar-next-adventure');
    if (nextAdvInput && nextAdvInput.value !== state.user.nextAdventure) {
      nextAdvInput.value = state.user.nextAdventure || '';
    }"""

render_all_new = """    const nextAdvInput = document.getElementById('sidebar-next-adventure');
    if (nextAdvInput && nextAdvInput.value !== state.user.nextAdventure) {
      nextAdvInput.value = state.user.nextAdventure || '';
    }
    
    // Update Stage Branding
    const stageName = document.getElementById('stage-name');
    if (stageName) {
      stageName.textContent = state.user.name ? `${state.user.name}'s Canada` : 'My Canada';
    }
    const stageAvatar = document.getElementById('stage-avatar');
    if (stageAvatar) {
      if (state.user.photo) {
        stageAvatar.src = state.user.photo;
        stageAvatar.style.display = 'block';
      } else {
        stageAvatar.style.display = 'none';
      }
    }
    const stageCount = document.getElementById('stage-count');
    if (stageCount) stageCount.textContent = state.visitedProvinces.length;"""

content = content.replace(render_all_old, render_all_new)

with open("/Users/saikatghosh/.gemini/antigravity/scratch/unseencanada/webapp/app.js", "w") as f:
    f.write(content)
