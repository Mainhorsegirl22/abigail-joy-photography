#!/usr/bin/env python3
"""Emit the Pine Hill homepage as native Elementor widgets.

Every line of copy, every photograph and every button is its own widget, so the
owner edits them from the Elementor panel without touching code.

Two things make this survive Elementor where the hand-coded page did not:

  * Every container is content_width="full".  A "boxed" container renders an
    extra .e-con-inner wrapper, and layout rules then have to target both the
    container and that wrapper.  Centring is done with max-width in CSS instead.

  * Styling never depends on _css_classes reaching the markup.  Elementor always
    emits .elementor-element-{id}, so every selector written as .ph-name is
    rewritten to :is(.ph-name, .elementor-element-a, .elementor-element-b, ...)
    listing the real elements that carry it.  Specificity is unchanged because
    every branch is a single class.

  python3 build_elementor.py data  -> _elementor_data JSON
  python3 build_elementor.py css   -> the page stylesheet (Elementor Custom CSS)
"""
import json, re, sys

U = "https://www.pinehillgermanshepherds.com/wp-content/uploads"
M = {
 "hero":     f"{U}/2026/07/hero-sunset.jpg",
 "freda":    f"{U}/2026/04/Freda-3.jpg",
 "working":  f"{U}/2026/09/BK706350-scaled.jpg",
 "puppies":  f"{U}/2024/10/AKC-German-Shepherd-Puppies-for-Sale-in-Maine-Pine-Hill-German-Shepherd-Breeders-scaled.jpg",
 "scholars": f"{U}/2025/01/AKC-East-Working-Line-German-Shepherd-Puppies-for-Sale-in-Maine-Pine-Hill-German-Shepherds-scaled.jpg",
 "montie":   f"{U}/2026/04/Cruz-AKC-German-Shepherd-dog-in-NH--scaled.jpg",
 "band":     f"{U}/2026/09/BK700068-scaled.jpg",
 "s1":       f"{U}/2026/08/Rangley-1-1-scaled.jpg",
 "s2":       f"{U}/2026/08/Rangley-3-scaled.jpg",
 "s3":       f"{U}/2026/08/Rrangley-5-scaled.jpg",
 "s4":       f"{U}/2026/09/BK700064-scaled.jpg",
}
ALT = {
 "freda": "Freda, our foundation female at Pine Hill German Shepherds",
 "working": "AKC working-line German Shepherd in Maine",
 "puppies": "German Shepherd puppies raised with Puppy Culture",
 "scholars": "K9 Scholars training program",
 "montie": "Captain Montie, IGP and personal protection",
 "s1": "Pine Hill German Shepherds in the Maine woods",
 "s2": "Working-line German Shepherd on the trail",
 "s3": "German Shepherd at Rangeley, Maine",
 "s4": "German Shepherd breeders in New England",
}

# ------------------------------------------------------------------ plumbing
_n = [0]
INDEX = {}          # semantic class -> [element ids that carry it]

def eid(prefix):
    _n[0] += 1
    return f"ph{prefix}{_n[0]:03d}"

def _record(i, classes):
    for c in classes.split():
        INDEX.setdefault(c, []).append(i)

def con(children, classes="", **settings):
    i = eid("c")
    s = {"content_width": "full", "flex_direction": "column"}
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

def h(text, classes="", tag="h2"):
    return w("heading", {"title": text, "header_size": tag}, classes)

def p(html, classes=""):
    return w("text-editor", {"editor": f"<p>{html}</p>"}, classes)

def ul(items, classes=""):
    body = "".join(f"<li>{x}</li>" for x in items)
    return w("text-editor", {"editor": f"<ul>{body}</ul>"}, classes)

def btn(text, url, classes=""):
    return w("button", {"text": text, "link": {"url": url, "is_external": "", "nofollow": ""}}, classes)

def img(key, classes="ph-frame"):
    return w("image", {"image": {"url": M[key], "id": 0, "size": "", "alt": ALT.get(key, ""),
                                 "source": "library"}, "image_size": "full"}, classes)

def rule():
    return w("divider", {"style": "solid"}, "ph-rule")

def icon_box(icon, title, desc):
    return w("icon-box", {"selected_icon": {"value": f"fas fa-{icon}", "library": "fa-solid"},
                          "title_text": title, "description_text": desc,
                          "position": "left", "title_size": "h4"}, "ph-step")

def photo(key):
    return w("image", {"image": {"url": M[key], "id": 0, "size": "", "alt": ALT.get(key, ""),
                                 "source": "library"}, "image_size": "full"}, "ph-strip__img")

BG = lambda key: dict(background_background="classic",
                      background_image={"url": M[key], "id": 0, "size": "", "alt": "", "source": "library"},
                      background_position="center center", background_size="cover")

# ------------------------------------------------------------------ sections
hero = con([
    con([h("New England&#8217;s Dedicated Breeders of Working-Line German Shepherds", tag="h1"),
         p("thoughtfully bred, intentionally raised", "ph-script"),
         btn("Meet Our Shepherds", "#story")], "ph-hero__in"),
    p("Working-line German Shepherds &middot; Northern Maine", "ph-hero__side"),
], "ph-hero", **BG("hero"))

trust = con([con([
    p("AKC Registered", "ph-trust__i"),
    p("Full OFA Health Testing", "ph-trust__i"),
    p("Puppy Culture Raised", "ph-trust__i"),
    p("Written Health Guarantee", "ph-trust__i"),
], "ph-trust__row", flex_direction="row")], "ph-trust")

story = con([con([
    img("freda"),
    con([p("welcome to pine hill", "ph-script"),
         h("Family Raised Working-Line German Shepherds in Northern Maine"),
         rule(),
         p("We&#8217;re a small family business raising working-line German Shepherds on 40 acres of rural "
           "countryside in the backwoods of New England. We specialize in producing high-quality German "
           "Shepherds known for their exceptional personalities, working drive, scent detection abilities, "
           "and balanced temperaments.", "ph-measure"),
         p("With only one breeding female, Freda &mdash; our beloved family member &mdash; we have the unique "
           "opportunity to carefully plan each litter, dedicating countless hours to observing and working "
           "with our puppies. Raised within our home and surrounded by our family, they receive plenty of "
           "love and care from day one.", "ph-measure"),
         btn("Read Our Full Story", "/about-us-maines-german-shepherds-2-2/")], "ph-col"),
], "ph-split", flex_direction="row", flex_align_items="center")], "ph-sec ph-white")

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
], "ph-edge", flex_direction="row", flex_align_items="center")], "ph-sec ph-sec--edge ph-linen")

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
], "ph-split", flex_direction="row", flex_align_items="center")], "ph-sec ph-white")

strip = con([
    p("Life at Pine Hill", "ph-strip__cap"),
    con([photo("s1"), photo("s2"), photo("s3"), photo("s4")], "ph-strip__row", flex_direction="row"),
], "ph-strip")
# Removed from the page at her request. It is still BUILT, not deleted,
# so it keeps consuming ids phw047-phw051 and phc052-phc053 and every
# element below it keeps the id the stylesheet already names. Deleting
# these five lines instead would renumber the whole back half of the
# page and unstyle everything from the litter band down.

litter = con([
    con([p("Open reservations for 2026", "ph-kicker"),
         h("Upcoming Litter &mdash; Late Fall 2026"),
         p("We very occasionally have puppies available. If you&#8217;re interested in getting on our waiting "
           "list for our upcoming litter, we&#8217;d love to hear from you.", "ph-lede"),
         btn("Join the Waiting List", "/reserve-a-puppy/")], "ph-band__card"),
], "ph-band", **BG("band"))

scholars = con([con([
    img("scholars"),
    con([p("k9 scholars", "ph-script"),
         h("Taking Puppy Training to the Next Level"),
         rule(),
         p("Puppies possess a remarkable ability to learn. Given a structured environment tailored to their "
           "rapidly developing brains, their potential knows no bounds. During their five-week comprehensive "
           "training program, they learn advanced manners and are introduced to new situations:", "ph-measure"),
         ul(["Advanced manners &mdash; sit, stay, come, leash", "Crate training",
             "Manding &mdash; automatic sit", "Food manners", "Advanced socialization",
             "Scent detection exercises", "Confidence building", "Manners in public"], "ph-list"),
         btn("Learn More About K9 Scholars", "/k9-scholars/")], "ph-col"),
], "ph-split", flex_direction="row", flex_align_items="center")], "ph-sec ph-white")

def dog(key, name, role):
    return con([img(key, "ph-frame ph-dogimg"), h(name, tag="h3"), p(role, "ph-role")], "ph-dog")

shepherds = con([
    con([p("meet our beloved shepherds", "ph-script"),
         h("We Are So Thankful for Our Shepherds"),
         rule(),
         p("Carefully chosen for their outstanding personalities, balanced temperaments, and working drive.",
           "ph-lede")], "ph-head"),
    con([dog("freda", "Freda Von Stephanitz", "Scent Detection &amp; SAR Training"),
         dog("montie", "Captain Montie", "IGP &amp; Personal Protection Work")],
        "ph-duo", flex_direction="row"),
    con([btn("Meet Our Beloved Shepherds", "/our-shepherds/")], "ph-cta"),
], "ph-sec ph-linen")

quote = con([con([
    p("kind words", "ph-script"),
    rule(),
    p("&#8220;Life is never boring when you own working-line German Shepherds.&#8221;", "ph-quote"),
    p("Pine Hill German Shepherds", "ph-by"),
], "ph-narrow")], "ph-sec ph-sec--tight ph-linen")

contact = con([con([
    w("google_maps", {"address": "Garland, Maine", "zoom": {"unit": "px", "size": 9, "sizes": []}}, "ph-map"),
    con([p("say hello", "ph-script"),
         h("Located in Northern Maine"),
         rule(),
         p("We are located in the rural backwoods of Northern Maine, in Penobscot County &mdash; about one hour "
           "from Bangor and two hours from Portland. All of our puppies can be picked up at our home, and for "
           "those unable to make the trip, we offer special delivery options.", "ph-measure"),
         p("Have a question? We&#8217;d love to hear from you.", "ph-measure"),
         btn("Contact Us", "/contac-us-german-shepherd-puppies/")], "ph-col"),
], "ph-split", flex_direction="row", flex_align_items="center")], "ph-sec ph-linen")

newsletter = con([con([
    p("Join the family", "ph-kicker"),
    h("Puppy Updates, Delivered"),
    rule(),
    p("Join our list so you never miss a litter announcement (or a new puppy photo).", "ph-lede"),
    btn("Join Our List", "/contac-us-german-shepherd-puppies/"),
], "ph-narrow")], "ph-sec ph-sec--tight ph-white")

follow = con([con([
    p("follow along", "ph-script"),
    h("Follow Our Journey"),
    rule(),
    w("shortcode", {"shortcode": "[instagram-feed feed=1]"}, "ph-feed"),
], "ph-narrow")], "ph-sec ph-linen")

DATA = [hero, trust, story, health, culture, litter, scholars, shepherds,
        quote, contact, newsletter, follow]

# ------------------------------------------------------------------ stylesheet
CSS = """@font-face{font-family:'Mrs Saint Delafield';font-style:normal;font-weight:400;font-display:swap;
  src:url(https://fonts.gstatic.com/s/mrssaintdelafield/v14/v6-IGZDIOVXH9xtmTZfRagunqBw5WC62QKknLw.woff2) format('woff2')}
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400;1,500&family=Montserrat:wght@300;400;500;600&family=Mrs+Saint+Delafield&display=swap');
body{--espresso:#1C1A18;--ivory:#F6F4F1;--linen:#F2F0EC;--taupe:#C6C1B8;--sand:#DCD8D1;
 --sage:#232020;--sage-deep:#3A3633;--brass:#7C7369;--body:#55504A;--hair:rgba(28,26,24,.12);
 --gut:clamp(24px,5vw,56px);--wrap:1180px;--sy:clamp(60px,7vw,100px);
 background:#FFFFFF;color:var(--body)}

/* ---- type ---------------------------------------------------------- */
.elementor-widget-heading .elementor-heading-title,.ph-step .elementor-icon-box-title{
 font-family:'Cormorant Garamond',Georgia,serif!important;font-weight:500!important;
 color:var(--espresso);letter-spacing:-.015em;line-height:1.12;margin:0}
.elementor-widget-heading .elementor-heading-title{font-size:clamp(26px,2.9vw,38px)!important}
.elementor-widget-text-editor,.elementor-widget-text-editor p,.elementor-widget-text-editor li,
.ph-step .elementor-icon-box-description{
 font-family:'Montserrat',system-ui,sans-serif!important;font-size:14.5px!important;
 line-height:1.85!important;color:var(--body)!important;margin:0}
.ph-sub .elementor-heading-title,.ph-step .elementor-icon-box-title{
 font-size:18px!important;line-height:1.35!important;letter-spacing:0!important}
.ph-script,.ph-script p{font-family:'Mrs Saint Delafield',cursive!important;color:var(--brass)!important;
 font-size:clamp(34px,3.8vw,48px)!important;line-height:1.1!important;font-style:normal!important}
.ph-kicker p{font-size:10.5px!important;font-weight:600!important;letter-spacing:.18em!important;
 text-transform:uppercase!important;color:var(--brass)!important}
.ph-lede p{font-size:15px!important;max-width:58ch}
.ph-measure p{max-width:62ch}
.ph-quote p{font-family:'Cormorant Garamond',Georgia,serif!important;font-style:italic!important;
 font-size:clamp(24px,3.1vw,40px)!important;line-height:1.45!important;color:var(--espresso)!important}
.ph-by p,.ph-role p{font-size:10.5px!important;letter-spacing:.2em!important;
 text-transform:uppercase!important;color:var(--brass)!important}
.ph-list ul{margin:0;padding:0;list-style:none;display:grid;grid-template-columns:1fr 1fr;gap:6px 24px}
.ph-list li{font-size:13.5px!important;line-height:1.7!important;padding-left:18px;position:relative}
.ph-list li::before{content:"";position:absolute;left:0;top:11px;width:7px;height:1px;background:var(--brass)}

/* ---- buttons ------------------------------------------------------- */
.elementor-button{background-color:var(--sage)!important;color:var(--ivory)!important;
 font-family:'Montserrat',system-ui,sans-serif!important;font-size:10.5px!important;font-weight:500!important;
 letter-spacing:.2em!important;text-transform:uppercase!important;border-radius:0!important;
 padding:17px 34px!important;transition:transform .3s cubic-bezier(.22,.9,.32,1),background-color .25s ease}
.elementor-button:hover,.elementor-button:focus{background-color:var(--sage-deep)!important;
 color:var(--ivory)!important;transform:translateY(-2px)}
.elementor-button:focus-visible{outline:2px solid var(--brass)!important;outline-offset:3px!important}

/* ---- section shells ------------------------------------------------ */
.ph-sec{padding:var(--sy) var(--gut)!important;gap:0!important}
.ph-sec--tight{padding-block:clamp(44px,4.6vw,68px)!important}
.ph-white{background-color:#FFFFFF!important}
.ph-linen{background-color:var(--linen)!important}
.ph-split{display:flex!important;flex-direction:row!important;align-items:center!important;
 gap:clamp(32px,4.5vw,72px)!important;max-width:var(--wrap)!important;width:100%!important;
 margin-inline:auto!important;padding:0!important}
.ph-split>*{flex:1 1 0!important;min-width:0!important;width:auto!important}
.ph-col{gap:24px!important;padding:0!important;max-width:none!important;align-items:flex-start!important}
.ph-narrow{max-width:820px!important;margin-inline:auto!important;align-items:center!important;
 text-align:center!important;gap:12px!important;padding:0!important}
.ph-narrow .elementor-divider,.ph-head .elementor-divider{display:flex!important;justify-content:center!important}
.ph-rule .elementor-divider{padding-block:10px!important}
.ph-rule .elementor-divider-separator{border-top:1px solid var(--brass)!important;width:56px!important;margin:0!important}

/* ---- photographs --------------------------------------------------- */
.ph-frame img{width:100%!important;height:clamp(400px,42vw,560px)!important;object-fit:cover!important;
 display:block!important;box-shadow:0 2px 6px rgba(28,26,24,.06),0 18px 40px -16px rgba(28,26,24,.20)}

/* ---- trust bar ----------------------------------------------------- */
.ph-trust{background-color:var(--linen)!important;padding:32px var(--gut)!important;
 border-bottom:1px solid var(--hair)!important}
.ph-trust__row{display:flex!important;flex-direction:row!important;flex-wrap:wrap!important;
 justify-content:center!important;gap:16px 64px!important;max-width:var(--wrap)!important;
 width:100%!important;margin-inline:auto!important;padding:0!important}
.ph-trust__i{width:auto!important;flex:0 0 auto!important}
.ph-trust__i p{font-size:10.5px!important;font-weight:500!important;letter-spacing:.2em!important;
 text-transform:uppercase!important;color:var(--espresso)!important}

/* ---- full-bleed photo strip ---------------------------------------- */
.ph-strip{padding:clamp(36px,4vw,56px) 0 clamp(48px,5.5vw,80px)!important;gap:0!important;
 background-color:#FFFFFF!important}
.ph-strip__cap p{text-align:center!important;font-size:10.5px!important;font-weight:600!important;
 letter-spacing:.2em!important;text-transform:uppercase!important;color:var(--brass)!important;
 padding-bottom:24px!important}
.ph-strip__row{display:flex!important;flex-direction:row!important;gap:3px!important;
 width:100%!important;max-width:none!important;padding:0!important}
.ph-strip__img{flex:1 1 0!important;min-width:0!important;width:auto!important}
.ph-strip__img img{width:100%!important;height:clamp(300px,30vw,420px)!important;
 object-fit:cover!important;display:block!important}

/* ---- puppy culture steps ------------------------------------------- */
.ph-steps{gap:40px!important;padding:8px 0!important;max-width:none!important}
.ph-step .elementor-icon-box-wrapper{display:flex!important;gap:24px!important;
 align-items:flex-start!important;text-align:left!important}
.ph-step .elementor-icon{background:var(--sand)!important;color:var(--espresso)!important;
 width:68px!important;height:68px!important;border-radius:50%!important;display:flex!important;
 align-items:center!important;justify-content:center!important;font-size:22px!important;flex:none!important}
.ph-step .elementor-icon-box-description{font-size:13.5px!important;line-height:1.7!important}

/* ---- health section, photo to the page edge ------------------------ */
.ph-sec--edge{padding-right:0!important}
.ph-edge{display:flex!important;flex-direction:row!important;align-items:center!important;
 gap:clamp(32px,5vw,72px)!important;width:100%!important;max-width:none!important;padding:0!important}
.ph-edge>*{flex:1 1 0!important;min-width:0!important;width:auto!important}
.ph-edge__text{max-width:none!important;gap:22px!important;align-items:flex-start!important;
 padding:0 clamp(24px,3vw,56px) 0 max(0px,calc((100vw - var(--wrap))/2 - var(--gut)))!important}
.ph-edge>.elementor-widget-image img{height:clamp(420px,46vw,620px)!important}

/* ---- our shepherds ------------------------------------------------- */
.ph-head{max-width:820px!important;margin-inline:auto!important;align-items:center!important;
 text-align:center!important;gap:10px!important;padding:0 0 64px!important}
.ph-duo{display:flex!important;flex-direction:row!important;gap:clamp(28px,4vw,56px)!important;
 max-width:var(--wrap)!important;width:100%!important;margin-inline:auto!important;padding:0!important}
.ph-dog{flex:1 1 0!important;min-width:0!important;gap:14px!important;
 align-items:flex-start!important;text-align:left!important;padding:0!important;max-width:none!important}
.ph-dog:nth-child(2){margin-top:clamp(0px,4.5vw,64px)!important}
.ph-cta{align-items:center!important;padding:64px 0 0!important;max-width:none!important}

/* ---- map ------------------------------------------------------------ */
.ph-map iframe,.ph-map .elementor-custom-embed{height:clamp(400px,42vw,560px)!important}

/* ---- hero ----------------------------------------------------------- */
.ph-hero{background-position:center 80%!important;
 position:relative!important;min-height:clamp(560px,82vh,800px)!important;display:flex!important;
 flex-direction:column!important;justify-content:flex-end!important;align-items:flex-start!important;
 padding:120px clamp(56px,7vw,110px) clamp(56px,9vh,104px) var(--gut)!important;overflow:hidden!important}
.ph-hero::after{content:""!important;position:absolute!important;inset:0!important;z-index:1!important;
 pointer-events:none!important;
 background:linear-gradient(105deg,rgba(26,19,13,.62) 0%,rgba(26,19,13,.34) 38%,transparent 66%)!important}
.ph-hero>*{position:relative!important;z-index:2!important}
.ph-hero__in{max-width:600px!important;width:auto!important;gap:10px!important;
 align-items:flex-start!important;padding:0!important}
.ph-hero .elementor-heading-title{color:#FFFFFF!important;font-size:clamp(27px,3.1vw,40px)!important;
 line-height:1.06!important;letter-spacing:-.02em!important}
.ph-hero .ph-script p{color:rgba(246,244,241,.95)!important;font-size:clamp(30px,3.4vw,44px)!important}
.ph-hero__side{position:absolute!important;right:calc(var(--gut)*.55)!important;top:50%!important;
 transform:translateY(-50%) rotate(180deg)!important;writing-mode:vertical-rl!important;z-index:2!important;
 white-space:nowrap!important;border-right:1px solid rgba(247,244,238,.28)!important;
 padding-block:32px!important;width:auto!important}
.ph-hero__side p{font-size:9px!important;font-weight:500!important;letter-spacing:.26em!important;
 text-transform:uppercase!important;color:rgba(247,244,238,.72)!important}

/* ---- litter band: the photograph carries it, copy sits on a card ---- */
.ph-band{position:relative!important;min-height:clamp(420px,54vh,560px)!important;display:flex!important;
 flex-direction:column!important;justify-content:center!important;
 padding:88px var(--gut)!important;overflow:hidden!important}
.ph-band::after{content:""!important;position:absolute!important;inset:0!important;z-index:1!important;
 pointer-events:none!important;
 background:linear-gradient(100deg,rgba(26,19,13,.22) 0%,rgba(26,19,13,.08) 52%,rgba(26,19,13,0) 100%)!important}
.ph-band>*{position:relative!important;z-index:2!important}
.ph-band__card{max-width:480px!important;width:100%!important;background-color:#FFFFFF!important;
 margin-left:max(0px,calc((100% - var(--wrap))/2))!important;
 padding:clamp(30px,3.4vw,46px) clamp(28px,3.2vw,44px) clamp(32px,3.6vw,48px)!important;
 gap:18px!important;align-items:flex-start!important;
 box-shadow:0 18px 44px -28px rgba(28,26,24,.34),0 2px 10px -6px rgba(28,26,24,.16)!important}

@media(max-width:880px){
.ph-hero__side{display:none!important}
.ph-hero{min-height:clamp(480px,74vh,620px)!important;padding-inline:var(--gut)!important}
.ph-split,.ph-edge,.ph-duo{flex-direction:column!important;gap:36px!important}
.ph-strip__row{flex-wrap:wrap!important;gap:3px!important}
.ph-strip__img{flex:0 0 calc(50% - 1.5px)!important}
.ph-sec--edge{padding-right:var(--gut)!important}
.ph-edge__text{padding-left:0!important;padding-right:0!important}
.ph-frame img,.ph-edge>.elementor-widget-image img{height:clamp(300px,78vw,380px)!important}
.ph-strip__img img{height:clamp(220px,58vw,300px)!important}
.ph-dog:nth-child(2){margin-top:0!important}
.ph-list ul{grid-template-columns:1fr}
.ph-trust__row{gap:10px!important}
.ph-band__card{margin-left:0!important;max-width:none!important}
}"""


def resolve(css):
    """Rewrite every .ph-name selector to also match the real element ids.

    Elementor is inconsistent about honouring _css_classes, but it always emits
    elementor-element-{id}, so each semantic class becomes a :is() group listing
    the concrete elements alongside the class itself.
    """
    def sub(m):
        name = m.group(1)
        ids = INDEX.get(name)
        if not ids:
            return m.group(0)
        branches = [f".{name}"] + [f".elementor-element-{i}" for i in ids]
        return ":is(" + ",".join(branches) + ")"
    return re.sub(r"\.(ph-[A-Za-z0-9_-]+)", sub, css)


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "data"
    if mode == "data":
        sys.stdout.write(json.dumps(DATA, separators=(",", ":")))
    elif mode == "css":
        sys.stdout.write(resolve(CSS))
    elif mode == "index":
        sys.stdout.write(json.dumps(INDEX, indent=1))
