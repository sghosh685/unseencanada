with open("/Users/saikatghosh/.gemini/antigravity/scratch/unseencanada/webapp/app.js", "r") as f:
    content = f.read()

render_all_logic = """
  function renderAll() {
    updateMapUI();
    updateSidebarUI();
    updateStats();
    renderExploreView();
    renderStatsView();
    
    // Update Theme picker UI
    document.querySelectorAll('.theme-swatch').forEach((btn, idx) => {
      if (idx === state.user.themeIndex) {
        btn.classList.add('active');
      } else {
        btn.classList.remove('active');
      }
    });
    applyTheme(state.user.themeIndex);

    const nameInput = document.getElementById('sidebar-name');
    if (nameInput && nameInput.value !== state.user.name) {
      nameInput.value = state.user.name;
    }
    const nextAdvInput = document.getElementById('sidebar-next-adventure');
    if (nextAdvInput && nextAdvInput.value !== state.user.nextAdventure) {
      nextAdvInput.value = state.user.nextAdventure || '';
    }
  }

"""

content = content.replace("  function init() {", render_all_logic + "  function init() {")

with open("/Users/saikatghosh/.gemini/antigravity/scratch/unseencanada/webapp/app.js", "w") as f:
    f.write(content)
