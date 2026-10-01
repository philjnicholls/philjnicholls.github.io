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
import math
import random
import re
import shutil
import socketserver
from datetime import date
from pathlib import Path

import yaml
from jinja2 import Environment, FileSystemLoader, select_autoescape

ROOT = Path(__file__).parent
DIST = ROOT / "dist"

# Hero map: drawn at build time so the site needs no JavaScript or images.
MAP_W, MAP_H = 1200, 440


def _fmt(n: float) -> str:
    return f"{n:.1f}".rstrip("0").rstrip(".")


def _closed_path(points: list[tuple[float, float]]) -> str:
    head, *rest = points
    return "M" + " L".join(f"{_fmt(x)},{_fmt(y)}" for x, y in [head, *rest]) + " Z"


def contour_paths() -> list[str]:
    """Wobbly concentric rings around a few 'hills', like a topographic map."""
    rng = random.Random(11)
    hills = [(250, 120, 9), (760, 330, 11), (1110, 70, 7)]
    paths = []
    for cx, cy, rings in hills:
        phases = [rng.uniform(0, math.tau) for _ in range(3)]
        for k in range(1, rings + 1):
            r = 34 * k
            pts = []
            for i in range(96):
                t = math.tau * i / 96
                wobble = (
                    1
                    + 0.13 * math.sin(3 * t + phases[0] + k * 0.15)
                    + 0.07 * math.sin(5 * t + phases[1])
                    + 0.04 * math.sin(7 * t + phases[2] - k * 0.1)
                )
                pts.append((cx + r * wobble * math.cos(t) * 1.25, cy + r * wobble * math.sin(t)))
            paths.append(_closed_path(pts))
    return paths


def flight_track() -> dict:
    """A soaring bird's day: glides between thermals, then a sudden stop."""
    rng = random.Random(3)
    x, y = 40.0, 300.0
    pts = [(x, y)]
    for thermal in range(4):
        # Glide east with a gentle drift.
        for _ in range(9):
            x += rng.uniform(13, 19)
            y += rng.uniform(-9, 7)
            pts.append((x, y))
        # Circle in a thermal, drifting with the wind.
        cx, cy, r = x, y - 24, rng.uniform(18, 26)
        start = math.pi / 2
        for i in range(1, 25 + thermal * 3):
            a = start + math.tau * i / 12
            pts.append((cx + r * math.cos(a) + i * 0.9, cy + r * math.sin(a) - i * 0.5))
        x, y = pts[-1]
    # Final descent to a motionless landing.
    for _ in range(8):
        x += rng.uniform(10, 14)
        y += rng.uniform(5, 11)
        pts.append((x, y))
    landing = (x, y)
    cluster = [(x + rng.uniform(-3, 3), y + rng.uniform(-3, 3)) for _ in range(7)]
    # Fit the track so the landing sits centre-right, visible even when the
    # map is cropped on narrow screens.
    x0, x1, target = pts[0][0], landing[0], MAP_W * 0.64
    sx = (target - x0) / (x1 - x0)
    fit = lambda p: (x0 + (p[0] - x0) * sx, p[1])  # noqa: E731
    pts = [fit(p) for p in pts]
    landing = fit(landing)
    cluster = [fit(p) for p in cluster]
    path = "M" + " L".join(f"{_fmt(px)},{_fmt(py)}" for px, py in pts)
    fixes = pts[::3]
    return {"path": path, "fixes": fixes, "landing": landing, "cluster": cluster}


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
    env.filters["n"] = _fmt

    if DIST.exists():
        shutil.rmtree(DIST)
    shutil.copytree(ROOT / "static", DIST)

    html = env.get_template("index.html").render(
        **content,
        map={"w": MAP_W, "h": MAP_H, "contours": contour_paths(), "track": flight_track()},
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
