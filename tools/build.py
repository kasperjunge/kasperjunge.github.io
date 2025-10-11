from __future__ import annotations

import html
import shutil
import re
from datetime import datetime
import subprocess
from pathlib import Path
from typing import Dict, Iterable, List, Tuple


POSTS_DIR = Path("posts")
DOCS_DIR = Path("docs")
TEMPLATE = Path("templates/base.html")


def discover_posts() -> Iterable[Tuple[str, Path]]:
    """Yield (year, src_path) for .md and .rst under posts/<year>/.

    Only accept four-digit year directory names to preserve URL shape.
    """
    if not POSTS_DIR.exists():
        return
    for year_dir in sorted(POSTS_DIR.glob("[0-9][0-9][0-9][0-9]")):
        if not year_dir.is_dir():
            continue
        for src in sorted(year_dir.iterdir()):
            if src.is_file() and src.suffix.lower() in {".md", ".rst"}:
                yield year_dir.name, src


def derive_slug(src_path: Path) -> str:
    return src_path.stem


def _parse_date(date_str: str) -> datetime | None:
    """Parse a human-readable date into a datetime.

    Tries a few common formats used in posts.
    """
    candidates = [
        "%b %d, %Y",  # Feb 16, 2025
        "%B %d, %Y",  # February 16, 2025
        "%Y-%m-%d",   # 2025-02-16
    ]
    for fmt in candidates:
        try:
            return datetime.strptime(date_str.strip(), fmt)
        except Exception:
            pass
    return None


def extract_meta(src_path: Path) -> Dict[str, str | None]:
    text = src_path.read_text(encoding="utf-8")
    # Minimal MD YAML front matter parser
    if src_path.suffix.lower() == ".md" and text.startswith("---"):
        m = re.search(r"^---\n([\s\S]+?)\n---\n", text)
        if m:
            fm = m.group(1)
            title = re.search(r"^title:\s*(.*)$", fm, re.MULTILINE)
            date = re.search(r"^date:\s*(.*)$", fm, re.MULTILINE)
            title_val = title.group(1).strip() if title else None
            if not title_val:
                # Fallback to first ATX heading in body if title missing
                h1 = re.search(r"^#\s*(.+)$", text, re.MULTILINE)
                if h1:
                    title_val = h1.group(1).strip()
            return {
                "title": title_val,
                "date": date.group(1).strip() if date else None,
            }
    # RST: look for a '.. post:: DATE' directive and the first underlined title
    if src_path.suffix.lower() == ".rst":
        date_match = re.search(r"^\.\.\s+post::\s+(.+)$", text, re.MULTILINE)
        # Title pattern: a line followed by an underline of ===, --- etc.
        title_match = re.search(
            r'^(?P<title>.+)\n(?P<underline>[=~`^"\'\-]{3,})\n',
            text,
            re.MULTILINE,
        )
        title_val = None
        if title_match:
            possible = title_match.group("title").strip()
            # Strip bold markers like **Title** if present
            if possible.startswith("**") and possible.endswith("**"):
                possible = possible[2:-2].strip()
            title_val = possible
        return {
            "title": title_val,
            "date": date_match.group(1).strip() if date_match else None,
        }
    # Fallback: first ATX heading or default to filename
    h1 = re.search(r"^#\s*(.+)$", text, re.MULTILINE)
    if h1:
        return {"title": h1.group(1).strip(), "date": None}
    return {"title": src_path.stem.replace("-", " ").title(), "date": None}


def render_post(year: str, src: Path) -> Path:
    slug = derive_slug(src)
    out_dir = DOCS_DIR / "posts" / year / slug
    out_dir.mkdir(parents=True, exist_ok=True)
    out_html = out_dir / "index.html"

    input_format = (
        "markdown+yaml_metadata_block" if src.suffix.lower() == ".md" else "rst"
    )
    cmd = [
        "pandoc",
        str(src),
        "--standalone",
        "--from",
        input_format,
        "--template",
        str(TEMPLATE),
        "--output",
        str(out_html),
    ]
    subprocess.run(cmd, check=True)
    return out_html


def render_home(posts_info: List[Dict[str, str]]) -> None:
    items: List[str] = []
    for p in posts_info[:10]:
        url = f"/posts/{p['year']}/{p['slug']}/"
        title = html.escape(p["title"]) if p.get("title") else p["slug"]
        items.append(f"<li><a href='{url}'>{title}</a></li>")
    html_doc = (
        "<html><head><meta charset='utf-8'><link rel='stylesheet' href='/_static/theme.css'></head>"
        "<body><h1>Kasper Junge Blog</h1><ul>" + "\n".join(items) + "</ul></body></html>"
    )
    (DOCS_DIR / "index.html").write_text(html_doc, encoding="utf-8")


def render_year_archives(posts_info: List[Dict[str, str]]) -> None:
    by_year: Dict[str, List[Dict[str, str]]] = {}
    for p in posts_info:
        by_year.setdefault(p["year"], []).append(p)
    for year, posts in by_year.items():
        # Already sorted globally; keep that order within the year subset
        items: List[str] = []
        for p in posts:
            url = f"/posts/{p['year']}/{p['slug']}/"
            title = html.escape(p["title"]) if p.get("title") else p["slug"]
            items.append(f"<li><a href='{url}'>{title}</a></li>")
        out_dir = DOCS_DIR / "blog" / year
        out_dir.mkdir(parents=True, exist_ok=True)
        html_doc = (
            "<html><head><meta charset='utf-8'><link rel='stylesheet' href='/_static/theme.css'></head>"
            f"<body><h1>{year}</h1><ul>" + "\n".join(items) + "</ul></body></html>"
        )
        (out_dir / "index.html").write_text(html_doc, encoding="utf-8")


def build_indices(posts_info: List[Dict[str, str]]) -> None:
    # posts_info is expected pre-sorted by descending sort_ts
    render_home(posts_info)
    render_year_archives(posts_info)


def copy_assets() -> None:
    """Mirror img/** to docs/img/**, preserving relative paths."""
    src_root = Path("img")
    dst_root = DOCS_DIR / "img"
    if not src_root.exists():
        return
    for p in src_root.rglob("*"):
        if p.is_file():
            out_path = dst_root / p.relative_to(src_root)
            out_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(p, out_path)


def main() -> None:
    posts_info: List[Dict[str, str]] = []
    for year, src in discover_posts():
        meta = extract_meta(src)
        out_html = render_post(year, src)
        # Determine sort key: prefer parsed date, else file mtime
        parsed_dt = _parse_date(meta.get("date")) if meta.get("date") else None
        sort_ts = (
            parsed_dt.timestamp() if parsed_dt else src.stat().st_mtime
        )
        posts_info.append(
            {
                "title": meta.get("title") or src.stem,
                "date": meta.get("date"),
                "year": year,
                "slug": src.stem,
                "path": str(out_html),
                "sort_ts": sort_ts,
            }
        )
    # Copy static assets after posts are rendered
    copy_assets()
    # Sort posts by descending recency
    posts_info.sort(key=lambda p: p["sort_ts"], reverse=True)
    build_indices(posts_info)


if __name__ == "__main__":
    main()


