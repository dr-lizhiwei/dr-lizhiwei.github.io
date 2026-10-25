#!/usr/bin/env python3
"""Check generated pages and local resource links before publishing the site."""

import argparse
import json
import posixpath
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit


class PageLinks(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.references = []

    def handle_starttag(self, tag, attributes):
        attributes = dict(attributes)
        for name in ("href", "src", "srcset", "poster"):
            value = attributes.get(name)
            if not value or value.startswith("data:"):
                continue
            values = [value]
            if name == "srcset":
                values = [
                    re.sub(r"\s+\d+(?:\.\d+)?[wx]$", "", item.strip())
                    for item in value.split(",")
                ]
            self.references.extend((name, item) for item in values)


def check_site(directory, site_url):
    directory = Path(directory)
    if not (directory / "index.html").is_file():
        return ["Missing generated homepage: index.html"], 0

    files = {
        path.relative_to(directory).as_posix()
        for path in directory.rglob("*")
        if path.is_file()
    }
    hostname = urlsplit(site_url).hostname
    errors = []
    pages = 0
    stylesheets = set()

    def check_reference(filename, attribute, value):
        if value.startswith("#"):
            return
        route = filename[:-10] if filename.endswith("index.html") else filename
        page_url = site_url.rstrip("/") + "/" + route
        target_url = urlsplit(urljoin(page_url, value))
        if target_url.scheme not in ("http", "https"):
            return
        if target_url.hostname != hostname:
            return

        url_path = unquote(target_url.path)
        if "//" in url_path:
            errors.append(f"{filename}: repeated slash in {attribute}={value}")
        target = posixpath.normpath("/" + url_path.lstrip("/")).lstrip("/")
        candidates = ("index.html",) if not target else (
            target,
            target.rstrip("/") + "/index.html",
            target + ".html",
        )
        matched = next((candidate for candidate in candidates if candidate in files), None)
        if matched is None:
            errors.append(f"{filename}: missing target for {attribute}={value}")
        elif matched.endswith(".css"):
            stylesheets.add(matched)

    for filename in sorted(files):
        path = directory / filename
        if filename.endswith(".json"):
            try:
                json.loads(path.read_text(encoding="utf-8"))
            except (ValueError, UnicodeError) as error:
                errors.append(f"{filename}: invalid JSON: {error}")
        if not filename.endswith(".html"):
            continue

        pages += 1
        parser = PageLinks()
        parser.feed(path.read_text(encoding="utf-8"))
        for attribute, value in parser.references:
            check_reference(filename, attribute, value)

    checked_stylesheets = set()
    while stylesheets - checked_stylesheets:
        filename = sorted(stylesheets - checked_stylesheets)[0]
        checked_stylesheets.add(filename)
        css = (directory / filename).read_text(encoding="utf-8")
        for value in re.findall(r"url\(([^)]+)\)", css):
            check_reference(filename, "url", value.strip().strip("\"'"))

    return errors, pages


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path, help="Jekyll output directory")
    parser.add_argument("--site-url", default="https://zhiweili.net")
    arguments = parser.parse_args()
    errors, pages = check_site(arguments.directory, arguments.site_url)
    if errors:
        for error in errors:
            print(error)
        print(f"Site check failed: {len(errors)} issue(s) across {pages} HTML pages.")
        return 1
    print(f"Site check passed: {pages} HTML pages; local links, CSS resources, and JSON are valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
