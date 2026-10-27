#!/usr/bin/env python3
"""Validate generated SEO metadata without making network requests."""

import argparse
import json
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import xml.etree.ElementTree as ET


class Metadata(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.lang = ''
        self.title = []
        self.in_title = False
        self.h1 = 0
        self.meta = {}
        self.links = []
        self.schemas = []
        self.schema = None
        self.images = []

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if tag == 'html':
            self.lang = attrs.get('lang', '')
        elif tag == 'title':
            self.in_title = True
        elif tag == 'h1':
            self.h1 += 1
        elif tag == 'meta':
            key = attrs.get('name') or attrs.get('property')
            if key:
                self.meta.setdefault(key, []).append(attrs.get('content', ''))
        elif tag == 'link':
            self.links.append(attrs)
        elif tag == 'script' and attrs.get('type') == 'application/ld+json':
            self.schema = []
        elif tag == 'img':
            self.images.append(attrs)

    def handle_endtag(self, tag):
        if tag == 'title':
            self.in_title = False
        elif tag == 'script' and self.schema is not None:
            self.schemas.append(''.join(self.schema))
            self.schema = None

    def handle_data(self, data):
        if self.in_title:
            self.title.append(data)
        if self.schema is not None:
            self.schema.append(data)


def sitemap_urls(path):
    root = ET.parse(path).getroot()
    return [item.text for item in root.findall('{*}url/{*}loc')]


def normalized(url):
    parts = urlsplit(url)
    return parts.scheme, parts.netloc, unquote(parts.path).replace('/index.html', '/')


def inspect_page(text, url):
    metadata = Metadata()
    metadata.feed(text)
    errors = []
    title = ''.join(metadata.title).strip()
    if not title or title.startswith('|'):
        errors.append('missing meaningful page title')
    if metadata.h1 != 1:
        errors.append(f'expected one H1, found {metadata.h1}')
    descriptions = metadata.meta.get('description', [])
    if len(descriptions) != 1 or len(descriptions[0].strip()) < 20:
        errors.append('missing or duplicate meta description')
    if not metadata.lang:
        errors.append('missing HTML language')
    if '-CHN/' in url and metadata.lang != 'zh-CN':
        errors.append('Chinese article must declare zh-CN')
    canonical = [link.get('href', '') for link in metadata.links if link.get('rel') == 'canonical']
    if len(canonical) != 1 or normalized(canonical[0]) != normalized(url):
        errors.append('canonical must identify this sitemap URL')
    if any('noindex' in value.lower() for value in metadata.meta.get('robots', [])):
        errors.append('noindex page is listed in sitemap')
    if not metadata.schemas:
        errors.append('missing JSON-LD')
    for raw in metadata.schemas:
        try:
            value = json.loads(raw)
            if not isinstance(value, dict) or not value.get('@context') or not value.get('@type'):
                errors.append('JSON-LD must have context and type')
        except (ValueError, TypeError) as error:
            errors.append(f'invalid JSON-LD: {error}')
    for name in ('og:image', 'twitter:image'):
        values = metadata.meta.get(name, [])
        if len(values) != 1 or not values[0].startswith('https://'):
            errors.append(f'{name} must contain one absolute HTTPS URL')
    for image in metadata.images:
        if not image.get('alt'):
            errors.append('image is missing descriptive alt text')
        source = image.get('src', '')
        local = source.startswith('/') or not urlsplit(source).scheme
        if local and source:
            if not all(image.get(key, '').isdigit() and int(image[key]) > 0 for key in ('width', 'height')):
                errors.append(f'local image lacks intrinsic dimensions: {source}')
    return metadata, errors


def check_seo(directory, reference_sitemap=None):
    directory = Path(directory)
    errors = []
    try:
        urls = sitemap_urls(directory / 'sitemap.xml')
    except (OSError, ET.ParseError) as error:
        return [f'invalid sitemap: {error}'], 0
    if len(urls) != len(set(urls)):
        errors.append('sitemap contains duplicate URLs')
    if reference_sitemap and set(urls) != set(sitemap_urls(reference_sitemap)):
        errors.append('sitemap URL set changed from the supplied baseline')
    pages = {}
    for url in urls:
        path = directory / unquote(urlsplit(url).path).lstrip('/')
        if not path.suffix or path.is_dir():
            path = path / 'index.html'
        if not path.is_file():
            errors.append(f'{url}: sitemap target is missing')
            continue
        metadata, page_errors = inspect_page(path.read_text(encoding='utf-8'), url)
        pages[normalized(url)] = metadata
        errors.extend(f'{url}: {error}' for error in page_errors)
        for name in ('og:image', 'twitter:image'):
            for image_url in metadata.meta.get(name, []):
                image = urlsplit(image_url)
                if image.netloc == urlsplit(url).netloc and not (directory / unquote(image.path).lstrip('/')).is_file():
                    errors.append(f'{url}: share image does not exist: {image_url}')
    for key, page in pages.items():
        alternatives = [link for link in page.links if link.get('hreflang')]
        if not alternatives:
            continue
        if not any(normalized(link.get('href', '')) == key and link['hreflang'] == page.lang for link in alternatives):
            errors.append(f'{key[2]}: hreflang is missing the current language/page')
        for link in alternatives:
            target = pages.get(normalized(link.get('href', '')))
            if target is None:
                errors.append(f'{key[2]}: hreflang target is not an indexable sitemap page')
            elif target.lang != link['hreflang']:
                errors.append(f'{key[2]}: hreflang target language does not match')
            elif not any(normalized(back.get('href', '')) == key for back in target.links if back.get('hreflang')):
                errors.append(f'{key[2]}: hreflang target does not link back')
    return errors, len(pages)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory', type=Path)
    parser.add_argument('--reference-sitemap', type=Path, help='Optional baseline to require the same indexable URL set')
    arguments = parser.parse_args()
    errors, count = check_seo(arguments.directory, arguments.reference_sitemap)
    for error in errors:
        print(error)
    print(f'SEO check {"failed" if errors else "passed"}: {count} sitemap pages; {len(errors)} issue(s).')
    return 1 if errors else 0


if __name__ == '__main__':
    raise SystemExit(main())
