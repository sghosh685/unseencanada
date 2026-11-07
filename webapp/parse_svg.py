from svg.path import parse_path
import xml.etree.ElementTree as ET

svg_content = open("index.html").read()
svg_part = svg_content.split('<svg id="canada-map"')[1].split('</svg>')[0]
svg_part = '<svg id="canada-map"' + svg_part + '</svg>'
root = ET.fromstring(svg_part)

bboxes = {}

for child in root.iter():
    idx = child.attrib.get("id")
    if idx and idx.startswith("CA-"):
        minx, miny, maxx, maxy = float('inf'), float('inf'), float('-inf'), float('-inf')
        
        paths = []
        if child.tag.endswith("path"):
            paths.append(child.attrib.get("d"))
        else:
            for p in child.iter():
                if p.tag.endswith("path"):
                    paths.append(p.attrib.get("d"))
                    
        for p_str in paths:
            if not p_str: continue
            path = parse_path(p_str)
            for seg in path:
                # evaluate at multiple t to find bbox
                for t in range(0, 11):
                    pt = seg.point(t/10.0)
                    minx = min(minx, pt.real)
                    maxx = max(maxx, pt.real)
                    miny = min(miny, pt.imag)
                    maxy = max(maxy, pt.imag)
                    
        if minx != float('inf'):
            bboxes[idx] = {"x": minx, "y": miny, "width": maxx - minx, "height": maxy - miny}

print("const HARDCODED_BBOXES = {")
for k, v in bboxes.items():
    print(f"  '{k}': {{ x: {v['x']:.1f}, y: {v['y']:.1f}, width: {v['width']:.1f}, height: {v['height']:.1f} }},")
print("};")
