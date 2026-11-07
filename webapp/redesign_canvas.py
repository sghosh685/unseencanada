import re

with open("/Users/saikatghosh/.gemini/antigravity/scratch/unseencanada/webapp/app.js", "r") as f:
    content = f.read()

# Replace generateImage body
canvas_logic_old = r'    const drawCard = \(\) => \{.*?URL\.revokeObjectURL\(url\);\n      callback\(canvas\.toDataURL\(\'image/png\'\)\);\n    \};'

canvas_logic_new = r"""    const drawCard = () => {
      loadedImgs++;
      if (loadedImgs < requiredImgs) return;

      canvas.width = 1200;
      canvas.height = 850; // Tighter height
      
      // Background gradient based on theme
      const grad = ctx.createLinearGradient(0, 0, 0, canvas.height);
      grad.addColorStop(0, '#FFFFFF');
      grad.addColorStop(1, theme.bg || '#F9FAFB');
      ctx.fillStyle = grad;
      ctx.fillRect(0, 0, canvas.width, canvas.height);
      
      // Top thick accent line
      ctx.fillStyle = theme.primary;
      ctx.fillRect(0, 0, canvas.width, 24);

      // Header Text & Avatar
      ctx.fillStyle = '#111827';
      ctx.font = '800 64px Inter, -apple-system, sans-serif';
      const nameText = state.user.name ? `${state.user.name}'s Canada` : 'My Canada';
      
      let textX = 60;
      if (avatarImg) {
        ctx.save();
        ctx.beginPath();
        ctx.arc(110, 130, 50, 0, Math.PI * 2);
        ctx.clip();
        ctx.drawImage(avatarImg, 60, 80, 100, 100);
        ctx.restore();
        
        // Avatar border
        ctx.beginPath();
        ctx.arc(110, 130, 50, 0, Math.PI * 2);
        ctx.lineWidth = 4;
        ctx.strokeStyle = theme.primary;
        ctx.stroke();
        
        textX = 190;
      }
      ctx.fillText(nameText, textX, 145);

      // Exploration Score
      const count = state.visitedProvinces.length;
      ctx.fillStyle = theme.primary;
      ctx.font = '800 48px Inter, -apple-system, sans-serif';
      ctx.fillText(`${count} / 13`, 60, 225);
      
      ctx.fillStyle = '#4B5563';
      ctx.font = '700 28px Inter, -apple-system, sans-serif';
      ctx.fillText(`provinces & territories explored`, 190, 222);

      // Progress bar overall
      const pct = count / 13;
      ctx.fillStyle = '#E5E7EB';
      ctx.beginPath(); ctx.roundRect(60, 260, 420, 16, 8); ctx.fill();
      if (pct > 0) {
          ctx.fillStyle = theme.primary;
          ctx.beginPath(); ctx.roundRect(60, 260, 420 * pct, 16, 8); ctx.fill();
      }

      // Map on the Right - make it larger and lower
      // original viewBox 629x609.
      ctx.drawImage(img, 450, 200, 750, 725);

      // List of provinces/territories as visual bars
      let startY = 330;
      const allProv = window.CANADA_DATA.provinces;
      const col1 = allProv.slice(0, 7);
      const col2 = allProv.slice(7, 13);
      
      const drawCol = (items, x, y) => {
        let curY = y;
        items.forEach(p => {
           const visited = state.visitedProvinces.includes(p.id);
           ctx.fillStyle = visited ? '#111827' : '#9CA3AF';
           ctx.font = visited ? '800 20px Inter, -apple-system, sans-serif' : '700 20px Inter, -apple-system, sans-serif';
           
           let displayName = p.name;
           if (displayName === "Newfoundland and Labrador") displayName = "Newfoundland & Lab.";
           if (displayName === "Northwest Territories") displayName = "Northwest Terr.";
           
           ctx.fillText(displayName, x, curY);
           
           // visual bar
           ctx.fillStyle = visited ? theme.primary : '#E5E7EB';
           ctx.beginPath(); ctx.roundRect(x, curY + 14, 180, 6, 3); ctx.fill();
           curY += 55;
        });
      };
      
      drawCol(col1, 60, startY);
      drawCol(col2, 280, startY);

      // Next Adventure
      if (state.user.nextAdventure) {
         ctx.fillStyle = '#4B5563';
         ctx.font = '700 24px Inter, -apple-system, sans-serif';
         ctx.fillText(`Next adventure:`, 60, 750);
         
         ctx.fillStyle = theme.primary;
         ctx.font = '800 32px Inter, -apple-system, sans-serif';
         ctx.fillText(`📍 ${state.user.nextAdventure}`, 60, 790);
      }

      // Footer branding
      ctx.fillStyle = '#9CA3AF';
      ctx.font = '500 18px Inter, -apple-system, sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText('Make your own map at MyCanada.com', canvas.width / 2, 820);

      URL.revokeObjectURL(url);
      callback(canvas.toDataURL('image/png'));
    };"""

content = re.sub(canvas_logic_old, canvas_logic_new, content, flags=re.DOTALL)

with open("/Users/saikatghosh/.gemini/antigravity/scratch/unseencanada/webapp/app.js", "w") as f:
    f.write(content)
