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
    # the one she chose for her profile on 2026-09-26
    "freda_pro":    f"{U}/2025/02/Edited-1-scaled.jpg",
    "working":      f"{U}/2026/09/BK706350-scaled.jpg",
    "montie":       f"{U}/2026/04/Cruz-AKC-German-Shepherd-dog-in-NH--scaled.jpg",
    "litter_band":  f"{U}/2026/09/BK700068-scaled.jpg",
    "puppies":      f"{U}/2024/10/AKC-German-Shepherd-Puppies-for-Sale-in-Maine-Pine-Hill-German-Shepherd-Breeders-scaled.jpg",
    "scholars":     f"{U}/2025/01/AKC-East-Working-Line-German-Shepherd-Puppies-for-Sale-in-Maine-Pine-Hill-German-Shepherds-scaled.jpg",
    # Rangeley - the stud. The uploaded filenames spell it "Rangley".
    "rangeley1":    f"{U}/2026/08/Rangley-1-1-scaled.jpg",
    "rangeley2":    f"{U}/2026/08/Rangley-2-scaled.jpg",
    "rangeley3":    f"{U}/2026/08/Rangley-3-scaled.jpg",
    "rangeley4":    f"{U}/2026/08/Rangley-4-scaled.jpg",
    "rangeley5":    f"{U}/2026/08/Rrangley-5-scaled.jpg",
    "rangeley6":    f"{U}/2026/08/Rangley-6-scaled.jpg",
    "rangeley7":    f"{U}/2026/08/Rangley-7-scaled.jpg",
    "portrait":     f"{U}/2026/09/BK700074-Edit-scaled.jpg",
    "pair":         f"{U}/2026/09/BK706246-Edit-scaled.jpg",
    "farm":         f"{U}/2026/09/AB9405DB-D650-4947-A274-59A0754E55A6-scaled.jpg",
    "wks":          f"{U}/2026/04/WKS-scaled.jpg",
    "breeders":     f"{U}/2026/03/EN7A9779-scaled.jpg",
    "sunlit":       f"{U}/2026/07/EN7A8251-scaled-Edit-scaled.jpg",
    # NOT a photograph - this is the Litter A announcement GRAPHIC, with
    # burned-in text and health results. Never use it behind a hero title.
    "litter_graphic": f"{U}/2026/09/Pine-Hill-German-Shepherds-scaled.jpg",
    "band2":        f"{U}/2026/09/BK700064-scaled.jpg",
}

ALT = {
    "freda": "Freda von Stephanitz, our foundation female",
    "freda_pro": "Working Line German Shepherd Breeder in Maine",
    "rangeley1": "Ledger Bei Mackenzie von Franzosisches Haus, called Rangeley",
    "rangeley2": "Rangeley, our stud dog",
    "rangeley3": "Rangeley, working-line German Shepherd sire",
    "rangeley5": "Rangeley at work",
    "working": "AKC working-line German Shepherd in Maine",
    "montie": "Captain Montie, IGP and personal protection",
    "puppies": "German Shepherd puppies raised with Puppy Culture",
    "scholars": "Puppies in the K9 Scholars training programme",
    "portrait": "Working-line German Shepherd portrait",
    "farm": "Pine Hill, Garland, Maine",
    "litter_graphic": "Pine Hill German Shepherds Litter A announcement",
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


def gform(form_id, classes="ph-gf"):
    """A Gravity form, shown through the Ultimate Addons styler widget.

    This is the widget her contact page already uses, and Gravity is the form
    engine that actually delivers mail on this site. Elementor Pro's own form
    widget rejected every submission here with "the form is invalid", so it is
    not used.
    """
    return w("uael-gf-styler", {
        "form_id": str(form_id),
        "form_ajax_option": "yes",
        "form_title_option": "none",
        "form_description_option": "none",
    }, classes)


def pin(node, fixed):
    """Give a node a permanent id instead of a positional one.

    Elementor's form handler finds the form widget by the id the browser posts
    back. Our ids are positional, so adding anything above a form renumbers it,
    and a page a visitor already had open then submits an id that is no longer
    in the page data - Elementor answers "your submission failed because the
    form is invalid" and the answers are lost. A pinned id survives a rebuild.
    """
    old = node["id"]
    node["id"] = fixed
    for ids in INDEX.values():
        for n, i in enumerate(ids):
            if i == old:
                ids[n] = fixed
    return node


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


def spec(pairs, classes="ph-spec"):
    """Inline facts, LABEL: value, one per line - the shape of the reference
    she sent (AKC#, colour, weight...). dl() is the two-column table."""
    rows = "".join(f"<li><b>{k}:</b> {v}</li>" for k, v in pairs)
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


def form(name, fields, button, email_to, subject):
    """An Elementor Pro form. Fields are (type, label, width, extra) tuples.

    Built as data rather than a shortcode so she can open it in the editor and
    change a label or add a question without touching anything else.
    """
    out = []
    for n, (ftype, label, width, extra) in enumerate(fields, 1):
        # custom_id is the one Elementor actually renders with: it becomes the
        # input's name (form_fields[<custom_id>]) and the label's for=. Leave it
        # out and every field submits under an empty key, so the email arrives
        # with the questions and none of the answers. _id alone is not enough.
        fid = f"f{n:02d}"
        f = {"_id": fid, "custom_id": fid, "field_type": ftype,
             "field_label": label, "width": str(width)}
        f.update(extra or {})
        out.append(f)
    return w("form", {
        "form_name": name,
        "form_fields": out,
        "button_text": button,
        "button_size": "sm",
        "submit_actions": ["email"],
        "email_to": email_to,
        "email_subject": subject,
        "email_content": "[all-fields]",
        "email_from": "pinehillgermanshepherds@gmail.com",
        "email_from_name": "Pine Hill German Shepherds",
    }, "ph-form")


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


def opener(title, kicker, image_key, lede=None):
    """An alternative to hero(): the title sits on clean ground and the
    photograph runs full width underneath it, large. Nothing is set over the
    image, so a busy photograph can never collide with the type."""
    section("open")
    head_kids = []
    if kicker:
        head_kids.append(p(kicker, "ph-script"))
    head_kids.append(h(title, tag="h1"))
    head_kids.append(rule(True))
    if lede:
        head_kids.append(p(lede, "ph-lede"))
    return con([con(head_kids, "ph-open__t"),
                img(image_key, "ph-open__img")], "ph-open")


def ph_img(slot, wd, ht, classes="ph-frame2"):
    """A LABELLED placeholder image widget. It is a real Elementor image
    widget, so swapping it is: click the image -> Choose Image -> pick yours.
    Nothing else on the page has to change."""
    return w_img(f"https://placehold.co/{wd}x{ht}/EDE6DF/8A7A66?text={slot}",
                 classes, alt=slot.replace("+", " "))


def w_img(url, classes, alt=""):
    return w("image", {"image": {"url": url, "id": 0, "size": "",
                                 "alt": alt, "source": "library"},
                       "image_size": "full"}, classes)


def bighero(title_html, kicker, image_url=None, slot="Hero+photo"):
    """Inset full-bleed photo with the type set low over it. The photo is a
    CONTAINER BACKGROUND, so it is swapped from the container's Style tab ->
    Background -> Image, not by clicking the picture."""
    section("bhero")
    url = image_url or f"https://placehold.co/2400x1400/EDE6DF/8A7A66?text={slot}"
    inner = con([con([p(kicker, "ph-script"), h(title_html, tag="h1")],
                     "ph-bhero__t")], "ph-bhero__in",
                background_background="classic",
                background_image={"url": url, "id": 0, "size": "",
                                  "alt": "", "source": "library"},
                background_position="center 50%", background_size="cover")
    return con([inner], "ph-bhero")


def splittop(title, kicker, lede, slot="Header+photo", reverse=False):
    """A masthead where the photograph sits beside the title rather than
    behind or above it. Different silhouette from bighero() and opener()."""
    section("stop")
    text = con([p(kicker, "ph-script"), h(title, tag="h1"), rule(False),
                p(lede, "ph-lede")], "ph-stop__t")
    pic = ph_img(slot, 1200, 900, "ph-stop__i")
    kids = [pic, text] if reverse else [text, pic]
    return con([row(kids, "ph-stop__r")], "ph-stop")


def quiettop(title, kicker, lede=None, tone="sand"):
    """A title band with no photograph at all, on a tinted ground."""
    section("qtop")
    # title=None drops the serif h1 and lets the script line carry the band.
    kids = [p(kicker, "ph-script")]
    if title:
        kids.append(h(title, tag="h1"))
    kids.append(rule(True))
    if lede:
        if isinstance(lede, (list, tuple)):
            lede = "</p><p>".join(lede)
        kids.append(p(lede, "ph-lede"))
    return con([con(kids, "ph-qtop__t")], f"ph-qtop ph-qtop--{tone}")


def intro(title, strap, lede):
    section("intro")
    return con([h(title, "ph-introh"), p(strap, "ph-strap"),
                p(lede, "ph-ilede")], "ph-intro")


def vals(title, strap, items):
    """items: list of (svg_markup, label)."""
    section("vals")
    cards = [con([w("html", {"html": svg}, "ph-vicon"), p(label, "ph-vlabel")],
                 "ph-val") for svg, label in items]
    return con([h(title, "ph-valsh"), p(strap, "ph-strap"),
                row(cards, "ph-valsrow")], "ph-vals")


def trivia(kicker, script, items, image=None):
    """items: list of (number, text)."""
    section("triv")
    rows = [con([p(n, "ph-tnum"), p(t, "ph-ttext")], "ph-trow")
            for n, t in items]
    left = con([p(kicker, "ph-tkick"), p(script, "ph-tscript")] + rows,
               "ph-trivl")
    right = image or ph_img("Family+photo", 1200, 900, "ph-frame2")
    return con([con([left, right], "ph-trivin")], "ph-triv")


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
body{--espresso:#1C1A18;--ivory:#F6F4F1;--linen:#F2F0EC;--sand:#E4DFD5;--pill:#DCD8D1;--sage:#232020;
 --sage-deep:#3A3633;--brass:#A48760;--brass-ink:#7A5F35;--body:#55504A;--hair:rgba(28,26,24,.12);
 --gut:clamp(24px,5vw,56px);--wrap:1180px;--sy:clamp(60px,7vw,100px);
 background:#FFFFFF;color:var(--body)}

.elementor-widget-heading .elementor-heading-title{font-family:'Cormorant Garamond',Georgia,serif!important;
 font-weight:500!important;color:var(--espresso)!important;letter-spacing:-.015em!important;
 line-height:1.12!important;margin:0!important;font-size:clamp(26px,2.9vw,38px)!important}
.elementor-widget-text-editor,.elementor-widget-text-editor p,.elementor-widget-text-editor li{
 font-family:'Montserrat',system-ui,sans-serif!important;font-size:14.5px!important;
 line-height:1.85!important;color:var(--body)!important;margin:0!important}
.ph-script,.ph-script p{font-family:'Mrs Saint Delafield',cursive!important;color:var(--brass)!important;
 font-size:clamp(44px,5vw,64px)!important;line-height:1.08!important}
.ph-lede p{font-size:15px!important}
.ph-measure p{max-width:62ch}

.elementor-button{background-color:var(--sage)!important;color:var(--ivory)!important;
 font-family:'Montserrat',system-ui,sans-serif!important;font-size:10.5px!important;font-weight:500!important;
 letter-spacing:.2em!important;text-transform:uppercase!important;border-radius:0!important;
 padding:17px 34px!important;transition:transform .3s cubic-bezier(.22,.9,.32,1),background-color .25s ease}
.elementor-button:hover,.elementor-button:focus{background-color:var(--sage-deep)!important;
 color:var(--ivory)!important;transform:translateY(-2px)}
.elementor-button:focus-visible{outline:2px solid var(--brass)!important;outline-offset:3px!important}

/* A link inside running text. Underlined in brass so it reads as a link
   without turning the paragraph a different colour. */
.elementor-widget-text-editor a{color:var(--espresso);text-decoration:underline;
 text-underline-offset:3px;text-decoration-color:var(--brass);
 transition:color .2s ease,text-decoration-color .2s ease}
.elementor-widget-text-editor a:hover{color:var(--brass);text-decoration-color:var(--brass)}
.elementor-widget-text-editor a:focus-visible{outline:2px solid var(--brass);outline-offset:2px;
 text-decoration:none}
.elementor-widget-text-editor a:active{color:var(--sage-deep)}
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
.ph-hero--slim{min-height:clamp(440px,54vh,620px)!important;justify-content:flex-end!important;
 padding-block:clamp(96px,11vh,140px) clamp(44px,6vh,72px)!important}
.ph-hero::after{content:''!important;position:absolute!important;inset:0!important;z-index:1!important;
 pointer-events:none!important;
 background:linear-gradient(100deg,rgba(26,19,13,.56) 0%,rgba(26,19,13,.28) 46%,rgba(26,19,13,.04) 80%)!important}
.ph-hero>*{position:relative!important;z-index:2!important}
.ph-hero__in{max-width:640px!important;width:auto!important;gap:10px!important;
 align-items:flex-start!important;padding:0!important}
.ph-hero .elementor-heading-title{color:#FFFFFF!important;font-size:clamp(28px,3.4vw,44px)!important;
 line-height:1.06!important;letter-spacing:-.02em!important}
.ph-hero .ph-script p{color:rgba(246,244,241,.92)!important;
 font-size:clamp(34px,3.2vw,44px)!important;margin-bottom:2px!important}

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

.ph-frame img{width:100%!important;height:auto!important;object-fit:contain!important;
 display:block!important;box-shadow:0 2px 6px rgba(28,26,24,.06),0 18px 40px -16px rgba(28,26,24,.20)}
.ph-frame--sq img{height:clamp(300px,30vw,400px)!important;object-fit:cover!important}
.ph-whole img{height:auto!important;width:100%!important;object-fit:contain!important;
 box-shadow:0 2px 6px rgba(28,26,24,.06),0 18px 40px -16px rgba(28,26,24,.20)}

.ph-trio,.ph-quad{display:flex!important;flex-direction:row!important;
 gap:clamp(20px,2.6vw,36px)!important;max-width:var(--wrap)!important;width:100%!important;
 margin-inline:auto!important;padding:0!important;align-items:stretch!important}
.ph-trio>*,.ph-quad>*{flex:1 1 0!important;min-width:0!important;width:auto!important;
 align-self:stretch!important;height:auto!important}
.ph-split>.ph-card{align-self:stretch!important;height:auto!important}

.ph-card{background-color:#FFFFFF!important;border:1px solid var(--hair)!important;
 padding:clamp(24px,2.6vw,34px)!important;gap:12px!important;align-items:flex-start!important;
 max-width:none!important}
.ph-linen .ph-card{background-color:#FFFFFF!important}
.ph-white .ph-card{background-color:var(--linen)!important;border-color:transparent!important}

.ph-stat{gap:2px!important;padding:0 0 0 16px!important;border-left:1px solid var(--brass)!important;
 align-items:flex-start!important;max-width:none!important}
.ph-stat__v p{font-family:'Cormorant Garamond',Georgia,serif!important;font-size:30px!important;
 color:var(--espresso)!important;line-height:1.1!important}
.ph-stat__l p{font-size:10.5px!important;letter-spacing:.18em!important;text-transform:uppercase!important;
 color:var(--brass-ink)!important}

.ph-steps{display:flex!important;flex-direction:row!important;align-items:flex-start!important;
 gap:clamp(20px,2.6vw,36px)!important;max-width:var(--wrap)!important;width:100%!important;
 margin-inline:auto!important;padding:0!important}
.ph-steps>*{flex:1 1 0!important;min-width:0!important;width:auto!important}
.ph-step{gap:8px!important;padding:14px 0 0!important;border-top:1px solid var(--brass)!important;
 align-items:flex-start!important;max-width:none!important}
.ph-step__n p{font-size:10.5px!important;font-weight:600!important;letter-spacing:.18em!important;
 text-transform:uppercase!important;color:var(--brass-ink)!important}
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
 color:var(--brass-ink);flex:0 0 auto}
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
 pointer-events:none!important;background:radial-gradient(ellipse 74% 82% at 50% 50%,rgba(26,19,13,.56) 0%,rgba(26,19,13,.34) 58%,rgba(26,19,13,.14) 100%)!important}
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
.ph-frame img,.ph-whole img{height:auto!important}
.ph-frame--sq img{height:clamp(280px,70vw,360px)!important}
.ph-list ul{grid-template-columns:1fr}
.ph-hero{min-height:clamp(340px,52vh,440px)!important;padding-inline:var(--gut)!important}
.ph-facts li{flex-direction:column;gap:2px}
.ph-facts li em{text-align:left}
}
.ph-open{padding:clamp(56px,6vw,90px) 0 0!important;gap:0!important;background-color:#FFFFFF!important}
.ph-open__t{max-width:900px!important;margin-inline:auto!important;align-items:center!important;
 text-align:center!important;gap:10px!important;
 padding:0 var(--gut) clamp(38px,4.2vw,58px)!important}
.ph-open__t .elementor-heading-title{font-size:clamp(34px,5vw,62px)!important;
 letter-spacing:-.025em!important;line-height:1.04!important}
.ph-open__t .ph-script p{font-size:clamp(38px,4vw,54px)!important;margin-bottom:2px!important}
.ph-open__img img{width:100%!important;height:clamp(400px,56vh,660px)!important;
 object-fit:cover!important;display:block!important;box-shadow:none!important}
.ph-about{max-width:var(--wrap)!important;width:100%!important;margin-inline:auto!important;
 padding:0!important;gap:0!important}
.ph-mid{max-width:820px!important;width:100%!important;margin-inline:auto!important;
 padding:0!important;gap:22px!important;align-items:center!important;text-align:center!important}
.ph-mid p{margin-inline:auto!important}
.ph-formwrap{max-width:820px!important;width:100%!important;margin-inline:auto!important;
 padding:0!important;gap:0!important;text-align:left!important}
@media(max-width:880px){.ph-open__img img{height:clamp(300px,46vh,420px)!important}}

.ph-bhero{padding:0 20px!important;gap:0!important;background-color:#FBF9F6!important}
.ph-bhero__in{position:relative!important;min-height:clamp(440px,78vh,780px)!important;
 overflow:hidden!important;display:flex!important;flex-direction:column!important;
 justify-content:flex-end!important;align-items:center!important;
 background-repeat:no-repeat!important;padding:0!important}
.ph-bhero__in::after{content:''!important;position:absolute!important;inset:0!important;
 z-index:1!important;pointer-events:none!important;
 background:linear-gradient(180deg,rgba(26,19,13,.10) 40%,rgba(26,19,13,.42) 100%)!important}
.ph-bhero__t{position:relative!important;z-index:2!important;text-align:center!important;
 align-items:center!important;padding:0 24px 9%!important;gap:0!important;max-width:none!important}
.ph-bhero__t .ph-script p{font-size:clamp(40px,4.6vw,62px)!important;color:#fff!important;
 margin-bottom:2px!important}
.ph-bhero__t .elementor-heading-title{color:#fff!important;
 font-size:clamp(34px,5.2vw,68px)!important;line-height:1.12!important}
.ph-bhero__t em{font-style:italic!important}
.ph-intro{padding:clamp(64px,8vw,110px) var(--gut) clamp(40px,5vw,66px)!important;
 text-align:center!important;align-items:center!important;gap:0!important;
 max-width:none!important;background-color:#FBF9F6!important}
.ph-introh .elementor-heading-title{color:var(--brass)!important;
 font-size:clamp(30px,4.2vw,54px)!important;max-width:30ch!important;
 margin:0 auto 24px!important;line-height:1.12!important}
.ph-strap p{font-size:12px!important;letter-spacing:.14em!important;
 text-transform:uppercase!important;color:var(--body)!important;margin:0 auto 34px!important}
.ph-ilede p{max-width:74ch!important;margin:0 auto!important;text-align:center!important}
.ph-asplit{max-width:var(--wrap)!important;width:100%!important;margin-inline:auto!important;
 display:flex!important;flex-direction:row!important;align-items:center!important;
 gap:clamp(36px,5vw,84px)!important;padding:clamp(40px,6vw,86px) 0!important}
.ph-frame2{flex:0 0 44%!important;background:#fff!important;padding:14px!important;
 box-shadow:0 2px 6px rgba(28,26,24,.05),0 22px 50px -24px rgba(28,26,24,.22)!important}
.ph-frame2 img{width:100%!important;height:auto!important;display:block!important}
/* the dog pages' own hero (sand): the portrait is the point of the page, so it
   takes the larger share of the row there. The Shepherds page rows keep 44%. */
.ph-sand .ph-frame2{flex:0 0 56%!important}
.ph-acol{flex:1 1 0!important;min-width:0!important;gap:18px!important;padding:0!important;
 align-items:flex-start!important;max-width:none!important}
.ph-pillbtn .elementor-button{border-radius:999px!important;background-color:var(--pill)!important;
 color:var(--espresso)!important;padding:16px 34px!important}
.ph-pillbtn .elementor-button:hover{background:var(--brass)!important;color:#fff!important}
.ph-vals{padding:clamp(56px,7vw,100px) var(--gut)!important;text-align:center!important;
 align-items:center!important;gap:0!important;max-width:none!important;background-color:#FBF9F6!important}
.ph-valsh .elementor-heading-title{color:var(--brass)!important;
 font-size:clamp(26px,3.4vw,44px)!important;margin-bottom:14px!important}
.ph-valsrow{display:flex!important;justify-content:center!important;
 gap:clamp(34px,6vw,96px)!important;flex-wrap:wrap!important;max-width:var(--wrap)!important;
 width:100%!important;margin-inline:auto!important;padding:0!important}
.ph-val{width:170px!important;flex:0 0 170px!important;align-items:center!important;
 text-align:center!important;gap:0!important;padding:0!important;max-width:none!important}
.ph-vicon svg{width:58px!important;height:58px!important;stroke:var(--espresso)!important;
 stroke-width:1.4!important;fill:none!important;stroke-linecap:round!important;
 stroke-linejoin:round!important}
.ph-vlabel p{margin-top:18px!important;font-size:11.5px!important;letter-spacing:.14em!important;
 text-transform:uppercase!important;color:var(--espresso)!important;line-height:1.5!important}
.ph-triv{background-color:var(--sand)!important;padding:clamp(56px,7vw,100px) var(--gut)!important;
 gap:0!important;max-width:none!important}
.ph-trivin{max-width:var(--wrap)!important;width:100%!important;margin-inline:auto!important;
 display:flex!important;flex-direction:row!important;align-items:center!important;
 gap:clamp(36px,5vw,84px)!important;padding:0!important}
.ph-trivl{flex:1 1 0!important;min-width:0!important;gap:0!important;padding:0!important;
 align-items:flex-start!important;max-width:none!important}
.ph-tkick p{font-size:11px!important;letter-spacing:.3em!important;text-transform:uppercase!important;
 color:var(--brass-ink)!important;margin-bottom:14px!important}
.ph-tscript p{font-family:'Mrs Saint Delafield',cursive!important;color:var(--espresso)!important;
 font-size:clamp(46px,5.4vw,72px)!important;line-height:1.05!important;margin-bottom:34px!important}
.ph-trow{display:flex!important;flex-direction:row!important;gap:26px!important;
 align-items:flex-start!important;padding:0 0 30px!important;width:100%!important;
 max-width:none!important}
.ph-tnum p{font-family:'Cormorant Garamond',Georgia,serif!important;font-size:64px!important;
 line-height:.78!important;color:var(--brass)!important;font-variant-numeric:lining-nums!important}
.ph-tnum{flex:0 0 64px!important;width:auto!important;max-width:none!important;padding:0!important}
.ph-ttext{flex:1 1 0!important;min-width:0!important;max-width:none!important;padding:0!important}
.ph-ttext p{font-size:14px!important;line-height:1.8!important}
@media(max-width:880px){
 .ph-asplit,.ph-trivin{flex-direction:column!important}
 .ph-frame2{flex:1 1 auto!important;width:100%!important}
 .ph-bhero__t{padding-bottom:14%!important}
 .ph-trow{gap:18px!important}
}

.ph-stop{padding:clamp(40px,5vw,72px) var(--gut) clamp(32px,4vw,56px)!important;
 gap:0!important;max-width:none!important;background-color:#FBF9F6!important}
.ph-stop__r{max-width:var(--wrap)!important;width:100%!important;margin-inline:auto!important;
 display:flex!important;flex-direction:row!important;align-items:center!important;
 gap:clamp(36px,5vw,80px)!important;padding:0!important}
.ph-stop__t{flex:1 1 0!important;min-width:0!important;align-items:flex-start!important;
 text-align:left!important;gap:12px!important;padding:0!important;max-width:none!important}
.ph-stop__t .elementor-heading-title{font-size:clamp(32px,4.4vw,58px)!important;
 line-height:1.06!important;letter-spacing:-.025em!important}
.ph-stop__t .ph-script p{font-size:clamp(38px,4vw,54px)!important;margin-bottom:0!important}
.ph-stop__i{flex:0 0 46%!important;background:#fff!important;padding:14px!important;
 box-shadow:0 2px 6px rgba(28,26,24,.05),0 22px 50px -24px rgba(28,26,24,.22)!important}
.ph-stop__i img{width:100%!important;height:clamp(320px,42vh,480px)!important;
 object-fit:cover!important;display:block!important}
.ph-qtop{padding:clamp(64px,8vw,116px) var(--gut)!important;gap:0!important;
 max-width:none!important;align-items:center!important}
.ph-qtop--sand{background-color:var(--sand)!important}
.ph-qtop--white{background-color:#FFFFFF!important}
.ph-qtop--linen{background-color:var(--linen)!important}
.ph-qtop__t{max-width:820px!important;margin-inline:auto!important;align-items:center!important;
 text-align:center!important;gap:10px!important;padding:0!important;max-width:820px!important}
.ph-qtop__t .elementor-heading-title{font-size:clamp(34px,4.6vw,60px)!important;
 line-height:1.06!important;letter-spacing:-.025em!important}
.ph-qtop__t .ph-script p{font-size:clamp(38px,4vw,54px)!important;margin-bottom:0!important}
.ph-qtop__t .ph-lede p+p{margin-top:14px!important}
.ph-gridsec{padding:clamp(40px,5vw,72px) var(--gut)!important;gap:0!important;
 max-width:none!important}
@media(max-width:880px){
 .ph-stop__r{flex-direction:column!important}
 .ph-stop__i{flex:1 1 auto!important;width:100%!important}
}

.ph-grid{display:grid!important;grid-template-columns:repeat(3,1fr)!important;
 gap:clamp(14px,1.8vw,24px)!important;max-width:1440px!important;width:100%!important;
 margin-inline:auto!important;padding:0!important}
.ph-grid img,.ph-gcell img{width:100%!important;height:clamp(240px,24vw,340px)!important;
 object-fit:cover!important;display:block!important;box-shadow:none!important}
@media(max-width:980px){.ph-grid{grid-template-columns:repeat(2,1fr)!important}}
@media(max-width:600px){.ph-grid{grid-template-columns:1fr!important}
 .ph-grid img,.ph-gcell img{height:clamp(240px,62vw,320px)!important}}
.ph-dog{align-items:flex-start!important;gap:14px!important;padding:0!important;
 max-width:none!important;flex:1 1 0!important;min-width:0!important}
.ph-dog .elementor-heading-title{font-size:clamp(26px,3vw,38px)!important}
.ph-dogname p{font-size:10.5px!important;letter-spacing:.2em!important;
 text-transform:uppercase!important;color:var(--brass-ink)!important}
/* Dog profile block, after the reference she sent 2026-09-26: portrait
   left at half the row (5:6, no mat), registered name as the kicker, call
   name large in the darker gold, an italic byline, the write-up, inline
   LABEL: value facts, two flat sand buttons. */
.ph-pro{max-width:var(--wrap)!important;width:100%!important;margin-inline:auto!important;
 display:flex!important;flex-direction:row!important;align-items:flex-start!important;
 gap:clamp(32px,4.8vw,68px)!important;padding:clamp(24px,3vw,40px) 0!important}
.ph-pro__pic{flex:0 0 50%!important;min-width:0!important;padding:0!important}
.ph-pro__pic img{width:100%!important;aspect-ratio:5/6!important;height:auto!important;
 object-fit:cover!important;display:block!important}
.ph-pro__txt{flex:1 1 0!important;min-width:0!important;align-items:flex-start!important;
 text-align:left!important;gap:0!important;padding:6px 0 0!important;max-width:none!important}
.ph-pro__txt .elementor-widget-text-editor p{font-size:15px!important;line-height:1.9!important;
 max-width:52ch!important;margin:0 0 18px!important}
.ph-pro__kick p{font-size:12.5px!important;font-weight:500!important;letter-spacing:.08em!important;
 text-transform:uppercase!important;color:var(--espresso)!important;line-height:1.6!important;
 margin:0!important}
.ph-pro__name .elementor-heading-title{font-size:clamp(44px,5vw,64px)!important;line-height:1!important;
 color:var(--brass-ink)!important;letter-spacing:-.02em!important;margin:14px 0 12px!important}
.ph-pro__by p{font-family:'Cormorant Garamond',Georgia,serif!important;font-style:italic!important;
 font-size:16px!important;max-width:none!important;letter-spacing:0!important;color:var(--body)!important;
 margin:0 0 26px!important;white-space:nowrap!important}
@media(max-width:1100px){.ph-pro__by p{white-space:normal!important}}
.ph-pro__by a{color:var(--brass-ink)!important;text-decoration:underline!important;text-underline-offset:3px!important}
.ph-spec ul{list-style:none!important;margin:0!important;padding:0!important}
.ph-spec li{font-size:13px!important;letter-spacing:.06em!important;text-transform:uppercase!important;
 line-height:2.15!important;color:var(--espresso)!important}
.ph-spec li b{font-weight:600!important}
.ph-spec a{color:var(--brass-ink)!important;text-decoration:underline!important;
 text-underline-offset:3px!important;text-transform:none!important;letter-spacing:.02em!important}
.ph-pro__btns{flex-direction:row!important;flex-wrap:wrap!important;gap:24px!important;padding:0!important;
 margin-top:32px!important;max-width:none!important;width:auto!important}
.ph-pro__btns>*{width:auto!important;flex:0 0 auto!important}
.ph-pro__btn .elementor-button{background-color:var(--sand)!important;color:var(--espresso)!important;
 font-size:9.5px!important;letter-spacing:.16em!important;padding:15px 28px!important}
.ph-pro__btn .elementor-button:hover,.ph-pro__btn .elementor-button:focus{background-color:var(--pill)!important;
 color:var(--espresso)!important;transform:none!important}
@media(max-width:880px){
.ph-pro{flex-direction:column!important}
.ph-pro__pic{flex:1 1 auto!important;width:100%!important}
}
/* Elementor's lightbox fits an image DOWN to the viewport but never up, so
   a small scan opens at its native pixel size in the middle of a dark
   screen. Fill the viewport instead. Capped at 1600px: upscaling further
   only adds blur. This cannot make a low-resolution screenshot sharp - the
   real fix for a certificate is uploading the document itself. */
.elementor-lightbox .elementor-lightbox-image{width:min(94vw,1600px)!important;
 max-width:94vw!important;height:auto!important;max-height:90vh!important;
 object-fit:contain!important}
"""


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


def split_rules(css):
    """Split minified CSS into top-level chunks, keeping @media blocks whole."""
    out, depth, start = [], 0, 0
    for i, ch in enumerate(css):
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                out.append(css[start:i + 1])
                start = i + 1
    return out


def prune(css, data_json):
    """Drop rules that can never match this page.

    A rule is kept when any of its selectors is NOT page-specific - global
    rules like body, .elementor-button, .elementor-widget-heading - or when it
    names a ph- class or an element id this page actually contains. An @media
    block is pruned the same way from the inside, and dropped if it empties.
    """
    import re
    names = set(re.findall(r'"_css_classes":"([^"]+)"', data_json))
    # classes also appear inside editor HTML, e.g. <span class='ph-fill'>,
    # and those are invisible to a _css_classes-only scan
    names |= set(re.findall(r"class=\\?['\"]([^'\"\\]+)", data_json))
    used = {c for group in names for c in group.split()}
    used |= set(re.findall(r'"id":"([a-z0-9]+)"', data_json))

    def keep(selector):
        for sel in selector.split(","):
            sel = sel.strip()
            tokens = re.findall(r"[.#]([\w-]+)", sel)
            specific = [t for t in tokens
                        if t.startswith("ph-") or t.startswith("elementor-element-")]
            if not specific:
                return True                      # global rule
            for t in specific:
                if t.startswith("elementor-element-"):
                    if t[len("elementor-element-"):] in used:
                        return True
                elif t in used:
                    return True
        return False

    out = []
    for chunk in split_rules(css):
        if chunk.startswith("@media"):
            head = chunk[:chunk.index("{") + 1]
            inner = chunk[chunk.index("{") + 1:-1]
            kept = [r for r in split_rules(inner)
                    if keep(r[:r.index("{")])]
            if kept:
                out.append(head + "".join(kept) + "}")
        elif "{" in chunk and keep(chunk[:chunk.index("{")]):
            out.append(chunk)
    return "".join(out)


def emit(data, extra_css=""):
    j = json.dumps(data, separators=(",", ":"), ensure_ascii=False)
    return (j, prune(minify(resolve(CSS + "\n" + extra_css)), j))
