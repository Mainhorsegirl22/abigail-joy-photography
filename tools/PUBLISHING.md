# Publishing a new page

Four steps. Miss the third and the page renders with the *old* header and
footer, which is what happened to Puppies and Available Litters.

### 1. Create the page

`wp_create_post`, post_type `page`, status `private`, with this meta:

    _elementor_edit_mode      builder
    _elementor_template_type  wp-page
    _wp_page_template         elementor_header_footer

### 2. Write the content

Two meta writes: `_elementor_data` (the JSON from `build_pages.py <page> wire`)
and `_elementor_page_settings` as a nested object `{custom_css: "..."}` passed
in the tool's `meta` argument, not `key`/`value` - `meta` is what the server
reads when both are present, and only `meta` can carry a nested object.

**The write runs stripslashes on the value, so a lone backslash never
survives the trip.** `Male\nFemale` arrives as `MalenFemale`; JSON's own `\"`
escapes arrive as bare `"` and corrupt the document. That is what broke header
2737 and footer 2820 - not the double quotes themselves.

So: send the JSON with every backslash doubled. `build_pages.py <page> wire`
does exactly that, and `data` gives the plain JSON for reading and diffing.
`\uXXXX` is decoded in transit instead of being stripped, so it arrives as the
real character either way; only the backslash needs the doubling.

Test any uncertainty cheaply: write a throwaway meta key, read it back, then
`wp_delete_post_meta` it.

### 3. Attach the new header and footer  ← the one that gets forgotten

The rebrand header (2737) and footer (2820) are attached to named pages only,
so the live site keeps its existing chrome until Abigail says otherwise. Add
the new page id to both lists in the option
`elementor_pro_theme_builder_conditions`:

    header.2737  += "include/singular/page/<id>"
    footer.2820  += "include/singular/page/<id>"

**2737 and 2820 are the only header and footer the rebrand uses.** Older
attempts are still in the library - headers 2581 and 2574, footers 2582 and
2575, and the part-template 2738 - and they are attached to nothing. Never
attach one of them to a page. Abigail has seen the footer change between
pages once already and it was wrong both times.

Leave header 32 and footer 25 on `include/general`. Elementor prefers the more
specific condition, so the new chrome wins on the named pages and nothing else
changes.

When the site goes live, these two lists collapse to `include/general` and the
old templates come off - but that is a going-live decision, not a page one.

### 2b. Never push data without the stylesheet  ← the page-goes-flat rule

Elementor puts a widget's `_css_classes` on the widget, but **it does not put a
container's `_css_classes` on the container**. A container renders as

    <div class="elementor-element elementor-element-conxc11 e-con-full e-flex e-con">

with no `ph-crow` on it. Every container-level rule in our stylesheet therefore
only ever matches through its id twin - which is why `resolve()` writes those
twins in the first place.

Our ids are positional, so any change to the page renumbers the containers
below it. Push `_elementor_data` without pushing the matching `custom_css` and
every container rule aims at ids that no longer exist: the type still looks
right, because widget classes survive, but the layout is gone and the page
reads as one long unformatted column.

**So the two writes are one operation.** Regenerate both from the same build
and send both, every time:

    python3 build_pages.py <page> wire > data
    python3 build_pages.py <page> css  > css

### 3b. Elementor's element cache  ← the one that cost a whole afternoon

Elementor 3.25+ ships an experiment called **Element Caching**. When it is on,
Elementor stores the *rendered HTML* of the page in postmeta `_elementor_element_cache`
and serves that to visitors instead of re-rendering `_elementor_data`.

Writing `_elementor_data` does not invalidate it. The result looks exactly like
a caching bug you cannot purge:

* the Elementor editor shows the new page - it reads `_elementor_data`
* the front end shows the old page - it reads `_elementor_element_cache`
* purging LiteSpeed changes nothing, because LiteSpeed is not the cache
* a `?v=2` cache-buster changes nothing either, for the same reason

**There are two switches, and turning off the experiment is not enough.**

    elementor_experiment-e_element_cache = inactive   <- the experiment
    elementor_element_cache_ttl          = disable    <- the real one

In Elementor 4 the caching lives in Settings > Performance > Element Caching,
stored as `elementor_element_cache_ttl` (hours, default 24). With the
experiment set to `inactive` but the TTL still at 24, pages kept being cached
and kept serving the old copy. Both are now off. In the admin it is
**Elementor > Settings > Performance > Element Caching > Disable**.

**Leave it off for the rest of the rebuild.** To expire one page's copy, write

    _elementor_element_cache = {"timeout":1,"value":{"content":"","scripts":[],"styles":[]}}

A timeout in the past makes Elementor re-render. `wp_delete_post_meta` on this
key returns "Deletion failed", so overwrite it rather than deleting it.

### 3c. Clear the compiled page CSS  ← why a style change never shows

Writing `_elementor_page_settings.custom_css` is not enough. Elementor
**compiles** that CSS once and stores the result in postmeta `_elementor_css`,
then serves the compiled copy. Change `custom_css` through the MCP and the
compiled copy is untouched, so the page keeps its old styling for ever - the
content updates, the layout and type do not.

After every CSS write, expire it:

    _elementor_css = {"0":"","time":0,"fonts":[],"icons":[],
                      "dynamic_elements_ids":[],"status":"empty","css":""}

`time: 0` is older than the post's modified date, so Elementor recompiles on
the next page load. Pass it in the tool's `meta` argument so it stores as an
array, the same as `_elementor_page_settings`.

### 4. Bump post_modified

A meta-only write does not update `post_modified`, so WordPress never fires a
save and LiteSpeed never purges the page. Abigail sees a stale render and
reports that nothing changed. Finish every page with a real field write:

    wp_update_post(ID, fields={"post_excerpt": "..."})

## (3d) NEVER hand-write or blank `_elementor_css`

`_elementor_css` is Elementor's **compiled** stylesheet record. Writing
`{"status":"empty","css":""}` does not mean "rebuild me" — it means "this post
needs no CSS", and Elementor obeys it forever. Deleting the meta is safe;
blanking it is not. Hand-writing a replacement is worse: a `time` value in the
future permanently blocks regeneration.

The only safe way to force a rebuild is to make `post_modified` newer than the
stored `time`:

    wp_update_post(ID, fields={"post_modified": "<now>", "post_modified_gmt": "<now utc>"})

Elementor compares the two on the next front-end view and recompiles from
`_elementor_data` + `_elementor_page_settings.custom_css`. Verify `custom_css`
is still present before relying on this.

The one-click equivalent, which also covers the kit and every template, is
**Elementor -> Tools -> Regenerate Files & Data**.

## (5) LiteSpeed Cache is installed on this site

LiteSpeed Cache 7.9.1 is active. It is a full-page cache and it is NOT purged
by MCP meta writes. Logged-in admins normally bypass it, but logged-out
visitors can keep seeing an old page long after the database is correct.
After any publish, purge it: admin bar -> LiteSpeed -> Purge All.
