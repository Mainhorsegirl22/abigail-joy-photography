---
name: pine-hill-blog-post
description: Write, optimize and publish blog posts for pinehillgermanshepherds.com (Pine Hill German Shepherds, a working line German Shepherd breeder in Garland, Maine) that score 90+ in Rank Math and read like the breeder wrote them, not an AI. Use this whenever the user asks for a blog post, article, pillar page, content calendar, "posts for next week", a rewrite of an existing post, or anything about ranking, SEO score, Rank Math, or keywords for the Pine Hill site, even if they do not say "blog" or "SEO". Also use it when merging or redirecting old Pine Hill posts.
---

# Pine Hill blog post

The site is WordPress with Rank Math Pro. Posts are written and saved through the WordPress MCP tools (`wp_create_post`, `wp_update_post`, `wp_alter_post`, `wp_update_post_meta`, `wp_set_featured_image`). The score the owner looks at is the Rank Math number in the editor sidebar. It is computed from a fixed list of tests, so a post can be built to pass them on purpose while still sounding like a person. Both halves matter: a 95 that reads like a robot gets rewritten, and a beautiful post that scores 60 does not rank.

## Workflow

1. **Pick the topic and keyword.** Buyer-intent topics only: questions a family asks before, during or right after buying a puppy (cost, lines, colour, sex, health testing, reserving, first weeks home, crate, biting, winter, breeder questions). Skip generic breed-care content that AKC and PetMD already own. Check the site's existing posts first (`wp_get_posts` with `search`) so the new post does not duplicate a live one, and choose a focus keyword no other post uses.
2. **Choose a short focus keyword.** Two to four words that will occur naturally 25+ times in 2,600 words ("sable German Shepherd", "crate training", "puppy biting"). Put the longer search query in the title instead. Rank Math counts exact-phrase occurrences, so a seven-word keyword forces robotic repetition. Add the long query and one variant as secondary keywords, comma separated.
3. **Draft to a local file first**, then run `scripts/measure.py` on it. Fix anything red before sending to WordPress. Targets are in the table below.
4. **Create the post as a draft** with `wp_create_post`: title, slug, excerpt, content, and `meta_input` carrying `rank_math_title`, `rank_math_description`, `rank_math_focus_keyword`. Then `wp_add_post_terms` category 1 (Blog) and `wp_set_featured_image`. Never publish; the owner reads it and publishes.
5. **Read it back once** (`wp_get_post`) to confirm the block markup survived, especially the table of contents block.
6. Tell the owner the post ID, the editor link `https://www.pinehillgermanshepherds.com/wp-admin/post.php?post=<ID>&action=edit`, and the measured numbers. Say plainly that the final score is computed in her editor.

## What Rank Math scores

Read `references/rank-math-rules.md` for the full table with point values. The tests that decide whether a post lands above 90:

| Test | Target |
|---|---|
| Focus keyword in SEO title, in the first half of it | Start the title with it |
| SEO title has a number, a power word and a sentiment word | "7 Proven", "9 Smart", "10 Vital ... Safe". Proven, Powerful, Remarkable and Smart cover both power and sentiment. Essential and Vital are power only, so pair them with a sentiment word like safe, best, love, right, wrong |
| Keyword in URL, URL under 75 characters | Slug contains the keyword words in order, hyphenated |
| Keyword in meta description and in the first 10% of the text | Use it in sentence one |
| Content length | 2,500+ words counts full |
| Keyword density | Between 1.0% and 2.5%. Aim 1.1 to 1.3 |
| Keyword in at least one H2/H3 and in at least one image alt | Headings with the keyword; alts short and plain |
| Rank Math table of contents block present | Required markup in `references/block-markup.md`. It crashes the editor if the `headings` attribute is missing |
| Four or more images | Body images plus the featured image |
| No paragraph over 120 words | Keep them 40 to 90 |
| Internal links, external links, at least one dofollow external | 8+ internal, 3+ external (AKC, OFA, USCA, Wikipedia) |
| Focus keyword not used on another post | Check with the list in `references/site-facts.md` and update it when you add one |

## Voice

Read `references/voice.md` before writing. The short version:

- The breeder is writing, not a content team. First person. "We" for the family and the program, "I" when it is her own opinion or experience. She uses exclamation points and rhetorical questions occasionally and it reads fine.
- Open with the phone call, the question, or the mistake families make. Never with a definition.
- Concrete over general: Freda, Rangeley, the kitchen floor, the baseboards, Garland, an hour north of Bangor, seven week temperament tests, day three to day sixteen.
- Uneven rhythm. Some fragments. A sentence that starts with "And" or "But". Do not write in matched triplets or "X, not Y" pairs more than once per post.
- Opinions with reasons. "We do not let families pick by photo, and here is why."
- No hedging filler, no "in today's world", no "it is important to note", no bullet lists of adjectives, no closing summary paragraph.
- Only state facts about the program that are on the site. Do not invent customer stories, litter dates, prices or health results.

## Structure that works

Intro paragraph (keyword in sentence one), a portrait photo, the table of contents block, then H2 sections that answer the question in the title, a comparison table or numbered list where the topic has one, a "how we do it at Pine Hill" section that links to Our Shepherds, Litters and Reserve a Puppy, and a FAQ of five to seven H3 questions people actually type. Three or four images spaced through the body. Alt text is a plain phrase with the keyword in it, like the owner writes: "sable German shepherd puppy", "working line German shepherd breeder".

## Pitfalls that cost real time

- Any backslash inside a tool parameter is consumed once by the harness. Gutenberg block attributes use plain double quotes, so the content is safe. Do not try to write Elementor data or anything with escaped quotes through these tools.
- The table of contents block must carry a full `headings` array in its attributes or the editor white-screens. Copy the template.
- `wp_alter_post` with `regex: true` and `flags: "s"` is the cheap way to replace one block after the fact.
- The owner's developer (Robert) edits the site in Elementor at the same time. Touch posts only, never pages, templates or options.
- Reuse existing media URLs from `references/site-facts.md`; the tools cannot upload photos. The owner swaps in new photos herself.
