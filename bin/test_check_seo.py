import json
from pathlib import Path
import tempfile
import unittest

from check_seo import check_seo, inspect_page


def page(url, lang='en', alternate=''):
    schema = json.dumps({'@context': 'https://schema.org', '@type': 'WebPage',
                         'description': 'Quotes "and" a newline\nare escaped safely.'})
    return f'''<html lang="{lang}"><head><title>Research article</title>
    <meta name="description" content="A specific research article summary for readers.">
    <link rel="canonical" href="{url}">{alternate}
    <meta property="og:image" content="https://example.com/image.png">
    <meta name="twitter:image" content="https://example.com/image.png">
    <script type="application/ld+json">{schema}</script></head>
    <body><h1>Research article</h1><img src="/image.png" width="100" height="80" alt="Research diagram"></body></html>'''


class SeoChecks(unittest.TestCase):
    def test_valid_json_escaping(self):
        self.assertEqual(inspect_page(page('https://example.com/'), 'https://example.com/')[1], [])

    def test_unescaped_newline_is_rejected(self):
        document = page('https://example.com/').replace(r'\n', '\n')
        self.assertTrue(any('invalid JSON-LD' in error for error in inspect_page(document, 'https://example.com/')[1]))

    def test_duplicate_canonical_is_rejected(self):
        document = page('https://example.com/').replace('</head>', '<link rel="canonical" href="https://example.com/"></head>')
        self.assertTrue(any('canonical' in error for error in inspect_page(document, 'https://example.com/')[1]))

    def test_empty_blog_title_is_rejected(self):
        document = page('https://example.com/').replace('Research article</title>', '| Homepage</title>')
        self.assertIn('missing meaningful page title', inspect_page(document, 'https://example.com/')[1])

    def test_chinese_language_is_checked(self):
        self.assertTrue(any('zh-CN' in error for error in inspect_page(page('https://example.com/post-CHN/'), 'https://example.com/post-CHN/')[1]))

    def test_intrinsic_dimensions_are_required(self):
        document = page('https://example.com/').replace('height="80"', 'height="auto"')
        self.assertTrue(any('dimensions' in error for error in inspect_page(document, 'https://example.com/')[1]))

    def test_nonreciprocal_translation_is_rejected(self):
        with tempfile.TemporaryDirectory(prefix='seo-check-', dir=Path(__file__).resolve().parent) as folder:
            root = Path(folder)
            urls = ['https://example.com/en/', 'https://example.com/zh/']
            root.joinpath('sitemap.xml').write_text('<urlset>' + ''.join(f'<url><loc>{url}</loc></url>' for url in urls) + '</urlset>')
            for slug, lang in [('en', 'en'), ('zh', 'zh-CN')]:
                root.joinpath(slug).mkdir()
                alternate = '<link rel="alternate" hreflang="en" href="https://example.com/en/"><link rel="alternate" hreflang="zh-CN" href="https://example.com/zh/">' if slug == 'en' else ''
                root.joinpath(slug, 'index.html').write_text(page(f'https://example.com/{slug}/', lang, alternate))
            self.assertTrue(any('link back' in error for error in check_seo(root)[0]))


if __name__ == '__main__':
    unittest.main()
