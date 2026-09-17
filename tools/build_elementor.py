#!/usr/bin/env python3
"""Emit the Pine Hill homepage as native Elementor widgets.

Every line of copy, every photograph and every button is its own widget, so the
owner edits them from the Elementor panel without touching code.

The layout rule of this file: **containers are styled by Elementor, widgets are
styled by the stylesheet.**

Elementor compiles each container's settings into its own CSS, keyed to the id
it actually renders, and shows those same settings in the editor panel. Padding,
backgrounds, column splits and stacking therefore cannot drift out of step with
the markup, and she can change any of them by clicking the section. The
stylesheet is left with only what Elementor has no control for - type, the
divider rule, image cropping, the icon circles - all of which sit on widgets.

  python3 build_elementor.py data  -> _elementor_data JSON
  python3 build_elementor.py css   -> the page stylesheet (Elementor Custom CSS)
  python3 build_elementor.py index -> semantic class -> element ids
"""
import json, re, sys

U = "https://www.pinehillgermanshepherds.com/wp-content/uploads"
M = {
 "hero":     f"{U}/2026/07/hero-sunset.jpg",
 "frida":    f"{U}/2026/04/Freda-3.jpg",
 "working":  f"{U}/2026/09/BK706350-scaled.jpg",
 "puppies":  f"{U}/2024/10/AKC-German-Shepherd-Puppies-for-Sale-in-Maine-Pine-Hill-German-Shepherd-Breeders-scaled.jpg",
 "scholars": f"{U}/2025/01/AKC-East-Working-Line-German-Shepherd-Puppies-for-Sale-in-Maine-Pine-Hill-German-Shepherds-scaled.jpg",
 "montie":   f"{U}/2026/04/Cruz-AKC-German-Shepherd-dog-in-NH--scaled.jpg",
 "band":     f"{U}/2026/09/BK700068-scaled.jpg",
}
ALT = {
 "frida": "Frida, our foundation female at Pine Hill German Shepherds",
 "working": "AKC working-line German Shepherd in Maine",
 "puppies": "German Shepherd puppies raised with Puppy Culture",
 "scholars": "K9 Scholars training program",
 "montie": "Captain Montie, IGP and personal protection",
}

# ------------------------------------------------------------------ plumbing
# Ids are namespaced per section and numbered within it, so adding or removing
# a whole section never renumbers any other section.
SECTION = ["x"]
_n = [0]
INDEX = {}          # semantic class -> [element ids that carry it]

def section(name):
    SECTION[0] = name
    _n[0] = 0

def eid(prefix):
    _n[0] += 1
    return f"ph{SECTION[0]}{prefix}{_n[0]:02d}"

def _record(i, classes):
    for c in classes.split():
        INDEX.setdefault(c, []).append(i)

# ------------------------------------------------- native container settings
# Everything below is an Elementor control, not CSS. Elementor compiles these
# against whatever id it renders, and every one of them shows up in the editor
# panel where she can change it.
def dim(t, r, b, l, unit="px"):
    return {"unit": unit, "top": str(t), "right": str(r), "bottom": str(b),
            "left": str(l), "isLinked": False}

def size(n, unit="px"):
    return {"unit": unit, "size": n, "sizes": []}

def gap(col, row=None):
    row = col if row is None else row
    return {"unit": "px", "size": col, "column": str(col), "row": str(row),
            "isLinked": row == col}

WHITE, LINEN, INK = "#FFFFFF", "#F2F0EC", "#1C1A18"

# A section is a boxed container: the colour runs the full width of the window,
# the content stops at 1180px. Side padding keeps a gutter on small screens.
def sec(bg=None, tight=False, **extra):
    s = {
        "content_width": "boxed",
        "boxed_width": size(1228),
        "padding":        dim(56 if tight else 88, 24, 56 if tight else 88, 24),
        "padding_tablet": dim(48 if tight else 64, 24, 48 if tight else 64, 24),
        "padding_mobile": dim(40 if tight else 56, 20, 40 if tight else 56, 20),
        "flex_gap": gap(0),
    }
    if bg:
        s.update(background_background="classic", background_color=bg)
    s.update(extra)
    return s

# Two columns that stack on tablet and below.
SPLIT = dict(flex_direction="row", flex_align_items="center", flex_gap=gap(56),
             flex_direction_tablet="column", flex_gap_tablet=gap(36))

# A child of a SPLIT row. width:50% plus flex-shrink gives two equal columns
# that absorb the gap instead of overflowing it.
def half(gap_px=24, align="flex-start"):
    return dict(content_width="full", width=size(50, "%"), width_tablet=size(100, "%"),
                flex_gap=gap(gap_px), flex_align_items=align)

# A centred, narrow measure - used by the quote, newsletter and follow blocks.
CENTRE = dict(content_width="full", width=size(820), width_tablet=size(100, "%"),
              flex_align_items="center", flex_gap=gap(12))

def bg_image(key, ypos=50):
    return dict(background_background="classic",
                background_image={"url": M[key], "id": 0, "size": "", "alt": "", "source": "library"},
                background_position="initial",
                background_xpos=size(50, "%"), background_ypos=size(ypos, "%"),
                background_repeat="no-repeat", background_size="cover")

def scrim(angle, c1, stop1, c2, stop2):
    """Elementor's own background overlay, in place of a ::after we cannot reach."""
    return dict(background_overlay_background="gradient",
                background_overlay_color=c1, background_overlay_color_stop=size(stop1, "%"),
                background_overlay_color_b=c2, background_overlay_color_b_stop=size(stop2, "%"),
                background_overlay_gradient_type="linear",
                background_overlay_gradient_angle=size(angle, "deg"),
                background_overlay_opacity=size(1, "px"))

def shadow(h_, v, blur, spread, color):
    return {"box_shadow_box_shadow_type": "yes",
            "box_shadow_box_shadow": {"horizontal": h_, "vertical": v, "blur": blur,
                                      "spread": spread, "color": color}}


def con(children, classes="", **settings):
    i = eid("c")
    s = {"content_width": "full", "flex_direction": "column",
         "padding": dim(0, 0, 0, 0)}
    s.update(settings)
    if classes:
        s["_css_classes"] = classes
        _record(i, classes)
    return {"id": i, "elType": "container", "settings": s, "elements": children, "isInner": False}

def w(widget_type, settings, classes=""):
    i = eid("w")
    s = dict(settings)
    if classes:
        s["_css_classes"] = classes
        _record(i, classes)
    return {"id": i, "elType": "widget", "widgetType": widget_type, "settings": s, "elements": []}

def h(text, classes="", tag="h2", align=None):
    s = {"title": text, "header_size": tag}
    if align:
        s["align"] = align
    return w("heading", s, classes)

def p(html, classes="", align=None):
    s = {"editor": f"<p>{html}</p>"}
    if align:
        s["align"] = align
    return w("text-editor", s, classes)

def ul(items, classes=""):
    body = "".join(f"<li>{x}</li>" for x in items)
    return w("text-editor", {"editor": f"<ul>{body}</ul>"}, classes)

def btn(text, url, classes="", align=None):
    s = {"text": text, "link": {"url": url, "is_external": "", "nofollow": ""}}
    if align:
        s["align"] = align
    return w("button", s, classes)

def img(key, classes="ph-frame"):
    return w("image", {"image": {"url": M[key], "id": 0, "size": "", "alt": ALT.get(key, ""),
                                 "source": "library"}, "image_size": "full"}, classes)

def rule(align=None):
    """align sets Elementor's own control and a class, because the divider
    sits in a flex column where text-align alone cannot move it."""
    s = {"style": "solid"}
    cls = "ph-rule"
    if align:
        s["align"] = align
        cls += " ph-rule--" + align[0]
    return w("divider", s, cls)

def icon_box(icon, title, desc):
    return w("icon-box", {"selected_icon": {"value": f"fas fa-{icon}", "library": "fa-solid"},
                          "title_text": title, "description_text": desc,
                          "position": "left", "title_size": "h4"}, "ph-step")


# ------------------------------------------------------------------ sections
section("hero")
hero = con([
    con([h("New England&#8217;s Dedicated Breeders of Working-Line German Shepherds", tag="h1"),
         p("thoughtfully bred, intentionally raised", "ph-script ph-hero__script"),
         btn("Meet Our Shepherds", "#story")],
        "ph-hero__in",
        content_width="full", width=size(600), width_mobile=size(100, "%"),
        flex_gap=gap(14), flex_align_items="flex-start"),
    p("Working-line German Shepherds &middot; Northern Maine", "ph-hero__side"),
], "ph-hero",
    content_width="full",
    min_height=size(760), min_height_tablet=size(620), min_height_mobile=size(540),
    flex_justify_content="flex-end", flex_align_items="flex-start",
    padding=dim(120, 110, 96, 56), padding_tablet=dim(96, 40, 72, 40),
    padding_mobile=dim(72, 20, 56, 20),
    overflow="hidden",
    **bg_image("hero", ypos=80),
    **scrim(105, "rgba(26,19,13,0.62)", 0, "rgba(26,19,13,0)", 66))

section("trust")
trust = con([
    p("AKC Registered", "ph-trust__i"),
    p("Full OFA Health Testing", "ph-trust__i"),
    p("Puppy Culture Raised", "ph-trust__i"),
    p("Written Health Guarantee", "ph-trust__i"),
], "ph-trust", **sec(LINEN,
    padding=dim(32, 24, 32, 24), padding_tablet=dim(32, 24, 32, 24),
    padding_mobile=dim(24, 20, 24, 20),
    flex_direction="row", flex_wrap="wrap", flex_justify_content="center",
    flex_gap=gap(64, 16), flex_gap_mobile=gap(24, 10)))

section("story")
story = con([
    con([img("frida")], **half()),
    con([p("welcome to pine hill", "ph-script"),
         h("Family Raised Working-Line German Shepherds in Northern Maine"),
         rule(),
         p("We&#8217;re a small family business raising working-line German Shepherds on 40 acres of rural "
           "countryside in the backwoods of New England. We specialize in producing high-quality German "
           "Shepherds known for their exceptional personalities, working drive, scent detection abilities, "
           "and balanced temperaments.", "ph-measure"),
         p("With only one breeding female, Frida &mdash; our beloved family member &mdash; we have the unique "
           "opportunity to carefully plan each litter, dedicating countless hours to observing and working "
           "with our puppies. Raised within our home and surrounded by our family, they receive plenty of "
           "love and care from day one.", "ph-measure"),
         btn("Read Our Full Story", "/about-us-maines-german-shepherds-2-2/")], **half()),
], **sec(WHITE, **SPLIT))

section("health")
health = con([
    con([p("health &amp; integrity", "ph-script"),
         h("We Believe in Going the Extra Mile"),
         rule(),
         p("All of our dogs are proudly registered with the AKC &mdash; but registration is only a starting "
           "point. To ensure our puppies grow up healthy and happy, we conduct comprehensive genetic and "
           "health screenings through reputable veterinarians.", "ph-measure"),
         h("Full OFA Evaluations", "ph-sub", tag="h4"),
         p("Hips, elbows, eyes, and heart evaluated by the OFA on every parent before breeding."),
         h("Genetic Disease Screening", "ph-sub", tag="h4"),
         p("Testing for the 12 most common genetic diseases in German Shepherds, so you know what you&#8217;re "
           "bringing home."),
         btn("Meet Our Shepherds", "/our-shepherds/")], **half(gap_px=20)),
    con([img("working")], **half()),
], **sec(LINEN, **SPLIT))

section("cult")
culture = con([
    con([h("Raised With Puppy Culture"),
         p("unleashing the best in each puppy", "ph-script"),
         con([icon_box("heart", "Health &amp; Integrity",
                       "Health-tested parents, veterinary screening, and a written health guarantee with every puppy."),
              icon_box("paw", "Temperament First",
                       "Every puppy has its own personality. Our goal is to match each one with the family that truly fits."),
              icon_box("seedling", "The First Nine Weeks",
                       "Puppy Culture, ESI (Early Scent Introduction), and early socialization from day one through go-home day.")],
             content_width="full", flex_gap=gap(36), padding=dim(8, 0, 8, 0)),
         btn("Learn About Puppy Culture", "/puppy-culture/")], **half()),
    con([img("puppies")], **half()),
], **sec(WHITE, **SPLIT))

section("band")
litter = con([
    con([p("Open reservations for 2026", "ph-kicker"),
         h("Upcoming Litter &mdash; Late Fall 2026"),
         p("We very occasionally have puppies available. If you&#8217;re interested in getting on our waiting "
           "list for our upcoming litter, we&#8217;d love to hear from you.", "ph-lede"),
         btn("Join the Waiting List", "/reserve-a-puppy/")],
        "ph-band__card",
        content_width="full", width=size(480), width_mobile=size(100, "%"),
        flex_gap=gap(18), flex_align_items="flex-start",
        background_background="classic", background_color=WHITE,
        padding=dim(44, 40, 46, 40), padding_mobile=dim(32, 24, 34, 24),
        **shadow(0, 18, 44, -28, "rgba(28,26,24,0.34)")),
], **sec(None,
    min_height=size(520), min_height_mobile=size(420),
    flex_justify_content="center", flex_align_items="flex-start",
    padding=dim(88, 24, 88, 24), padding_mobile=dim(56, 20, 56, 20),
    overflow="hidden",
    **bg_image("band", ypos=62),
    **scrim(100, "rgba(26,19,13,0.22)", 0, "rgba(26,19,13,0)", 100)))

section("schol")
scholars = con([
    con([img("scholars")], **half()),
    con([p("k9 scholars", "ph-script"),
         h("Taking Puppy Training to the Next Level"),
         rule(),
         p("Puppies possess a remarkable ability to learn. Given a structured environment tailored to their "
           "rapidly developing brains, their potential knows no bounds. During their five-week comprehensive "
           "training program, they learn advanced manners and are introduced to new situations:", "ph-measure"),
         ul(["Advanced manners &mdash; sit, stay, come, leash", "Crate training",
             "Manding &mdash; automatic sit", "Food manners", "Advanced socialization",
             "Scent detection exercises", "Confidence building", "Manners in public"], "ph-list"),
         btn("Learn More About K9 Scholars", "/k9-scholars/")], **half()),
], **sec(WHITE, **SPLIT))

def dog(key, name, role, offset=0):
    s = dict(content_width="full", width=size(50, "%"), width_tablet=size(100, "%"),
             flex_gap=gap(14), flex_align_items="flex-start")
    if offset:
        s["margin"] = dim(offset, 0, 0, 0)
        s["margin_tablet"] = dim(0, 0, 0, 0)
    return con([img(key, "ph-frame"), h(name, tag="h3"), p(role, "ph-role")], **s)

section("shep")
shepherds = con([
    con([p("meet our beloved shepherds", "ph-script", align="center"),
         h("We Are So Thankful for Our Shepherds", align="center"),
         rule(align="center"),
         p("Carefully chosen for their outstanding personalities, balanced temperaments, and working drive.",
           "ph-lede", align="center")],
        content_width="full", width=size(820), width_tablet=size(100, "%"),
        padding=dim(0, 0, 56, 0),
        flex_gap=gap(10), flex_align_items="center"),
    con([dog("frida", "Frida Von Stephanitz", "Scent Detection &amp; SAR Training"),
         dog("montie", "Captain Montie", "IGP &amp; Personal Protection Work", offset=56)],
        content_width="full", flex_direction="row", flex_gap=gap(48),
        flex_direction_tablet="column", flex_gap_tablet=gap(36)),
    con([btn("Meet Our Beloved Shepherds", "/our-shepherds/", align="center")],
        content_width="full", flex_align_items="center", padding=dim(56, 0, 0, 0)),
], **sec(LINEN, flex_align_items="center"))

section("quote")
quote = con([
    con([p("kind words", "ph-script", align="center"),
         rule(align="center"),
         p("&#8220;Life is never boring when you own working-line German Shepherds.&#8221;", "ph-quote",
           align="center"),
         p("Pine Hill German Shepherds", "ph-by", align="center")], **CENTRE),
], **sec(LINEN, tight=True, flex_align_items="center"))

section("contact")
contact = con([
    con([w("google_maps", {"address": "Garland, Maine", "zoom": size(9)}, "ph-map")], **half()),
    con([p("say hello", "ph-script"),
         h("Located in Northern Maine"),
         rule(),
         p("We are located in the rural backwoods of Northern Maine, in Penobscot County &mdash; about one hour "
           "from Bangor and two hours from Portland. All of our puppies can be picked up at our home, and for "
           "those unable to make the trip, we offer special delivery options.", "ph-measure"),
         p("Have a question? We&#8217;d love to hear from you.", "ph-measure"),
         btn("Contact Us", "/contac-us-german-shepherd-puppies/")], **half()),
], **sec(LINEN, **SPLIT))

section("news")
newsletter = con([
    con([p("Join the family", "ph-kicker", align="center"),
         h("Puppy Updates, Delivered", align="center"),
         rule(align="center"),
         p("Join our list so you never miss a litter announcement (or a new puppy photo).", "ph-lede",
           align="center"),
         btn("Join Our List", "/contac-us-german-shepherd-puppies/", align="center")], **CENTRE),
], **sec(WHITE, tight=True, flex_align_items="center"))

section("follow")
follow = con([
    con([p("follow along", "ph-script", align="center"),
         h("Follow Our Journey", align="center"),
         rule(align="center"),
         w("shortcode", {"shortcode": "[instagram-feed feed=1]"}, "ph-feed")], **CENTRE),
], **sec(LINEN, flex_align_items="center"))

DATA = [hero, trust, story, health, culture, litter, scholars, shepherds,
        quote, contact, newsletter, follow]


# ------------------------------------------------------------------ stylesheet
# Widgets only. Nothing here lays out a container; if a rule below stopped
# applying the page would lose polish, not structure.
CSS = """@font-face{font-family:'Mrs Saint Delafield';font-style:normal;font-weight:400;font-display:swap;
  src:url(https://fonts.gstatic.com/s/mrssaintdelafield/v14/v6-IGZDIOVXH9xtmTZfRagunqBw5WC62QKknLw.woff2) format('woff2')}
body{--espresso:#1C1A18;--ivory:#F6F4F1;--linen:#F2F0EC;--sand:#DCD8D1;--sage:#232020;
 --sage-deep:#3A3633;--brass:#7C7369;--body:#55504A;color:#55504A}

/* ---- type ---------------------------------------------------------- */
.elementor-widget-heading .elementor-heading-title,
.ph-step .elementor-icon-box-title{
 font-family:'Cormorant Garamond',Georgia,serif!important;font-weight:500!important;
 color:#1C1A18!important;letter-spacing:-.015em!important;line-height:1.12!important;margin:0!important}
.elementor-widget-heading .elementor-heading-title{font-size:clamp(26px,2.9vw,38px)!important}
.elementor-widget-text-editor,.elementor-widget-text-editor p,.elementor-widget-text-editor li,
.ph-step .elementor-icon-box-description{
 font-family:'Montserrat',system-ui,sans-serif!important;font-size:14.5px!important;
 line-height:1.85!important;color:#55504A!important;margin:0!important}
.ph-sub .elementor-heading-title,.ph-step .elementor-icon-box-title{
 font-size:18px!important;line-height:1.35!important;letter-spacing:0!important}
.ph-script,.ph-script p{font-family:'Mrs Saint Delafield',cursive!important;color:#7C7369!important;
 font-size:clamp(34px,3.8vw,48px)!important;line-height:1.1!important;font-style:normal!important}
.ph-kicker p{font-size:10.5px!important;font-weight:600!important;letter-spacing:.18em!important;
 text-transform:uppercase!important;color:#7C7369!important}
.ph-lede p{font-size:15px!important}
.ph-measure p{max-width:62ch}
.ph-quote p{font-family:'Cormorant Garamond',Georgia,serif!important;font-style:italic!important;
 font-size:clamp(24px,3.1vw,40px)!important;line-height:1.45!important;color:#1C1A18!important}
.ph-by p,.ph-role p{font-size:10.5px!important;letter-spacing:.2em!important;
 text-transform:uppercase!important;color:#7C7369!important}
.ph-list ul{margin:0;padding:0;list-style:none;display:grid;grid-template-columns:1fr 1fr;gap:6px 24px}
.ph-list li{font-size:13.5px!important;line-height:1.7!important;padding-left:18px;position:relative}
.ph-list li::before{content:'';position:absolute;left:0;top:11px;width:7px;height:1px;background:#7C7369}

/* ---- buttons ------------------------------------------------------- */
.elementor-button{background-color:#232020!important;color:#F6F4F1!important;
 font-family:'Montserrat',system-ui,sans-serif!important;font-size:10.5px!important;font-weight:500!important;
 letter-spacing:.2em!important;text-transform:uppercase!important;border-radius:0!important;
 padding:17px 34px!important;transition:transform .3s cubic-bezier(.22,.9,.32,1),background-color .25s ease}
.elementor-button:hover,.elementor-button:focus{background-color:#3A3633!important;
 color:#F6F4F1!important;transform:translateY(-2px)}
.elementor-button:focus-visible{outline:2px solid #7C7369!important;outline-offset:3px!important}

/* ---- divider ------------------------------------------------------- */
.ph-rule .elementor-divider{padding-block:10px!important}
.ph-rule .elementor-divider-separator{border-top:1px solid #7C7369!important;width:56px!important}
.ph-rule--c .elementor-divider{justify-content:center!important}

/* ---- photographs --------------------------------------------------- */
.ph-frame img{width:100%!important;height:clamp(400px,42vw,560px)!important;object-fit:cover!important;
 display:block!important;box-shadow:0 2px 6px rgba(28,26,24,.06),0 18px 40px -16px rgba(28,26,24,.20)}
.ph-map iframe,.ph-map .elementor-custom-embed{height:clamp(400px,42vw,560px)!important}

/* ---- trust bar: badges size to their text, not to equal columns ----- */
.ph-trust__i{width:auto!important;max-width:none!important;flex:0 0 auto!important}
.ph-trust__i p{font-size:10.5px!important;font-weight:500!important;letter-spacing:.2em!important;
 text-transform:uppercase!important;color:#1C1A18!important}

/* ---- puppy culture steps ------------------------------------------- */
.ph-step .elementor-icon-box-wrapper{display:flex!important;gap:24px!important;
 align-items:flex-start!important;text-align:left!important}
.ph-step .elementor-icon{background:#DCD8D1!important;color:#1C1A18!important;
 width:68px!important;height:68px!important;border-radius:50%!important;display:flex!important;
 align-items:center!important;justify-content:center!important;font-size:22px!important;flex:none!important}
.ph-step .elementor-icon-box-description{font-size:13.5px!important;line-height:1.7!important}

/* ---- hero ----------------------------------------------------------- */
.ph-hero .elementor-heading-title{color:#FFFFFF!important;font-size:clamp(27px,3.1vw,40px)!important;
 line-height:1.06!important;letter-spacing:-.02em!important}
.ph-hero__script p{color:rgba(246,244,241,.95)!important;font-size:clamp(30px,3.4vw,44px)!important}
.ph-hero__side{position:absolute!important;right:30px!important;top:50%!important;
 transform:translateY(-50%) rotate(180deg)!important;writing-mode:vertical-rl!important;z-index:3!important;
 white-space:nowrap!important;border-right:1px solid rgba(247,244,238,.28)!important;
 padding-block:32px!important;width:auto!important;max-width:none!important}
.ph-hero__side p{font-size:9px!important;font-weight:500!important;letter-spacing:.26em!important;
 text-transform:uppercase!important;color:rgba(247,244,238,.72)!important}

@media(max-width:1024px){
.ph-frame img{height:clamp(320px,52vw,460px)!important}
.ph-map iframe,.ph-map .elementor-custom-embed{height:clamp(320px,52vw,460px)!important}
}
@media(max-width:767px){
.ph-hero__side{display:none!important}
.ph-frame img{height:clamp(280px,74vw,360px)!important}
.ph-list ul{grid-template-columns:1fr}
}"""


def resolve(css):
    """Give every .ph-name selector an id twin.

    Elementor always emits .elementor-element-{id}; _css_classes is the part we
    cannot prove reaches every element type. Listing both, as plain comma
    branches rather than :is(), means a rule lands whichever of the two the
    page turns out to carry, with no selector syntax to go wrong.
    """
    # comments are stripped first: a comma inside one would otherwise split a
    # selector list in the wrong place and leave the rule un-twinned
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)

    def expand(sel):
        m = re.match(r"^(\s*(?:/\*.*?\*/\s*)*)(\.ph-[A-Za-z0-9_-]+)(.*)$", sel, re.S)
        if not m:
            return [sel]
        lead, cls, rest = m.groups()
        ids = INDEX.get(cls[1:], [])
        tails = expand(rest) if ".ph-" in rest else [rest]
        return [f"{lead}{b}{t}"
                for b in [cls] + [f".elementor-element-{i}" for i in ids]
                for t in tails]

    def sub(m):
        head, brace = m.group(1), m.group(2)
        out = []
        for part in head.split(","):
            out.extend(expand(part))
        return ",".join(out) + brace

    return re.sub(r"([^{}@]+)(\{)", sub, css).strip()


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "data"
    if mode == "data":
        sys.stdout.write(json.dumps(DATA, separators=(",", ":")))
    elif mode == "css":
        sys.stdout.write(resolve(CSS))
    elif mode == "index":
        sys.stdout.write(json.dumps(INDEX, indent=1))
