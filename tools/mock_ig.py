#!/usr/bin/env python3
"""Render the homepage's Instagram section against a stand-in for Smash
Balloon's markup, so the strip can be screenshot-tested locally.

The live feed is a plugin shortcode, so the emulator only leaves a grey
box where it goes. This substitutes markup using the plugin's long-stable
hooks, with half the tiles drawn the background-image way and half with a
real <img>, because the page cannot be loaded from here to see which one
6.13 emits - the stylesheet has to survive both.
"""
import base64, json, os, subprocess, sys
sys.path.insert(0, "tools")
import build_elementor as be

S = "/tmp/claude-0/-home-user-abigail-joy-photography/e575f777-2c94-5737-948b-2e39a7522532/scratchpad"
json.dump([be.DATA[-1]], open(f"{S}/ig.json", "w"), separators=(",", ":"))
css = be.resolve(be.CSS + be.CSS_FEED)
if os.environ.get("PH_FLAT") == "1":
    # exactly the bytes the meta write will carry
    css = subprocess.run([sys.executable, "tools/build_elementor.py", "push"],
                         capture_output=True, text=True, check=True).stdout
open(f"{S}/ig.css", "w").write(css)
raw = subprocess.run([sys.executable, "tools/emulate_elementor.py",
                      f"{S}/ig.json", f"{S}/ig.css"],
                     capture_output=True, text=True, check=True).stdout


def swatch(tone, w, h):
    svg = ("<svg xmlns='http://www.w3.org/2000/svg' width='%d' height='%d'>"
           "<rect width='%d' height='%d' fill='%s'/></svg>" % (w, h, w, h, tone))
    return "data:image/svg+xml;base64," + base64.b64encode(svg.encode()).decode()


TONES = ["#6E5B45", "#8A7458", "#4F4438", "#9C8567", "#5C4E3C", "#7E6A50",
         "#3F3830", "#A08A6B", "#6A5A46", "#8F7A5C", "#544738", "#93805F"]
items = []
for i, t in enumerate(TONES):
    if i % 2:
        photo = ('<a class="sbi_photo" href="#" style="background:url(' + swatch(t, 10, 10)
                 + ') no-repeat center center;background-size:cover"></a>')
    else:
        photo = '<a class="sbi_photo" href="#"><img src="' + swatch(t, 400, 500) + '" alt=""></a>'
    items.append(
        '<div class="sbi_item sbi_type_image sbi_new sbi_transition">'
        '<div class="sbi_photo_wrap">' + photo + '</div>'
        '<div class="sbi_info"><div class="sbi_meta"><span>128</span><span>7</span></div>'
        '<div class="sbi_caption_wrap"><p class="sbi_caption">Already so in love. '
        'Now is the time to unfollow if you do not want puppy spam.</p></div></div></div>')

mock = ('<div id="sb_instagram" class="sbi sbi_col_4 sbi_width_resp" style="padding:5px;width:100%">'
        '<div class="sb_instagram_header">header</div>'
        '<div id="sbi_images" style="padding:5px">' + "".join(items) + '</div>'
        '<div id="sbi_load"><a class="sbi_load_btn" href="#">Load More...</a>'
        '<span class="sbi_follow_btn"><a href="#">Follow Us On Instagram!</a></span></div>'
        '</div>')
ph = '<div style="min-height:220px;background:#E8E5DF"></div>'
assert ph in raw, "emulator no longer marks the shortcode slot this way"
out = raw.replace(ph, mock)

b = base64.b64encode(open(f"{S}/msd.woff2", "rb").read()).decode()
head = ("<link rel='stylesheet' href='https://fonts.googleapis.com/css2?"
        "family=Cormorant+Garamond:ital,wght@0,400;0,500;1,500"
        "&family=Montserrat:wght@400;500;600&display=swap'>"
        "<style>@font-face{font-family:'Mrs Saint Delafield';font-style:normal;"
        "font-weight:400;src:url(data:font/woff2;base64," + b + ") format('woff2')}"
        # a stand-in for the footer, so the join at the bottom is visible
        ".mock-foot{background:#F2F0EC;border-top:1px solid rgba(28,26,24,.10);"
        "padding:22px 56px;font:10px/1.6 Montserrat,sans-serif;letter-spacing:.16em;"
        "text-transform:uppercase;color:#55504A}</style>")
out = out.replace("</head>", head + "</head>", 1)
out = out.replace("</body>", '<div class="mock-foot">&copy; 2026 Pine Hill German '
                             'Shepherds</div></body>', 1)
open("design/ig-strip.html", "w").write(out)
print("design/ig-strip.html")
