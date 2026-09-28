#!/usr/bin/env python3
"""Measure a draft post against Rank Math's content tests.

Usage: python3 measure.py <post.html> "<focus keyword>"
Prints word count, keyword density, longest paragraph, images, links,
headings with the keyword, and a PASS/FIX line per test.
"""
import re, sys

path, kw = sys.argv[1], sys.argv[2].strip()
h = open(path, encoding="utf-8").read()
text = re.sub(r"<[^>]+>", " ", h)
text = re.sub(r"\s+", " ", text)
words = text.split()
wc = len(words)
kw_re = re.compile(r"\b" + r"\s+".join(re.escape(w) for w in kw.split()) + r"s?\b", re.I)
count = len(kw_re.findall(text))
density = count / wc * 100 if wc else 0
paras = re.findall(r"<p[^>]*>(.*?)</p>", h, re.S)
longest = max((len(re.sub(r"<[^>]+>", " ", p).split()) for p in paras), default=0)
imgs = len(re.findall(r"<img", h))
alts = re.findall(r'alt="([^"]*)"', h)
alt_ok = any(kw_re.search(a) for a in alts)
ext = len(re.findall(r'href="https?://(?!www\.pinehillgermanshepherds\.com)', h))
internal = len(re.findall(r'href="https://www\.pinehillgermanshepherds\.com', h))
heads = re.findall(r"<h[2-6][^>]*>(.*?)</h[2-6]>", h, re.S)
head_ok = sum(1 for x in heads if kw_re.search(x))
first10 = bool(kw_re.search(" ".join(words[: max(1, wc // 10)])))
toc = "wp-block-rank-math-toc-block" in h

def line(ok, label, val):
    print(("PASS " if ok else "FIX  ") + f"{label}: {val}")

line(wc >= 2500, "words (2500+)", wc)
line(1.0 < density <= 2.5, "keyword density 1.0-2.5%", f"{density:.2f}% ({count} uses of '{kw}')")
line(longest <= 120, "longest paragraph <=120 words", longest)
line(imgs >= 3, "images in body (3+, plus featured)", imgs)
line(alt_ok, "keyword in an image alt", alt_ok)
line(head_ok >= 1, "headings containing keyword", head_ok)
line(first10, "keyword in first 10%", first10)
line(internal >= 5, "internal links", internal)
line(ext >= 2, "external links", ext)
line(toc, "Rank Math TOC block present", toc)
