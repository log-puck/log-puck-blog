# CLAUDE.md — AI Assistant Guide for LOG_PUCK Blog

## Project Overview

**LOG_PUCK** is a human-AI collaboration laboratory blog, exploring creative symbiosis through a Zen Koan Mu-inspired aesthetic. The project uses Jekyll for static site generation and GitHub Pages for hosting.

**Live Site:** https://log-puck.github.io/log-puck-blog/
**Primary Language:** Italian

## Tech Stack

| Technology | Purpose |
|------------|---------|
| Jekyll 4.3 | Static site generator |
| HTML5 | Semantic structure (W3C validated) |
| CSS3 Vanilla | Responsive layout (Grid + Flexbox) |
| GitHub Pages | Automated deployment |
| Notion API | CMS backend (Phase 2) |
| Python 3 | Notion-to-Jekyll builder script |

**Zero-JS Philosophy:** The site uses 0 KB of JavaScript. All interactions are CSS-only.

## Repository Structure

```
log-puck-blog/
├── _config.yml           # Jekyll configuration
├── index.html            # Homepage (static HTML)
├── style.css             # All site styles
├── Gemfile               # Ruby dependencies
├── README.md             # Project documentation
├── CODEX.md              # Repo guardrails for AI
├── ob-session/           # Session content (articles)
├── ob-ai/                # AI-related content
├── ob-archives/          # Archive documents
│   └── docs/documents/   # Document storage
├── ob-progetti/          # Project content (planned)
├── tools/                # Build tools
│   └── notion_to_jekyll_builder_v2_3.py
└── .github/workflows/
    └── jekyll-docker.yml # CI/CD pipeline
```

## Content Sections

The blog has 4 main sections with specific purposes:

| Section | Directory | Layout | Purpose |
|---------|-----------|--------|---------|
| OB-Session | `ob-session/` | `ob_session` | Creative human-AI explorations |
| OB-Progetti | `ob-progetti/` | `ob_project` | Algorithmic collaboration projects |
| OB-AI | `ob-ai/` | `ob_ai` | Technical/philosophical AI reflections |
| OB-Archivio | `ob-archives/` | `ob_archive` | Document archives |

## Content Frontmatter Format

All content files must use Jekyll frontmatter. Example:

```yaml
---
title: "Article Title"
slug: "article-slug"
date: "2025-12-25"
type: "article"           # article | document | landing
section: "OB-Session"     # OB-Session | OB-AI | OB-Progetti | OB-Archives
subsection: "Default"     # Optional subsection
layout: "ob_session"      # ob_session | ob_ai | ob_project | ob_archive
meta_title: "SEO title"
meta_description: "SEO description"
keywords_seo: "keyword1,keyword2"
tags:
  - Tag1
  - Tag2
---
```

## Development Commands

```bash
# Install dependencies
bundle install

# Run local server
bundle exec jekyll serve

# Build for production
bundle exec jekyll build
```

## Key Conventions

### Styling Rules
- **NO inline styles** in HTML
- Keep CSS in `style.css` (root level for current structure)
- Prefer small, reviewable diffs
- Use CSS transitions for interactions (no JS)

### Color Palette
| Color | Hex | Usage |
|-------|-----|-------|
| Primary Violet | `#A78BFA` | Card hover, link hover |
| Accent Yellow | `#FFD700` | Tag hover, title highlight |
| Dark Text | `#1a1a1a` | Body text |
| Light Gray | `#f9f9f9` | Background |

### Folder Naming
- **NEVER** use underscore prefix (`_`) for content folders
- Jekyll ignores folders starting with `_` (except special folders like `_layouts`, `_posts`)
- Use kebab-case: `ob-session`, `ob-archives`, NOT `_ob-session`

### URL/Path Handling
- Always use `{{ site.baseurl }}` for internal links in templates
- `baseurl` is set to `/log-puck-blog` for GitHub Pages

## CI/CD Pipeline

The site builds automatically via GitHub Actions:
- Trigger: Push to `main` branch or pull request
- Container: `jekyll/builder:latest`
- Output: `_site/` directory

## Notion Integration (Phase 2)

The `tools/notion_to_jekyll_builder_v2_3.py` script converts Notion content to Jekyll markdown:

### Configuration Required
```python
NOTION_API_KEY = "YOUR_NOTION_API_KEY"
DB_CONTENT_ID = "YOUR_DB_CONTENT_ID"
```

### Layout Mapping
```python
LAYOUT_MAP = {
    "home": "ob_home",
    "archive": "ob_archive",
    "ai": "ob_ai",
    "project": "ob_project",
    "session": "ob_session"
}
```

### Section-to-Directory Mapping
```python
{
    "OB-Session": "ob-session",
    "OB-AI": "ob-ai",
    "OB-Progetti": "ob-progetti",
    "OB-Archives": "ob-archives"
}
```

## Common Tasks

### Adding New Content
1. Create `.md` file in appropriate section directory
2. Add proper frontmatter (see format above)
3. Content goes after the `---` closing of frontmatter

### Modifying Styles
1. Edit `style.css`
2. Follow existing CSS organization (reset, header, hero, grid, feed, footer)
3. Use consistent spacing (rem units)
4. Test responsive breakpoints (768px)

### Check Repository Health
When asked to "check repo":
1. Verify files: `_config.yml`, `index.html`, `Gemfile`
2. Verify `baseurl`/`url` configuration
3. Check for unsupported GitHub Pages plugins
4. Propose fixes as unified diff

## Excluded from Build

These paths are excluded from Jekyll processing:
- `node_modules/`
- `vendor/`
- `venv/`
- `scripts/`
- `tools/`
- `CODEX.md`
- `Gemfile*`

## Git Workflow

- **Main branch:** `main`
- **Feature branches:** `claude/claude-md-*` pattern for AI-assisted work
- Always push with `-u` flag for new branches
- Keep commits focused and descriptive

## AI Team Roles (Hurricane Modules)

| Agent | Role |
|-------|------|
| Claude | Orchestrator - high-level vision |
| Synapse/Gemini | Lead Dev - implementation |
| Analysis/Grok | Code Reviewer - quality validation |

## Important Warnings

1. **No `_posts/` directory** - Content is managed via section directories
2. **No Jekyll themes** - Custom styling only (theme: minima is commented out)
3. **Italian language** - UI text is in Italian
4. **Underscore prevention** - Script has anti-underscore validation for folder names

## Quick Reference

```bash
# Local development
bundle exec jekyll serve --livereload

# Check Jekyll version
bundle exec jekyll -v

# Build with drafts
bundle exec jekyll build --drafts
```

---

*Last updated: 2025-12-28*
