import re

with open("/Users/saikatghosh/.gemini/antigravity/scratch/unseencanada/webapp/app.js", "r") as f:
    content = f.read()

stats_logic = """
    // Update global stat elements
    const statProv = document.getElementById('stat-provinces');
    if (statProv) statProv.textContent = visited;
    
    const statPct = document.getElementById('stat-percentage');
    if (statPct) statPct.innerHTML = `${percentage}<small>%</small>`;
    
    const statCities = document.getElementById('stat-cities');
    if (statCities) statCities.textContent = cities;
    
    const statParks = document.getElementById('stat-parks');
    if (statParks) statParks.textContent = parks;

    const fillProg = document.getElementById('progress-fill');
    if (fillProg) fillProg.style.width = `${percentage}%`;

    const txtProg = document.getElementById('progress-text');
    if (txtProg) txtProg.textContent = `${percentage}% explored`;

    const statProvBar = document.getElementById('stat-provinces-bar');
    if (statProvBar) statProvBar.style.width = `${(visited/total)*100}%`;
    
    const statCitiesBar = document.getElementById('stat-cities-bar');
    if (statCitiesBar) statCitiesBar.style.width = `${Math.min((cities/50)*100, 100)}%`; // arbitrary max 50
    
    const statParksBar = document.getElementById('stat-parks-bar');
    if (statParksBar) statParksBar.style.width = `${Math.min((parks/20)*100, 100)}%`; // arbitrary max 20
    
    const statPctBar = document.getElementById('stat-percentage-bar');
    if (statPctBar) statPctBar.style.width = `${percentage}%`;
"""

pattern = re.compile(r"// Update global stat elements.*?document\.querySelectorAll\('\.progress-bar-fill'\)\.forEach\(el => \{\n      el\.style\.width = `\$\{percentage\}%`;\n    \}\);", re.DOTALL)
content = pattern.sub(stats_logic.strip(), content)

with open("/Users/saikatghosh/.gemini/antigravity/scratch/unseencanada/webapp/app.js", "w") as f:
    f.write(content)
