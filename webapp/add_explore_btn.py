import re

with open("/Users/saikatghosh/.gemini/antigravity/scratch/unseencanada/webapp/app.js", "r") as f:
    js = f.read()

# Add visitedPlaces to initial state
js = js.replace('unlockedAchievements: []', 'unlockedAchievements: [],\n  visitedPlaces: []')

# Add Explore button to modal footer
old_footer = r"""    // Footer
    document\.getElementById\('modal-footer'\)\.innerHTML = `
      <button class="btn \$\{isVisited \? 'btn-outline' : 'btn-primary'\}" id="modal-toggle-visited" data-id="\$\{p\.id\}">
        \$\{isVisited \? 'Mark as Unvisited' : 'Mark as Visited'\}
      </button>
    `;"""

new_footer = """    // Footer
    document.getElementById('modal-footer').innerHTML = `
      <button class="btn ${isVisited ? 'btn-outline' : 'btn-primary'}" id="modal-toggle-visited" data-id="${p.id}">
        ${isVisited ? 'Mark as Unvisited' : 'Mark as Visited'}
      </button>
      <button class="btn btn-primary" style="background: var(--ink); color: white; border: none;" onclick="window.location.hash='#province/${p.id}'; document.getElementById('province-modal').classList.remove('active');">
        Explore ${p.name} →
      </button>
    `;"""

js = re.sub(old_footer, new_footer, js)

with open("/Users/saikatghosh/.gemini/antigravity/scratch/unseencanada/webapp/app.js", "w") as f:
    f.write(js)
