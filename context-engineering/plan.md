# Blog Styling (B/W) and About Page Implementation Plan

## Overview
Implement a minimal black/white site-wide style via a single CSS file and add a simple Markdown-based About page, with a consistent header containing links to “blog” and “about”.

## Current State Analysis
- Static site generator in `tools/build.py` renders posts from `posts/YYYY/*.md|.rst` to `docs/posts/YYYY/<slug>/index.html` using Pandoc and the template `templates/base.html`.
- Both the Pandoc template and generated index pages reference a global stylesheet at `/_static/theme.css`, but no `docs/_static/` directory exists.
- No About page is generated; some legacy pages link to `/about/`, but `docs/about/` does not exist.

Key Discoveries:
- Stylesheet link in template:
```1:14:/Users/kasperjunge/gitrepo/writing/kasperjunge.github.io/templates/base.html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>$title$</title>
    <link rel="stylesheet" href="/_static/theme.css" />
  </head>
  <body>
    <main class="container">
      $body$
    </main>
  </body>
  </html>
```
- Home/year pages also reference the same stylesheet:
```124:135:/Users/kasperjunge/gitrepo/writing/kasperjunge.github.io/tools/build.py
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
```
```149:155:/Users/kasperjunge/gitrepo/writing/kasperjunge.github.io/tools/build.py
        out_dir.mkdir(parents=True, exist_ok=True)
        html_doc = (
            "<html><head><meta charset='utf-8'><link rel='stylesheet' href='/_static/theme.css'></head>"
            f"<body><h1>{year}</h1><ul>" + "\n".join(items) + "</ul></body></html>"
        )
        (out_dir / "index.html").write_text(html_doc, encoding="utf-8")
```

## Desired End State
- A global, minimal black/white stylesheet exists at `docs/_static/theme.css` and is served by GitHub Pages without additional build steps.
- All pages (posts, home, yearly archives) show a simple header with links: “blog” (to `/`) and “about” (to `/about/`).
- An About page is authored in Markdown and published to `docs/about/index.html` using the same Pandoc template.

## What We're NOT Doing
- No complex theme frameworks, no JavaScript-based theming.
- No refactor of the URL structure or content pipeline beyond what’s needed for About.
- No additional asset pipelines beyond committing `docs/_static/theme.css` directly.

## Implementation Approach
- Keep styling simple by committing `docs/_static/theme.css` to the repo so existing references resolve immediately.
- Extend the Pandoc template and generated index pages to include a minimal nav header.
- Add a `pages/about.md` source and teach the builder to render `pages/*.md` to `docs/<slug>/index.html`.

---

## Phase 1: Add global black/white stylesheet

### Overview
Create a minimal stylesheet at `docs/_static/theme.css` that defines base typography, layout, and a simple header. This requires no build changes and leverages existing `<link rel="stylesheet" href="/_static/theme.css" />`.

### Changes Required

#### 1. Create stylesheet file
- File: `docs/_static/theme.css`
- Create directories as needed and add minimal styles:
```css
:root { color-scheme: light dark; }
* { box-sizing: border-box; }
html, body { margin: 0; padding: 0; background: #fff; color: #000; font-family: -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Helvetica, Arial, sans-serif; line-height: 1.6; }
@media (prefers-color-scheme: dark) { html, body { background: #000; color: #fff; } a { color: #fff; } }
.container { max-width: 720px; margin: 2rem auto; padding: 0 1rem; }
header.site-header { border-bottom: 1px solid currentColor; }
header.site-header .inner { max-width: 720px; margin: 0 auto; padding: 0.75rem 1rem; display: flex; gap: 1rem; align-items: center; }
header.site-header a { color: inherit; text-decoration: none; }
header.site-header a:hover { text-decoration: underline; }
main.container h1, main.container h2, main.container h3 { line-height: 1.25; }
ul { padding-left: 1.25rem; }
```

### Success Criteria

#### Automated Verification
- [x] Build succeeds: `uv run python tools/build.py` (exit code 0).
- [x] CSS file exists post-build: `test -f docs/_static/theme.css`.

#### Manual Verification
- [ ] Visit `/` and any post page; styles apply (fonts, spacing, colors) without 404s for `/_static/theme.css`.

---

## Phase 2: Add header with “blog” and “about” links

### Overview
Inject a minimal header into both the Pandoc template (for posts) and the generated index/year pages.

### Changes Required

#### 1. Update Pandoc template header
- File: `templates/base.html`
- Insert the header after the `<body>` tag and before `<main class="container">`.
- Current context:
```1:14:/Users/kasperjunge/gitrepo/writing/kasperjunge.github.io/templates/base.html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>$title$</title>
    <link rel="stylesheet" href="/_static/theme.css" />
  </head>
  <body>
    <main class="container">
      $body$
    </main>
  </body>
  </html>
```
- Edit at line 9 (after `</head>` and `<body>`):
```html
  <body>
    <header class="site-header">
      <div class="inner">
        <a href="/">blog</a>
        <a href="/about/">about</a>
      </div>
    </header>
    <main class="container">
```

#### 2. Update home page generation
- File: `tools/build.py`
- Modify `render_home()` body to include the same header. Current lines:
```124:135:/Users/kasperjunge/gitrepo/writing/kasperjunge.github.io/tools/build.py
    html_doc = (
        "<html><head><meta charset='utf-8'><link rel='stylesheet' href='/_static/theme.css'></head>"
        "<body><h1>Kasper Junge Blog</h1><ul>" + "\n".join(items) + "</ul></body></html>"
    )
```
- Replace with:
```html
    html_doc = (
        "<html><head><meta charset='utf-8'><link rel='stylesheet' href='/_static/theme.css'></head>"
        "<body><header class='site-header'><div class='inner'><a href='/'>blog</a> <a href='/about/'>about</a></div></header>"
        "<main class='container'><h1>Kasper Junge Blog</h1><ul>" + "\n".join(items) + "</ul></main></body></html>"
    )
```

#### 3. Update yearly archive generation
- File: `tools/build.py`
- Modify `render_year_archives()` body similarly. Current lines:
```149:155:/Users/kasperjunge/gitrepo/writing/kasperjunge.github.io/tools/build.py
        html_doc = (
            "<html><head><meta charset='utf-8'><link rel='stylesheet' href='/_static/theme.css'></head>"
            f"<body><h1>{year}</h1><ul>" + "\n".join(items) + "</ul></body></html>"
        )
```
- Replace with:
```html
        html_doc = (
            "<html><head><meta charset='utf-8'><link rel='stylesheet' href='/_static/theme.css'></head>"
            f"<body><header class='site-header'><div class='inner'><a href='/'>blog</a> <a href='/about/'>about</a></div></header>"
            f"<main class='container'><h1>{year}</h1><ul>" + "\n".join(items) + "</ul></main></body></html>"
        )
```

### Success Criteria

#### Automated Verification
- [x] Build succeeds: `uv run python tools/build.py`.
- [x] Grep confirms header in generated pages:
  - `rg "site-header" docs/ -n` returns matches in `docs/index.html` and `docs/blog/*/index.html`.

#### Manual Verification
- [ ] Visit a post page, `/`, and `/blog/2025/`; header shows “blog” and “about”.
- [ ] Header styling applies from `theme.css`.

---

## Phase 3: Add Markdown About page and build support for pages

### Overview
Author `pages/about.md` in Markdown and extend the builder to render `pages/*.md` to `docs/<slug>/index.html` via Pandoc and the same template.

### Changes Required

#### 1. Create About source
- File: `pages/about.md`
- Content skeleton:
```markdown
# About

Hi, I’m Kasper. This is a minimal, text-first blog.
```

#### 2. Add page rendering function
- File: `tools/build.py`
- Insert after line 121 (end of `render_post`):
```python
def render_page(src: Path) -> Path:
    """Render a generic Markdown page to docs/<slug>/index.html using the same template."""
    slug = src.stem
    out_dir = DOCS_DIR / slug
    out_dir.mkdir(parents=True, exist_ok=True)
    out_html = out_dir / "index.html"
    cmd = [
        "pandoc",
        str(src),
        "--standalone",
        "--from",
        "markdown+yaml_metadata_block",
        "--template",
        str(TEMPLATE),
        "--output",
        str(out_html),
    ]
    subprocess.run(cmd, check=True)
    return out_html
```

#### 3. Discover and render pages in main
- File: `tools/build.py`
- Edit `main()` to render pages before copying assets and building indices. Current context:
```176:201:/Users/kasperjunge/gitrepo/writing/kasperjunge.github.io/tools/build.py
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
```
- Replace the marked section (just before `copy_assets()`) by inserting pages rendering:
```python
    # Render standalone pages (e.g., About)
    pages_dir = Path("pages")
    if pages_dir.exists():
        for src in sorted(pages_dir.glob("*.md")):
            render_page(src)
```

### Success Criteria

#### Automated Verification
- [x] Build succeeds: `uv run python tools/build.py`.
- [x] File exists: `test -f docs/about/index.html`.

#### Manual Verification
- [ ] Visit `/about/`; content renders with site header and template styles.

---

## Phase 4: Verify locally and deploy

### Overview
Confirm generation locally and push for GitHub Pages to serve.

### Changes Required
- Local serve: `python serve.py` then open `http://localhost:8000/` and `http://localhost:8000/about/`.
- Deploy: `python deploy.py` (or your preferred git workflow).

### Success Criteria

#### Automated Verification
- [x] Build succeeds: `uv run python tools/build.py`.
- [ ] Git push succeeds.

#### Manual Verification
- [ ] GitHub Pages serves `/` and `/about/` with styles and header.

---

## Testing Strategy

### Unit Tests
- None in this repo; rely on build success and file existence checks.

### Integration Tests
- Sanity check with `curl`:
  - `curl -sSf http://localhost:8000/about/ | rg 'site-header'` → header present
  - `curl -sSf http://localhost:8000/posts/2023/a-process-for-building-llm-classifiers/ | rg '<main'` → body present

### Manual Testing Steps
1. Run `uv run python tools/build.py`.
2. Inspect `docs/_static/theme.css`, `docs/index.html`, `docs/blog/2023/index.html`, and `docs/about/index.html` for expected markup.
3. Serve locally and verify header links and styles load.

## Performance Considerations
- CSS is a single small file; negligible impact. No JS added.

## Migration Notes
- None required. Existing content is unaffected; new CSS applies globally.

## Rollback Strategy
- Revert edits to `templates/base.html` and `tools/build.py` and remove `docs/_static/theme.css` and `docs/about/`.

## References
- Research: `context-engineering/2025-10-12-research-blog-styling-and-about-page.md`
- Template: `templates/base.html`
- Builder: `tools/build.py`
