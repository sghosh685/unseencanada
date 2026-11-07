import re

with open("/Users/saikatghosh/.gemini/antigravity/scratch/unseencanada/webapp/app.js", "r") as f:
    js = f.read()

# The sidebar province groups render chips.
# We want clicking a chip to toggle the province, BUT maybe we can add a small "details" icon next to it?
# Or when a province is visited, show a button?
# Let's look at updateMapUI where it renders chips:
# Actually the chips are static in HTML or dynamically generated in setupMap?
# In setupMap:
# const chip = document.createElement('button'); chip.className = 'chip'; chip.textContent = p.name;
old_chip = r"""            const chip = document\.createElement\('button'\);
            chip\.className = 'chip';
            chip\.setAttribute\('aria-pressed', 'false'\);
            chip\.textContent = p\.name;
            chip\.dataset\.id = p\.id;"""

new_chip = """            const chipWrap = document.createElement('div');
            chipWrap.style.display = 'inline-flex';
            chipWrap.style.alignItems = 'center';
            chipWrap.style.gap = '4px';
            chipWrap.style.marginRight = '8px';
            chipWrap.style.marginBottom = '8px';

            const chip = document.createElement('button');
            chip.className = 'chip';
            chip.setAttribute('aria-pressed', 'false');
            chip.textContent = p.name;
            chip.dataset.id = p.id;
            chip.style.margin = '0';
            
            const exploreBtn = document.createElement('button');
            exploreBtn.innerHTML = '→';
            exploreBtn.className = 'chip';
            exploreBtn.style.padding = '0.2rem 0.6rem';
            exploreBtn.style.background = 'transparent';
            exploreBtn.style.margin = '0';
            exploreBtn.title = `Explore ${p.name}`;
            exploreBtn.onclick = (e) => { e.stopPropagation(); window.location.hash = `#province/${p.id}`; };
            
            chipWrap.appendChild(chip);
            chipWrap.appendChild(exploreBtn);"""

js = re.sub(old_chip, new_chip, js)

# We also need to change container.appendChild(chip) to container.appendChild(chipWrap)
old_append = r"""container\.appendChild\(chip\);"""
new_append = """container.appendChild(chipWrap);"""

js = re.sub(old_append, new_append, js)

with open("/Users/saikatghosh/.gemini/antigravity/scratch/unseencanada/webapp/app.js", "w") as f:
    f.write(js)
