# Research: Current blog architecture and URL/slug structure

## Research Question
Transform this blog into a custom static site (no ABlog/Sphinx) while preserving existing post URLs/slugs and GitHub Pages hosting. Document how the current system works: build/deploy, content locations, and how URLs are produced.

## Summary
The site is generated with Sphinx + ABlog and published to GitHub Pages from the `docs/` directory. Source content lives under `posts/YYYY/` as `.rst` or `.md` with either ABlog ``.. post::`` directives (RST) or front matter (MD). ABlog renders posts into `docs/posts/YYYY/<slug>/index.html`. Blog taxonomies (author, tag, category, language, location, archives) are generated under `docs/blog/…/`. The build/serve/deploy flow is handled by small Python scripts invoking `ablog` via `uv`.

## Detailed Findings

### Build and configuration
- Sphinx/ABlog configuration: `conf.py`
  - Extensions include ABlog and MyST: 
```199:206:/Users/kasperjunge/gitrepo/writing/kasperjunge.github.io/conf.py
extensions = [
    'sphinx.ext.extlinks',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'alabaster',
    'ablog',
    'myst_parser',
]
```
  - Source suffixes support both RST and Markdown:
```208:214:/Users/kasperjunge/gitrepo/writing/kasperjunge.github.io/conf.py
source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
}
```
  - Blog metadata and theme setup:
```21:29:/Users/kasperjunge/gitrepo/writing/kasperjunge.github.io/conf.py
# blog_path = 'blog'
blog_title = "Kasper Junge Blog"
blog_baseurl = ""
ablog_website = "docs"
```
```295:307:/Users/kasperjunge/gitrepo/writing/kasperjunge.github.io/conf.py
html_theme = "pydata_sphinx_theme"
html_theme_options["analytics"] = {
    "google_analytics_id": "G-3CEVPVH0T7",
}
```
  - Sidebar includes ABlog widgets:
```111:121:/Users/kasperjunge/gitrepo/writing/kasperjunge.github.io/conf.py
html_sidebars = {
    '**': [ 
        'ablog/postcard.html', 
        'ablog/recentposts.html', 
        'ablog/tagcloud.html',
        'ablog/categories.html',  
        'ablog/archives.html',
        'searchfield.html',
        ],
    }
```

- Local dev script: `serve.py` builds and runs the dev server via ABlog:
```4:9:/Users/kasperjunge/gitrepo/writing/kasperjunge.github.io/serve.py
def serve():
    subprocess.run("uv run ablog build -w docs", shell=True)
    subprocess.run("uv run ablog serve -r -w docs", shell=True)
```

- Deploy script: `deploy.py` builds, commits, deploys to GitHub Pages, and pushes:
```4:24:/Users/kasperjunge/gitrepo/writing/kasperjunge.github.io/deploy.py
def deploy():
    build_path = str((Path(__file__).parent / "docs").resolve())
    subprocess.run("uv run ablog build -w docs", shell=True)
    subprocess.run("git add .", shell=True)
    subprocess.run('git commit -m "update blog"', shell=True)
    subprocess.run(
        f"uv run ablog deploy --github-branch main -w {build_path} -g kasperjunge -p {build_path}",
        shell=True
    )
    subprocess.run("git push", shell=True)
```

### Content model and sources
- Root index uses ABlog postlist and a hidden toctree:
```7:25:/Users/kasperjunge/gitrepo/writing/kasperjunge.github.io/index.rst
Recent posts
-------------
.. postlist:: 5
   :excerpts:
.. toctree::
   :hidden:
   about.rst
```

- Posts are kept under `posts/YYYY/` and can be either RST with ABlog directives or Markdown with front matter:
  - Example RST post with ABlog `.. post::` directive:
```1:6:/Users/kasperjunge/gitrepo/writing/kasperjunge.github.io/posts/2025/how-i-created-a-free-blog-using-python-and-github-pages.rst
.. post:: Feb 16, 2025  
   :tags: Tutorial, Sphinx, GitHub Pages  
   :author: Kasper Junge

**How I created a free blog using Python and GitHub Pages**
```
  - Example Markdown post with YAML front matter that ABlog consumes:
```1:12:/Users/kasperjunge/gitrepo/writing/kasperjunge.github.io/posts/2025/how-mcp-or-similar-standards-could-change-the-way-we-use-software-with-ai.md
---
blogpost: true
date: Apr 07, 2025
author: Kasper Junge
location: Denmark
category: MCP, AI
language: English
---

# How MCP (or similar standards) Could Change the Way We Use Software with AI
```

### Output structure and URL mapping
- Built posts live under `docs/posts/YYYY/<slug>/index.html`. The slug derives from the source file name/title and ABlog’s slug logic. Examples:
  - RST example renders to:
```1:1:/Users/kasperjunge/gitrepo/writing/kasperjunge.github.io/docs/posts/2025/how-i-created-a-free-blog-using-python-and-github-pages/index.html
```
  - MD example renders to:
```1:1:/Users/kasperjunge/gitrepo/writing/kasperjunge.github.io/docs/posts/2025/how-mcp-or-similar-standards-could-change-the-way-we-use-software-with-ai/index.html
```
  - Additional slugs observed under `docs/posts/2025/` (indicating canonical per-post directories):
```1:50:/Users/kasperjunge/gitrepo/writing/kasperjunge.github.io/docs/posts/2025
0_ablog_github_pages_setup/
0_hello-world/
1_ablog_github_pages_setup/
100-best-tips-tricks-hacks-and-methods-users-of-cursor-have-for-coding-with-ai-in-cursor/
100-tips-tricks-hacks-and-methods-users-of-cursor-have-for-coding-with-ai-in-cursor/
... (many others) ...
```

- Blog taxonomy pages (archives, tags, categories, author, language, location) live under `docs/blog/`:
```1:1:/Users/kasperjunge/gitrepo/writing/kasperjunge.github.io/docs/blog/2025/index.html
```
and subfolders such as `docs/blog/tag/<tag>/index.html`, `docs/blog/category/<category>/index.html`, etc., linked from built post sidebars.

### How slugs are determined (observed)
- Each post outputs to `docs/posts/<YYYY>/<slug>/index.html` which becomes the public URL `/posts/<YYYY>/<slug>/` when hosted at the site root.
- For RST posts, the directory name matches the source filename (kebab/literal) unless ABlog normalization alters it based on the title; the example shows a 1:1 mapping from filename `how-i-created-a-free-blog-using-python-and-github-pages.rst` to slug `how-i-created-a-free-blog-using-python-and-github-pages/`.
- For Markdown posts with front matter, the output slug also mirrors the filename: `how-mcp-or-similar-standards-could-change-the-way-we-use-software-with-ai.md` → `how-mcp-or-similar-standards-could-change-the-way-we-use-software-with-ai/`.
- The year segment is the folder under `posts/` (e.g., `posts/2025/`) and matches the built output year directory `docs/posts/2025/`.

### Integration points visible in built HTML
- Sidebars link to taxonomy pages under `docs/blog/…/` and show ABlog widgets (recent posts, tag cloud, categories, archives). Example snippets show author, tags, and archives rendered in the sidebar for each post.

## Code References
- `conf.py:21-29` — Blog metadata and ABlog website path
- `conf.py:199-206` — Extensions including ABlog and MyST
- `conf.py:208-214` — Source suffix configuration for RST and MD
- `conf.py:111-121` — `html_sidebars` with ABlog components
- `conf.py:295-307` — Theme and analytics configuration
- `serve.py:4-9` — Local build and serve commands
- `deploy.py:4-24` — Build and deploy to GitHub Pages
- `index.rst:7-25` — Home page post list and toctree
- `posts/2025/how-i-created-a-free-blog-using-python-and-github-pages.rst:1-6` — RST post with ABlog directive
- `posts/2025/how-mcp-or-similar-standards-could-change-the-way-we-use-software-with-ai.md:1-12` — Markdown post with front matter
- `docs/posts/2025/.../index.html` — Built per-post output paths establishing final slugs
- `docs/blog/2025/index.html` — Year archive under blog taxonomy

## Architecture Documentation (as-is)
- Static site generator: Sphinx with ABlog extension
- Source content locations: `index.rst`, `about.rst`, and posts under `posts/YYYY/` (RST/MD)
- Templating/theme: `pydata_sphinx_theme`, ABlog sidebars
- Build outputs: `docs/` directory (GitHub Pages publishing root)
- URL scheme: `/posts/<YYYY>/<slug>/` for posts; taxonomy under `/blog/.../`
- Deployment: local script uses `uv run ablog build` and `uv run ablog deploy` targeting `docs/`

## Open Questions
- Exact ABlog slug normalization rules if titles differ from filenames (not observed to diverge here).
- Whether any redirects exist for alternate slugs present in `docs/posts/2025/` (multiple similarly named folders).

## Follow-up Research: Minimal Pandoc + Markdown stack (decision, no implementation)

Goal: Author posts in Markdown, keep URLs stable (`/posts/<YYYY>/<slug>/`), generate a static site, customize styling freely, and host via GitHub Pages with minimal tooling.

### Proposed Stack (as simple as possible)
- Authoring: Markdown with YAML front matter (title, date, tags optional).
- Generator: `pandoc` CLI to convert each Markdown file to a standalone HTML file.
- URL layout: emit to `docs/posts/<year>/<slug>/index.html` to preserve current scheme.
- Index pages: tiny generated `docs/index.html` (and optionally simple yearly index pages) built by a short script (bash or Python) that enumerates posts and renders links.
- Styling: custom CSS placed in `docs/_static/theme.css` (or similar), linked in a minimal Pandoc HTML template.
- Deploy: GitHub Pages serving from `docs/` (no CI required beyond push).

### File/Directory Conventions (proposed)
- Source posts: `posts/<year>/<slug>.md`
- Output per-post: `docs/posts/<year>/<slug>/index.html`
- Static assets: `docs/_static/` (CSS, images, JS if needed)
- Templates: `templates/base.html` (Pandoc template, minimal head + body structure)

### Example Pandoc commands (illustrative, not implemented)
```bash
pandoc posts/2025/my-post.md \
  --standalone \
  --from markdown+yaml_metadata_block \
  --metadata title="My Post" \
  --template templates/base.html \
  --output docs/posts/2025/my-post/index.html
```

### Notes on slug/date mapping
- `slug` comes from the source filename (`my-post.md` → `my-post/`).
- `year` comes from the directory under `posts/`.
- This mirrors current ABlog output paths, keeping existing URLs stable when content is migrated.

### Open Questions for this approach
- Whether to generate taxonomy pages (tags/categories) now or later.
- How much navigation to include on `docs/index.html` (recent posts vs. all posts).


