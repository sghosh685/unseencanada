import re

with open("/Users/saikatghosh/.gemini/antigravity/scratch/unseencanada/webapp/app.js", "r") as f:
    content = f.read()

setup_map_old = """            const bbox = el.getBBox();
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
            const topPct = (cy / vh) * 100;"""

setup_map_new = """            let leftPct, topPct;
            if (typeof el.getBBox === 'function') {
                const bbox = el.getBBox();
                let cx = bbox.x + bbox.width / 2;
                let cy = bbox.y + bbox.height / 2;
                if (p.id === 'CA-NU') { cx -= 60; cy += 60; }
                if (p.id === 'CA-BC') { cx += 20; cy -= 20; }
                if (p.id === 'CA-ON') { cy += 50; cx += 10; }
                if (p.id === 'CA-QC') { cx -= 30; cy += 50; }
                if (p.id === 'CA-NL') { cx += 60; cy += 40; }
                if (p.id === 'CA-PE') { cy -= 5; cx += 15; }
                if (p.id === 'CA-NS') { cx += 20; cy += 10; }
                if (p.id === 'CA-NT') { cx += 20; cy -= 10; }
                leftPct = (cx / vw) * 100;
                topPct = (cy / vh) * 100;
            } else {
                throw new Error("No getBBox");
            }"""

setup_map_catch_old = """        } catch (e) {
            // getBBox might fail if svg is display:none
        }"""

setup_map_catch_new = """        } catch (e) {
            const FALLBACK_POS = {
              "CA-BC": {left: 15, top: 60}, "CA-AB": {left: 28, top: 65},
              "CA-SK": {left: 40, top: 68}, "CA-MB": {left: 50, top: 68},
              "CA-ON": {left: 65, top: 75}, "CA-QC": {left: 80, top: 65},
              "CA-NB": {left: 88, top: 78}, "CA-NS": {left: 92, top: 82},
              "CA-PE": {left: 90, top: 75}, "CA-NL": {left: 92, top: 60},
              "CA-YT": {left: 15, top: 35}, "CA-NT": {left: 35, top: 35},
              "CA-NU": {left: 60, top: 35}
            };
            const pos = FALLBACK_POS[p.id];
            if (pos) {
                const label = document.createElement('div');
                label.className = 'province-label';
                label.id = `label-${p.id}`;
                label.style.left = `${pos.left}%`;
                label.style.top = `${pos.top}%`;
                label.textContent = p.name;
                container.appendChild(label);
            }
        }"""

content = content.replace(setup_map_old, setup_map_new)
content = content.replace(setup_map_catch_old, setup_map_catch_new)

with open("/Users/saikatghosh/.gemini/antigravity/scratch/unseencanada/webapp/app.js", "w") as f:
    f.write(content)
