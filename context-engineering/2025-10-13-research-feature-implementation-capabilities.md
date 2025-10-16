# Research: Feature Implementation Capabilities

## Research Question
How can the following features be implemented in the current blog system:
1. Auto update / hot reload on save, when the server is running
2. Date on blog posts
3. A way to have both Danish and English blog posts on the site
4. A page with links for articles, podcasts etc. that I've been participating in

## Summary
The blog is a minimal Python-based static site generator that uses Pandoc to convert Markdown/RST posts into HTML. Posts live in `posts/YYYY/` and are built to `docs/posts/YYYY/<slug>/index.html`. The build system already supports metadata extraction (including dates and language), has a pages system for standalone content, and uses a simple Python HTTP server for local development. Currently, there is no file watching/hot reload, dates are extracted but not displayed, language metadata exists but isn't utilized for filtering, and the pages system can support additional content types.

## Detailed Findings

### Current Build System Architecture

#### Build Pipeline
The build process is orchestrated by `tools/build.py`:

**Entry Point:**
```199:232:tools/build.py
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
    # Render standalone pages (e.g., About)
    pages_dir = Path("pages")
    if pages_dir.exists():
        for src in sorted(pages_dir.glob("*.md")):
            render_page(src)
    # Copy static assets after posts are rendered
    copy_assets()
    # Sort posts by descending recency
    posts_info.sort(key=lambda p: p["sort_ts"], reverse=True)
    build_indices(posts_info)
```

The `posts_info` dictionary already captures date information from post metadata, but this data is only used for sorting, not for display.

#### Post Discovery
Posts are discovered by scanning year directories:
```17:29:tools/build.py
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
```

#### Metadata Extraction
The system extracts metadata including title, date, and other fields from YAML front matter:
```54:97:tools/build.py
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
```

**Important:** The `extract_meta()` function currently only extracts `title` and `date` fields. Other metadata fields like `language`, `category`, `author`, etc. that exist in post front matter are not extracted.

#### Date Parsing
The system has date parsing capability:
```36:51:tools/build.py
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
```

### Current Serving Mechanism

The `serve.py` script runs a one-time build followed by a basic HTTP server:
```4:9:serve.py
def serve():
    subprocess.run("uv run python tools/build.py", shell=True)
    subprocess.run("python -m http.server -d docs 8000", shell=True)
```

**Key observation:** The server does not watch for file changes or rebuild automatically. It builds once, then serves static files.

### Template System

The Pandoc template is minimal and currently doesn't include date display:
```1:21:templates/base.html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>$title$</title>
    <link rel="stylesheet" href="/_static/theme.css" />
  </head>
  <body>
    <header class="site-header">
      <div class="inner">
        <a href="/">blog</a>
        <a href="/about/">about</a>
      </div>
    </header>
    <main class="container">
      $body$
    </main>
  </body>
  </html>
```

The template uses Pandoc variables (`$title$`, `$body$`) which are populated from the Markdown front matter during conversion.

### Index and Archive Pages

Home page generation:
```145:156:tools/build.py
def render_home(posts_info: List[Dict[str, str]]) -> None:
    items: List[str] = []
    for p in posts_info[:10]:
        url = f"/posts/{p['year']}/{p['slug']}/"
        title = html.escape(p["title"]) if p.get("title") else p["slug"]
        items.append(f"<li><a href='{url}'>{title}</a></li>")
    html_doc = (
        "<html><head><meta charset='utf-8'><link rel='stylesheet' href='/_static/theme.css'></head>"
        "<body><header class='site-header'><div class='inner'><a href='/'>blog</a> <a href='/about/'>about</a></div></header>"
        "<main class='container'><h1>Kasper Junge Blog</h1><ul>" + "\n".join(items) + "</ul></main></body></html>"
    )
    (DOCS_DIR / "index.html").write_text(html_doc, encoding="utf-8")
```

Year archive generation:
```159:177:tools/build.py
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
            f"<body><header class='site-header'><div class='inner'><a href='/'>blog</a> <a href='/about/'>about</a></div></header>"
            f"<main class='container'><h1>{year}</h1><ul>" + "\n".join(items) + "</ul></main></body></html>"
        )
        (out_dir / "index.html").write_text(html_doc, encoding="utf-8")
```

**Key observation:** Both functions have access to `posts_info` which contains the `date` field, but dates are not included in the rendered HTML.

### Pages System

The build system supports standalone pages via the `pages/` directory:
```124:142:tools/build.py
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

Currently, only `pages/about.md` exists:
```1:4:pages/about.md
# About

Hi, I'm Kasper. This is a minimal, text-first blog.
```

This system can be used to add additional pages like a media/press page.

### Existing Post Metadata Patterns

#### Example: English Post with Full Metadata
```1:8:posts/2023/prompting-patterns-the-clarification-pattern.md
---
blogpost: true
date: Nov 2, 2023
author: Kasper Junge
location: Denmark
category: LLM, Prompt Engineering
language: English
---
```

#### Example: English Post with Minimal Metadata
```1:6:posts/2023/a-process-for-building-llm-classifiers.md
---
blogpost: true
title: A Process for Building LLM Classifiers
date: Aug 17, 2023
author: Kasper Junge
---
```

#### Example: Danish Post without Language Tag
```1:1:posts/2025/henry-fords-rookie-mistake.md
# Hvad Gjorde Henry Ford?
```

**Key observation:** The Danish post (`henry-fords-rookie-mistake.md`) has no YAML front matter at all, and no language indicator. The `language: English` field exists in at least one post, indicating a precedent for language metadata.

### Styling System

The site uses a single CSS file referenced at `/_static/theme.css`:
```1:12:docs/_static/theme.css
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

The styling is minimal, black/white with dark mode support, and includes basic typography.

## Feature-Specific Findings

### Feature 1: Auto Update / Hot Reload on Save

**Current State:**
- No file watching mechanism exists
- `serve.py` builds once, then serves static files via `python -m http.server`
- The HTTP server (`http.server`) is read-only and doesn't trigger rebuilds

**Implementation Approach:**
To implement hot reload, the system would need:
1. A file watcher to monitor changes in `posts/`, `pages/`, `templates/`, and `img/`
2. Automatic rebuild trigger when files change
3. Optional: browser auto-refresh via WebSocket or SSE

**Python Libraries Available for File Watching:**
- `watchdog` - cross-platform file system events library (standard choice)
- `watchfiles` - Rust-based, faster alternative
- Built-in approaches using `os.stat()` polling (simpler but less efficient)

**Minimal Implementation Pattern:**
```python
# Pseudo-code showing the pattern
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class RebuildHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if not event.is_directory:
            # Trigger rebuild
            subprocess.run("uv run python tools/build.py", shell=True)

def serve_with_watch():
    # Start file watcher
    observer = Observer()
    observer.schedule(RebuildHandler(), "posts", recursive=True)
    observer.schedule(RebuildHandler(), "pages", recursive=True)
    observer.schedule(RebuildHandler(), "templates", recursive=True)
    observer.start()
    
    # Start HTTP server
    subprocess.run("python -m http.server -d docs 8000", shell=True)
```

### Feature 2: Date on Blog Posts

**Current State:**
- Dates ARE extracted from post metadata: `tools/build.py:54-97`
- Dates ARE parsed into datetime objects: `tools/build.py:36-51`
- Dates ARE stored in `posts_info` dictionary during build
- Dates ARE NOT displayed anywhere (not in templates, not in index pages, not in post pages)

**Where Dates Exist:**
1. In post front matter (e.g., `date: Aug 17, 2023`)
2. In the `posts_info` dictionary as the `"date"` key
3. Parsed as `sort_ts` for sorting purposes

**Display Locations to Add Dates:**
1. **Post pages:** Add date display in `templates/base.html` using Pandoc's `$date$` variable
2. **Home page:** Modify `render_home()` to include `p['date']` in list items
3. **Year archives:** Modify `render_year_archives()` to include `p['date']` in list items

**Implementation Pattern for Post Pages:**
The template can use Pandoc's automatic metadata variables. When Pandoc processes a Markdown file with `date: Aug 17, 2023` in front matter, it makes `$date$` available to templates:

```html
<!-- In templates/base.html -->
<main class="container">
  $if(date)$
  <div class="post-meta">
    <time>$date$</time>
  </div>
  $endif$
  $body$
</main>
```

**Implementation Pattern for Index Pages:**
```python
# In render_home()
for p in posts_info[:10]:
    url = f"/posts/{p['year']}/{p['slug']}/"
    title = html.escape(p["title"]) if p.get("title") else p["slug"]
    date = p.get("date", "")
    date_html = f" <span class='date'>({date})</span>" if date else ""
    items.append(f"<li><a href='{url}'>{title}</a>{date_html}</li>")
```

### Feature 3: Danish and English Blog Posts

**Current State:**
- At least one post has `language: English` in front matter
- The Danish post has no language metadata
- The `extract_meta()` function does NOT extract language field
- No language-based filtering or display exists

**Implementation Approach:**

**Option A: Language Metadata + Filtered Views**
1. Extract `language` field in `extract_meta()`
2. Store language in `posts_info` dictionary
3. Create language-specific index pages (e.g., `/blog/danish/`, `/blog/english/`)
4. Add language filter to main index (show both with language tags, or default to one language)
5. Add language switcher in header

**Option B: Language-Specific Directories**
1. Organize posts by language: `posts/YYYY/en/*.md` and `posts/YYYY/da/*.md`
2. Modify `discover_posts()` to capture language from directory structure
3. Generate separate indexes for each language

**Option C: Language Tags on Posts**
1. Extract and display language metadata
2. Show all posts together with language indicators
3. No filtering, just visual identification

**Existing Pattern to Follow:**
The front matter pattern already exists:
```yaml
---
language: English
---
```

To extract this, modify `extract_meta()` to add:
```python
language = re.search(r"^language:\s*(.*)$", fm, re.MULTILINE)
return {
    "title": title_val,
    "date": date.group(1).strip() if date else None,
    "language": language.group(1).strip() if language else None,
}
```

### Feature 4: Page for Articles/Podcasts/Media Appearances

**Current State:**
- Pages system exists and renders `.md` files from `pages/` directory
- Currently only `pages/about.md` exists
- Pages are rendered to `docs/<slug>/index.html`
- Header already links to `/about/`, could add more links

**Implementation Approach:**
1. Create `pages/media.md` (or `press.md`, `appearances.md`, etc.)
2. Add content with links to external articles, podcasts, etc.
3. Add navigation link in template header
4. The build system will automatically render it

**Example Content Structure:**
```markdown
# Media & Appearances

Articles I've written for other publications, podcasts I've been on, and other media appearances.

## Articles

- [Article Title](https://example.com) - Publication Name, Date
- [Another Article](https://example.com) - Publication Name, Date

## Podcasts

- [Podcast Episode Title](https://example.com) - Podcast Name, Date
  > Brief description of the episode

## Talks

- [Talk Title](https://example.com) - Event Name, Date
```

**Template Modification for Navigation:**
```html
<header class="site-header">
  <div class="inner">
    <a href="/">blog</a>
    <a href="/about/">about</a>
    <a href="/media/">media</a>
  </div>
</header>
```

## Key Files Reference

- `tools/build.py` - Main build script orchestrating all generation
  - `discover_posts()` lines 17-29 - Finds all posts in `posts/YYYY/`
  - `extract_meta()` lines 54-97 - Parses front matter (currently only title and date)
  - `_parse_date()` lines 36-51 - Converts date strings to datetime objects
  - `render_post()` lines 100-121 - Converts post to HTML via Pandoc
  - `render_page()` lines 124-142 - Converts page to HTML via Pandoc
  - `render_home()` lines 145-156 - Generates homepage with recent posts
  - `render_year_archives()` lines 159-177 - Generates year-based archive pages
  - `copy_assets()` lines 186-196 - Copies `img/` to `docs/img/`
  - `main()` lines 199-232 - Orchestrates the full build
- `serve.py` - Development server (build once, serve static)
- `deploy.py` - Deployment script (build, commit, push)
- `templates/base.html` - Pandoc HTML template for all pages
- `docs/_static/theme.css` - Global stylesheet
- `posts/YYYY/*.md` - Source posts organized by year
- `pages/*.md` - Source standalone pages

## Information Flow

### Build Flow
1. `main()` calls `discover_posts()` to find all `.md` and `.rst` files in `posts/YYYY/`
2. For each post:
   - `extract_meta()` reads file and extracts title and date from YAML front matter
   - `render_post()` invokes Pandoc to convert Markdown to HTML using `templates/base.html`
   - Metadata stored in `posts_info` list with title, date, year, slug, path, and sort timestamp
3. After all posts: `render_page()` is called for each file in `pages/`
4. `copy_assets()` mirrors `img/` directory to `docs/img/`
5. `posts_info` is sorted by date (descending)
6. `build_indices()` generates homepage and year archives using sorted post list

### Serve Flow
1. `serve.py` runs `tools/build.py` once
2. Starts Python's built-in HTTP server serving `docs/` on port 8000
3. Server continues running, serving static files only (no rebuild on change)

## Architecture Documentation

### Static Site Generator Pattern
- **Input sources:** Markdown/RST files in `posts/` and `pages/`
- **Converter:** Pandoc CLI with custom template
- **Output:** Static HTML in `docs/` directory (GitHub Pages compatible)
- **Metadata:** YAML front matter in Markdown files
- **Styling:** Single global CSS file
- **Navigation:** Generated index pages with links to all posts

### URL Structure
- Posts: `/posts/<YEAR>/<slug>/` (slug derived from filename)
- Pages: `/<slug>/` (slug derived from filename)
- Year archives: `/blog/<YEAR>/`
- Assets: `/img/*` (mirrored from source), `/_static/*` (CSS)

### Metadata Extraction Pattern
The system uses regex to parse YAML front matter for Markdown files and directive syntax for RST files. It extracts metadata into a dictionary that's used for:
- Sorting posts by date
- Generating page titles
- Building index listings

**Current limitation:** Only `title` and `date` are extracted, even though posts contain other metadata like `language`, `author`, `category`, etc.

## Open Questions

1. **Language defaults:** If implementing language filtering, what should be the default behavior?
   - Show all languages mixed?
   - Default to English with option to see Danish?
   - Separate language-specific homepages?

2. **Date display format:** What format should dates use in display?
   - Keep source format as-is (varies: "Aug 17, 2023", "Nov 2, 2023")?
   - Standardize to one format?
   - Use relative dates ("2 years ago")?

3. **Hot reload scope:** Should hot reload rebuild everything or only changed files?
   - Full rebuild is simpler but slower
   - Partial rebuild is faster but more complex
   - For a blog this size, full rebuild is likely fast enough

4. **Media page naming:** What should the media/appearances page be called and where in navigation?
   - `/media/`, `/press/`, `/appearances/`, `/elsewhere/`?
   - Position in header navigation?

5. **Language migration:** Should existing posts without language metadata be tagged?
   - Retroactively add language metadata to all posts?
   - Or infer from content/filename?


