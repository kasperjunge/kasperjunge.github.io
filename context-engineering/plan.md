# Migrate blog to minimal Python + Pandoc static site (preserve URLs)

## Overview
Replace Sphinx/ABlog with a minimal Python-driven builder that uses Pandoc to render posts while preserving existing public URLs under `/posts/<YYYY>/<slug>/` and continuing to publish from `docs/` for GitHub Pages.

## Current State Analysis
- Generator: Sphinx + ABlog configured in `conf.py`.
- Sources: RST with `.. post::` and Markdown with YAML front matter in `posts/<year>/`.
- Output: Built files at `docs/` with per-post pages at `docs/posts/<year>/<slug>/index.html`.
- Tooling: Local scripts `serve.py` and `deploy.py` call `ablog` (via `uv`).

Key files and lines observed:
- `conf.py:199-206` — ABlog/Myst extensions configured.
- `conf.py:208-214` — `source_suffix` supports `.rst` and `.md`.
- `conf.py:111-121` — `html_sidebars` includes ABlog components.
- `serve.py:4-9` — invokes `ablog build` and `ablog serve`.
- `deploy.py:4-24` — invokes `ablog build` and `ablog deploy`.
- Posts examples: `posts/2025/how-i-created-a-free-blog-using-python-and-github-pages.rst`, `posts/2025/how-mcp-or-similar-standards-could-change-the-way-we-use-software-with-ai.md`.
- Output examples: `docs/posts/2025/<slug>/index.html`.

## Desired End State
- A single Python script builds the site:
  - Reads `posts/<year>/*.{md,rst}`
  - Emits `docs/posts/<year>/<slug>/index.html` using Pandoc and a minimal HTML template
  - Generates a simple `docs/index.html` and yearly index pages `docs/blog/<year>/index.html`
- Existing URLs remain unchanged; GitHub Pages continues serving from `docs/`.
- ABlog/Sphinx configs remain in repo for easy rollback, but not used by scripts.

Key Discoveries:
- `conf.py:208-214` shows both RST and MD inputs; we must support both.
- `docs/posts/<year>/<slug>/index.html` is canonical for posts; we will replicate this exactly.
- `serve.py:5-6` and `deploy.py:10` are the only places directly calling ABlog; swapping these preserves workflow.

## What We're NOT Doing
- No tag/category/author/language taxonomy pages (for now)
- No feeds (RSS/Atom) generation
- No removal of ABlog/Sphinx files or theme assets yet
- No CI changes; continue to deploy from local script and Git pushes

## Implementation Approach
- Keep scope minimal: a Python builder orchestrates Pandoc CLI calls.
- Derive `year` from parent directory and `slug` from filename stem to preserve path structure.
- Use a lightweight Pandoc HTML template (`templates/base.html`) and a single CSS file under `docs/_static/theme.css`.
- Generate simple indices with vanilla Python (no templating engine dependency).
- Maintain ABlog/Sphinx alongside for immediate rollback.

---

## Phase 1: Scaffold minimal builder, template, and CSS

### Overview
Introduce a Python builder and minimal HTML template/CSS without modifying existing serve/deploy scripts. This validates content discovery and Pandoc rendering.

### Changes Required

#### 1. Python builder script
**File**: `tools/build.py` (new)
**Changes**:
- [x] Create a script that:
  - [x] Discovers posts: `posts/<year>/*.{md,rst}`
  - [x] Parses `year` from the parent folder name and `slug` from the filename stem
  - [x] Infers input format for Pandoc: `markdown+yaml_metadata_block` for `.md`, `rst` for `.rst`
  - [x] Renders to `docs/posts/<year>/<slug>/index.html` using `templates/base.html`
  - [x] Extracts `title` and `date` from YAML front matter (MD) or first heading/`.. post::` line (RST) for indices
  - [x] Generates a minimal `docs/index.html` (recent posts) and `docs/blog/<year>/index.html`

  Example structure:
  ```python
  from pathlib import Path
  import subprocess, re, html

  POSTS_DIR = Path('posts')
  DOCS_DIR = Path('docs')
  TEMPLATE = Path('templates/base.html')

  def discover_posts():
      for year_dir in sorted((POSTS_DIR).glob('[0-9][0-9][0-9][0-9]')):
          for src in sorted(year_dir.glob('*.*')):
              if src.suffix.lower() in {'.md', '.rst'}:
                  yield year_dir.name, src

  def derive_slug(src_path: Path) -> str:
      return src_path.stem

  def extract_meta(src_path: Path) -> dict:
      text = src_path.read_text(encoding='utf-8')
      # Minimal MD YAML front matter parser
      if src_path.suffix.lower() == '.md' and text.startswith('---'):
          m = re.search(r'^---\n([\s\S]+?)\n---\n', text)
          if m:
              fm = m.group(1)
              title = re.search(r'^title:\s*(.*)$', fm, re.MULTILINE)
              date = re.search(r'^date:\s*(.*)$', fm, re.MULTILINE)
              return {
                  'title': title.group(1).strip() if title else None,
                  'date': date.group(1).strip() if date else None,
              }
      # Fallback: first ATX heading or RST title underline
      h1 = re.search(r'^#\s*(.+)$', text, re.MULTILINE)
      if h1:
          return {'title': h1.group(1).strip(), 'date': None}
      return {'title': src_path.stem.replace('-', ' ').title(), 'date': None}

  def render_post(year: str, src: Path):
      slug = derive_slug(src)
      out_dir = DOCS_DIR / 'posts' / year / slug
      out_dir.mkdir(parents=True, exist_ok=True)
      out_html = out_dir / 'index.html'

      input_format = 'markdown+yaml_metadata_block' if src.suffix.lower() == '.md' else 'rst'
      cmd = [
          'pandoc', str(src),
          '--standalone',
          '--from', input_format,
          '--template', str(TEMPLATE),
          '--metadata-file', '-',  # provision for future if needed
          '--output', str(out_html),
      ]
      subprocess.run(cmd, check=True)
      return out_html

  def build_indices(posts_info):
      # posts_info: list of dict(title, date, year, slug)
      # Generate docs/index.html and docs/blog/<year>/index.html
      pass

  def main():
      posts_info = []
      for year, src in discover_posts():
          meta = extract_meta(src)
          out_html = render_post(year, src)
          posts_info.append({
              'title': meta.get('title') or src.stem,
              'date': meta.get('date'),
              'year': year,
              'slug': src.stem,
              'path': out_html,
          })
      build_indices(posts_info)

  if __name__ == '__main__':
      main()
  ```

#### 2. Pandoc HTML template
**File**: `templates/base.html` (new)
**Changes**:
- [x] Minimal HTML5 shell with a content placeholder compatible with Pandoc template variables; include link to `/_static/theme.css`.

  Example structure:
  ```html
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

#### 3. Minimal CSS
**File**: `docs/_static/theme.css` (new)
**Changes**:
- [x] Add a tiny stylesheet to provide basic typography and spacing.

### Success Criteria

#### Automated Verification:
- [x] `pandoc -v` runs successfully
- [x] `uv run python tools/build.py` completes without error
- [x] At least one output file exists, e.g., `docs/posts/2025/how-i-created-a-free-blog-using-python-and-github-pages/index.html`

#### Manual Verification:
- [ ] Open the generated HTML files in a browser; content renders
- [ ] Confirm per-post URL structure under `docs/posts/<year>/<slug>/index.html`

---

## Phase 2: Deterministic URL mapping and asset handling

### Overview
Guarantee output paths exactly mirror existing scheme and ensure static assets are copied/preserved.

### Changes Required

#### 1. Enforce path scheme and slug behavior
**File**: `tools/build.py`
**Changes**:
- [x] Ensure output directory structure is `docs/posts/<year>/<slug>/` where `slug = src.stem`.
- [x] Reject/skip files whose parent directory is not a 4-digit year.
- [x] Normalize slugs (no changes applied; rely on existing filenames to avoid accidental renames).

#### 2. Copy static assets
**File**: `tools/build.py`
**Changes**:
- [x] Copy `img/**` to `docs/img/**` (preserve relative paths).
- [x] Ensure `docs/_static/**` remains untouched; create if missing.

  Example structure:
  ```python
  import shutil

  def copy_assets():
      src = Path('img')
      dst = Path('docs/img')
      if src.exists():
          for p in src.rglob('*'):
              if p.is_file():
                  out = dst / p.relative_to(src)
                  out.parent.mkdir(parents=True, exist_ok=True)
                  shutil.copy2(p, out)
  ```

### Success Criteria

#### Automated Verification:
- [x] Builder places files strictly under `docs/posts/<year>/<slug>/index.html`
- [x] `docs/img/**` mirrors `img/**`

#### Manual Verification:
- [ ] Spot-check a few posts and images load correctly

---

## Phase 3: Generate minimal index pages

### Overview
Produce a simple homepage listing recent posts and a yearly archive page per year.

### Changes Required

#### 1. Homepage index
**File**: `tools/build.py`
**Changes**:
- [x] In `build_indices`, sort posts by (1) parsed date if available, else (2) file mtime.
- [x] Render `docs/index.html` with a list of the N most recent posts (`/posts/<year>/<slug>/`).

  Example structure:
  ```python
  def render_home(posts_info, limit=10):
      items = []
      for p in posts_info[:limit]:
          url = f"/posts/{p['year']}/{p['slug']}/"
          title = html.escape(p['title'])
          items.append(f"<li><a href='{url}'>{title}</a></li>")
      html_doc = """
      <html><head><meta charset='utf-8'><link rel='stylesheet' href='/_static/theme.css'></head>
      <body><h1>Kasper Junge Blog</h1><ul>
      %s
      </ul></body></html>
      """ % ("\n".join(items))
      (DOCS_DIR / 'index.html').write_text(html_doc, encoding='utf-8')
  ```

#### 2. Yearly archives
**File**: `tools/build.py`
**Changes**:
- [x] Render `docs/blog/<year>/index.html` per year, listing all posts for that year.

### Success Criteria

#### Automated Verification:
- [x] `docs/index.html` exists
- [x] `docs/blog/<year>/index.html` exists for years with posts

#### Manual Verification:
- [ ] Open homepage and year pages; links resolve to post pages

---

## Phase 4: Swap serve/deploy scripts to use Python builder

### Overview
Switch `serve.py` and `deploy.py` from ABlog to the new builder, preserving the developer workflow. Keep ABlog files unchanged for rollback.

### Changes Required

#### 1. Update local serve script
**File**: `serve.py`
**Changes**:
- [x] Replace ABlog build/serve calls with: run builder, then serve `docs/` statically.
- [x] Line 5 replaced with `subprocess.run("uv run python tools/build.py", shell=True)`
- [x] Line 6 replaced with `subprocess.run("python -m http.server -d docs 8000", shell=True)`

#### 2. Update deploy script
**File**: `deploy.py`
**Changes**:
- [x] Replace ABlog build with builder invocation; keep commit/push and GH Pages deploy if still desired.
- [x] Line 10 replaced with `subprocess.run("uv run python tools/build.py", shell=True)`
- [x] Use git push for deploy; Pages serves from `docs/` on main

### Success Criteria

#### Automated Verification:
- [x] `uv run python tools/build.py` is called by both `serve.py` and `deploy.py` without errors
- [x] Running `python serve.py` serves the site locally on `http://localhost:8000/` (manual to confirm)

#### Manual Verification:
- [ ] Visit `http://localhost:8000/` and navigate to several posts; URLs match prior scheme
- [ ] Run `python deploy.py` on a test branch and confirm GitHub Pages updates normally

---

## Testing Strategy

### Unit/Smoke Tests
- Add a simple smoke check script to validate outputs after build (optional for minimalism):
  - **File**: `tools/smoke_check.py`
  - Checks that a sample of expected `docs/posts/<year>/<slug>/index.html` files exist and that `docs/index.html` contains links.

### Manual Testing Steps
1. Ensure Pandoc is installed: `pandoc -v`.
2. Run `uv run python tools/build.py`.
3. Open `docs/index.html` directly and click through to a few posts.
4. Start server: `python -m http.server -d docs 8000` and navigate to `http://localhost:8000/`.
5. Validate images and `_static/theme.css` are loading.

## Performance Considerations
- The builder traverses a small tree and runs Pandoc per post; acceptable for current scale.
- Future optimization: parallelize Pandoc calls if build time becomes material.

## Migration Notes
- ABlog/Sphinx files remain untouched; `serve.py`/`deploy.py` are the only scripts switching behavior.
- If issues arise, re-run ABlog build and deploy (see rollback) and revert script changes.

## Rollback Strategy
- Revert `serve.py` line 5 to `subprocess.run("uv run ablog build -w docs", shell=True)` and line 6 to `subprocess.run("uv run ablog serve -r -w docs", shell=True)`.
- Revert `deploy.py` line 10 to `subprocess.run("uv run ablog build -w docs", shell=True)` and keep existing deploy steps.
- Delete any newly added files if desired: `tools/build.py`, `templates/base.html`, `docs/_static/theme.css`.

## References
- Research: `context-engineering/2025-10-11-research-current-blog-architecture-and-slugs.md`
- Config: `conf.py`
- Scripts: `serve.py`, `deploy.py`
- Sources: `posts/`
- Outputs: `docs/`
