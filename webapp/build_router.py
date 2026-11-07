import re

with open("/Users/saikatghosh/.gemini/antigravity/scratch/unseencanada/webapp/app.js", "r") as f:
    js = f.read()

# Add to routing
old_router = r"""  function handleNavigation\(\) \{
    let hash = window\.location\.hash \|\| '#map';
    const validViews = \['#map', '#explore', '#stats'\];
    if \(!validViews\.includes\(hash\)\) hash = '#map';

    document\.querySelectorAll\('\.view'\)\.forEach\(section => \{
      section\.classList\.remove\('active'\);
    \}\);

    const viewId = hash\.substring\(1\);
    const viewEl = document\.getElementById\(`view-\$\{viewId\}`\);
    if \(viewEl\) viewEl\.classList\.add\('active'\);"""

new_router = """  function handleNavigation() {
    let hash = window.location.hash || '#map';
    
    // Handle Phase 2 drilldown routing
    if (hash.startsWith('#province/')) {
        const provinceId = hash.split('/')[1];
        document.querySelectorAll('.view').forEach(s => s.classList.remove('active'));
        const drillView = document.getElementById('view-province');
        if (drillView) {
            drillView.classList.add('active');
            renderProvinceDrilldown(provinceId);
        }
        return;
    }

    const validViews = ['#map', '#explore', '#stats'];
    if (!validViews.includes(hash)) hash = '#map';

    document.querySelectorAll('.view').forEach(section => {
      section.classList.remove('active');
    });

    const viewId = hash.substring(1);
    const viewEl = document.getElementById(`view-${viewId}`);
    if (viewEl) viewEl.classList.add('active');"""

js = re.sub(old_router, new_router, js)

with open("/Users/saikatghosh/.gemini/antigravity/scratch/unseencanada/webapp/app.js", "w") as f:
    f.write(js)
