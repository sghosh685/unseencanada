import re

with open("/Users/saikatghosh/.gemini/antigravity/scratch/unseencanada/webapp/app.js", "r") as f:
    js = f.read()

# Fix font size in canvas
old_font = r"""ctx\.font = '700 22px Inter, -apple-system, sans-serif';"""
new_font = """ctx.font = '700 14px Inter, -apple-system, sans-serif';"""

js = re.sub(old_font, new_font, js)

# Fix padding for pills
old_rect = r"""const paddingX = 20;
                    const paddingY = 12;
                    
                    ctx\.fillStyle = theme\.primary;
                    ctx\.beginPath\(\);
                    ctx\.roundRect\(drawX - textWidth/2 - paddingX, drawY - 14 - paddingY, textWidth \+ paddingX\*2, 28 \+ paddingY\*2, 25\);"""
new_rect = """const paddingX = 12;
                    const paddingY = 8;
                    
                    ctx.fillStyle = theme.primary;
                    ctx.beginPath();
                    ctx.roundRect(drawX - textWidth/2 - paddingX, drawY - 10 - paddingY, textWidth + paddingX*2, 20 + paddingY*2, 20);"""

js = re.sub(old_rect, new_rect, js)

with open("/Users/saikatghosh/.gemini/antigravity/scratch/unseencanada/webapp/app.js", "w") as f:
    f.write(js)
