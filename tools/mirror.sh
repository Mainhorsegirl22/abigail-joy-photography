#!/bin/bash
set -e
S=/tmp/claude-0/-home-user-abigail-joy-photography/e575f777-2c94-5737-948b-2e39a7522532/scratchpad
cd /home/user/abigail-joy-photography/tools
for pg in "$@"; do
  python3 build_pages.py $pg data > $S/$pg.json
  python3 build_pages.py $pg css  > $S/$pg.css
  python3 emulate_elementor.py $S/$pg.json $S/$pg.css > $S/$pg.raw.html
  python3 - "$pg" <<'PY'
import base64,sys,os
S="/tmp/claude-0/-home-user-abigail-joy-photography/e575f777-2c94-5737-948b-2e39a7522532/scratchpad"
pg=sys.argv[1]
b=base64.b64encode(open(S+"/msd.woff2","rb").read()).decode()
s=open(f"{S}/{pg}.raw.html").read()
head=("<link rel='stylesheet' href='https://fonts.googleapis.com/css2?"
 "family=Cormorant+Garamond:ital,wght@0,400;0,500;1,500&family=Montserrat:wght@400;500;600&display=swap'>"
 "<style>@font-face{font-family:'Mrs Saint Delafield';font-style:normal;font-weight:400;"
 f"src:url(data:font/woff2;base64,{b}) format('woff2')}}</style>")
s=s.replace("</head>", head+"</head>",1)
open(f"/home/user/abigail-joy-photography/design/{pg}.html","w").write(s)
print("design/%s.html"%pg)
PY
done
