import xml.etree.ElementTree as ET
import re

svg_content = open("index.html").read()
svg_part = svg_content.split('<svg id="canada-map"')[1].split('</svg>')[0]
svg_part = '<svg id="canada-map"' + svg_part + '</svg>'
root = ET.fromstring(svg_part)

bboxes = {}

for child in root.iter():
    idx = child.attrib.get("id")
    if idx and idx.startswith("CA-"):
        paths = []
        if child.tag.endswith("path"):
            paths.append(child.attrib.get("d"))
        else:
            for p in child.iter():
                if p.tag.endswith("path"):
                    paths.append(p.attrib.get("d"))
                    
        # Find all absolute commands (M, L) roughly
        all_xs = []
        all_ys = []
        for p_str in paths:
            if not p_str: continue
            # find all M <x> <y>
            matches = re.findall(r'[ML]\s*(-?\d+\.?\d*)[,\s]*(-?\d+\.?\d*)', p_str, re.IGNORECASE)
            for m in matches:
                all_xs.append(float(m[0]))
                all_ys.append(float(m[1]))
                
        if all_xs and all_ys:
            # simple average is the centroid
            cx = sum(all_xs) / len(all_xs)
            cy = sum(all_ys) / len(all_ys)
            bboxes[idx] = {"cx": cx, "cy": cy}

print("const PROVINCE_CENTERS = {")
for k, v in bboxes.items():
    print(f"  '{k}': {{ cx: {v['cx']:.1f}, cy: {v['cy']:.1f} }},")
print("};")
