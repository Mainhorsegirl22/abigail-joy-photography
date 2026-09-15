#!/usr/bin/env python3
"""Emit Elementor _elementor_data for the Pine Hill homepage.

Every piece of copy, every photograph and every button is its own widget, so
the owner edits them in the Elementor panel. Layout comes from Elementor's
container controls; the stylesheet carries appearance only and lives in the
page's Custom CSS, where the text editor cannot strip it.

  python3 build_elementor.py data  -> _elementor_data JSON
  python3 build_elementor.py css   -> the page stylesheet
"""
import json, sys

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
_n = [0]
def eid(p):
    _n[0] += 1
    return f"ph{p}{_n[0]:03d}"

def con(children, classes="", **s):
    st = {"content_width": "full", "flex_direction": "column"}
    st.update(s)
    if classes: st["_css_classes"] = classes
    return {"id": eid("c"), "elType": "container", "settings": st, "elements": children, "isInner": False}

def w(t, s, classes=""):
    if classes: s = dict(s, _css_classes=classes)
    return {"id": eid("w"), "elType": "widget", "widgetType": t, "settings": s, "elements": []}

def h(text, classes="", tag="h2"): return w("heading", {"title": text, "header_size": tag}, classes)
def p(html, classes=""):           return w("text-editor", {"editor": f"<p>{html}</p>"}, classes)
def btn(t, u, classes=""):         return w("button", {"text": t, "link": {"url": u, "is_external": "", "nofollow": ""}}, classes)
def img(k, classes="ph-frame"):
    return w("image", {"image": {"url": M[k], "id": 0, "size": "", "alt": ALT.get(k, ""), "source": "library"},
                       "image_size": "full"}, classes)
def rule():  return w("divider", {"style": "solid"}, "ph-rule")
def icon_box(icon, title, desc):
    return w("icon-box", {"selected_icon": {"value": f"fas fa-{icon}", "library": "fa-solid"},
                          "title_text": title, "description_text": desc,
                          "position": "left", "title_size": "h4"}, "ph-step")

BOXED = dict(content_width="boxed")
ROW   = dict(flex_direction="row", flex_align_items="center",
             flex_gap={"unit": "px", "size": 56, "column": "56", "row": "56", "isLinked": True})

# ------------------------------------------------------------------ sections
hero = con([
    con([h("New England&#8217;s Dedicated Breeders of Working-Line German Shepherds", tag="h1"),
         p("thoughtfully bred, intentionally raised", "ph-script"),
         btn("Meet Our Shepherds", "#story")], "ph-hero__in"),
    p("Working-line German Shepherds &middot; Northern Maine", "ph-hero__side"),
], "ph-hero", background_background="classic",
   background_image={"url": M["hero"], "id": 0, "size": "", "alt": "", "source": "library"},
   background_position="center center", background_size="cover")

story = con([con([
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
         btn("Read Our Full Story", "/about-us-maines-german-shepherds-2-2/")], "ph-panel"),
    img("frida"),
], "ph-split", **BOXED, **ROW)], "ph-sec")

health = con([con([
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
         btn("Meet Our Shepherds", "/our-shepherds/")], "ph-edge__text"),
    img("working"),
], "ph-edge", content_width="full", **ROW)], "ph-sec ph-sec--edge")

culture = con([con([
    con([h("Raised With Puppy Culture"),
         p("unleashing the best in each puppy", "ph-script"),
         con([icon_box("heart", "Health &amp; Integrity",
                       "Health-tested parents, veterinary screening, and a written health guarantee with every puppy."),
              icon_box("paw", "Temperament First",
                       "Every puppy has its own personality. Our goal is to match each one with the family that truly fits."),
              icon_box("seedling", "The First Nine Weeks",
                       "Puppy Culture, ESI (Early Scent Introduction), and early socialization from day one through go-home day.")],
             "ph-steps"),
         btn("Learn About Puppy Culture", "/puppy-culture/")], "ph-col"),
    img("puppies"),
], "ph-split", **BOXED, **ROW)], "ph-sec")

litter = con([
    con([p("Open reservations for 2026", "ph-kicker"),
         h("Upcoming Litter &mdash; Late Fall 2026"),
         p("We very occasionally have puppies available. If you&#8217;re interested in getting on our waiting "
           "list for our upcoming litter, we&#8217;d love to hear from you.", "ph-lede"),
         btn("Join the Waiting List", "/reserve-a-puppy/")], "ph-band__in", **BOXED),
], "ph-band", background_background="classic",
   background_image={"url": M["band"], "id": 0, "size": "", "alt": "", "source": "library"},
   background_position="center center", background_size="cover")

scholars = con([con([
    img("scholars"),
    con([p("k9 scholars", "ph-script"),
         h("Taking Puppy Training to the Next Level"),
         rule(),
         p("Puppies possess a remarkable ability to learn. Given a structured environment tailored to their "
           "rapidly developing brains, their potential knows no bounds. During their five-week comprehensive "
           "training program, they learn advanced manners and are introduced to new situations:", "ph-measure"),
         p("Advanced manners &mdash; sit, stay, come, leash &middot; Crate training &middot; Manding &mdash; "
           "automatic sit &middot; Food manners &middot; Advanced socialization &middot; Scent detection "
           "exercises &middot; Confidence building &middot; Manners in public", "ph-measure"),
         btn("Learn More About K9 Scholars", "/k9-scholars/")], "ph-col"),
], "ph-split", **BOXED, **ROW)], "ph-sec")

def dog(k, name, role):
    return con([img(k), h(name, tag="h3"), p(role, "ph-role")], "ph-dog")

shepherds = con([con([
    con([p("meet our beloved shepherds", "ph-script"),
         h("We Are So Thankful for Our Shepherds"),
         rule(),
         p("Carefully chosen for their outstanding personalities, balanced temperaments, and working drive.", "ph-lede")],
        "ph-head", **BOXED),
    con([dog("frida", "Frida Von Stephanitz", "Scent Detection &amp; SAR Training"),
         dog("montie", "Captain Montie", "IGP &amp; Personal Protection Work")],
        "ph-duo", flex_direction="row",
        flex_gap={"unit": "px", "size": 48, "column": "48", "row": "48", "isLinked": True}),
    btn("Meet Our Beloved Shepherds", "/our-shepherds/"),
], "ph-col ph-center", **BOXED)], "ph-sec")

quote = con([con([
    p("kind words", "ph-script"),
    rule(),
    p("&#8220;Life is never boring when you own working-line German Shepherds.&#8221;", "ph-quote"),
    p("Pine Hill German Shepherds", "ph-by"),
], "ph-col ph-center", **BOXED)], "ph-sec ph-sand")

contact = con([con([
    w("google_maps", {"address": "Garland, Maine", "zoom": {"unit": "px", "size": 9, "sizes": []}}, "ph-map"),
    con([p("say hello", "ph-script"),
         h("Located in Northern Maine"),
         rule(),
         p("We are located in the rural backwoods of Northern Maine, in Penobscot County &mdash; about one hour "
           "from Bangor and two hours from Portland. All of our puppies can be picked up at our home, and for "
           "those unable to make the trip, we offer special delivery options.", "ph-measure"),
         p("Have a question? We&#8217;d love to hear from you.", "ph-measure"),
         btn("Contact Us", "/contac-us-german-shepherd-puppies/")], "ph-panel"),
], "ph-split", **BOXED, **ROW)], "ph-sec")

newsletter = con([con([
    p("Join the family", "ph-kicker"),
    h("Puppy Updates, Delivered"),
    rule(),
    p("Join our list so you never miss a litter announcement (or a new puppy photo).", "ph-lede"),
    btn("Join Our List", "/contac-us-german-shepherd-puppies/"),
], "ph-col ph-center", **BOXED)], "ph-sec")

follow = con([con([
    p("follow along", "ph-script"),
    h("Follow Our Journey"),
    rule(),
    w("shortcode", {"shortcode": "[instagram-feed feed=1]"}, "ph-feed"),
], "ph-col ph-center", **BOXED)], "ph-sec ph-sand")

DATA = [hero, story, health, culture, litter, scholars, shepherds, quote, contact, newsletter, follow]

CSS = """@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400;1,500&family=Montserrat:wght@300;400;500;600&family=Mrs+Saint+Delafield&display=swap');
body{--espresso:#2E2A26;--shell:#F3F0EA;--sand:#DDD2C4;--sand-soft:#E9E1D5;--sage:#DCE0CD;--sage-deep:#CBD1B8;--brass:#A28465;--body:#4A443D;--hair:rgba(46,42,38,.12);--container:1180px;--gutter:clamp(24px,5vw,56px);--sy:clamp(72px,9vw,120px);background:var(--shell);color:var(--body);font-family:'Montserrat',system-ui,sans-serif;font-size:13px;line-height:1.95}
.elementor-widget-heading .elementor-heading-title{font-family:'Cormorant Garamond',Georgia,serif;font-weight:500;color:var(--espresso);letter-spacing:-.015em;line-height:1.1;margin:0}
.ph-sec .elementor-widget-heading .elementor-heading-title{font-size:clamp(26px,2.9vw,38px)}
.ph-sub .elementor-heading-title,.ph-step .elementor-icon-box-title{font-size:16px!important;line-height:1.35;letter-spacing:0}
.ph-hero .elementor-heading-title{color:#FFFFFF;font-size:clamp(27px,3.1vw,40px);line-height:1.04;letter-spacing:-.02em}
.ph-band .elementor-heading-title{color:#FFFFFF}
.elementor-widget-text-editor{font-family:'Montserrat',sans-serif;font-size:13px;line-height:1.95;color:var(--body)}
.elementor-widget-text-editor p{margin:0}
.ph-measure{max-width:66ch}
.ph-lede{max-width:60ch;font-size:13.5px}
.ph-band .ph-lede{color:rgba(255,255,255,.88)}
.ph-script,.ph-script p{font-family:'Mrs Saint Delafield',cursive;color:var(--brass);font-size:clamp(32px,3.6vw,44px);line-height:1}
.ph-hero .ph-script,.ph-hero .ph-script p{color:rgba(247,244,238,.95);font-size:clamp(26px,3vw,38px)}
.ph-kicker p{font-size:10.5px;font-weight:600;letter-spacing:.18em;text-transform:uppercase;color:var(--brass)}
.ph-band .ph-kicker p{color:var(--sand)}
.ph-quote p{font-family:'Cormorant Garamond',serif;font-style:italic;font-size:clamp(20px,2.3vw,28px);line-height:1.45;color:var(--espresso)}
.ph-by p{font-size:10px;letter-spacing:.22em;text-transform:uppercase;color:var(--brass)}
.ph-role p{font-size:10.5px;letter-spacing:.2em;text-transform:uppercase;color:var(--brass)}
.elementor-button{font-family:'Montserrat',sans-serif;font-size:10.5px;font-weight:500;letter-spacing:.2em;text-transform:uppercase;background-color:var(--sage);color:var(--espresso);border-radius:0;padding:17px 34px;transition:transform .3s cubic-bezier(.22,.9,.32,1),background-color .25s ease}
.elementor-button:hover,.elementor-button:focus{background-color:var(--sage-deep);color:var(--espresso);transform:translateY(-2px)}
.ph-sec{padding-block:var(--sy);padding-inline:var(--gutter)}
.ph-sand{background:var(--sand-soft)}
.ph-col{gap:24px}
.ph-center{align-items:center;text-align:center}
.ph-head{gap:8px;align-items:center;text-align:center;max-width:820px;margin-inline:auto}
.ph-split>.ph-panel,.ph-split>.ph-col,.ph-split>.elementor-widget-image,.ph-split>.ph-map{flex:1 1 0;min-width:0;width:auto}
.ph-panel{background:#FFFFFF;padding:clamp(30px,3.6vw,52px);gap:24px}
.ph-frame img{width:100%;height:clamp(400px,42vw,560px);object-fit:cover;display:block;box-shadow:0 2px 6px rgba(43,37,31,.06),0 18px 40px -16px rgba(43,37,31,.18)}
.ph-rule .elementor-divider{padding-block:10px}
.ph-rule .elementor-divider-separator{border-top:1px solid var(--brass);width:56px}
.ph-center .ph-rule .elementor-divider{justify-content:center;display:flex}
.ph-map iframe,.ph-map .elementor-custom-embed{height:clamp(400px,42vw,560px)}
.ph-sec--edge{padding-inline:var(--gutter) 0}
.ph-edge__text{max-width:calc(var(--container)/2);margin-left:auto;padding-right:clamp(24px,3vw,56px);gap:24px}
.ph-edge>.elementor-widget-image{flex:1 1 0;min-width:0}
.ph-edge>.elementor-widget-image img{height:clamp(420px,46vw,620px)}
.ph-steps{gap:40px;margin-block:8px}
.ph-step .elementor-icon-box-wrapper{display:flex;gap:24px;align-items:flex-start;text-align:left}
.ph-step .elementor-icon{background:var(--sand);color:var(--espresso);width:68px;height:68px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:22px}
.ph-step .elementor-icon-box-description{font-size:12.5px;line-height:1.7;color:var(--body)}
.ph-band{position:relative;min-height:clamp(420px,54vh,560px);justify-content:center;padding-block:88px;padding-inline:var(--gutter);overflow:hidden}
.ph-band::after{content:"";position:absolute;inset:0;z-index:1;pointer-events:none;background:linear-gradient(100deg,rgba(26,19,13,.66) 0%,rgba(26,19,13,.38) 46%,rgba(26,19,13,.12) 100%)}
.ph-band>*{position:relative;z-index:2}
.ph-band__in{align-items:flex-start;gap:20px}
.ph-band__in>*{max-width:520px}
.ph-duo>.ph-dog{flex:1 1 0;min-width:0;gap:16px}
.ph-duo>.ph-dog:nth-child(2){margin-top:clamp(0px,4.5vw,64px)}
.ph-hero{position:relative;min-height:clamp(560px,82vh,800px);justify-content:flex-end;align-items:flex-start;padding:120px clamp(56px,7vw,110px) clamp(56px,9vh,104px) var(--gutter);overflow:hidden}
.ph-hero::after{content:"";position:absolute;inset:0;z-index:1;pointer-events:none;background:linear-gradient(105deg,rgba(26,19,13,.62) 0%,rgba(26,19,13,.34) 38%,transparent 66%)}
.ph-hero>*{position:relative;z-index:2}
.ph-hero__in{max-width:600px;gap:8px;align-items:flex-start}
.ph-hero__side{position:absolute;right:calc(var(--gutter)*.55);top:50%;transform:translateY(-50%) rotate(180deg);writing-mode:vertical-rl;z-index:2;white-space:nowrap;border-right:1px solid rgba(247,244,238,.28);padding-block:32px;width:auto}
.ph-hero__side p{font-size:9px;font-weight:500;letter-spacing:.26em;text-transform:uppercase;color:rgba(247,244,238,.72)}
@media(max-width:880px){
.ph-hero__side{display:none}
.ph-split,.ph-edge,.ph-duo{flex-direction:column}
.ph-sec--edge{padding-inline:var(--gutter)}
.ph-edge__text{max-width:none;margin-left:0;padding-right:0}
.ph-frame img,.ph-edge>.elementor-widget-image img{height:auto}
.ph-duo>.ph-dog:nth-child(2){margin-top:0}
}"""

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "data"
    sys.stdout.write(json.dumps(DATA, separators=(",", ":")) if mode == "data" else CSS)
