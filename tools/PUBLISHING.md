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

Leave header 32 and footer 25 on `include/general`. Elementor prefers the more
specific condition, so the new chrome wins on the named pages and nothing else
changes.

When the site goes live, these two lists collapse to `include/general` and the
old templates come off - but that is a going-live decision, not a page one.

### 4. Bump post_modified

A meta-only write does not update `post_modified`, so WordPress never fires a
save and LiteSpeed never purges the page. Abigail sees a stale render and
reports that nothing changed. Finish every page with a real field write:

    wp_update_post(ID, fields={"post_excerpt": "..."})
