import re

with open("/Users/saikatghosh/.gemini/antigravity/scratch/unseencanada/webapp/app.js", "r") as f:
    js = f.read()

# Replace the drawing of the Pill with the new Bangladesh-style label
old_pill = r"""                    // Draw Pill
                    ctx\.font = '700 14px Inter, -apple-system, sans-serif';
                    const textWidth = ctx\.measureText\(p\.name\)\.width;
                    const paddingX = 12;
                    const paddingY = 8;
                    
                    ctx\.fillStyle = theme\.primary;
                    ctx\.beginPath\(\);
                    ctx\.roundRect\(drawX - textWidth/2 - paddingX, drawY - 10 - paddingY, textWidth \+ paddingX\*2, 20 \+ paddingY\*2, 20\);
                    ctx\.fill\(\);
                    
                    // Draw Text
                    ctx\.fillStyle = '#FFFFFF';
                    ctx\.fillText\(p\.name, drawX, drawY\);"""

new_label = """                    // Unseen Bangladesh-style labels
                    // 1. Red location dot
                    ctx.fillStyle = theme.primary;
                    ctx.beginPath();
                    ctx.arc(drawX, drawY + 12, 4, 0, Math.PI * 2);
                    ctx.fill();
                    ctx.strokeStyle = '#FFFFFF';
                    ctx.lineWidth = 1.5;
                    ctx.stroke();
                    
                    // 2. Bold text with white outline
                    ctx.font = '800 16px Inter, -apple-system, sans-serif';
                    
                    // Outline
                    ctx.strokeStyle = '#FFFFFF';
                    ctx.lineWidth = 4;
                    ctx.lineJoin = 'round';
                    ctx.strokeText(p.name, drawX, drawY - 5);
                    
                    // Fill
                    ctx.fillStyle = '#111827'; // Dark text
                    ctx.fillText(p.name, drawX, drawY - 5);"""

js = re.sub(old_pill, new_label, js)

with open("/Users/saikatghosh/.gemini/antigravity/scratch/unseencanada/webapp/app.js", "w") as f:
    f.write(js)
