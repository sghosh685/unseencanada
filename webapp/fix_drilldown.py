import re

with open("/Users/saikatghosh/.gemini/antigravity/scratch/unseencanada/webapp/app.js", "r") as f:
    js = f.read()

# 1. In setupMap, cache the bbox while the map is visible!
old_setup = r"""                const bbox = el\.getBBox\(\);
                if \(bbox\.width === 0 && bbox\.height === 0\) throw new Error\("Zero BBox"\);
                let cx = bbox\.x \+ bbox\.width / 2;"""

new_setup = """                const bbox = el.getBBox();
                p._cachedBBox = {x: bbox.x, y: bbox.y, width: bbox.width, height: bbox.height};
                if (bbox.width === 0 && bbox.height === 0) throw new Error("Zero BBox");
                let cx = bbox.x + bbox.width / 2;"""

js = re.sub(old_setup, new_setup, js)

# 2. In renderProvinceDrilldown, use the cached bbox!
old_render = r"""    const svgEl = document\.getElementById\(p\.id\);
    const mapContainer = document\.getElementById\('drilldown-map-container'\);
    if \(svgEl\) \{
        const bbox = svgEl\.getBBox\(\);"""

new_render = """    const svgEl = document.getElementById(p.id);
    const mapContainer = document.getElementById('drilldown-map-container');
    if (svgEl) {
        // Fallback to 0 0 629 609 if no cached bbox
        const bbox = p._cachedBBox || {x: 0, y: 0, width: 629, height: 609};"""

js = re.sub(old_render, new_render, js)

with open("/Users/saikatghosh/.gemini/antigravity/scratch/unseencanada/webapp/app.js", "w") as f:
    f.write(js)
