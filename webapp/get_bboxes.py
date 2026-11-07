import xml.etree.ElementTree as ET
import re

svg_content = open("index.html").read()
svg_part = svg_content.split('<svg id="canada-map"')[1].split('</svg>')[0]
svg_part = '<svg id="canada-map"' + svg_part + '</svg>'

def parse_path(d):
    # Extremely basic approximation: just extract all numbers and treat as x, y alternately
    nums = [float(x) for x in re.findall(r'-?\d+\.?\d*', d)]
    if not nums: return None
    # x are even indices, y are odd
    xs = nums[0::2]
    ys = nums[1::2]
    return (min(xs), min(ys), max(xs), max(ys))

root = ET.fromstring(svg_part)
ns = {'svg': 'http://www.w3.org/2000/svg'}

bboxes = {}

# The provinces are either <g> with <path>s or directly <path>
for child in root.iter():
    idx = child.attrib.get("id")
    if idx and idx.startswith("CA-"):
        # find all paths inside
        paths = []
        if child.tag.endswith("path"):
            paths.append(child.attrib.get("d"))
        else:
            for p in child.iter():
                if p.tag.endswith("path"):
                    paths.append(p.attrib.get("d"))
        
        all_xs = []
        all_ys = []
        for p in paths:
            if not p: continue
            res = parse_path(p)
            if res:
                all_xs.extend([res[0], res[2]])
                all_ys.extend([res[1], res[3]])
        
        if all_xs and all_ys:
            minx, miny, maxx, maxy = min(all_xs), min(all_ys), max(all_xs), max(all_ys)
            bboxes[idx] = {"x": minx, "y": miny, "width": maxx - minx, "height": maxy - miny}

print("const HARDCODED_BBOXES = {")
for k, v in bboxes.items():
    print(f"  '{k}': {{ x: {v['x']:.1f}, y: {v['y']:.1f}, width: {v['width']:.1f}, height: {v['height']:.1f} }},")
print("};")
