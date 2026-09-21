#!/usr/bin/env python3
"""The rebrand footer (template 2820), as data + stylesheet.

Until now this lived only in WordPress, which is exactly why it drifted off
the palette while every page moved on without it. It is generated here so it
is versioned, diffable and screenshot-testable like the rest of the site.

Ids are FIXED, not positional: the template already exists on the live site
and a renumber would unstyle it. New elements take new ids at the end.

  python3 build_footer.py data -> _elementor_data JSON
  python3 build_footer.py css  -> Elementor Custom CSS
"""
import json, re, sys

MAIL = "pinehillgermanshepherds@gmail.com"
TEL_H, TEL_L = "207-703-8043", "+12077038043"
LOGO = ("https://www.pinehillgermanshepherds.com/wp-content/uploads/"
        "2026/09/Pine-Hill-Logo.png")
# Both supplied by her. Worth noting the Instagram handle is
# "pinehillshepherds", not "pinehillgermanshepherds" - which is exactly why
# guessing it would have sent her buyers to a stranger's account.
FB = "https://www.facebook.com/profile.php?id=61564685349435"
IG = "https://www.instagram.com/pinehillshepherds/"

def con(i, children, classes="", **s):
    st = {"content_width": "full"}
    st.update(s)
    if classes:
        st["_css_classes"] = classes
    return {"id": i, "elType": "container", "settings": st,
            "elements": children, "isInner": False}

def w(i, t, s, classes=""):
    s = dict(s)
    if classes:
        s["_css_classes"] = classes
    return {"id": i, "elType": "widget", "widgetType": t, "settings": s,
            "elements": []}

def h(i, text, tag="h4", classes=""):
    return w(i, "heading", {"title": text, "header_size": tag}, classes)

def p(i, html, classes=""):
    return w(i, "text-editor", {"editor": f"<p>{html}</p>"}, classes)

def links(i, items, classes="ph-foot__links"):
    body = "".join(
        f"<li><a href='{u}'>{t}</a></li>" if u else f"<li>{t}</li>"
        for t, u in items)
    return w(i, "text-editor", {"editor": f"<ul>{body}</ul>"}, classes)

DATA = [con("phf001", [
    con("phf002", [
        con("phf003", [
            w("phf004", "image", {"image": {"url": LOGO, "id": 0, "size": "",
                                             "alt": "Pine Hill German Shepherds",
                                             "source": "library"},
                                   "image_size": "full"}, "ph-foot__logo"),
            p("phf005", "Working-line German Shepherds raised in our home on "
                        "40 acres in Garland, Maine."),
            p("phf006", "thoughtfully bred, intentionally raised", "ph-script"),
            w("phf020", "social-icons", {
                "social_icon_list": [
                    {"_id": "sfb", "social_icon": {"value": "fab fa-facebook-f",
                                                   "library": "fa-brands"},
                     "link": {"url": FB, "is_external": "true", "nofollow": ""}},
                    {"_id": "sig", "social_icon": {"value": "fab fa-instagram",
                                                   "library": "fa-brands"},
                     "link": {"url": IG, "is_external": "true", "nofollow": ""}},
                ],
                "shape": "square", "columns": "2", "align": "left",
            }, "ph-foot__social"),
        ], "ph-foot__brand"),

        con("phf007", [
            h("phf008", "Explore"),
            links("phf009", [("About Us", "/about-us-maines-german-shepherds-2-2/"),
                             ("Our Shepherds", "/our-shepherds/"),
                             ("Puppies", "/workinglinegermanshepherdpuppies/"),
                             ("Available Litters", "/tgermanshepherdlitterspuppies/"),
                             ("Reserve a Puppy", "/reserve-a-puppy/"),
                             ("Puppy Culture", "/puppy-culture/"),
                             ("Gallery", "/gallery/")]),
        ], "ph-foot__col"),

        # The reach-us column is what people scroll down here for, so it gets
        # the weight: a real address block, not a third list of nav links.
        con("phf017", [
            h("phf018", "Get in Touch"),
            links("phf019", [(TEL_H, f"tel:{TEL_L}"),
                             ("Email us", f"mailto:{MAIL}")],
                  "ph-foot__links ph-foot__contact"),
            p("phf021", "Garland, Penobscot County<br>Maine, USA", "ph-foot__addr"),
        ], "ph-foot__col ph-foot__reach"),
    ], "ph-foot__top", flex_direction="row"),

    w("phf013", "divider", {"style": "solid"}, "ph-foot__rule"),

    con("phf014", [
        p("phf015", "&copy; 2026 Pine Hill German Shepherds"),
        p("phf016", "AKC Registered &middot; Working Line"),
    ], "ph-foot__legal", flex_direction="row"),
], "ph-foot")]

CSS = """.ph-foot{background-color:var(--linen,#F2F0EC)!important;
 border-top:1px solid rgba(28,26,24,.10)!important;
 padding:clamp(64px,8vw,104px) clamp(24px,5vw,56px) clamp(28px,3vw,40px)!important}
.ph-foot__top,.ph-foot__top>.e-con-inner{display:flex!important;flex-direction:row!important;
 align-items:flex-start!important;gap:clamp(32px,4vw,64px)!important;max-width:1180px!important;
 width:100%!important;margin-inline:auto!important;padding:0!important;
 margin-bottom:clamp(40px,5vw,64px)!important}
.ph-foot__brand{flex:1.7 1 0!important;min-width:0!important}
.ph-foot__col{flex:1 1 0!important;min-width:0!important}
.ph-foot__reach{flex:1.2 1 0!important}
.ph-foot__brand>.e-con-inner,.ph-foot__col>.e-con-inner,
.ph-foot__brand,.ph-foot__col{gap:14px!important;padding:0!important;max-width:none!important}

.ph-foot .elementor-heading-title{font-family:'Cormorant Garamond',Georgia,serif!important;
 font-weight:500!important;color:#1C1A18!important;margin:0!important}
.ph-foot__logo .elementor-widget-container{text-align:left!important}
.ph-foot__logo img{max-width:240px!important;width:auto!important;height:auto!important;
 display:block!important;margin:0 auto 4px 0!important}
/* column headings: the darker gold, because the display gold is too faint
   to read at 10.5px */
.ph-foot__col .elementor-heading-title{font-family:'Montserrat',system-ui,sans-serif!important;
 font-size:10.5px!important;font-weight:600!important;letter-spacing:.2em!important;
 text-transform:uppercase!important;color:var(--brass-ink,#7A5F35)!important;
 padding-bottom:4px!important}

.ph-foot .elementor-widget-text-editor,.ph-foot .elementor-widget-text-editor p,
.ph-foot .elementor-widget-text-editor li{font-family:'Montserrat',system-ui,sans-serif!important;
 font-size:13.5px!important;line-height:1.85!important;color:#55504A!important;margin:0!important}
.ph-foot__brand p{max-width:40ch}
.ph-foot__brand .ph-script p{font-family:'Mrs Saint Delafield',cursive!important;
 font-style:normal!important;font-size:clamp(34px,3vw,42px)!important;line-height:1.1!important;
 color:var(--brass,#A48760)!important;padding-top:2px!important}

.ph-foot__links ul{list-style:none!important;margin:0!important;padding:0!important;
 display:grid!important;gap:11px!important}
.ph-foot__links a,.ph-foot__links li{text-decoration:none!important;color:#1C1A18!important;
 font-size:13px!important;letter-spacing:.01em!important;text-transform:none!important}
.ph-foot__links a{border-bottom:1px solid transparent!important;
 transition:color .25s ease,border-color .25s ease}
.ph-foot__links a:hover,.ph-foot__links a:focus-visible{color:var(--brass-ink,#7A5F35)!important;
 border-bottom-color:var(--brass-ink,#7A5F35)!important}
.ph-foot__contact a{font-variant-numeric:lining-nums!important}
.ph-foot__addr p{font-size:13px!important;line-height:1.7!important;padding-top:2px!important}

.ph-foot__social{margin-top:6px!important}
.ph-foot__social .elementor-social-icon{background-color:transparent!important;
 border:1px solid rgba(28,26,24,.18)!important;color:#1C1A18!important;
 width:36px!important;height:36px!important;font-size:14px!important;
 border-radius:0!important;margin:0 8px 0 0!important;
 transition:background-color .25s ease,color .25s ease,border-color .25s ease}
.ph-foot__social .elementor-social-icon:hover,
.ph-foot__social .elementor-social-icon:focus-visible{background-color:#232020!important;
 border-color:#232020!important;color:#F6F4F1!important}

.ph-foot__rule .elementor-divider{padding-block:0!important}
.ph-foot__rule .elementor-divider-separator{border-top:1px solid rgba(28,26,24,.14)!important;
 width:100%!important;max-width:1180px!important;margin-inline:auto!important}
.ph-foot__legal,.ph-foot__legal>.e-con-inner{display:flex!important;flex-direction:row!important;
 justify-content:space-between!important;align-items:center!important;max-width:1180px!important;
 width:100%!important;margin-inline:auto!important;margin-top:clamp(20px,2.4vw,28px)!important;
 padding:0!important}
.ph-foot__legal>*,.ph-foot__legal>.e-con-inner>*{width:auto!important;flex:0 0 auto!important;max-width:none!important}
.ph-foot__legal p{font-size:10px!important;letter-spacing:.16em!important;
 text-transform:uppercase!important;color:#55504A!important}

@media(max-width:980px){
.ph-foot__top,.ph-foot__top>.e-con-inner{flex-wrap:wrap!important;gap:40px 32px!important}
.ph-foot__brand{flex:1 1 100%!important}
.ph-foot__col{flex:1 1 calc(50% - 32px)!important}
}
@media(max-width:640px){
.ph-foot__top,.ph-foot__top>.e-con-inner{flex-direction:column!important;gap:34px!important}
.ph-foot__col{flex:1 1 auto!important}
.ph-foot__legal,.ph-foot__legal>.e-con-inner{flex-direction:column!important;
 align-items:flex-start!important;gap:8px!important}
}"""

def flatten(css):
    """One line, no comments.

    The MCP meta write runs stripslashes on the value, and a newline arrives
    as the two characters backslash-n, so stripslashes leaves a literal "n"
    welded into the rule ("!important;n border-top:..."). Verified by reading
    the value back. So nothing that crosses that wire may contain a newline.
    """
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    css = re.sub(r"\s*\n\s*", "", css)
    return re.sub(r"\s{2,}", " ", css).strip()


def settings(css):
    """custom_css as page settings, for the MCP write's "meta" object.

    Do NOT hand-serialize this. WordPress update_post_meta() runs the value
    through maybe_serialize(), which serializes a string that already looks
    serialized a SECOND time. Elementor then reads a string where it expects
    an array and the site throws a critical error - not at write time, but
    later, whenever something forces the page settings to be parsed. Pass a
    real object and let WordPress serialize it once.

    _elementor_data is the opposite case: Elementor stores it as a JSON
    string, so it goes over the wire as a string and must stay one.
    """
    return {"custom_css": css}


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "data"
    if mode == "data":
        out = json.dumps(DATA, separators=(",", ":"), ensure_ascii=False)
        assert "\\" not in out, "backslash will not survive the MCP write"
        sys.stdout.write(out)
    elif mode == "settings":
        css = flatten(CSS)
        assert "\\" not in css and "\n" not in css
        sys.stdout.write(json.dumps({"_elementor_page_settings": settings(css)},
                                    ensure_ascii=False))
    else:
        sys.stdout.write(CSS)
