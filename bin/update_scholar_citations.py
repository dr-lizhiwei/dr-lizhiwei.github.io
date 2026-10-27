#!/usr/bin/env python3
"""Refresh citation counts from one public Google Scholar profile request."""

import argparse
from datetime import datetime, timezone
from html.parser import HTMLParser
import json
from pathlib import Path
import re
from urllib.parse import parse_qs, urlencode, urlsplit
from urllib.request import Request, urlopen


class ScholarProfile(HTMLParser):
    def __init__(self, author):
        super().__init__(convert_charrefs=True)
        self.author = author
        self.publications = {}
        self.row = None
        self.anchor = None

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        classes = attrs.get('class', '').split()
        if tag == 'tr' and 'gsc_a_tr' in classes:
            self.row = {'title': [], 'count': [], 'has_count': False, 'id': None}
        if tag != 'a' or self.row is None:
            return
        if 'gsc_a_at' in classes:
            identifier = parse_qs(urlsplit(attrs.get('href', '')).query).get('citation_for_view', [''])[0]
            prefix = self.author + ':'
            if identifier.startswith(prefix):
                article_id = identifier[len(prefix):]
                if re.fullmatch(r'[A-Za-z0-9_-]+', article_id):
                    self.row['id'] = article_id
            self.anchor = 'title'
        elif 'gsc_a_ac' in classes:
            self.row['has_count'] = True
            self.anchor = 'count'

    def handle_data(self, data):
        if self.row is not None and self.anchor:
            self.row[self.anchor].append(data)

    def handle_endtag(self, tag):
        if tag == 'a':
            self.anchor = None
        if tag != 'tr' or self.row is None:
            return
        row, self.row = self.row, None
        title = ''.join(row['title']).strip()
        count = ''.join(row['count']).strip().replace(',', '')
        # An empty, present Scholar citation cell means zero. A missing cell
        # or an error/challenge page does not provide a citation count.
        if not (row['id'] and title and row['has_count']):
            return
        if count and not count.isdecimal():
            return
        if row['id'] in self.publications:
            raise ValueError('Duplicate Scholar article ID')
        self.publications[row['id']] = {'title': title, 'citations': int(count or '0')}


def parse_profile(document, author):
    parser = ScholarProfile(author)
    parser.feed(document)
    if not parser.publications:
        raise ValueError('No verified publication rows found in the public profile')
    return parser.publications


def main():
    root = Path(__file__).resolve().parent.parent
    config = (root / '_config.yml').read_text(encoding='utf-8-sig')
    configured = re.search(r'^scholar_userid:\s*([^\s#]+)', config, re.MULTILINE)
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--author', default=configured.group(1).strip('\"\'') if configured else '')
    parser.add_argument('--output', type=Path, default=root / '_data/google_scholar_citations.json')
    args = parser.parse_args()
    if not re.fullmatch(r'[A-Za-z0-9_-]+', args.author):
        parser.error('A valid Google Scholar author ID is required')
    url = 'https://scholar.google.com/citations?' + urlencode({
        'user': args.author, 'hl': 'en', 'pagesize': 100, 'sortby': 'pubdate'})
    try:
        request = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urlopen(request, timeout=15) as response:
            document = response.read().decode('utf-8')
        publications = parse_profile(document, args.author)
        snapshot = {'scholar_userid': args.author, 'profile_url': url,
                    'updated_at': datetime.now(timezone.utc).isoformat(timespec='seconds'),
                    'publications': publications}
        args.output.parent.mkdir(parents=True, exist_ok=True)
        temporary = args.output.with_suffix('.json.tmp')
        temporary.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2) + '\n',
                             encoding='utf-8', newline='\n')
        temporary.replace(args.output)
        print(f'Updated Google Scholar citation data: {len(publications)} publications.')
    except (OSError, ValueError) as error:
        print(f'Google Scholar refresh unavailable: {error}. Existing citation data retained.')
        # A citation provider outage must not prevent publishing the website.
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
