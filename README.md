# Congwei Zhang — Academic Homepage

Minimal academic website built with Hugo, versioned Markdown and per-paper BibTeX, hosted free on GitHub Pages.

**Website after deployment:** https://congweizhang.github.io/

## Local preview

Install Hugo Extended (0.152.2) and Python 3.10+, then run:

    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    python scripts/build_publications.py
    hugo server -D

Visit http://localhost:1313/.

## Add a paper

Create `content/publications/<slug>/paper.bib` containing exactly **one** BibTeX entry.
Optionally add `metadata.yaml` alongside it, with fields like:

    venue: "ACM MobiCom 2026"
    status: "Published"
    featured: true
    order: 1
    summary: "One or two sentences about the contribution."
    details: "Optional expanded summary."
    links:
      paper: "https://example.org/paper"
      code: "https://github.com/example/repo"
      slides: "https://example.org/talk.pdf"

The optional `cover.png`, `cover.webp`, `cover.jpg`, `cover.jpeg` or `cover.svg` is shown with aspect ratio preserved. If no cover is provided, a styled typography cover is shown automatically.

Run `python scripts/build_publications.py`. It creates Hugo data, per-paper downloadable BibTeX and a combined `/publications.bib` (generated files are gitignored). The website is rebuilt automatically on push.

The Selected Research section takes the first five entries with `featured: true`, ordered by `order`. Full Publications are automatically sorted newest first.

## Add news

Create `content/news/YYYY-MM-DD-title.md` with:

    ---
    title: "Research update"
    date: 2026-11-09
    summary: "One-line update."
    ---
    More details here.

The homepage automatically displays recent news.

## Edit other information

- `content/_index.md` — main biography
- `hugo.toml` — email, Google Scholar, GitHub
- `content/projects/` — research projects
- `content/service/_index.md` — academic service
- `layouts/` and `static/css/site.css` — layout and styling
- The profile portrait is intentionally a placeholder pending an authorized real photo.

## Publish

The PR only runs build checks. After review, merge it into `main` and in **Settings → Pages → Build and deployment**, choose **GitHub Actions** as the source. Deployments occur on future main-branch pushes (including the PR merge).

## Editorial checks

Before publication, verify final author lists, bibliographic fields, email and affiliations, performance metrics, and links against the papers. Slant is deliberately marked as an arXiv *preprint*. The cover visuals are original typographic placeholders; no copyrighted figures were copied.

This v1 deliberately uses a small **custom Hugo theme** rather than the larger Hugo Blox theme module. The agreed layout and all publication-maintenance conventions are preserved, while reducing theme complexity.
