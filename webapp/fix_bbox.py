import re

with open("/Users/saikatghosh/.gemini/antigravity/scratch/unseencanada/webapp/app.js", "r") as f:
    content = f.read()

old_bbox = r"""                    const bbox = el\.getBBox\(\);
                    let cx = bbox\.x \+ bbox\.width / 2;
                    let cy = bbox\.y \+ bbox\.height / 2;"""

new_bbox = """                    const bbox = el.getBBox();
                    if (bbox.width === 0 && bbox.height === 0) throw new Error("Zero BBox");
                    let cx = bbox.x + bbox.width / 2;
                    let cy = bbox.y + bbox.height / 2;"""

content = re.sub(old_bbox, new_bbox, content)

with open("/Users/saikatghosh/.gemini/antigravity/scratch/unseencanada/webapp/app.js", "w") as f:
    f.write(content)
