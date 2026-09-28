# Rank Math content analysis, as scored on pinehillgermanshepherds.com

Pulled from the plugin's own analyzer.js (Rank Math 1.0.279). The score shown in the editor is points earned divided by points applicable, times 100. Tests and their point values:

| Test id | Points | Passes when |
|---|---|---|
| keywordInTitle | 36 | The focus keyword words appear in order in the SEO title |
| titleStartWithKeyword | 3 | The keyword begins before the midpoint of the SEO title |
| titleHasNumber | 1 | Any digit in the SEO title |
| titleHasPowerWords | 1 | A word from Rank Math's power word list. Known to pass: Proven, Powerful, Remarkable, Smart, Essential, Vital, Ultimate, Best |
| titleSentiment | 1 | AFINN sentiment score is not zero. Proven +2, powerful +2, remarkable +2, smart +1, best +3, love +3, right +4, wrong -2, safe +1, honest +2, worth +2. Essential and vital score 0 |
| keywordInMetaDescription | 2 | Keyword in the SEO description |
| keywordInPermalink | 5 | Slugified keyword is a contiguous substring of the slug |
| lengthPermalink | 4 | Slug at most 75 characters |
| keywordIn10Percent | 3 | Keyword within the first 10% of the words |
| keywordInContent | 3 | Keyword anywhere in the text |
| lengthContent | 8 | 2,500+ words for full points. 2,000 gives 5, 1,500 gives 4, 1,000 gives 3, 600 gives 2 |
| keywordDensity | 6 | Count of exact keyword phrase (and plural variants) divided by word count. Over 1.0% up to 2.5% gives 6. 0.76 to 1.0 gives 3. 0.5 to 0.75 gives 2. Below 0.5 or above 2.5 gives 0 |
| keywordInSubheadings | 3 | Keyword words in order inside any h2 to h6 |
| keywordInImageAlt | 2 | Keyword words, in order, anywhere in one img alt attribute |
| contentHasAssets | 6 | Images counted from img tags plus the featured image. 1 image gives 1, 2 gives 2, 3 gives 4, 4 or more gives 6 |
| contentHasShortParagraphs | 3 | No paragraph over 120 words |
| contentHasTOC | 2 | The text contains `wp-block-rank-math-toc-block` |
| linksHasInternal | 5 | At least one link to the same domain |
| linksHasExternals | 4 | At least one link to another domain |
| linksNotAllExternals | 2 | At least one external link without rel=nofollow |
| keywordNotUsed | info | Rank Math asks the database whether another post uses the same focus keyword. Keep keywords unique anyway |

Word count strips HTML tags first, so alt text and block comments do not count but captions, table cells and list items do.
