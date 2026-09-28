#!/usr/bin/env python3
"""Render el_data.json as the markup Elementor actually emits, so the page
stylesheet can be screenshot-tested before it goes anywhere near the site.

This does not emulate Elementor's editor - it emulates its front-end DOM:
the .elementor-element-{id} hooks, the .elementor-widget-{type} wrappers and
the inner markup of each widget type used on this page, plus the parts of
Elementor's own base stylesheet that affect layout.
"""
import json, os, sys, html

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
    if t == "posts":
        # Elementor Pro Posts widget, classic skin: the front-end DOM it emits,
        # filled with real titles and featured images from her blog so the
        # grid is judged on the content it will actually carry.
        U = "https://www.pinehillgermanshepherds.com/wp-content/uploads"
        sample = [
            ("German Shepherd Breeders in New England: A Smart Buyer Guide for Finding the Right Program",
             "September 19, 2026", f"{U}/2026/02/ghows-LK-91aec015-bcf2-408a-a9fb-61a6f5ea16a4-4886035b.webp",
             "Searching for German Shepherd breeders in New England turns up a long list very quickly, and the listings tend to look alike. Same photos of puppies in grass, same phrases about health…"),
            ("German Shepherd Puppy Checklist: 25 Must Haves to Prepare Before Pickup Day",
             "September 12, 2026", f"{U}/2026/02/CAMP9905-Edit-scaled.jpg",
             "This German Shepherd puppy checklist exists because of a phone call we get every litter, usually on the evening of go home day, usually about a crate that turned out…"),
            ("German Shepherd Puppy Training: 10 Powerful Habits to Build in the First 30 Days",
             "September 5, 2026", f"{U}/2025/01/AKC-East-Working-Line-German-Shepherd-Puppies-for-Sale-in-Maine-Pine-Hill-German-Shepherds-scaled.jpg",
             "German Shepherd puppy training starts the moment the crate door opens in your driveway, whether you meant to start or not. This breed learns constantly, so your puppy…"),
            ("Early Puppy Socialization: The Vital First 16 Weeks Behind Every Confident Shepherd",
             "August 29, 2026", f"{U}/2026/09/BK700068-scaled.jpg",
             "Early puppy socialization is the closest thing to a guarantee that exists in dog raising. It does not fix genetics and it does not replace training, but it decides…"),
            ("German Shepherd Health Testing: The 5 Clearances That Truly Protect Your Puppy",
             "August 22, 2026", f"{U}/2026/09/BK700074-Edit-scaled.jpg",
             "German Shepherd health testing is the part of a breeding program a buyer never sees and then feels for the next twelve years. Two puppies can look identical in…"),
            ("German Shepherd Puppies Maine: 7 Essential Facts About Freda's Fall 2026 Litter",
             "August 15, 2026", f"{U}/2024/10/AKC-German-Shepherd-Puppies-for-Sale-in-Maine-Pine-Hill-German-Shepherd-Breeders-scaled.jpg",
             "We are so excited to announce that Freda is expecting, and by the end of September we should have working line German Shepherd puppies Maine families can bring…"),
        ]
        n = int(s.get("classic_posts_per_page", 6))
        arts = "".join(
            '<article class="elementor-post elementor-grid-item post">'
            f'<a class="elementor-post__thumbnail__link" href="#"><div class="elementor-post__thumbnail">'
            f'<img src="{im}" alt=""></div></a>'
            '<div class="elementor-post__text">'
            f'<h3 class="elementor-post__title"><a href="#">{html.escape(ti)}</a></h3>'
            f'<div class="elementor-post__meta-data"><span class="elementor-post-date">{dt}</span></div>'
            f'<div class="elementor-post__excerpt"><p>{html.escape(ex)}</p></div>'
            f'<a class="elementor-post__read-more" href="#">{s.get("classic_read_more_text", "Read More")}</a>'
            '</div></article>'
            for ti, dt, im, ex in (sample * 3)[:n])
        pag = ('<nav class="elementor-pagination" aria-label="Pagination">'
               '<span aria-current="page" class="page-numbers current">1</span>'
               '<a class="page-numbers" href="#">2</a><a class="page-numbers" href="#">3</a>'
               '<a class="page-numbers" href="#">4</a><a class="page-numbers" href="#">5</a>'
               f'<a class="next page-numbers" href="#">{s.get("pagination_next_label", "Next")} &raquo;</a></nav>')
        return ('<div class="elementor-posts-container elementor-posts elementor-posts--skin-classic elementor-grid">'
                + arts + "</div>" + pag)
    if t == "theme-post-title":
        tag = s.get("header_size", "h1")
        return (f'<{tag} class="elementor-heading-title elementor-size-default">'
                'German Shepherd Breeders in New England: A Smart Buyer Guide '
                f'for Finding the Right Program</{tag}>')
    if t == "theme-post-featured-image":
        return ('<img src="https://www.pinehillgermanshepherds.com/wp-content/uploads/2026/02/'
                'ghows-LK-91aec015-bcf2-408a-a9fb-61a6f5ea16a4-4886035b.webp" '
                'class="attachment-full size-full wp-post-image" alt="">')
    if t == "theme-post-content":
        here = os.path.dirname(os.path.abspath(__file__))
        return open(os.path.join(here, "sample_post.html")).read()
    if t == "post-navigation":
        return ('<div class="elementor-post-navigation elementor-grid">'
                '<div class="elementor-post-navigation__prev elementor-post-navigation__link">'
                '<a href="#" rel="prev"><span class="post-navigation__arrow-wrapper post-navigation__arrow-prev">&lsaquo;</span>'
                '<span class="elementor-post-navigation__link__prev">'
                f'<span class="post-navigation__prev--label">{s.get("prev_label", "Previous")}</span>'
                '<span class="post-navigation__prev--title">German Shepherd Puppy Checklist: 25 Must Haves to Prepare Before Pickup Day</span>'
                '</span></a></div>'
                '<div class="elementor-post-navigation__separator-wrapper"><div class="elementor-post-navigation__separator"></div></div>'
                '<div class="elementor-post-navigation__next elementor-post-navigation__link">'
                '<a href="#" rel="next"><span class="elementor-post-navigation__link__next">'
                f'<span class="post-navigation__next--label">{s.get("next_label", "Next")}</span>'
                '<span class="post-navigation__next--title">Early Puppy Socialization: The Vital First 16 Weeks</span>'
                '</span><span class="post-navigation__arrow-wrapper post-navigation__arrow-next">&rsaquo;</span></a></div>'
                '</div>')
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
