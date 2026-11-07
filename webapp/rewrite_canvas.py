import re

with open("/Users/saikatghosh/.gemini/antigravity/scratch/unseencanada/webapp/app.js", "r") as f:
    content = f.read()

new_generate_image = """
  function generateImage(callback) {
    const svg = document.getElementById('canada-map');
    if (!svg) return;

    // Clone SVG to modify it for rendering
    const clonedSvg = svg.cloneNode(true);
    // Make sure we have proper CSS on the cloned SVG before serializing
    const style = document.createElement('style');
    const theme = window.CANADA_DATA.themes[state.user.themeIndex] || window.CANADA_DATA.themes[0];
    
    // Create the visual styling purely for the export
    style.innerHTML = `
      path { fill: #E5E7EB; stroke: #FFFFFF; stroke-width: 1.5px; }
      path.visited { fill: ${theme.primary}; }
    `;
    clonedSvg.insertBefore(style, clonedSvg.firstChild);

    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');
    
    const svgData = new XMLSerializer().serializeToString(clonedSvg);
    const img = new Image();
    const svgBlob = new Blob([svgData], { type: 'image/svg+xml;charset=utf-8' });
    const url = URL.createObjectURL(svgBlob);

    // Profile photo logic
    let avatarImg = null;
    if (state.user.photo) {
      avatarImg = new Image();
      avatarImg.src = state.user.photo;
    }

    // Wait for map and optionally avatar to load
    let loadedImgs = 0;
    const requiredImgs = avatarImg ? 2 : 1;

    const drawCard = () => {
      loadedImgs++;
      if (loadedImgs < requiredImgs) return;

      canvas.width = 1200;
      canvas.height = 1000;
      
      // Background gradient based on theme
      const grad = ctx.createLinearGradient(0, 0, 0, canvas.height);
      grad.addColorStop(0, '#FFFFFF');
      grad.addColorStop(1, theme.bg || '#F9FAFB');
      ctx.fillStyle = grad;
      ctx.fillRect(0, 0, canvas.width, canvas.height);
      
      // Top Border
      ctx.fillStyle = theme.primary;
      ctx.fillRect(0, 0, canvas.width, 16);

      // Map on the Right
      ctx.drawImage(img, 520, 100, 640, 500);

      // Header Text
      ctx.fillStyle = '#111827';
      ctx.font = 'bold 54px -apple-system, sans-serif';
      const name = state.user.name ? `${state.user.name}'s Canada` : 'My Canada';
      
      // Avatar
      if (avatarImg) {
        ctx.save();
        ctx.beginPath();
        ctx.arc(100, 100, 48, 0, Math.PI * 2);
        ctx.clip();
        ctx.drawImage(avatarImg, 52, 52, 96, 96);
        ctx.restore();
        ctx.fillText(name, 170, 115);
      } else {
        ctx.fillText("🇨🇦 " + name, 60, 115);
      }

      // Exploration Count
      const count = state.visitedProvinces.length;
      ctx.fillStyle = theme.primary;
      ctx.font = 'bold 36px -apple-system, sans-serif';
      ctx.fillText(`${count} / 13`, 60, 180);
      
      ctx.fillStyle = '#4B5563';
      ctx.font = '600 24px -apple-system, sans-serif';
      ctx.fillText(`provinces & territories explored`, 180, 178);

      // Progress bar overall
      const pct = count / 13;
      ctx.fillStyle = '#E5E7EB';
      ctx.beginPath(); ctx.roundRect(60, 210, 400, 12, 6); ctx.fill();
      ctx.fillStyle = theme.primary;
      ctx.beginPath(); ctx.roundRect(60, 210, 400 * pct, 12, 6); ctx.fill();

      // List of provinces/territories as visual bars
      ctx.font = '600 20px -apple-system, sans-serif';
      let startY = 280;
      
      // Draw two columns for provinces list
      const allProv = window.CANADA_DATA.provinces;
      const col1 = allProv.slice(0, 7);
      const col2 = allProv.slice(7, 13);
      
      const drawCol = (items, x, y) => {
        let curY = y;
        items.forEach(p => {
           const visited = state.visitedProvinces.includes(p.id);
           ctx.fillStyle = visited ? '#111827' : '#9CA3AF';
           ctx.fillText(p.name, x, curY);
           
           // visual bar
           ctx.fillStyle = visited ? theme.primary : '#E5E7EB';
           ctx.beginPath(); ctx.roundRect(x, curY + 12, 200, 8, 4); ctx.fill();
           curY += 60;
        });
      };
      
      drawCol(col1, 60, startY);
      drawCol(col2, 300, startY);

      // Next Adventure
      if (state.user.nextAdventure) {
         ctx.fillStyle = '#4B5563';
         ctx.font = '600 24px -apple-system, sans-serif';
         ctx.fillText(`Next adventure:`, 60, 760);
         
         ctx.fillStyle = theme.primary;
         ctx.font = 'bold 32px -apple-system, sans-serif';
         ctx.fillText(`📍 ${state.user.nextAdventure}`, 60, 800);
      }

      // Footer branding
      ctx.fillStyle = '#6B7280';
      ctx.font = '18px -apple-system, sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText('Make your own map at MyCanada.com', canvas.width / 2, 950);

      URL.revokeObjectURL(url);
      callback(canvas.toDataURL('image/png'));
    };

    img.onload = drawCard;
    if (avatarImg) {
      avatarImg.onload = drawCard;
      avatarImg.onerror = drawCard; // fallback
    }
  }
"""

# Now we replace the old generateImage block.
# We'll use regex to replace from "function generateImage(callback) {" up to "img.src = url;\n  }"
pattern = re.compile(r"function generateImage\(callback\) \{.*?img\.src = url;\n  \}", re.DOTALL)
new_content = pattern.sub(new_generate_image.strip(), content)

with open("/Users/saikatghosh/.gemini/antigravity/scratch/unseencanada/webapp/app.js", "w") as f:
    f.write(new_content)
