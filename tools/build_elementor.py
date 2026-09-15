#!/usr/bin/env python3
"""Emit Elementor _elementor_data for the Pine Hill homepage.

Every piece of copy, every photograph and every button is its own widget so
the owner can click and edit it in the Elementor panel. Layout comes from
Elementor's own container controls; the stylesheet only carries appearance
(colour, type, the sand circles, the hero scrim) and lives in the page's
Custom CSS, where the text editor cannot strip it.
"""
import json, sys

U = "https://www.pinehillgermanshepherds.com/wp-content/uploads"
MEDIA = {
    "hero":    (f"{U}/2026/07/hero-sunset.jpg", 0, "Working-line German Shepherd at sunset in Maine"),
    "freda":   (f"{U}/2026/04/Freda-3.jpg", 0, "Frida, our foundation female at Pine Hill German Shepherds"),
}

_n = [0]
def eid(p):
    _n[0] += 1
    return f"ph{p}{_n[0]:03d}"

def container(children, classes="", **settings):
    s = {"content_width": "full", "flex_direction": "column"}
    s.update(settings)
    if classes:
        s["_css_classes"] = classes
    return {"id": eid("c"), "elType": "container", "settings": s,
            "elements": children, "isInner": False}

def widget(wtype, settings, classes=""):
    if classes:
        settings = dict(settings, _css_classes=classes)
    return {"id": eid("w"), "elType": "widget", "widgetType": wtype,
            "settings": settings, "elements": []}

def heading(text, classes="", tag="h2"):
    return widget("heading", {"title": text, "header_size": tag}, classes)

def para(html, classes=""):
    return widget("text-editor", {"editor": f"<p>{html}</p>"}, classes)

def button(text, url, classes=""):
    return widget("button", {"text": text, "link": {"url": url, "is_external": "", "nofollow": ""}}, classes)

def image(key, classes=""):
    url, mid, alt = MEDIA[key]
    return widget("image", {"image": {"url": url, "id": mid, "size": "", "alt": alt, "source": "library"},
                            "image_size": "full"}, classes)

# ---------------------------------------------------------------- sections --
hero = container(
    [
        container(
            [
                heading("New England&#8217;s Dedicated Breeders of Working-Line German Shepherds", tag="h1"),
                para("thoughtfully bred, intentionally raised", "ph-script"),
                button("Meet Our Shepherds", "#story"),
            ],
            classes="ph-hero__in", content_width="full",
        ),
        para("Working-line German Shepherds &middot; Northern Maine", "ph-hero__side"),
    ],
    classes="ph-hero",
    background_background="classic",
    background_image={"url": MEDIA["hero"][0], "id": MEDIA["hero"][1], "size": "", "alt": "", "source": "library"},
    background_position="center center",
    background_size="cover",
)

story = container(
    [container(
        [
            container(
                [
                    para("welcome to pine hill", "ph-script"),
                    heading("Family Raised Working-Line German Shepherds in Northern Maine"),
                    widget("divider", {"style": "solid"}, "ph-rule"),
                    para("We&#8217;re a small family business raising working-line German Shepherds on 40 acres "
                         "of rural countryside in the backwoods of New England. We specialize in producing "
                         "high-quality German Shepherds known for their exceptional personalities, working drive, "
                         "scent detection abilities, and balanced temperaments.", "ph-measure"),
                    para("With only one breeding female, Frida &mdash; our beloved family member &mdash; we have "
                         "the unique opportunity to carefully plan each litter, dedicating countless hours to "
                         "observing and working with our puppies. Raised within our home and surrounded by our "
                         "family, they receive plenty of love and care from day one.", "ph-measure"),
                    button("Read Our Full Story", "/about-us-maines-german-shepherds-2-2/"),
                ],
                classes="ph-panel", content_width="full", _flex_size="grow",
            ),
            image("freda", "ph-frame"),
        ],
        classes="ph-split", content_width="boxed", flex_direction="row",
        flex_align_items="center", flex_gap={"unit": "px", "size": 56, "column": "56", "row": "56", "isLinked": True},
    )],
    classes="ph-sec ph-ivory", flex_direction="column",
)

print(json.dumps([hero, story], separators=(",", ":")))
