#!/usr/bin/env python3
"""Shared builder for every Pine Hill page.

The homepage proved which approach survives on this site: native Elementor
widgets for the content, and one page stylesheet that reaches them through
BOTH a semantic class and the element id Elementor actually renders. Every
page below is built the same way, so they share one visual system and one set
of bugs rather than nine.

  - ids are namespaced per page and per section, so removing a section never
    renumbers anything outside it
  - resolve() rewrites `.ph-name` into a plain comma list that also names the
    concrete element ids, because _css_classes is the half we cannot prove
    reaches every element type
  - every value only Abigail can supply is written with fill() so it shows up
    on the page as an obvious blank, never as an invented fact
"""
import json, re

U = "https://www.pinehillgermanshepherds.com/wp-content/uploads"

# Real photographs from her library. No stock, no placeholders.
IMG = {
    "hero_sunset":  f"{U}/2026/07/hero-sunset.jpg",
    "freda":        f"{U}/2026/04/Freda-3.jpg",
    "working":      f"{U}/2026/09/BK706350-scaled.jpg",
    "montie":       f"{U}/2026/04/Cruz-AKC-German-Shepherd-dog-in-NH--scaled.jpg",
    "litter_band":  f"{U}/2026/09/BK700068-scaled.jpg",
    "puppies":      f"{U}/2024/10/AKC-German-Shepherd-Puppies-for-Sale-in-Maine-Pine-Hill-German-Shepherd-Breeders-scaled.jpg",
    "scholars":     f"{U}/2025/01/AKC-East-Working-Line-German-Shepherd-Puppies-for-Sale-in-Maine-Pine-Hill-German-Shepherds-scaled.jpg",
    "rangley1":     f"{U}/2026/08/Rangley-1-1-scaled.jpg",
    "rangley2":     f"{U}/2026/08/Rangley-2-scaled.jpg",
    "rangley3":     f"{U}/2026/08/Rangley-3-scaled.jpg",
    "rangley4":     f"{U}/2026/08/Rangley-4-scaled.jpg",
    "rangley5":     f"{U}/2026/08/Rrangley-5-scaled.jpg",
    "rangley6":     f"{U}/2026/08/Rangley-6-scaled.jpg",
    "rangley7":     f"{U}/2026/08/Rangley-7-scaled.jpg",
    "portrait":     f"{U}/2026/09/BK700074-Edit-scaled.jpg",
    "pair":         f"{U}/2026/09/BK706246-Edit-scaled.jpg",
    "farm":         f"{U}/2026/09/AB9405DB-D650-4947-A274-59A0754E55A6-scaled.jpg",
    "wks":          f"{U}/2026/04/WKS-scaled.jpg",
    "breeders":     f"{U}/2026/03/EN7A9779-scaled.jpg",
    "sunlit":       f"{U}/2026/07/EN7A8251-scaled-Edit-scaled.jpg",
    "family":       f"{U}/2026/09/Pine-Hill-German-Shepherds-scaled.jpg",
    "band2":        f"{U}/2026/09/BK700064-scaled.jpg",
}

ALT = {
    "freda": "Freda von Stephanitz, our foundation female",
    "working": "AKC working-line German Shepherd in Maine",
    "montie": "Captain Montie, IGP and personal protection",
    "puppies": "German Shepherd puppies raised with Puppy Culture",
    "scholars": "Puppies in the K9 Scholars training programme",
    "portrait": "Working-line German Shepherd portrait",
    "farm": "Pine Hill, Garland, Maine",
    "family": "Pine Hill German Shepherds",
}

# --------------------------------------------------------------------- state
_PAGE = ["x"]
_SEC = ["x"]
_N = [0]
INDEX = {}


def start(page):
    """Begin a page. Clears the class index so each page resolves on its own."""
    _PAGE[0] = page
    INDEX.clear()


def section(name):
    _SEC[0] = name
    _N[0] = 0


def eid(kind):
    _N[0] += 1
    return f"{_PAGE[0]}{_SEC[0]}{kind}{_N[0]:02d}"


def _record(i, classes):
    for c in classes.split():
        INDEX.setdefault(c, []).append(i)


# ------------------------------------------------------------------ builders
def con(children, classes="", **settings):
    i = eid("c")
    s = {"content_width": "full", "flex_direction": "column"}
    s.update(settings)
    if classes:
        s["_css_classes"] = classes
        _record(i, classes)
    return {"id": i, "elType": "container", "settings": s,
            "elements": children, "isInner": False}


def row(children, classes="", **settings):
    return con(children, classes, flex_direction="row", **settings)


def w(widget_type, settings, classes=""):
    i = eid("w")
    s = dict(settings)
    if classes:
        s["_css_classes"] = classes
        _record(i, classes)
    return {"id": i, "elType": "widget", "widgetType": widget_type,
            "settings": s, "elements": []}


def h(text, classes="", tag="h2"):
    return w("heading", {"title": text, "header_size": tag}, classes)


def p(html, classes=""):
    return w("text-editor", {"editor": f"<p>{html}</p>"}, classes)


def ul(items, classes="ph-list"):
    body = "".join(f"<li>{x}</li>" for x in items)
    return w("text-editor", {"editor": f"<ul>{body}</ul>"}, classes)


def dl(pairs, classes="ph-facts"):
    """A labelled fact table - the shape a buyer scans for."""
    rows = "".join(f"<li><span>{k}</span><em>{v}</em></li>" for k, v in pairs)
    return w("text-editor", {"editor": f"<ul>{rows}</ul>"}, classes)


def btn(text, url, classes="", variant=""):
    cls = (classes + " " + variant).strip()
    return w("button", {"text": text,
                        "link": {"url": url, "is_external": "", "nofollow": ""}}, cls)


def img(key, classes="ph-frame", alt=None):
    return w("image", {"image": {"url": IMG[key], "id": 0, "size": "",
                                 "alt": alt or ALT.get(key, ""), "source": "library"},
                       "image_size": "full"}, classes)


def rule(centred=False):
    return w("divider", {"style": "solid"}, "ph-rule" + (" ph-rule--c" if centred else ""))


def spacer(px=24):
    return w("spacer", {"space": {"unit": "px", "size": px, "sizes": []}})


def fill(label):
    """A value only she can supply. Renders as a visible blank, never a guess."""
    return f"<span class='ph-fill'>{label}</span>"


def pill(text, tone="open"):
    return p(f"<span class='ph-pill ph-pill--{tone}'>{text}</span>", "ph-pillwrap")


# ------------------------------------------------------------- page sections
def hero(title, kicker, image_key, ypos=70, button=None, tall=True):
    section("hero")
    kids = [h(title, tag="h1")]
    if kicker:
        kids.insert(0, p(kicker, "ph-script"))
    if button:
        kids.append(btn(button[0], button[1]))
    return con([con(kids, "ph-hero__in")],
               "ph-hero" + ("" if tall else " ph-hero--slim"),
               background_background="classic",
               background_image={"url": IMG[image_key], "id": 0, "size": "",
                                 "alt": "", "source": "library"},
               background_position=f"center {ypos}%",
               background_size="cover")


def sec(children, name, tone="white", tight=False, extra=""):
    section(name)
    cls = f"ph-sec ph-{tone}" + (" ph-sec--tight" if tight else "")
    if extra:
        cls += " " + extra
    return con(children, cls)


def head(kicker, title, lede=None, centred=True):
    kids = []
    if kicker:
        kids.append(p(kicker, "ph-script"))
    kids.append(h(title))
    kids.append(rule(centred))
    if lede:
        kids.append(p(lede, "ph-lede"))
    return con(kids, "ph-head" if centred else "ph-headL")


def split(left, right, reverse=False):
    a, b = (right, left) if reverse else (left, right)
    return row([a, b], "ph-split", flex_align_items="center")


def col(children, classes="ph-col"):
    return con(children, classes)


def trio(cards):
    return row(cards, "ph-trio")


def quad(cards):
    return row(cards, "ph-quad")


def card(children, classes="ph-card"):
    return con(children, classes)


def stat(value, label):
    return con([p(value, "ph-stat__v"), p(label, "ph-stat__l")], "ph-stat")


def steps(items):
    """items: list of (marker, title, body). Numbered only where order is real."""
    return row([con([p(m, "ph-step__n"), h(t, tag="h4", classes="ph-step__t"),
                     p(b)], "ph-step") for m, t, b in items], "ph-steps")


def faq(items):
    out = []
    for q, a in items:
        out.append(h(q, "ph-q", tag="h3"))
        out.append(p(a, "ph-a"))
    return con(out, "ph-faq")


def cta(title, body, label, url, image_key=None):
    section("cta")
    inner = con([h(title), p(body, "ph-lede"), btn(label, url)], "ph-cta__in")
    if image_key:
        return con([inner], "ph-band",
                   background_background="classic",
                   background_image={"url": IMG[image_key], "id": 0, "size": "",
                                     "alt": "", "source": "library"},
                   background_position="center 60%", background_size="cover")
    return con([inner], "ph-sec ph-sand ph-cta")


# ------------------------------------------------------------------ the css
CSS = """@font-face{font-family:'Mrs Saint Delafield';font-style:normal;font-weight:400;font-display:swap;
 src:url(https://fonts.gstatic.com/s/mrssaintdelafield/v14/v6-IGZDIOVXH9xtmTZfRagunqBw5WC62QKknLw.woff2) format('woff2')}
body{--espresso:#1C1A18;--ivory:#F6F4F1;--linen:#F2F0EC;--sand:#DCD8D1;--sage:#232020;
 --sage-deep:#3A3633;--brass:#7C7369;--body:#55504A;--hair:rgba(28,26,24,.12);
 --gut:clamp(24px,5vw,56px);--wrap:1180px;--sy:clamp(60px,7vw,100px);
 background:#FFFFFF;color:var(--body)}

.elementor-widget-heading .elementor-heading-title{font-family:'Cormorant Garamond',Georgia,serif!important;
 font-weight:500!important;color:var(--espresso)!important;letter-spacing:-.015em!important;
 line-height:1.12!important;margin:0!important;font-size:clamp(26px,2.9vw,38px)!important}
.elementor-widget-text-editor,.elementor-widget-text-editor p,.elementor-widget-text-editor li{
 font-family:'Montserrat',system-ui,sans-serif!important;font-size:14.5px!important;
 line-height:1.85!important;color:var(--body)!important;margin:0!important}
.ph-script,.ph-script p{font-family:'Mrs Saint Delafield',cursive!important;color:var(--brass)!important;
 font-size:clamp(34px,3.8vw,48px)!important;line-height:1.1!important}
.ph-lede p{font-size:15px!important}
.ph-measure p{max-width:62ch}

.elementor-button{background-color:var(--sage)!important;color:var(--ivory)!important;
 font-family:'Montserrat',system-ui,sans-serif!important;font-size:10.5px!important;font-weight:500!important;
 letter-spacing:.2em!important;text-transform:uppercase!important;border-radius:0!important;
 padding:17px 34px!important;transition:transform .3s cubic-bezier(.22,.9,.32,1),background-color .25s ease}
.elementor-button:hover,.elementor-button:focus{background-color:var(--sage-deep)!important;
 color:var(--ivory)!important;transform:translateY(-2px)}
.elementor-button:focus-visible{outline:2px solid var(--brass)!important;outline-offset:3px!important}
.ph-ghost .elementor-button{background:transparent!important;color:var(--espresso)!important;
 border:1px solid var(--espresso)!important}
.ph-ghost .elementor-button:hover{background:var(--espresso)!important;color:var(--ivory)!important}

.ph-rule .elementor-divider{padding-block:10px!important}
.ph-rule .elementor-divider-separator{border-top:1px solid var(--brass)!important;width:56px!important;margin:0!important}
.ph-rule--c .elementor-divider{justify-content:center!important}

.ph-sec{padding:var(--sy) var(--gut)!important;gap:0!important}
.ph-sec--tight{padding-block:clamp(44px,4.6vw,68px)!important}
.ph-white{background-color:#FFFFFF!important}
.ph-linen{background-color:var(--linen)!important}
.ph-sand{background-color:var(--sand)!important}

.ph-hero{position:relative!important;min-height:clamp(420px,56vh,620px)!important;display:flex!important;
 flex-direction:column!important;justify-content:flex-end!important;align-items:flex-start!important;
 padding:120px clamp(56px,7vw,110px) clamp(48px,7vh,88px) var(--gut)!important;
 background-repeat:no-repeat!important;overflow:hidden!important}
.ph-hero--slim{min-height:clamp(280px,34vh,380px)!important;justify-content:center!important;
 padding-block:clamp(72px,9vh,110px) clamp(40px,5vh,60px)!important}
.ph-hero::after{content:''!important;position:absolute!important;inset:0!important;z-index:1!important;
 pointer-events:none!important;
 background:linear-gradient(100deg,rgba(26,19,13,.66) 0%,rgba(26,19,13,.36) 42%,rgba(26,19,13,.06) 78%)!important}
.ph-hero>*{position:relative!important;z-index:2!important}
.ph-hero__in{max-width:640px!important;width:auto!important;gap:10px!important;
 align-items:flex-start!important;padding:0!important}
.ph-hero .elementor-heading-title{color:#FFFFFF!important;font-size:clamp(28px,3.4vw,44px)!important;
 line-height:1.06!important;letter-spacing:-.02em!important}
.ph-hero .ph-script p{color:rgba(246,244,241,.92)!important;
 font-size:clamp(26px,2.4vw,32px)!important;margin-bottom:2px!important}

.ph-head{max-width:820px!important;margin-inline:auto!important;align-items:center!important;
 text-align:center!important;gap:10px!important;padding:0 0 48px!important}
.ph-headL{max-width:760px!important;align-items:flex-start!important;gap:10px!important;padding:0 0 40px!important}
.ph-split{display:flex!important;flex-direction:row!important;align-items:center!important;
 gap:clamp(32px,4.5vw,72px)!important;max-width:var(--wrap)!important;width:100%!important;
 margin-inline:auto!important;padding:0!important}
.ph-split>*{flex:1 1 0!important;min-width:0!important;width:auto!important}
.ph-col{gap:22px!important;padding:0!important;max-width:none!important;align-items:flex-start!important}
.ph-narrow{max-width:820px!important;margin-inline:auto!important;align-items:center!important;
 text-align:center!important;gap:14px!important;padding:0!important}

.ph-frame img{width:100%!important;height:clamp(380px,40vw,540px)!important;object-fit:cover!important;
 display:block!important;box-shadow:0 2px 6px rgba(28,26,24,.06),0 18px 40px -16px rgba(28,26,24,.20)}
.ph-frame--sq img{height:clamp(300px,30vw,400px)!important}

.ph-trio,.ph-quad{display:flex!important;flex-direction:row!important;
 gap:clamp(20px,2.6vw,36px)!important;max-width:var(--wrap)!important;width:100%!important;
 margin-inline:auto!important;padding:0!important;align-items:stretch!important}
.ph-trio>*,.ph-quad>*{flex:1 1 0!important;min-width:0!important;width:auto!important;
 align-self:stretch!important;height:auto!important}
.ph-split>.ph-card{align-self:stretch!important;height:auto!important}

.ph-card{background:#FFFFFF!important;border:1px solid var(--hair)!important;
 padding:clamp(24px,2.6vw,34px)!important;gap:12px!important;align-items:flex-start!important;
 max-width:none!important}
.ph-linen .ph-card{background:#FFFFFF!important}
.ph-white .ph-card{background:var(--linen)!important;border-color:transparent!important}

.ph-stat{gap:2px!important;padding:0 0 0 16px!important;border-left:1px solid var(--brass)!important;
 align-items:flex-start!important;max-width:none!important}
.ph-stat__v p{font-family:'Cormorant Garamond',Georgia,serif!important;font-size:30px!important;
 color:var(--espresso)!important;line-height:1.1!important}
.ph-stat__l p{font-size:10.5px!important;letter-spacing:.18em!important;text-transform:uppercase!important;
 color:var(--brass)!important}

.ph-steps{display:flex!important;flex-direction:row!important;align-items:flex-start!important;
 gap:clamp(20px,2.6vw,36px)!important;max-width:var(--wrap)!important;width:100%!important;
 margin-inline:auto!important;padding:0!important}
.ph-steps>*{flex:1 1 0!important;min-width:0!important;width:auto!important}
.ph-step{gap:8px!important;padding:14px 0 0!important;border-top:1px solid var(--brass)!important;
 align-items:flex-start!important;max-width:none!important}
.ph-step__n p{font-size:10.5px!important;font-weight:600!important;letter-spacing:.18em!important;
 text-transform:uppercase!important;color:var(--brass)!important}
.ph-step__t .elementor-heading-title{font-size:19px!important;letter-spacing:0!important}
.ph-step p{font-size:13.5px!important;line-height:1.7!important}

.ph-list ul{margin:0;padding:0;list-style:none;display:grid;grid-template-columns:1fr 1fr;gap:6px 24px}
.ph-list li{font-size:13.5px!important;line-height:1.7!important;padding-left:18px;position:relative}
.ph-list li::before{content:'';position:absolute;left:0;top:11px;width:7px;height:1px;background:var(--brass)}
.ph-list--one ul{grid-template-columns:1fr}

.ph-facts ul{margin:0;padding:0;list-style:none;display:flex;flex-direction:column}
.ph-facts li{display:flex;gap:18px;justify-content:space-between;align-items:baseline;
 padding:11px 0;border-bottom:1px solid var(--hair)}
.ph-facts li span{font-size:10.5px!important;letter-spacing:.16em;text-transform:uppercase;
 color:var(--brass);flex:0 0 auto}
.ph-facts li em{font-style:normal;font-size:14px;color:var(--espresso);text-align:right}

.ph-q .elementor-heading-title{font-size:18px!important;letter-spacing:0!important;
 padding-top:22px!important;border-top:1px solid var(--hair)!important;margin-top:4px!important}
.ph-faq{gap:8px!important;max-width:820px!important;margin-inline:auto!important;padding:0!important}
.ph-a p{font-size:14px!important;padding-bottom:6px!important}

.ph-pillwrap{width:auto!important}
.ph-pill{display:inline-block;font-size:9.5px;font-weight:600;letter-spacing:.18em;
 text-transform:uppercase;padding:5px 11px;border:1px solid currentColor}
.ph-pill--open{color:#4A5F46}
.ph-pill--soon{color:#8C6A3C}
.ph-pill--closed{color:#7A5050}

.ph-fill{display:inline-block;min-width:96px;padding:1px 10px;border-bottom:1px dashed var(--brass);
 color:var(--brass);font-style:italic;font-size:13.5px}

.ph-band{position:relative!important;min-height:clamp(360px,44vh,460px)!important;display:flex!important;
 flex-direction:column!important;justify-content:center!important;align-items:center!important;
 padding:clamp(64px,8vw,96px) var(--gut)!important;background-repeat:no-repeat!important;overflow:hidden!important}
.ph-band::after{content:''!important;position:absolute!important;inset:0!important;z-index:1!important;
 pointer-events:none!important;background:rgba(26,19,13,.52)!important}
.ph-band>*{position:relative!important;z-index:2!important}
.ph-band .elementor-heading-title{color:#FFFFFF!important}
.ph-band p{color:rgba(246,244,241,.92)!important}
.ph-cta__in{max-width:640px!important;align-items:center!important;text-align:center!important;
 gap:16px!important;padding:0!important}
.ph-cta .ph-cta__in{align-items:center!important}

@media(max-width:980px){
.ph-trio,.ph-quad{flex-wrap:wrap!important}
.ph-trio>*{flex:1 1 calc(50% - 18px)!important}
.ph-quad>*{flex:1 1 calc(50% - 18px)!important}
}
@media(max-width:880px){
.ph-split{flex-direction:column!important;gap:36px!important}
.ph-trio,.ph-quad,.ph-steps{flex-direction:column!important;flex-wrap:nowrap!important}
.ph-trio>*,.ph-quad>*{flex:1 1 auto!important}
.ph-frame img,.ph-frame--sq img{height:clamp(280px,70vw,360px)!important}
.ph-list ul{grid-template-columns:1fr}
.ph-hero{min-height:clamp(340px,52vh,440px)!important;padding-inline:var(--gut)!important}
.ph-facts li{flex-direction:column;gap:2px}
.ph-facts li em{text-align:left}
}"""


def resolve(css, index=None):
    """Give every .ph-name selector an id twin, as plain comma branches."""
    idx = INDEX if index is None else index
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)

    def expand(sel):
        m = re.match(r"^(\s*)(\.ph-[A-Za-z0-9_-]+)(.*)$", sel, re.S)
        if not m:
            return [sel]
        lead, cls, rest = m.groups()
        ids = idx.get(cls[1:], [])
        tails = expand(rest) if ".ph-" in rest else [rest]
        return [f"{lead}{b}{t}"
                for b in [cls] + [f".elementor-element-{i}" for i in ids]
                for t in tails]

    def sub(m):
        out = []
        for part in m.group(1).split(","):
            out.extend(expand(part))
        return ",".join(out) + m.group(2)

    return re.sub(r"([^{}@]+)(\{)", sub, css).strip()


def minify(css):
    css = re.sub(r"\s*\n\s*", "", css)
    return re.sub(r";\}", "}", css)


def emit(data, extra_css=""):
    return (json.dumps(data, separators=(",", ":")),
            minify(resolve(CSS + "\n" + extra_css)))
