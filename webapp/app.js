(function() {
  // 1. STATE MANAGEMENT
  const DEFAULT_STATE = {
    user: { name: '', photo: null, nextAdventure: '', themeIndex: 0, createdAt: Date.now() },
    visitedProvinces: [],
    unlockedAchievements: [],
    visitedPlaces: []
  };

  let state = { ...DEFAULT_STATE };

  function loadState() {
    try {
      const saved = localStorage.getItem('my-canada-state');
      if (saved) {
        state = JSON.parse(saved);
        // Migration
        if (!state.user) state.user = { ...DEFAULT_STATE.user };
        if (!state.visitedProvinces) state.visitedProvinces = [];
        if (!state.unlockedAchievements) state.unlockedAchievements = [];
        if (!state.visitedPlaces) state.visitedPlaces = [];
      }
    } catch (e) {
      console.error('Failed to load state', e);
      state = { ...DEFAULT_STATE };
    }
  }

  function saveState() {
    try {
      localStorage.setItem('my-canada-state', JSON.stringify(state));
    } catch (e) {
      console.error('Failed to save state', e);
    }
  }

  function getState() {
    return state;
  }

  function setState(newState) {
    state = { ...state, ...newState };
    saveState();
  }

  function toggleProvince(id) {
    const isVisited = state.visitedProvinces.includes(id);
    let newVisited = [...state.visitedProvinces];
    
    if (isVisited) {
      newVisited = newVisited.filter(p => p !== id);
    } else {
      newVisited.push(id);
    }
    
    setState({ visitedProvinces: newVisited });
    renderAll();
    checkAchievements();
  }

  // 2. THEME
  function applyTheme(themeIndex) {
    if (!window.CANADA_DATA || !window.CANADA_DATA.themes) return;
    const theme = window.CANADA_DATA.themes[themeIndex] || window.CANADA_DATA.themes[0];
    document.documentElement.style.setProperty('--brand', theme.primary);
    document.documentElement.style.setProperty('--brand-hover', theme.hover || (theme.primary + 'dd'));
    document.documentElement.style.setProperty('--brand-bg', theme.bg || (theme.primary + '1a'));
    
    setState({ user: { ...state.user, themeIndex } });
  }

  // 3. NAVIGATION
  function handleNavigation() {
    const hash = window.location.hash || '#map';
    const parts = hash.split('/');
    const baseHash = parts[0];
    const provinceId = parts[1];

    // Hide all views
    document.querySelectorAll('.view').forEach(view => {
      view.classList.remove('active');
    });
    
    // Deactivate nav tabs
    document.querySelectorAll('.nav-tab').forEach(tab => {
      tab.classList.remove('active');
    });

    if (baseHash === '#province' && provinceId) {
      const view = document.getElementById('view-province');
      if (view) view.classList.add('active');
      renderProvinceDrilldown(provinceId);
    } else {
      const viewId = baseHash === '#map' ? 'view-map' : 
                     baseHash === '#explore' ? 'view-explore' : 
                     baseHash === '#stats' ? 'view-stats' : 'view-map';
      
      const view = document.getElementById(viewId);
      if (view) view.classList.add('active');
      
      const tabView = baseHash.substring(1);
      const tab = document.querySelector(`.nav-tab[data-view="${tabView}"]`);
      if (tab) tab.classList.add('active');
    }
  }

  // 4. MAP SETUP
  const FALLBACK_POS = { x: 0, y: 0, width: 629, height: 609 };

  function setupMap() {
    if (!window.CANADA_DATA) return;
    
    const svg = document.getElementById('canada-map');
    const labelsContainer = document.getElementById('map-labels');
    const viewMap = document.getElementById('view-map');
    if (!svg || !labelsContainer || !viewMap) return;

    const PROVINCE_CENTERS = {
      'CA-BC': { cx: 100, cy: 340 },
      'CA-AB': { cx: 170, cy: 380 },
      'CA-SK': { cx: 240, cy: 400 },
      'CA-MB': { cx: 310, cy: 410 },
      'CA-ON': { cx: 390, cy: 460 },
      'CA-QC': { cx: 470, cy: 390 },
      'CA-NL': { cx: 560, cy: 300 },
      'CA-NB': { cx: 510, cy: 470 },
      'CA-NS': { cx: 550, cy: 505 },
      'CA-PE': { cx: 535, cy: 485 },
      'CA-YT': { cx: 90, cy: 180 },
      'CA-NT': { cx: 210, cy: 200 },
      'CA-NU': { cx: 360, cy: 190 }
    };

    window.CANADA_DATA.provinces.forEach(p => {
      let { cx, cy } = PROVINCE_CENTERS[p.id] || { cx: 314, cy: 304 };
      p._cachedBBox = { x: cx - 50, y: cy - 50, width: 100, height: 100 }; // Fake bbox for drilldown preview

      const pctX = (cx / 629) * 100;
      const pctY = (cy / 609) * 100;

          const label = document.createElement('div');
          label.className = 'map-label';
          label.id = `label-${p.id}`;
          label.style.left = `${pctX}%`;
          label.style.top = `${pctY}%`;
          label.innerHTML = `
            <div class="label-dot"></div>
            <div class="label-text-wrap">
              <span class="label-text">${p.name}</span>
              <span class="label-subtext" id="label-sub-${p.id}" style="display:none; font-size:10px; opacity:0.8;"></span>
            </div>
            <span class="explore-arrow" style="font-size:14px; margin-left:4px; opacity:0.5;">→</span>
          `;
          label.dataset.id = p.id;

          label.addEventListener('click', (e) => {
            e.stopPropagation();
            window.location.hash = '#province/' + p.id;
          });
          
          label.addEventListener('mouseenter', (e) => {
            showTooltip(e, p);
          });
          
          label.addEventListener('mouseleave', hideTooltip);
          
          labelsContainer.appendChild(label);
    });

    updateMapUI();

    // SVG click handler
    svg.addEventListener('click', (e) => {
      let target = e.target;
      while (target && target !== svg) {
        if (target.id && target.id.startsWith('CA-')) {
          toggleProvince(target.id);
          break;
        }
        target = target.parentNode;
      }
    });

    // Tooltip hover
    svg.addEventListener('mousemove', (e) => {
      let target = e.target;
      let provinceId = null;
      while (target && target !== svg) {
        if (target.id && target.id.startsWith('CA-')) {
          provinceId = target.id;
          break;
        }
        target = target.parentNode;
      }

      if (provinceId) {
        const p = window.CANADA_DATA.provinces.find(prov => prov.id === provinceId);
        if (p) showTooltip(e, p);
      } else {
        hideTooltip();
      }
    });
    
    svg.addEventListener('mouseleave', hideTooltip);
  }

  let tooltipEl = null;
  function showTooltip(e, p) {
    if (!tooltipEl) {
      tooltipEl = document.createElement('div');
      tooltipEl.className = 'map-tooltip';
      document.body.appendChild(tooltipEl);
    }
    const isVisited = state.visitedProvinces.includes(p.id);
    const totalPlaces = (p.cities?.length||0) + (p.parks?.length||0) + (p.hiddenGems?.length||0);
    const visitedPlaces = state.visitedPlaces.filter(id => id.startsWith(p.id)).length;
    
    let subtext = `<small style="opacity:0.8; font-weight:normal; display:block; margin-top:4px;">Click map to ${isVisited ? 'unmark' : 'mark'} visited<br>Click label to explore deeper</small>`;
    if (visitedPlaces > 0) {
      subtext += `<div style="margin-top:4px; font-size:11px; color:var(--brand-hover);">Places explored: ${visitedPlaces}/${totalPlaces}</div>`;
    }
    
    tooltipEl.innerHTML = `<strong>${p.name}</strong>${subtext}`;
    tooltipEl.style.display = 'block';
    tooltipEl.style.left = `${e.pageX + 15}px`;
    tooltipEl.style.top = `${e.pageY + 15}px`;
  }
  
  function hideTooltip() {
    if (tooltipEl) tooltipEl.style.display = 'none';
  }

  // 5. UPDATE MAP UI
  function updateMapUI() {
    const visited = state.visitedProvinces || [];
    
    // SVG paths
    document.querySelectorAll('#canada-map [id^="CA-"]').forEach(el => {
      if (visited.includes(el.id)) {
        el.classList.add('visited');
      } else {
        el.classList.remove('visited');
      }
    });


    // Labels
    const showNames = document.getElementById('toggle-names')?.checked !== false;
    document.querySelectorAll('.map-label').forEach(label => {
      const pid = label.dataset.id;
      const isVisited = visited.includes(pid);
      
      if (isVisited && showNames) {
        label.classList.add('show');
      } else {
        label.classList.remove('show');
      }

      // Update subtext
      const subTextEl = document.getElementById(`label-sub-${pid}`);
      if (subTextEl && window.CANADA_DATA) {
        const p = window.CANADA_DATA.provinces.find(prov => prov.id === pid);
        if (p) {
          const totalPlaces = (p.cities?.length||0) + (p.parks?.length||0) + (p.hiddenGems?.length||0);
          const visitedPlaces = state.visitedPlaces.filter(id => id.startsWith(pid)).length;
          if (visitedPlaces > 0) {
            subTextEl.textContent = `${visitedPlaces}/${totalPlaces} places`;
            subTextEl.style.display = 'block';
          } else {
            subTextEl.style.display = 'none';
          }
        }
      }
    });
  }

  // 6. SIDEBAR
  function renderSidebarPicker() {
    const container = document.getElementById('province-groups');
    if (!container || !window.CANADA_DATA) return;

    container.innerHTML = '';
    
    const regions = window.CANADA_DATA.regions;
    regions.forEach(region => {
      const regionProvs = window.CANADA_DATA.provinces.filter(p => p.region === region.name);
      if (regionProvs.length === 0) return;

      const group = document.createElement('div');
      group.className = 'region-group';
      
      const header = document.createElement('div');
      header.className = 'region-header';
      header.innerHTML = `
        <span class="region-title">${region.name}</span>
        <div class="region-actions">
          <button class="btn-text btn-region-all" data-region="${region.name}">All</button>
          <button class="btn-text btn-region-none" data-region="${region.name}">None</button>
        </div>
      `;
      
      const chips = document.createElement('div');
      chips.className = 'province-chips';
      
      regionProvs.forEach(p => {
        const wrap = document.createElement('div');
        wrap.className = 'chip-wrap';
        
        const chip = document.createElement('button');
        chip.className = 'chip province-chip';
        chip.dataset.id = p.id;
        chip.textContent = p.name;
        chip.setAttribute('aria-pressed', 'false');
        
        const exploreBtn = document.createElement('button');
        exploreBtn.className = 'explore-btn';
        exploreBtn.innerHTML = '→';
        exploreBtn.onclick = (e) => {
            e.stopPropagation();
            window.location.hash = '#province/' + p.id;
        };
        
        wrap.appendChild(chip);
        wrap.appendChild(exploreBtn);
        chips.appendChild(wrap);
      });
      
      group.appendChild(header);
      group.appendChild(chips);
      container.appendChild(group);
    });
  }

  function updateSidebarUI() {
    const visited = state.visitedProvinces || [];
    
    // Chips
    document.querySelectorAll('.province-chip').forEach(chip => {
      const isVisited = visited.includes(chip.dataset.id);
      chip.classList.toggle('active', isVisited);
      chip.setAttribute('aria-pressed', isVisited.toString());
    });

    // Badge
    const badge = document.querySelector('.visit-badge');
    if (badge) {
      badge.textContent = `${visited.length} / 13`;
    }
  }

  // 7. STATISTICS
  function updateStats() {
    if (!window.CANADA_DATA) return;
    const visitedCount = (state.visitedProvinces || []).length;
    const total = 13;
    const pct = Math.round((visitedCount / total) * 100);

    // Hero
    const heroCount = document.getElementById('hero-count');
    if (heroCount) heroCount.textContent = `${visitedCount}/${total}`;

    // Progress cards
    const fillCard = document.getElementById('progress-fill-card');
    if (fillCard) fillCard.style.width = `${pct}%`;
    const textCard = document.getElementById('progress-text-card');
    if (textCard) textCard.textContent = `${pct}% explored`;

    // Stage branding
    const stageInfo = getStageInfo(visitedCount);
    const stageName = document.getElementById('stage-name');
    const stageAvatar = document.getElementById('stage-avatar');
    const stageCount = document.getElementById('stage-count');
    
    if (stageName) stageName.textContent = stageInfo.name;
    if (stageAvatar) stageAvatar.textContent = stageInfo.emoji;
    if (stageCount) stageCount.textContent = `${visitedCount} Province${visitedCount !== 1 ? 's' : ''}`;
  }

  function getStageInfo(count) {
    if (count === 0) return { name: "Couch Potato", emoji: "🛋️" };
    if (count <= 3) return { name: "Rookie Explorer", emoji: "🎒" };
    if (count <= 7) return { name: "Avid Traveller", emoji: "✈️" };
    if (count <= 12) return { name: "True North Voyager", emoji: "🏔️" };
    return { name: "Canadian Legend", emoji: "🍁" };
  }

  // 8. EXPLORE VIEW
  function renderExploreView(filterStr = '') {
    const container = document.getElementById('explore-grid');
    if (!container || !window.CANADA_DATA) return;

    const query = filterStr.toLowerCase();
    
    const cards = window.CANADA_DATA.provinces.filter(p => {
      if (!query) return true;
      return p.name.toLowerCase().includes(query) || 
             p.capital.toLowerCase().includes(query) || 
             p.region.toLowerCase().includes(query) ||
             (p.description && p.description.toLowerCase().includes(query));
    }).map(p => {
      const isVisited = state.visitedProvinces.includes(p.id);
      
      // Calculate micro-places completion
      const totalPlaces = (p.cities?.length || 0) + (p.parks?.length || 0) + (p.hiddenGems?.length || 0);
      const visitedPlacesCount = state.visitedPlaces.filter(id => id.startsWith(p.id)).length;
      let progressHTML = '';
      if (totalPlaces > 0) {
          const pct = Math.round((visitedPlacesCount / totalPlaces) * 100);
          progressHTML = `
              <div class="explore-card-progress">
                  <div class="explore-progress-bar"><div class="explore-progress-fill" style="width: ${pct}%"></div></div>
                  <span class="explore-progress-text">${visitedPlacesCount}/${totalPlaces} highlights</span>
              </div>
          `;
      }

      return `
        <div class="explore-card ${isVisited ? 'visited' : ''}" data-id="${p.id}" onclick="window.openProvinceModal('${p.id}')">
          <div class="explore-card-header">
            <h3>${p.name}</h3>
            <span class="explore-card-code">${p.code}</span>
          </div>
          <div class="explore-card-body">
            <p><strong>Capital:</strong> ${p.capital}</p>
            <p><strong>Region:</strong> ${window.CANADA_DATA.regions.find(r=>r.id===p.region)?.name || p.region}</p>
            <p class="explore-desc">${p.description || ''}</p>
            ${progressHTML}
          </div>
          <div class="explore-card-footer">
            <button class="btn btn-primary btn-sm" onclick="event.stopPropagation(); window.toggleProvince('${p.id}')">
              ${isVisited ? 'Unmark Visited' : 'Mark Visited'}
            </button>
            <button class="btn btn-outline btn-sm" onclick="event.stopPropagation(); window.location.hash='#province/${p.id}'">
              Drilldown →
            </button>
          </div>
        </div>
      `;
    });

    container.innerHTML = cards.join('');
  }

  // 9. PROVINCE MODAL
  window.openProvinceModal = function(id) {
    const modal = document.getElementById('province-modal');
    if (!modal || !window.CANADA_DATA) return;

    const p = window.CANADA_DATA.provinces.find(prov => prov.id === id);
    if (!p) return;

    const isVisited = state.visitedProvinces.includes(id);

    const header = document.getElementById('modal-header');
    if (header) {
      header.innerHTML = `
        <h2>${p.name}</h2>
        <button class="modal-close" onclick="window.closeProvinceModal()">&times;</button>
      `;
    }

    const body = document.getElementById('modal-body');
    if (body) {
      const famous = p.famousFor ? p.famousFor.map(f => `<li>${f}</li>`).join('') : '';
      body.innerHTML = `
        <div class="modal-stats">
          <div class="modal-stat"><strong>Capital:</strong> ${p.capital}</div>
          <div class="modal-stat"><strong>Population:</strong> ${p.population}</div>
          <div class="modal-stat"><strong>Area:</strong> ${p.area}</div>
        </div>
        <p>${p.description}</p>
        ${famous ? `<h4>Famous For:</h4><ul>${famous}</ul>` : ''}
      `;
    }

    const footer = document.getElementById('modal-footer');
    if (footer) {
      footer.innerHTML = `
        <button class="btn btn-outline" onclick="window.toggleProvince('${p.id}'); window.openProvinceModal('${p.id}')">
          ${isVisited ? 'Unmark Visited' : 'Mark Visited'}
        </button>
        <button class="btn btn-primary" onclick="window.location.hash='#province/${p.id}'; window.closeProvinceModal();">
          Explore ${p.name} &rarr;
        </button>
      `;
    }

    modal.hidden = false;
    // Small delay to allow display:block to apply before animating opacity via .show
    setTimeout(() => {
      modal.classList.add('show');
    }, 10);
  };

  window.closeProvinceModal = function() {
    const modal = document.getElementById('province-modal');
    if (!modal) return;
    modal.classList.remove('show');
    setTimeout(() => {
      modal.hidden = true;
    }, 300); // match transition time
  };

  // 10. STATS VIEW
  function renderStatsView() {
    if (!window.CANADA_DATA) return;
    
    // Achievements
    const achContainer = document.getElementById('achievements-grid');
    if (achContainer) {
      const html = window.CANADA_DATA.achievements.map(ach => {
        const unlocked = state.unlockedAchievements.includes(ach.id);
        return `
          <div class="achievement-card ${unlocked ? 'unlocked' : 'locked'}">
            <div class="achievement-icon">${ach.icon}</div>
            <div class="achievement-info">
              <h4>${ach.title}</h4>
              <p>${ach.description}</p>
            </div>
          </div>
        `;
      }).join('');
      achContainer.innerHTML = html;
    }

    // Challenges (Regions)
    const chContainer = document.getElementById('challenges-grid');
    if (chContainer) {
      const html = window.CANADA_DATA.regions.map(r => {
        const rProvs = window.CANADA_DATA.provinces.filter(p => p.region === r.name);
        const rCount = rProvs.filter(p => state.visitedProvinces.includes(p.id)).length;
        const total = rProvs.length;
        const pct = total === 0 ? 0 : Math.round((rCount / total) * 100);
        const completed = rCount === total && total > 0;
        
        return `
          <div class="challenge-card ${completed ? 'completed' : ''}">
            <h4>${r.name} Explorer</h4>
            <div class="challenge-progress">
              <div class="challenge-progress-bar">
                <div class="challenge-progress-fill" style="width: ${pct}%"></div>
              </div>
              <span>${rCount}/${total}</span>
            </div>
          </div>
        `;
      }).join('');
      chContainer.innerHTML = html;
    }
  }

  function checkAchievements() {
    if (!window.CANADA_DATA) return;
    
    const v = state.visitedProvinces;
    let newlyUnlocked = [];

    window.CANADA_DATA.achievements.forEach(ach => {
      if (state.unlockedAchievements.includes(ach.id)) return;
      
      let met = false;
      if (ach.threshold) {
        if (v.length >= ach.threshold) met = true;
      }
      if (ach.requires) {
        if (ach.requires.every(id => v.includes(id))) met = true;
      }
      
      if (met) {
        newlyUnlocked.push(ach.id);
        showToast("Achievement Unlocked!", `${ach.icon} ${ach.title}`);
      }
    });

    if (newlyUnlocked.length > 0) {
      setState({ unlockedAchievements: [...state.unlockedAchievements, ...newlyUnlocked] });
      renderStatsView();
    }
  }

  // 11. TOASTS
  function showToast(title, message) {
    const container = document.getElementById('toast-container');
    if (!container) return;

    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.innerHTML = `<strong>${title}</strong><br>${message}`;
    container.appendChild(toast);

    setTimeout(() => {
      toast.style.opacity = '0';
      setTimeout(() => toast.remove(), 300);
    }, 4000);
  }

  // 12. CANVAS EXPORT
  async function generateImage() {
    return new Promise((resolve, reject) => {
      const canvas = document.createElement('canvas');
      canvas.width = 1080;
      canvas.height = 1350;
      const ctx = canvas.getContext('2d');
      if (!ctx) return reject(new Error("No 2d context"));

      const themeIndex = state.user?.themeIndex || 0;
      const themeColor = window.CANADA_DATA?.themes?.[themeIndex]?.color || '#e31837';

      // 1. Background
      ctx.fillStyle = '#fafaf9';
      ctx.fillRect(0, 0, canvas.width, canvas.height);
      
      ctx.fillStyle = 'rgba(0,0,0,0.06)';
      for (let x = 20; x < canvas.width; x += 40) {
        for (let y = 20; y < canvas.height; y += 40) {
          ctx.beginPath();
          ctx.arc(x, y, 2, 0, Math.PI * 2);
          ctx.fill();
        }
      }

      // Accent Bar
      ctx.fillStyle = themeColor;
      ctx.fillRect(0, 0, canvas.width, 16);

      // 2. Header (Avatar, Name, Stage)
      const stage = getStageInfo(state.visitedProvinces.length);
      const name = state.user?.name || 'Explorer';
      
      let startY = 120;
      
      if (state.user?.photo) {
        // Draw Avatar
        const img = new Image();
        img.onload = () => {
          ctx.save();
          ctx.beginPath();
          ctx.arc(140, startY, 60, 0, Math.PI * 2);
          ctx.closePath();
          ctx.clip();
          // cover fill
          const size = Math.min(img.width, img.height);
          const sx = (img.width - size) / 2;
          const sy = (img.height - size) / 2;
          ctx.drawImage(img, sx, sy, size, size, 80, startY - 60, 120, 120);
          ctx.restore();
          
          // Avatar border
          ctx.beginPath();
          ctx.arc(140, startY, 60, 0, Math.PI * 2);
          ctx.lineWidth = 4;
          ctx.strokeStyle = themeColor;
          ctx.stroke();

          drawText();
        };
        img.onerror = drawText;
        img.src = state.user.photo;
      } else {
        drawText();
      }

      function drawText() {
        const textX = state.user?.photo ? 230 : 80;
        
        ctx.fillStyle = '#111827';
        ctx.font = 'bold 48px system-ui, -apple-system, sans-serif';
        ctx.fillText(`${name}'s Canada`, textX, startY - 10);
        
        ctx.fillStyle = '#6b7280';
        ctx.font = '32px system-ui, -apple-system, sans-serif';
        ctx.fillText(`${stage.emoji} ${stage.name}`, textX, startY + 40);

        // Score bubble
        ctx.fillStyle = themeColor;
        ctx.beginPath();
        ctx.roundRect(canvas.width - 240, startY - 40, 160, 80, 40);
        ctx.fill();
        
        ctx.fillStyle = '#ffffff';
        ctx.font = 'bold 36px system-ui, -apple-system, sans-serif';
        ctx.textAlign = 'center';
        ctx.fillText(`${state.visitedProvinces.length}/13`, canvas.width - 160, startY + 12);
        
        const placesCount = state.visitedPlaces.length;
        if (placesCount > 0) {
           ctx.fillStyle = '#6b7280';
           ctx.font = '22px system-ui, -apple-system, sans-serif';
           ctx.fillText(`${placesCount} places explored`, canvas.width - 160, startY + 60);
        }
        ctx.textAlign = 'left';

        drawMap();
      }

      function drawMap() {
        const svgEl = document.getElementById('canada-map');
        if (!svgEl) return finishCanvas();

        const clone = svgEl.cloneNode(true);
        // Clean clone
        clone.style.width = '100%';
        clone.style.height = '100%';
        clone.setAttribute('width', '629');
        clone.setAttribute('height', '609');

        // Apply visited colors inline
        const visited = state.visitedProvinces || [];
        const style = document.createElement('style');
        style.textContent = `
          path, g { fill: #f3f4f6; stroke: #d1d5db; stroke-width: 1.5px; stroke-linejoin: round; }
          ${visited.map(id => `#${id}`).join(', ')} { fill: ${themeColor} !important; stroke: #ffffff !important; stroke-width: 2.5px !important; filter: drop-shadow(0 8px 12px ${themeColor}60); }
          ${visited.map(id => `#${id} path`).join(', ')} { fill: ${themeColor} !important; stroke: #ffffff !important; stroke-width: 2.5px !important; }
        `;
        clone.appendChild(style);

        const svgData = new XMLSerializer().serializeToString(clone);
        const svgBlob = new Blob([svgData], {type: 'image/svg+xml;charset=utf-8'});
        const DOMURL = window.URL || window.webkitURL || window;
        const url = DOMURL.createObjectURL(svgBlob);

        const img = new Image();
        img.onload = () => {
          // Draw map at specific bounds
          ctx.drawImage(img, 90, 280, 900, 870);
          DOMURL.revokeObjectURL(url);
          drawLabels();
        };
        img.onerror = () => {
          DOMURL.revokeObjectURL(url);
          drawLabels();
        };
        img.src = url;
      }

      function drawLabels() {
        // Bangladesh style labels
        const visited = state.visitedProvinces || [];
        
        window.CANADA_DATA.provinces.forEach(p => {
          if (!visited.includes(p.id)) return;
          
          const bbox = p._cachedBBox || FALLBACK_POS;
          let cx = bbox.x + bbox.width / 2;
          let cy = bbox.y + bbox.height / 2;



          // Map scale: 629x609 mapped to 900x870 at 90,280
          const scaleX = 900 / 629;
          const scaleY = 870 / 609;
          
          const x = 90 + cx * scaleX;
          const y = 280 + cy * scaleY;

          // Red Dot
          ctx.beginPath();
          ctx.arc(x, y, 6, 0, 2 * Math.PI);
          ctx.fillStyle = '#ffffff'; 
          ctx.fill();
          ctx.lineWidth = 4;
          ctx.strokeStyle = themeColor;
          ctx.stroke();

          // Bold Text with stroke
          ctx.font = 'bold 24px system-ui, -apple-system, sans-serif';
          ctx.fillStyle = '#111827';
          ctx.strokeStyle = '#ffffff';
          ctx.lineWidth = 6;
          ctx.lineJoin = 'round';
          
          ctx.strokeText(p.name, x + 16, y + 8);
          ctx.fillText(p.name, x + 16, y + 8);

          const visitedPlaces = state.visitedPlaces.filter(id => id.startsWith(p.id)).length;
          if (visitedPlaces > 0) {
            const totalPlaces = (p.cities?.length||0) + (p.parks?.length||0) + (p.hiddenGems?.length||0);
            ctx.font = 'bold 14px system-ui, -apple-system, sans-serif';
            ctx.fillStyle = themeColor;
            ctx.lineWidth = 4;
            ctx.strokeText(`${visitedPlaces}/${totalPlaces} places`, x + 16, y + 26);
            ctx.fillText(`${visitedPlaces}/${totalPlaces} places`, x + 16, y + 26);
          }
        });

        finishCanvas();
      }

      function finishCanvas() {
        // Next adventure footer
        const footerY = 1220;
        if (state.user?.nextAdventure) {
          ctx.fillStyle = '#6b7280';
          ctx.font = '28px system-ui, -apple-system, sans-serif';
          ctx.fillText("Next up:", 80, footerY);
          
          ctx.fillStyle = themeColor;
          ctx.font = 'bold 32px system-ui, -apple-system, sans-serif';
          ctx.fillText(state.user.nextAdventure, 80, footerY + 40);
        }

        // Domain branding
        ctx.fillStyle = '#9ca3af';
        ctx.font = '24px system-ui, -apple-system, sans-serif';
        ctx.textAlign = 'right';
        ctx.fillText("mycanada.app", canvas.width - 80, footerY + 40);
        
        resolve(canvas);
      }
    });
  }

  async function handleDownload(type = 'image/png') {
    try {
      const canvas = await generateImage();
      const link = document.createElement('a');
      link.download = `my-canada-map.${type === 'image/jpeg' ? 'jpg' : 'png'}`;
      link.href = canvas.toDataURL(type, type === 'image/jpeg' ? 0.9 : undefined);
      link.click();
    } catch (e) {
      console.error(e);
      showToast("Error", "Could not generate image");
    }
  }

  async function openShareModal() {
    const modal = document.getElementById('share-modal');
    const container = document.getElementById('share-canvas');
    if (!modal || !container) return;

    container.innerHTML = '<div class="loading">Generating preview...</div>';
    modal.classList.add('show');
    modal.hidden = false;

    try {
      const canvas = await generateImage();
      // scale down for preview
      canvas.style.width = '100%';
      canvas.style.height = 'auto';
      canvas.style.borderRadius = '12px';
      canvas.style.boxShadow = '0 10px 25px rgba(0,0,0,0.1)';
      container.innerHTML = '';
      container.appendChild(canvas);
    } catch (e) {
      container.innerHTML = '<div class="error">Failed to generate preview</div>';
    }
  }

  function closeShareModal() {
    const modal = document.getElementById('share-modal');
    if (!modal) return;
    modal.classList.remove('show');
    setTimeout(() => { modal.hidden = true; }, 300);
  }

  async function handleShare() {
    try {
      const canvas = document.querySelector('#share-canvas canvas');
      if (!canvas) throw new Error("No canvas");

      canvas.toBlob(async (blob) => {
        if (!blob) throw new Error("Blob failed");
        
        const file = new File([blob], "my-canada.png", { type: "image/png" });
        
        if (navigator.share && navigator.canShare && navigator.canShare({ files: [file] })) {
          await navigator.share({
            title: 'My Canada Exploration',
            text: `I've explored ${state.visitedProvinces.length} provinces in Canada!`,
            files: [file]
          });
        } else {
          // fallback to download
          handleDownload('image/png');
        }
      }, 'image/png');
    } catch (e) {
      console.error(e);
      handleDownload('image/png'); // absolute fallback
    }
  }

  // 13. PHASE 2: PROVINCE DRILLDOWN
  window.toggleMicroPlace = function(placeId) {
    let newPlaces = [...state.visitedPlaces];
    if (newPlaces.includes(placeId)) {
      newPlaces = newPlaces.filter(id => id !== placeId);
    } else {
      newPlaces.push(placeId);
    }
    setState({ visitedPlaces: newPlaces });
    
    // Auto-mark province as visited if they visit any place inside it
    const parts = placeId.split('-');
    const provId = parts[0] + '-' + parts[1];
    if (!state.visitedProvinces.includes(provId)) {
      toggleProvince(provId);
    }
    
    // Re-render drilldown if we are in it
    const hash = window.location.hash || '';
    if (hash.startsWith('#province/')) {
       renderProvinceDrilldown(hash.split('/')[1]);
    }
    
    renderExploreView(); // Update progress bars in explore view
  };

  function renderProvinceDrilldown(provinceId) {
    const p = window.CANADA_DATA.provinces.find(prov => prov.id === provinceId);
    if (!p) return;

    const isVisited = state.visitedProvinces.includes(provinceId);

    // Header info
    document.getElementById('drilldown-name').textContent = p.name;
    const regionName = window.CANADA_DATA.regions.find(r => r.id === p.region)?.name || p.region;
    document.getElementById('drilldown-region').textContent = `${regionName} • Capital: ${p.capital}`;
    document.getElementById('drilldown-desc').textContent = p.description || '';

    // Draw Isolated Map
    const container = document.getElementById('drilldown-map-container');
    const svgEl = document.getElementById('canada-map');
    
    if (container && svgEl) {
      container.innerHTML = '';
      const clone = svgEl.cloneNode(true);
      clone.removeAttribute('id');
      
      // Hide all other provinces
      Array.from(clone.children).forEach(child => {
        if (child.tagName === 'path' || child.tagName === 'g') {
          if (child.id !== p.id && child.id !== 'canada-map-bg') {
            child.style.display = 'none';
          }
        }
      });
      
      // Force visited color if visited
      if (isVisited) {
        const target = clone.querySelector(`#${p.id}`);
        if (target) {
           target.style.fill = 'var(--brand)';
           // Also color child paths if it's a group
           target.querySelectorAll('path').forEach(childPath => {
              childPath.style.fill = 'var(--brand)';
           });
        }
      }
      
      // Adjust viewBox to crop to province
      const bbox = p._cachedBBox || FALLBACK_POS;
      const padding = 20;
      clone.setAttribute('viewBox', `${Math.max(0, bbox.x - padding)} ${Math.max(0, bbox.y - padding)} ${bbox.width + padding*2} ${bbox.height + padding*2}`);
      clone.style.width = '100%';
      clone.style.height = '200px';
      
      container.appendChild(clone);
    }

    // Render Grids
    const renderGrid = (items, prefix, gridId) => {
      const grid = document.getElementById(gridId);
      if (!grid) return 0;
      if (!items || items.length === 0) {
        grid.innerHTML = '<p class="text-muted">None available.</p>';
        return 0;
      }
      
      let html = '';
      items.forEach(item => {
        const fullId = `${p.id}-${prefix}-${item.id}`;
        const visited = state.visitedPlaces.includes(fullId);
        const icon = prefix === 'CITY' ? '🏙️' : prefix === 'PARK' ? '🌲' : '💎';
        
        html += `
          <div class="place-card ${visited ? 'visited' : ''}" onclick="window.toggleMicroPlace('${fullId}')">
            <div class="place-checkbox"></div>
            <div class="place-info">
              <b>${icon} ${item.name}</b>
              ${item.highlight ? `<small>${item.highlight}</small>` : ''}
            </div>
          </div>
        `;
      });
      grid.innerHTML = html;
      return items.length;
    };

    const totalCities = renderGrid(p.cities, 'CITY', 'grid-cities');
    const totalParks = renderGrid(p.parks, 'PARK', 'grid-parks');
    const totalGems = renderGrid(p.hiddenGems, 'GEM', 'grid-gems');

    // Update Progress
    const totalPlaces = totalCities + totalParks + totalGems;
    const visitedInProv = state.visitedPlaces.filter(id => id.startsWith(p.id)).length;
    
    document.getElementById('drilldown-score').textContent = totalPlaces > 0 ? `${visitedInProv} / ${totalPlaces} Highlights` : '0 Highlights';
    
    const progressFill = document.getElementById('drilldown-progress-fill');
    if (progressFill) {
      const pct = totalPlaces > 0 ? (visitedInProv / totalPlaces) * 100 : 0;
      progressFill.style.width = `${pct}%`;
    }
  }

  // 14. EVENT BINDING
  function bindEvents() {
    window.addEventListener('hashchange', handleNavigation);

    // Settings / Profile inputs
    const nameInputs = ['name-input-nav', 'sidebar-name', 'share-name'].map(id => document.getElementById(id)).filter(Boolean);
    nameInputs.forEach(input => {
      input.value = state.user.name || '';
      input.addEventListener('input', (e) => {
        const val = e.target.value;
        setState({ user: { ...state.user, name: val } });
        nameInputs.forEach(i => { if (i !== e.target) i.value = val; });
        updateStats();
      });
    });

    const nextAdvInput = document.getElementById('sidebar-next-adventure');
    if (nextAdvInput) {
      nextAdvInput.value = state.user.nextAdventure || '';
      nextAdvInput.addEventListener('input', (e) => {
        setState({ user: { ...state.user, nextAdventure: e.target.value } });
      });
    }

    const photoInput = document.getElementById('sidebar-photo');
    if (photoInput) {
      photoInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) {
          const reader = new FileReader();
          reader.onload = (ev) => {
            setState({ user: { ...state.user, photo: ev.target.result } });
            renderAll();
          };
          reader.readAsDataURL(file);
        }
      });
    }

    // Theme Swatches
    const themeContainer = document.getElementById('theme-swatches');
    if (themeContainer && window.CANADA_DATA && window.CANADA_DATA.themes) {
      themeContainer.innerHTML = window.CANADA_DATA.themes.map((t, i) => `
        <button class="theme-swatch ${i === state.user.themeIndex ? 'active' : ''}" 
                style="background-color: ${t.color}"
                data-index="${i}"
                title="${t.name}"></button>
      `).join('');

      themeContainer.addEventListener('click', (e) => {
        if (e.target.classList.contains('theme-swatch')) {
          const index = parseInt(e.target.dataset.index, 10);
          applyTheme(index);
          document.querySelectorAll('.theme-swatch').forEach(btn => btn.classList.remove('active'));
          e.target.classList.add('active');
        }
      });
    }

    // Sidebar buttons (delegation)
    const provinceGroups = document.getElementById('province-groups');
    if (provinceGroups) {
      provinceGroups.addEventListener('click', (e) => {
        if (e.target.classList.contains('province-chip')) {
          toggleProvince(e.target.dataset.id);
        }
        else if (e.target.classList.contains('btn-region-all')) {
          const region = e.target.dataset.region;
          const provs = window.CANADA_DATA.provinces.filter(p => p.region === region).map(p => p.id);
          const newVisited = new Set([...state.visitedProvinces, ...provs]);
          setState({ visitedProvinces: Array.from(newVisited) });
          renderAll();
          checkAchievements();
        }
        else if (e.target.classList.contains('btn-region-none')) {
          const region = e.target.dataset.region;
          const provs = window.CANADA_DATA.provinces.filter(p => p.region === region).map(p => p.id);
          const newVisited = state.visitedProvinces.filter(id => !provs.includes(id));
          setState({ visitedProvinces: newVisited });
          renderAll();
        }
      });
    }

    // Global all/none
    const btnAll = document.getElementById('btn-all');
    if (btnAll) {
      btnAll.addEventListener('click', () => {
        setState({ visitedProvinces: window.CANADA_DATA.provinces.map(p => p.id) });
        renderAll();
        checkAchievements();
      });
    }

    const btnClear = document.getElementById('btn-clear');
    if (btnClear) {
      btnClear.addEventListener('click', () => {
        setState({ visitedProvinces: [] });
        renderAll();
      });
    }

    // Explore filter
    const searchInput = document.getElementById('explore-search');
    if (searchInput) {
      searchInput.addEventListener('input', (e) => {
        renderExploreView(e.target.value);
      });
    }

    // Download/Share
    document.getElementById('download-btn-png')?.addEventListener('click', () => handleDownload('image/png'));
    document.getElementById('download-btn-jpg')?.addEventListener('click', () => handleDownload('image/jpeg'));
    document.getElementById('share-btn')?.addEventListener('click', openShareModal);
    document.getElementById('share-execute')?.addEventListener('click', handleShare);

    // Hero CTA
    document.getElementById('hero-cta')?.addEventListener('click', () => {
      window.location.hash = '#map';
    });
    
    // Toggle labels
    const toggleNames = document.getElementById('toggle-names');
    if (toggleNames) {
      toggleNames.addEventListener('change', (e) => {
        const labels = document.getElementById('map-labels');
        if (labels) {
          labels.style.display = e.target.checked ? 'block' : 'none';
        }
      });
    }

    // Modal overlays & escapes
    document.addEventListener('click', (e) => {
      if (e.target.classList.contains('modal')) {
        if (e.target.id === 'province-modal') closeProvinceModal();
        if (e.target.id === 'share-modal') closeShareModal();
      }
    });

    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') {
        closeProvinceModal();
        closeShareModal();
      }
    });
    
    // Expose close for share modal
    window.closeShareModal = closeShareModal;
    // Expose toggleProvince globally just in case
    window.toggleProvince = toggleProvince;
  }

  // 15. RENDER ALL
  function renderAll() {
    updateMapUI();
    updateSidebarUI();
    updateStats();
    
    const searchInput = document.getElementById('explore-search');
    renderExploreView(searchInput ? searchInput.value : '');
    
    renderStatsView();

    // Re-apply avatar if it exists
    const avatar = document.getElementById('sidebar-avatar');
    if (avatar && state.user.photo) {
      avatar.style.backgroundImage = `url(${state.user.photo})`;
    }
  }

  // 16. INIT
  function init() {
    loadState();
    
    // Ensure data exists before proceeding heavily
    if (window.CANADA_DATA) {
      applyTheme(state.user.themeIndex || 0);
      setupMap();
      renderSidebarPicker();
      bindEvents();
      renderAll();
      checkAchievements();
    } else {
      console.error("CANADA_DATA not loaded.");
    }
    
    handleNavigation(); // Route to correct view
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

})();
