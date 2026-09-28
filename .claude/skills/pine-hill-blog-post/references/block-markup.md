# Gutenberg markup the site uses

## Table of contents block (Rank Math)

The `headings` attribute is mandatory. Without it the block's save function throws and the editor shows a blank page with "undefined is not an object (evaluating 't.headings.length')". One entry per H2 you want listed; the editor regenerates the list with H3s nested when the post is opened.

```
<!-- wp:rank-math/toc-block {"title":"Table of Contents","headings":[{"key":"ph-toc-01","content":"First H2 Text","level":2,"link":"#first-h2-anchor","disable":false,"isUpdated":false,"isGeneratedLink":true},{"key":"ph-toc-02","content":"Second H2 Text","level":2,"link":"#second-h2-anchor","disable":false,"isUpdated":false,"isGeneratedLink":true}],"listStyle":"ul","titleWrapper":"h2","excludeHeadings":[]} -->
<div class="wp-block-rank-math-toc-block" id="rank-math-toc"><h2>Table of Contents</h2><nav><ul><li class=""><a href="#first-h2-anchor">First H2 Text</a></li><li class=""><a href="#second-h2-anchor">Second H2 Text</a></li></ul></nav></div>
<!-- /wp:rank-math/toc-block -->
```

## Headings with anchors

```
<!-- wp:heading {"anchor":"first-h2-anchor"} -->
<h2 class="wp-block-heading" id="first-h2-anchor">First H2 Text</h2>
<!-- /wp:heading -->

<!-- wp:heading {"level":3} -->
<h3 class="wp-block-heading">Question people type?</h3>
<!-- /wp:heading -->
```

## Paragraph, image, list, table

```
<!-- wp:paragraph -->
<p>Text.</p>
<!-- /wp:paragraph -->

<!-- wp:image {"sizeSlug":"large"} -->
<figure class="wp-block-image size-large"><img src="URL" alt="sable German shepherd puppy" class="wp-image-ID"/><figcaption class="wp-element-caption">Optional caption.</figcaption></figure>
<!-- /wp:image -->

<!-- wp:list -->
<ul class="wp-block-list"><!-- wp:list-item -->
<li>Item.</li>
<!-- /wp:list-item --></ul>
<!-- /wp:list -->

<!-- wp:list {"ordered":true} -->
<ol class="wp-block-list"><!-- wp:list-item -->
<li><strong>Bold lead.</strong> Rest.</li>
<!-- /wp:list-item --></ol>
<!-- /wp:list -->

<!-- wp:table -->
<figure class="wp-block-table"><table class="has-fixed-layout"><thead><tr><th>A</th><th>B</th></tr></thead><tbody><tr><td>1</td><td>2</td></tr></tbody></table></figure>
<!-- /wp:table -->
```

## Post meta to set on create

```
"meta_input": {
  "rank_math_focus_keyword": "primary keyword,secondary phrase,another variant",
  "rank_math_title": "Primary Keyword ...: 7 Proven ...",
  "rank_math_description": "Under 160 characters, contains the keyword, names Maine.",
  "rank_math_pillar_content": "on"   (pillar posts only)
}
```
Then `wp_add_post_terms` with taxonomy `category`, terms `[1]`, and `wp_set_featured_image` with a media id from site-facts.
