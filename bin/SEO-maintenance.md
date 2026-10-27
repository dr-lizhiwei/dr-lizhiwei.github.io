# SEO maintenance

This directory is excluded from the published website. These notes and checks do
not add public pages or change which pages participate in search.

## Before publishing

1. Refresh public citation data with `python bin/update_scholar_citations.py`, then
   build with the production configuration: `bundle exec jekyll build --lsi`.
2. Run the existing CSS optimization: `purgecss -c purgecss.config.js`.
3. Run `python -m unittest discover -s bin -p 'test_*.py'`.
4. Run `python bin/check_site.py _site --site-url https://zhiweili.net`.
5. Run `python bin/check_seo.py _site`.

The deploy workflow runs these checks before publication. SEO validation checks
titles, descriptions, canonical URLs, valid JSON-LD, HTML language, reciprocal
hreflang, share images, heading presence, and local image dimensions. Existing
link validation covers local PDF, image, CSS, font, and script references.

For an update that must preserve all indexable URLs, save the previous sitemap
outside the source directory and additionally run:

`python bin/check_seo.py _site --reference-sitemap /path/to/previous-sitemap.xml`

## Content updates

- Keep existing permalinks and PDF paths stable.
- Use `seo_description` for page and post metadata without changing visible
  introductions. Keep blog `description` as the short citation shown in the index.
- Give both versions of a translated post the same `translation_key`, with `lang:
  en` and `lang: zh-CN`. Both URLs remain independently canonical.
- Local images included with `figure.html` obtain their intrinsic dimensions from
  image headers. Direct HTML images need real width and height attributes.
- The sitemap uses source-file Git modification dates. CI checks out full history;
  ordinary rebuilds do not claim that all content was newly updated. Explicit
  `last_modified_at` values take precedence.
- Keep font license files alongside self-hosted fonts.
- Scholar data is fetched once per deployment from the public author profile.
  If that request fails, the existing saved snapshot remains available;
  each badge shows its data date in its tooltip. Unknown counts are never zeroed.
  A new featured paper also needs its verified `google_scholar_id` in `papers.bib`.

## Search account review (deferred at the owner's request)

Google, Bing, and Baidu verification tags remain enabled. Their presence does not
prove account ownership status, sitemap acceptance, or indexing.

When convenient, inspect the already verified property for `https://zhiweili.net/`
in Google Search Console, Bing Webmaster Tools, and Baidu's search resource
platform. Confirm sitemap acceptance and inspect the homepage, research page,
publication list, positions page, and one English/Chinese article pair. Do not
change canonical or indexing rules merely to remove a report warning.

Record a baseline for a clearly identified date range (for example, the previous
28 days): impressions, clicks, CTR, average position where provided, and indexed
page counts. Separate name-related queries from research-topic queries, and note
country/device filters. Keep unavailable metrics blank rather than treating them
as zero. Compare equal periods after search engines have recrawled the updates.

Private account data has not been retrieved in this update. No metrics, indexing
success, performance score, or ranking increase should be inferred from the local
build checks.
