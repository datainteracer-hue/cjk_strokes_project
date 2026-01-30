import json
from pathlib import Path
import re

### CONFIG ###
# Converts makemeahanzi JSON to svg
DIR   = r"C:\Users\User\Downloads\strokeprocess\newCrawl\" + "\\"
OUT   = r"C:\Users\User\Downloads\strokeprocess\newCrawl\output\styleless" + "\\"
OUT2  = r"C:\Users\User\Downloads\strokeprocess\newCrawl\output\style" + "\\"


def increase_y(match):
  x = match.group(1)
  y = match.group(2)
  if "." in y:
    y = float(y) + 100
  else:
    y = int(y) + 100   # increase y by 100
  y -= 100
  return f"{x} {y}"

def svg(name, data):
  output = []
  n = len(data['strokes'])
  svgHead = f'<svg id="z{name}" class="acjk" viewBox="0 0 1024 1024" xmlns="http://www.w3.org/2000/svg">\n'
  # STYLE, for full
  svgStyle = '<style>\n<![CDATA[\n@keyframes zk {\n	to {\n		stroke-dashoffset:0;\n	}\n}\nsvg.acjk path[clip-path] {\n	--t:0.8s;\n	animation:zk var(--t) linear forwards var(--d);\n	stroke-dasharray:3337;\n	stroke-dashoffset:3339;\n	stroke-width:128;\n	stroke-linecap:round;\n	stroke-linejoin:round;\n	fill:none;\n	stroke:#000;\n}\nsvg.acjk path[id] {fill:#ccc;}\n]]>\n</style>\n'
  output.append(svgHead)
  output.append(svgStyle)
  
  for i in range(n):
    path = data['strokes'][i]
    pattern = r"(-?\d+\.?\d*)\s+(-?\d+\.?\d*)"
    path = re.sub(pattern, increase_y, path)
    output.append(f'  <path id="z{name}d{i+1}" d="{path}"/>\n')
  output.append("<defs>\n")
  for i in range(n):
    output.append(f'  <clipPath id="z{name}c{i+1}"><use href="#z{name}d{i+1}"/></clipPath>\n')
  output.append("</defs>\n")
  for i in range(n):
    path = "M " + ' L '.join(map(lambda x: f'{x[0]} {(x[1])}', data['medians'][i]))
    output.append(f'<path style="--d:{i+1}s;" pathLength="3333" clip-path="url(#z{name}c{i+1})" d="{path}"/>\n')
  output.append("</svg>")
  with open(f"{OUT2}zh_{name}.svg", "w") as f:
    f.write(f'{"".join(output)}')
  output.pop(1)
  with open(f"{OUT}zh_{name}.svg", "w") as f:
    f.write(f'{"".join(output)}')
  

path = Path(DIR)

for f in path.glob("*.json"):
  with open(f, 'r') as file:
    name = f.name[:f.name.find(".")]
    data = json.load(file)
    svg(name, data)
    print(f"{f} done")
