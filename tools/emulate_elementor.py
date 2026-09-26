#!/usr/bin/env python3
"""Render el_data.json as the markup Elementor actually emits, so the page
stylesheet can be screenshot-tested before it goes anywhere near the site.

This does not emulate Elementor's editor - it emulates its front-end DOM:
the .elementor-element-{id} hooks, the .elementor-widget-{type} wrappers and
the inner markup of each widget type used on this page, plus the parts of
Elementor's own base stylesheet that affect layout.
"""
import json, sys, html

BASE = """
*{box-sizing:border-box}
body{margin:0}
.e-con{--width:100%;position:relative;display:flex;flex-direction:column;width:var(--width);
  max-width:var(--width);align-content:flex-start}
.e-con>.elementor-widget{max-width:100%}
.elementor-widget{position:relative;width:100%}
.elementor-widget-container{}
.elementor-heading-title{margin:0}
.elementor-widget-text-editor p{margin:0 0 1em}
.elementor-widget-text-editor p:last-child{margin-bottom:0}
.elementor-button{display:inline-block;text-decoration:none;line-height:1;
  background-color:#61ce70;color:#fff;padding:12px 24px;border-radius:3px}
.elementor-button-wrapper{}
.elementor-divider{display:flex;padding-block:10px}
.elementor-divider-separator{display:block;width:100%;border-top:1px solid #000}
.elementor-icon-box-wrapper{display:block;text-align:center}
.elementor-icon{display:inline-block;font-style:normal;line-height:1}
.elementor-icon-box-title{margin:0}
.elementor-icon-box-description{margin:0}
.elementor-widget-image img{display:inline-block;max-width:100%;height:auto;vertical-align:middle}
.elementor-custom-embed{line-height:0}
.elementor-custom-embed iframe{width:100%;border:0}
"""

# stand-in glyphs so the icon circles have something in them
GLYPH = {"heart": "♥", "paw": "✿", "seedling": "❀"}


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
    if t == "html":
        return s.get("html", "")
    if t == "shortcode":
        return '<div style="min-height:220px;background:#E8E5DF"></div>'
    if t == "sbi-widget":
        # Smash Balloon feed: stand in with six tinted squares so the section
        # can be judged for rhythm before it ever touches the live site.
        cells = "".join('<div style="aspect-ratio:1;background:#DCD8D1"></div>' for _ in range(6))
        return ('<div id="sb_instagram" style="display:grid;grid-template-columns:repeat(6,1fr);gap:8px">'
                + cells + "</div>")
    return ""


def render(node):
    i = node["id"]
    s = node.get("settings", {})
    extra = s.get("_css_classes", "")
    if node["elType"] == "container":
        full = s.get("content_width") == "full"
        cls = (f'elementor-element elementor-element-{i} e-flex e-con '
               f'{"e-con-full" if full else "e-con-boxed"} {extra}')
        st = f'flex-direction:{s.get("flex_direction", "column")};'
        if s.get("background_image"):
            st += (f'background-image:url(\'{s["background_image"]["url"]}\');'
                   'background-position:center center;background-size:cover')
        style = f' style="{st}"'
        kids = "".join(render(k) for k in node.get("elements", []))
        return f'<div class="{cls}" data-id="{i}"{style}>{kids}</div>'
    t = node["widgetType"]
    cls = (f'elementor-element elementor-element-{i} elementor-widget '
           f'elementor-widget-{t} {extra}')
    return (f'<div class="{cls}" data-id="{i}">'
            f'<div class="elementor-widget-container">{widget_inner(t, s)}</div></div>')


if __name__ == "__main__":
    data = json.load(open(sys.argv[1]))
    css = open(sys.argv[2]).read()
    body = "".join(render(n) for n in data)
    sys.stdout.write(
        "<!doctype html><html><head><meta charset='utf-8'>"
        "<meta name='viewport' content='width=device-width,initial-scale=1'>"
        f"<style>{BASE}</style><style>{css}</style></head><body>{body}</body></html>")
