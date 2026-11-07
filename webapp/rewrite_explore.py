import re

with open("/Users/saikatghosh/.gemini/antigravity/scratch/unseencanada/webapp/app.js", "r") as f:
    content = f.read()

explore_logic = """
    document.getElementById('explore-filters')?.addEventListener('click', (e) => {
      if (e.target.classList.contains('filter-chip')) {
        document.querySelectorAll('.filter-chip').forEach(c => {
          c.classList.remove('active');
          c.setAttribute('aria-pressed', 'false');
        });
        e.target.classList.add('active');
        e.target.setAttribute('aria-pressed', 'true');
        
        exploreRegionFilter = e.target.dataset.filter === 'all' ? 'All' : e.target.dataset.filter;
        renderExploreView();
      }
    });
"""

pattern = re.compile(r"document\.getElementById\('explore-region-filter'\)\?\.addEventListener\('change', \(e\) => \{.*?\}\);", re.DOTALL)
content = pattern.sub(explore_logic.strip(), content)

with open("/Users/saikatghosh/.gemini/antigravity/scratch/unseencanada/webapp/app.js", "w") as f:
    f.write(content)
