#!/usr/bin/env python3
"""Single post template - Elementor Pro theme builder template 20.

    python3 build_post.py data  -> _elementor_data (plain JSON)
    python3 build_post.py wire  -> same, backslashes doubled for the MCP write
    python3 build_post.py css   -> _elementor_page_settings.custom_css

The template renders every blog post: date over a serif title, the featured
photograph, the post body at a reading measure, previous/next, then the same
waiting-list band the other pages close on. Fonts, colours, tracking and
section spacing come from phkit so a post reads as one page of the site,
not the old one.

The post widgets (theme-post-title, theme-post-featured-image,
theme-post-content, post-navigation) are Elementor Pro's own. Their
dynamic tags are written exactly as Elementor stores them, which is the one
place this JSON carries backslashes - hence the wire mode.
"""
import json
import os
import sys
from urllib.parse import quote

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from phkit import start, section, con, w, p, rule, cta, emit  # noqa: E402


def tag(name, settings=None):
    """An Elementor dynamic tag, as the editor serialises it."""
    s = json.dumps(settings or {}, separators=(",", ":"))
    return f'[elementor-tag id="" name="{name}" settings="{quote(s, safe="")}"]'


def post():
    start("pst")
    section("head")
    head = con([
        w("text-editor", {
            "editor": "<p>September 19, 2026</p>",
            "__dynamic__": {"editor": tag("post-date", {
                "type": "post_date_gmt", "format": "F j, Y"})},
        }, "ph-post__date"),
        w("theme-post-title", {
            "header_size": "h1",
            "__dynamic__": {"title": tag("post-title")},
        }, "ph-post__title"),
        rule(centred=True),
    ], "ph-post__head")

    section("pic")
    img = w("theme-post-featured-image", {"image_size": "full"}, "ph-post__img")

    section("body")
    body = con([w("theme-post-content", {}, "ph-post__content")], "ph-post__body")

    section("nav")
    nav = w("post-navigation", {
        "show_label": "yes", "prev_label": "Previous", "next_label": "Next",
        "show_arrow": "", "show_title": "yes", "show_borders": "",
        "in_same_term": [], "post_taxonomy": "category",
    }, "ph-post__nav")

    d = [con([head, img, body, nav], "ph-sec ph-white ph-post")]
    d.append(cta("Want to Hear First?",
                 "The waiting list is short and it moves.",
                 "Join the Waiting List", "/reserve-a-puppy-new/",
                 image_key="litter_band"))
    return d


EXTRA = """
/* Post page. One column, the reading measure of a book page. */
.ph-post{padding-top:clamp(40px,5vw,72px)!important}
.ph-post__head{max-width:820px!important;width:100%!important;margin-inline:auto!important;
 align-items:center!important;text-align:center!important;gap:14px!important;
 padding:0 0 clamp(28px,3.4vw,44px)!important}
.ph-post__date p{font-size:10.5px!important;font-weight:600!important;letter-spacing:.2em!important;
 text-transform:uppercase!important;color:var(--brass-ink)!important}
.ph-post__title .elementor-heading-title{font-size:clamp(30px,3.8vw,50px)!important;
 line-height:1.1!important;letter-spacing:-.02em!important;text-wrap:balance}
.ph-post__img{max-width:1040px!important;width:100%!important;margin-inline:auto!important}
.ph-post__img img{width:100%!important;aspect-ratio:16/9!important;height:auto!important;
 object-fit:cover!important;display:block!important;
 box-shadow:0 2px 6px rgba(28,26,24,.06),0 18px 40px -16px rgba(28,26,24,.20)}
.ph-post__body{max-width:720px!important;width:100%!important;margin-inline:auto!important;
 padding:clamp(40px,5vw,64px) 0 0!important;gap:0!important;align-items:stretch!important}
/* The body is WordPress content, so the elements are the editor's own. */
.ph-post__content p{font-family:'Montserrat',system-ui,sans-serif!important;font-size:16px!important;
 line-height:1.85!important;color:var(--body)!important;margin:0 0 22px!important}
.ph-post__content h2,.ph-post__content h3,.ph-post__content h4{
 font-family:'Cormorant Garamond',Georgia,serif!important;font-weight:500!important;
 color:var(--espresso)!important;letter-spacing:-.015em!important;line-height:1.15!important}
.ph-post__content h2{font-size:clamp(25px,2.7vw,34px)!important;margin:44px 0 14px!important}
.ph-post__content h3{font-size:clamp(21px,2.2vw,26px)!important;margin:34px 0 10px!important}
.ph-post__content h4{font-size:19px!important;margin:28px 0 8px!important}
.ph-post__content ul,.ph-post__content ol{margin:0 0 24px!important;padding:0 0 0 22px!important}
.ph-post__content li{font-family:'Montserrat',system-ui,sans-serif!important;font-size:15.5px!important;
 line-height:1.8!important;color:var(--body)!important;margin:0 0 10px!important}
.ph-post__content li::marker{color:var(--brass)}
.ph-post__content strong{color:var(--espresso)!important;font-weight:600!important}
.ph-post__content a{color:var(--espresso)!important;text-decoration:underline!important;
 text-underline-offset:3px!important;text-decoration-color:var(--brass)!important;
 transition:color .2s ease}
.ph-post__content a:hover{color:var(--brass)!important}
.ph-post__content a:focus-visible{outline:2px solid var(--brass);outline-offset:2px;text-decoration:none!important}
.ph-post__content a:active{color:var(--sage-deep)!important}
.ph-post__content figure,.ph-post__content .wp-block-image{margin:36px 0!important;max-width:none!important}
.ph-post__content img{width:100%!important;max-width:100%!important;height:auto!important;display:block!important}
.ph-post__content figcaption{font-family:'Montserrat',system-ui,sans-serif!important;font-size:10.5px!important;
 letter-spacing:.2em!important;text-transform:uppercase!important;color:var(--brass-ink)!important;
 text-align:center!important;margin:12px 0 0!important}
.ph-post__content blockquote{margin:36px 0!important;padding:4px 0 4px 26px!important;
 border-left:1px solid var(--brass)!important;background:none!important}
.ph-post__content blockquote p{font-family:'Cormorant Garamond',Georgia,serif!important;font-style:italic!important;
 font-size:22px!important;line-height:1.5!important;color:var(--espresso)!important;margin:0!important}
.ph-post__content hr{border:0!important;border-top:1px solid var(--hair)!important;margin:40px 0!important}
.ph-post__content>*:last-child{margin-bottom:0!important}
/* Previous / next. Two quiet links on a hairline, no arrows. */
.ph-post__nav{max-width:720px!important;width:100%!important;margin:clamp(48px,6vw,80px) auto 0!important;
 padding:28px 0 0!important;border-top:1px solid var(--hair)!important}
.ph-post__nav .elementor-post-navigation{display:flex!important;justify-content:space-between!important;
 align-items:flex-start!important;gap:32px!important}
.ph-post__nav .elementor-post-navigation__separator-wrapper{display:none!important}
.ph-post__nav .elementor-post-navigation__link{flex:1 1 0!important;min-width:0!important}
.ph-post__nav .elementor-post-navigation__next{text-align:right!important}
.ph-post__nav .elementor-post-navigation__link a{display:flex!important;flex-direction:column!important;
 gap:6px!important;text-decoration:none!important}
.ph-post__nav .elementor-post-navigation__next a{align-items:flex-end!important}
.ph-post__nav .elementor-post-navigation__link__prev,.ph-post__nav .elementor-post-navigation__link__next{
 display:flex!important;flex-direction:column!important;gap:6px!important;min-width:0!important}
.ph-post__nav .elementor-post-navigation__link__next{align-items:flex-end!important}
.ph-post__nav .post-navigation__arrow-wrapper{display:none!important}
.ph-post__nav .post-navigation__prev--label,.ph-post__nav .post-navigation__next--label{
 font-family:'Montserrat',system-ui,sans-serif!important;font-size:10.5px!important;font-weight:600!important;
 letter-spacing:.2em!important;text-transform:uppercase!important;color:var(--brass-ink)!important}
.ph-post__nav .post-navigation__prev--title,.ph-post__nav .post-navigation__next--title{
 font-family:'Cormorant Garamond',Georgia,serif!important;font-weight:500!important;font-size:20px!important;
 line-height:1.25!important;color:var(--espresso)!important;transition:color .2s ease}
.ph-post__nav a:hover .post-navigation__prev--title,.ph-post__nav a:hover .post-navigation__next--title{
 color:var(--brass)!important}
.ph-post__nav a:focus-visible{outline:2px solid var(--brass);outline-offset:3px}
@media(max-width:600px){
 .ph-post__title .elementor-heading-title{font-size:clamp(26px,7vw,32px)!important}
 .ph-post__content p{font-size:15px!important}
 .ph-post__content h2{font-size:24px!important;margin-top:36px!important}
 .ph-post__nav .elementor-post-navigation{flex-direction:column!important;gap:22px!important}
 .ph-post__nav .elementor-post-navigation__next{text-align:left!important}
 .ph-post__nav .elementor-post-navigation__next a,.ph-post__nav .elementor-post-navigation__link__next{align-items:flex-start!important}
}
"""

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "data"
    j, c = emit(post(), EXTRA)
    if mode == "data":
        sys.stdout.write(j)
    elif mode == "wire":
        sys.stdout.write(j.replace("\\", "\\\\"))
    elif mode == "css":
        sys.stdout.write(c)
