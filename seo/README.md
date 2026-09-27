# SEO working files

- `content-audit.csv` / `content-audit.md`: every published blog post grouped by the query it targets, with keep / merge / redirect / noindex / delete. A plan, not an action. Nothing is trashed until it is approved.
- `redirects-go-live.csv`: import into Redirection (Tools > Redirection > Import) **on launch day, after the slugs are renamed**, not before. Columns are Redirection's CSV format: source, target, regex, code. Drop the header row if the importer complains.

## Go-live sequence the redirect map assumes

1. Trash page 2287 (the empty old `/puppies/`).
2. Rename each rebuilt page's slug from `*-new` to the final slug in the target column. Where the final slug is held by an old page (`/our-shepherds/`, `/reserve-a-puppy/`, `/puppy-culture/`, `/gallery/`, `/news/`), trash the old page first so WordPress does not append `-2`.
3. Remove `noindex` from the rebuilt pages (the `rank_math_robots` meta).
4. Import the CSV. Test every source URL.
5. Set page 70 (Global Styles) to private.
6. Resubmit the sitemap in Search Console.

Old slugs that the new pages inherit directly need no row: WordPress serves the new page at the old address.
