#!/usr/bin/env python3
"""Build the static portfolio site.

    python build.py            # render into dist/
    python build.py --serve    # render, then preview at http://localhost:8000

Content lives in content/site.yaml, layout in templates/, styles in static/.
The output in dist/ is plain HTML and CSS that any static host can serve.
"""

from __future__ import annotations

import argparse
import functools
import http.server
import re
import shutil
import socketserver
from datetime import date
from pathlib import Path

import yaml
from jinja2 import Environment, FileSystemLoader, select_autoescape

ROOT = Path(__file__).parent
DIST = ROOT / "dist"

def tel_href(phone: str) -> str:
    return "tel:" + re.sub(r"[^\d+]", "", phone)


def build() -> None:
    content = yaml.safe_load((ROOT / "content" / "site.yaml").read_text(encoding="utf-8"))
    env = Environment(
        loader=FileSystemLoader(ROOT / "templates"),
        autoescape=select_autoescape(["html"]),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    env.filters["tel"] = tel_href

    if DIST.exists():
        shutil.rmtree(DIST)
    shutil.copytree(ROOT / "static", DIST)

    html = env.get_template("index.html").render(
        **content,
        year=date.today().year,
    )
    (DIST / "index.html").write_text(html, encoding="utf-8")
    (DIST / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {content['site']['url']}/sitemap.xml\n")
    (DIST / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
        f"<url><loc>{content['site']['url']}/</loc><lastmod>{date.today()}</lastmod></url></urlset>\n"
    )
    print(f"Built {DIST / 'index.html'}")


def serve(port: int) -> None:
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=DIST)
    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"Serving dist/ at http://localhost:{port} (Ctrl+C to stop)")
        httpd.serve_forever()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--serve", action="store_true", help="preview the built site locally")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    build()
    if args.serve:
        serve(args.port)
