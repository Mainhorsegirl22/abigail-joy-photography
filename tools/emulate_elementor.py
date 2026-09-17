#!/usr/bin/env python3
"""Render el_data.json the way Elementor's front end renders it.

Two halves, both of which have to be right or the emulation lies:

  1. BASE - Elementor's own static frontend stylesheet, the part that defines
     what .e-con actually is.  Elementor containers do almost nothing directly:
     they set custom properties, and this stylesheet turns those properties
     into layout.  A boxed container puts its flex layout on .e-con-inner, a
     full one puts it on itself; getting that wrong is the difference between
     a page that stacks and a page that lays out.

  2. elementor_css() - the per-element rules Elementor compiles from each
     element's settings.  These are reproduced from the real compiled output
     read back off the site (postmeta _elementor_css on page 2804), so the
     control names and value shapes here are observed, not guessed.

Usage: emulate.py el_data.json page.css > page.html
"""
import json, sys, html

BASE = r"""
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0}
:root{--container-max-width:1140px;--widgets-spacing:20px}

/* ---- Elementor container model ------------------------------------- */
.e-con{
 --border-radius:0;
 --container-widget-width:100%;
 --container-widget-height:initial;
 --container-widget-flex-grow:0;
 --container-widget-align-self:initial;
 --content-width:min(100%,var(--container-max-width,1140px));
 --width:100%;
 --min-height:initial;
 --height:auto;
 --text-align:initial;
 --margin-block-start:0px;--margin-block-end:0px;
 --margin-inline-start:0px;--margin-inline-end:0px;
 --padding-block-start:var(--container-default-padding-block-start,10px);
 --padding-block-end:var(--container-default-padding-block-end,10px);
 --padding-inline-start:var(--container-default-padding-inline-start,10px);
 --padding-inline-end:var(--container-default-padding-inline-end,10px);
 --position:relative;--z-index:auto;--overflow:visible;
 --gap:var(--widgets-spacing,20px);
 --row-gap:var(--widgets-spacing,20px);
 --column-gap:var(--widgets-spacing,20px);
 --overlay-opacity:.5;
 position:var(--position);
 width:var(--width);
 min-width:0;
 min-height:var(--min-height);
 height:var(--height);
 border-radius:var(--border-radius);
 z-index:var(--z-index);
 overflow:var(--overflow);
 margin-block-start:var(--margin-block-start);
 margin-block-end:var(--margin-block-end);
 margin-inline-start:var(--margin-inline-start);
 margin-inline-end:var(--margin-inline-end);
 --flex-wrap-mobile:wrap;
}
.e-con.e-flex{--flex-basis:auto;--flex-grow:0;--flex-shrink:1;
 flex:var(--flex-grow) var(--flex-shrink) var(--flex-basis)}

/* a full-width container is its own flex parent and carries its own padding */
.e-con-full,.e-con>.e-con-inner{
 padding-block-start:var(--padding-block-start);
 padding-block-end:var(--padding-block-end);
 padding-inline-start:var(--padding-inline-start);
 padding-inline-end:var(--padding-inline-end);
}
.e-con-full.e-flex,.e-con.e-flex>.e-con-inner{
 display:var(--display,flex);
 flex-direction:var(--flex-direction,column);
 flex-wrap:var(--flex-wrap,nowrap);
 justify-content:var(--justify-content,normal);
 align-items:var(--align-items,normal);
 align-content:var(--align-content,normal);
 gap:var(--row-gap) var(--column-gap);
}
/* a boxed container is only a full-bleed band; .e-con-inner is the measure */
.e-con-boxed{display:flex;flex-direction:column;text-align:initial;gap:initial;
 padding-block-start:0;padding-block-end:0;padding-inline-start:0;padding-inline-end:0}
.e-con>.e-con-inner{width:100%;max-width:var(--content-width);margin-inline:auto;
 text-align:var(--text-align);height:100%}

.e-con>.elementor-widget{
 width:var(--container-widget-width,100%);
 max-width:100%;
 height:var(--container-widget-height);
 flex-grow:var(--container-widget-flex-grow);
 align-self:var(--container-widget-align-self);
}
.e-con>.e-con{max-width:100%}

/* background overlay pseudo-element */
.e-con>.elementor-background-overlay{content:'';display:block;position:absolute;
 inset:0;z-index:0;opacity:var(--overlay-opacity);pointer-events:none}
.e-con>.elementor-widget,.e-con>.e-con{position:relative;z-index:1}

/* ---- widgets -------------------------------------------------------- */
.elementor-widget{position:relative}
.elementor-heading-title{margin:0}
.elementor-widget-text-editor p{margin:0 0 1em}
.elementor-widget-text-editor p:last-child{margin-bottom:0}
.elementor-button{display:inline-block;text-decoration:none;line-height:1;
 background-color:#61ce70;color:#fff;padding:12px 24px;border-radius:3px}
.elementor-divider{display:flex;padding-block:10px}
.elementor-divider-separator{display:block;width:100%;border-top:1px solid #000}
.elementor-icon-box-wrapper{display:block;text-align:center}
.elementor-icon{display:inline-block;font-style:normal;line-height:1}
.elementor-icon-box-title,.elementor-icon-box-description{margin:0}
.elementor-widget-image{text-align:center}
.elementor-widget-image img{display:inline-block;max-width:100%;height:auto;vertical-align:middle}
.elementor-custom-embed{line-height:0}
.elementor-custom-embed iframe{width:100%;border:0}
"""


# Photographs live on the site and the sandbox cannot fetch them, so swap in a
# neutral tile of the same aspect. Layout is what these screenshots are for.
TILE = ("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' "
        "width='1200' height='800'><rect width='1200' height='800' fill='%23b9b2a7'/>"
        "<rect x='0' y='0' width='1200' height='800' fill='none' stroke='%23908a80' "
        "stroke-width='4'/></svg>")


def stub_images(css_or_html):
    import re as _re
    return _re.sub(r"https://www\.pinehillgermanshepherds\.com/wp-content/uploads/[^\"')\s]+", TILE,
                   css_or_html)

GLYPH = {"heart": "♥", "paw": "✿", "seedling": "❀"}
PAGE = "2804"


# --------------------------------------------------------------- compiled css
def _dim(v, prop):
    """Elementor writes padding/margin as logical longhands."""
    u = v.get("unit", "px")
    m = {"top": "block-start", "right": "inline-end",
         "bottom": "block-end", "left": "inline-start"}
    out = []
    for k, side in m.items():
        if v.get(k, "") != "":
            out.append(f"--{prop}-{side}:{v[k]}{u};")
    return "".join(out)


def _size(v):
    if v is None:
        return None
    return f'{v.get("size","")}{v.get("unit","px")}'


def elementor_css(nodes):
    """Reproduce the per-element rules Elementor compiles from settings.

    Elementor writes one block per breakpoint: the bare control name is
    desktop, "_tablet" goes in a max-width:1024px query and "_mobile" in a
    max-width:767px query (the two viewports set in this site's kit).
    """
    buckets = {"": [], "_tablet": [], "_mobile": []}

    def sel(i):
        return f".elementor-{PAGE} .elementor-element.elementor-element-{i}"

    def g(s, name, dev):
        return s.get(name + dev) if (name + dev) in s else None

    def walk(n):
        i, s = n["id"], n.get("settings", {})
        for dev in ("", "_tablet", "_mobile"):
            d = []
            if n["elType"] == "container":
                fd = g(s, "flex_direction", dev)
                if dev == "" and fd is None:
                    fd = "column"
                if fd is not None:
                    d.append("--display:flex;")
                    d.append(f"--flex-direction:{fd};")
                    if fd == "row":
                        d.append("--container-widget-width:calc( ( 1 - var( --container-widget-flex-grow ) ) * 100% );"
                                 "--container-widget-height:100%;--container-widget-flex-grow:1;"
                                 "--container-widget-align-self:stretch;")
                    else:
                        d.append("--container-widget-width:100%;--container-widget-height:initial;"
                                 "--container-widget-flex-grow:0;--container-widget-align-self:initial;")
                for ctl, var in (("flex_align_items", "--align-items"),
                                 ("flex_justify_content", "--justify-content"),
                                 ("flex_wrap", "--flex-wrap"),
                                 ("overflow", "--overflow")):
                    v = g(s, ctl, dev)
                    if v:
                        d.append(f"{var}:{v};")
                gp = g(s, "flex_gap", dev)
                if gp:
                    u = gp.get("unit", "px")
                    d.append(f'--row-gap:{gp.get("row", gp.get("size", 0))}{u};'
                             f'--column-gap:{gp.get("column", gp.get("size", 0))}{u};')
                bw = g(s, "boxed_width", dev)
                if bw and s.get("content_width") == "boxed":
                    d.append(f"--content-width:{_size(bw)};")
                wd = g(s, "width", dev)
                if wd and s.get("content_width", "boxed") == "full":
                    d.append(f"--width:{_size(wd)};")
                mh = g(s, "min_height", dev)
                if mh:
                    d.append(f"--min-height:{_size(mh)};")
                for ctl, prop in (("padding", "padding"), ("margin", "margin")):
                    v = g(s, ctl, dev)
                    if v:
                        d.append(_dim(v, prop))
                fg = g(s, "_flex_grow", dev)
                if fg is not None:
                    d.append(f"--flex-grow:{fg};")
                if dev == "" and s.get("box_shadow_box_shadow"):
                    b = s["box_shadow_box_shadow"]
                    d.append("box-shadow:{h}px {v}px {bl}px {sp}px {c};".format(
                        h=b.get("horizontal", 0), v=b.get("vertical", 0),
                        bl=b.get("blur", 0), sp=b.get("spread", 0), c=b.get("color", "")))
            else:
                al = g(s, "align", dev)
                if al:
                    buckets[dev].append(sel(i) + "{text-align:" + al + ";}")
                ew = g(s, "_element_custom_width", dev)
                if ew and s.get("_element_width") == "initial":
                    d.append(f"width:{_size(ew)};max-width:{_size(ew)};")
                if dev == "" and n.get("widgetType") == "divider":
                    d.append("--divider-border-style:solid;--divider-color:#000;--divider-border-width:1px;")
            if d:
                buckets[dev].append(sel(i) + "{" + "".join(d) + "}")

        if n["elType"] == "container":
            if s.get("background_color"):
                buckets[""].append(sel(i) + "{background-color:" + s["background_color"] + ";}")
            bi = s.get("background_image", {}) or {}
            if bi.get("url"):
                if s.get("background_position") == "initial":
                    pos = f'{_size(s.get("background_xpos"))} {_size(s.get("background_ypos"))}'
                else:
                    pos = s.get("background_position", "center center")
                buckets[""].append(
                    sel(i) + ":not(.elementor-motion-effects-element-type-background){"
                    f'background-image:url("{bi["url"]}");'
                    f'background-position:{pos};'
                    f'background-repeat:{s.get("background_repeat", "no-repeat")};'
                    f'background-size:{s.get("background_size", "cover")};}}')
            if s.get("background_overlay_background") == "gradient":
                a = s.get("background_overlay_gradient_angle", {}).get("size", 180)
                g1, s1 = s.get("background_overlay_color", ""), _size(s.get("background_overlay_color_stop"))
                g2, s2 = s.get("background_overlay_color_b", ""), _size(s.get("background_overlay_color_b_stop"))
                buckets[""].append(
                    sel(i) + " > .elementor-background-overlay{"
                    f"background-image:linear-gradient({a}deg, {g1} {s1}, {g2} {s2});}}")
            if s.get("background_overlay_opacity"):
                buckets[""].append(sel(i) + " > .elementor-background-overlay{--overlay-opacity:"
                                   + str(s["background_overlay_opacity"].get("size", .5)) + ";}")
            for k in n.get("elements", []):
                walk(k)

    for n in nodes:
        walk(n)
    out = "\n".join(buckets[""])
    if buckets["_tablet"]:
        out += "\n@media(max-width:1024px){" + "\n".join(buckets["_tablet"]) + "}"
    if buckets["_mobile"]:
        out += "\n@media(max-width:767px){" + "\n".join(buckets["_mobile"]) + "}"
    return out


# ------------------------------------------------------------------- markup
def widget_inner(t, s):
    if t == "heading":
        tag = s.get("header_size", "h2")
        return f'<{tag} class="elementor-heading-title elementor-size-default">{s["title"]}</{tag}>'
    if t == "text-editor":
        return s["editor"]
    if t == "button":
        return ('<div class="elementor-button-wrapper">'
                '<a class="elementor-button elementor-button-link elementor-size-sm" href="#">'
                '<span class="elementor-button-content-wrapper">'
                f'<span class="elementor-button-text">{s["text"]}</span>'
                '</span></a></div>')
    if t == "image":
        im = s["image"]
        return f'<img src="{im["url"]}" alt="{html.escape(im.get("alt",""))}">'
    if t == "divider":
        return ('<div class="elementor-divider">'
                '<span class="elementor-divider-separator"></span></div>')
    if t == "icon-box":
        icon = s["selected_icon"]["value"].replace("fas fa-", "")
        return ('<div class="elementor-icon-box-wrapper">'
                '<div class="elementor-icon-box-icon">'
                f'<span class="elementor-icon">{GLYPH.get(icon, "✦")}</span></div>'
                '<div class="elementor-icon-box-content">'
                f'<h4 class="elementor-icon-box-title"><span>{s["title_text"]}</span></h4>'
                f'<p class="elementor-icon-box-description">{s["description_text"]}</p>'
                '</div></div>')
    if t == "google_maps":
        return ('<div class="elementor-custom-embed">'
                '<iframe src="about:blank" style="background:#dcd8d1;height:400px"></iframe></div>')
    if t == "shortcode":
        return '<div style="min-height:220px;background:#E8E5DF"></div>'
    if t == "html":
        return s.get("html", "")
    return ""


def render(node):
    i = node["id"]
    s = node.get("settings", {})
    extra = s.get("_css_classes", "")
    if node["elType"] == "container":
        full = s.get("content_width", "boxed") == "full"
        cls = (f'elementor-element elementor-element-{i} e-flex e-con '
               f'{"e-con-full" if full else "e-con-boxed"} {extra}')
        kids = "".join(render(k) for k in node.get("elements", []))
        overlay = ('<div class="elementor-background-overlay"></div>'
                   if s.get("background_overlay_color") or s.get("background_overlay_image", {}).get("url")
                   else "")
        if full:
            return f'<div class="{cls}" data-id="{i}">{overlay}{kids}</div>'
        return (f'<div class="{cls}" data-id="{i}">{overlay}'
                f'<div class="e-con-inner">{kids}</div></div>')
    t = node["widgetType"]
    cls = (f'elementor-element elementor-element-{i} elementor-widget '
           f'elementor-widget-{t} {extra}')
    return (f'<div class="{cls}" data-id="{i}">'
            f'<div class="elementor-widget-container">{widget_inner(t, s)}</div></div>')


if __name__ == "__main__":
    data = json.load(open(sys.argv[1]))
    custom = open(sys.argv[2]).read() if len(sys.argv) > 2 else ""
    body = stub_images("".join(render(n) for n in data))
    sys.stdout.write(
        "<!doctype html><html><head><meta charset='utf-8'>"
        "<meta name='viewport' content='width=device-width,initial-scale=1'>"
        "<link rel='stylesheet' href='https://fonts.googleapis.com/css2?"
        "family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400;1,500&"
        "family=Montserrat:wght@300;400;500;600&family=Mrs+Saint+Delafield&display=swap'>"
        f"<style>{BASE}</style><style>{stub_images(elementor_css(data))}</style>"
        f"<style>{custom}</style></head>"
        f"<body class='elementor elementor-{PAGE}'>{body}</body></html>")
