#!/usr/bin/env python3
"""Fail if any page uses a ph- class that has no rule in its own stylesheet.

A container's _css_classes is never emitted onto the container by Elementor,
so a class with no rule is invisible in the data and only shows up as a
section that renders unstyled - full width, hard left, stray vertical space.
That is exactly how ph-mid shipped. Run this before every push.
"""
import re, subprocess, sys

PAGES = ("about", "reserve", "contact", "gallery", "news", "puppyculture",
         "contract", "puppies", "litters", "shepherds", "freda", "rangeley")

def build(page, mode):
    r = subprocess.run([sys.executable, "tools/build_pages.py", page, mode],
                       capture_output=True, text=True)
    if r.returncode:
        raise SystemExit(f"{page} failed to build:\n{r.stderr}")
    return r.stdout

bad = False
for page in PAGES:
    data, css = build(page, "data"), build(page, "css")
    have = set(re.findall(r"\.(ph-[\w-]+)", css))
    used = set()
    for group in re.findall(r'"_css_classes":"([^"]+)"', data):
        used.update(group.split())
    for group in re.findall(r"class=\\?['\"]([^'\"\\]+)", data):
        used.update(group.split())
    missing = sorted(c for c in used if c not in have)
    slashes = data.count("\\")
    note = []
    if missing:
        note.append(f"no CSS rule: {missing}")
    if slashes:
        note.append(f"{slashes} backslashes (the MCP write eats these)")
    bad = bad or bool(note)
    print(f"  {page:<14} {'; '.join(note) if note else 'clean'}")

raise SystemExit(1 if bad else 0)
