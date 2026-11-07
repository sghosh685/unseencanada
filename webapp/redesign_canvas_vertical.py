import re

with open("/Users/saikatghosh/.gemini/antigravity/scratch/unseencanada/webapp/app.js", "r") as f:
    content = f.read()

# Replace generateImage body
canvas_logic_old = r'    const drawCard = \(\) => \{.*?URL\.revokeObjectURL\(url\);\n      callback\(canvas\.toDataURL\(format\)\);\n    \};'

canvas_logic_new = r"""    const drawCard = () => {
      loadedImgs++;
      if (loadedImgs < requiredImgs) return;

      canvas.width = 1080;
      canvas.height = 1350; // Instagram portrait ratio (4:5)
      
      // Background
      const grad = ctx.createLinearGradient(0, 0, 0, canvas.height);
      grad.addColorStop(0, '#FFFFFF');
      grad.addColorStop(1, theme.bg || '#F9FAFB');
      ctx.fillStyle = grad;
      ctx.fillRect(0, 0, canvas.width, canvas.height);
      
      // Top accent
      ctx.fillStyle = theme.primary;
      ctx.fillRect(0, 0, canvas.width, 24);

      // Header
      const nameText = state.user.name ? `${state.user.name}'s Canada` : 'My Canada';
      ctx.fillStyle = '#111827';
      ctx.font = '800 64px Inter, -apple-system, sans-serif';
      
      let textX = 80;
      if (avatarImg) {
        ctx.save();
        ctx.beginPath();
        ctx.arc(130, 150, 60, 0, Math.PI * 2);
        ctx.clip();
        ctx.drawImage(avatarImg, 70, 90, 120, 120);
        ctx.restore();
        
        ctx.beginPath();
        ctx.arc(130, 150, 60, 0, Math.PI * 2);
        ctx.lineWidth = 4;
        ctx.strokeStyle = theme.primary;
        ctx.stroke();
        textX = 220;
      }
      ctx.fillText(nameText, textX, 175);

      // Score on the right
      const count = state.visitedProvinces.length;
      ctx.fillStyle = theme.primary;
      ctx.font = '800 64px Inter, -apple-system, sans-serif';
      ctx.textAlign = 'right';
      ctx.fillText(`${count} / 13`, 1000, 175);
      
      // Reset align
      ctx.textAlign = 'left';

      // Map (huge, centered)
      // original viewBox 629x609. Let's make it 900x870.
      const mapX = 90;
      const mapY = 280;
      const mapW = 900;
      const mapH = 870;
      ctx.drawImage(img, mapX, mapY, mapW, mapH);

      // Draw Labels on the Map Canvas!
      const showNames = document.getElementById('toggle-names')?.checked !== false;
      if (showNames) {
        const vw = 629; const vh = 609;
        
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        
        window.CANADA_DATA.provinces.forEach(p => {
          if (state.visitedProvinces.includes(p.id)) {
            const el = document.getElementById(p.id);
            if (el && typeof el.getBBox === 'function') {
                try {
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
                    
                    const drawX = mapX + (cx / vw) * mapW;
                    const drawY = mapY + (cy / vh) * mapH;
                    
                    // Draw Pill
                    ctx.font = '700 22px Inter, -apple-system, sans-serif';
                    const textWidth = ctx.measureText(p.name).width;
                    const paddingX = 20;
                    const paddingY = 12;
                    
                    ctx.fillStyle = theme.primary;
                    ctx.beginPath();
                    ctx.roundRect(drawX - textWidth/2 - paddingX, drawY - 14 - paddingY, textWidth + paddingX*2, 28 + paddingY*2, 25);
                    ctx.fill();
                    
                    // Draw Text
                    ctx.fillStyle = '#FFFFFF';
                    ctx.fillText(p.name, drawX, drawY);
                } catch(e) {}
            }
          }
        });
      }
      ctx.textAlign = 'left';
      ctx.textBaseline = 'alphabetic';

      // Footer Area
      const footerY = 1220;
      
      // Next Adventure
      if (state.user.nextAdventure) {
         ctx.fillStyle = '#4B5563';
         ctx.font = '700 28px Inter, -apple-system, sans-serif';
         ctx.fillText(`Next adventure:`, 80, footerY);
         
         ctx.fillStyle = theme.primary;
         ctx.font = '800 36px Inter, -apple-system, sans-serif';
         ctx.fillText(`📍 ${state.user.nextAdventure}`, 80, footerY + 45);
      }

      // Progress bar overall
      const pct = count / 13;
      ctx.fillStyle = '#E5E7EB';
      ctx.beginPath(); ctx.roundRect(580, footerY - 5, 420, 16, 8); ctx.fill();
      if (pct > 0) {
          ctx.fillStyle = theme.primary;
          ctx.beginPath(); ctx.roundRect(580, footerY - 5, 420 * pct, 16, 8); ctx.fill();
      }
      
      ctx.fillStyle = '#4B5563';
      ctx.font = '700 24px Inter, -apple-system, sans-serif';
      ctx.fillText(`${Math.round(pct * 100)}% of Canada explored`, 580, footerY + 40);

      // Domain branding
      ctx.fillStyle = '#9CA3AF';
      ctx.font = '600 20px Inter, -apple-system, sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText('Make your own map at MyCanada.com', canvas.width / 2, 1310);

      URL.revokeObjectURL(url);
      callback(canvas.toDataURL(format));
    };"""

content = re.sub(canvas_logic_old, canvas_logic_new, content, flags=re.DOTALL)

with open("/Users/saikatghosh/.gemini/antigravity/scratch/unseencanada/webapp/app.js", "w") as f:
    f.write(content)
