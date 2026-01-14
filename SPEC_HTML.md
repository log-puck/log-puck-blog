# SPEC_HTML.md — Specifiche HTML/Layout per LOG_PUCK Blog

## Panoramica

Questo documento descrive la struttura HTML modulare del sito LOG_PUCK, inclusi layouts Jekyll e includes riutilizzabili.

**Versione:** 4.0 (Modulare)  
**Ultimo aggiornamento:** 2025-01-12

---

## Struttura Modulare

### Architettura

Il sistema HTML è strutturato in modo modulare:

```
_layouts/
├── default.html          # Layout base (19 righe - struttura minimale)
└── ob_*.html            # Layout specifici per sezioni (ereditano da default)

_includes/
├── head.html            # Meta tags, SEO, JSON-LD (140+ righe)
├── header.html          # Navigation/Header (30 righe)
├── breadcrumb.html      # Breadcrumb navigation (18 righe)
├── footer.html          # Footer con koan (16 righe)
├── scripts.html         # JavaScript per mobile menu (55 righe)
├── article-card.html    # Card per articoli (riutilizzabile)
├── project-card.html    # Card per progetti (riutilizzabile)
└── tags-list.html       # Lista tag (riutilizzabile)
```

---

## Layout Base: `default.html`

### Struttura

```liquid
<!DOCTYPE html>
<html lang="it">
{% include head.html %}

<body>
    {% include header.html %}
    {% include breadcrumb.html %}
    
    <main>
        {{ content }}
    </main>
    
    {% include footer.html %}
    {% include scripts.html %}
</body>
</html>
```

**Caratteristiche:**
- Layout minimale (19 righe)
- Include tutti i componenti modulari
- Usato da tutti i layout specifici (`layout: default`)

---

## Layout Specifici

### `ob_session.html`
- **Eredita da:** `default`
- **Uso:** Articoli/sessioni (OB-Session)
- **Classi CSS:** `.article-page`, `.article-header`, `.article-content`

### `ob_document.html`
- **Eredita da:** `default`
- **Uso:** Documenti (OB-Archives)
- **Classi CSS:** `.document-page`, `.document-header`, `.document-content`
- **Campi extra:** `version`, `next_review`

### `ob_ai.html`
- **Eredita da:** `default`
- **Uso:** Profili AI (OB-AI)
- **Classi CSS:** `.persona-page`, `.persona-header`, `.persona-content`
- **Campi frontmatter:** `avatar`, `profilo`, `epoca`, `style`

### `ob_progetti.html`
- **Eredita da:** `default`
- **Uso:** Landing progetti (OB-Progetti)
- **Classi CSS:** `.landing-page`, `.projects-grid`
- **Filtri:** Esclude sessioni WAW Council

### `ob_landing.html`
- **Eredita da:** `default`
- **Uso:** Landing generiche
- **Classi CSS:** `.landing-page`, `.landing-content`

### `ob_tag.html`
- **Eredita da:** `default`
- **Uso:** Pagine tag
- **Classi CSS:** `.hero`, `.tags-cloud`, `.articles-grid`

---

## Includes Modulari

### `head.html`

**Responsabilità:**
- Meta tags (charset, viewport, canonical)
- SEO (title, description, keywords)
- Open Graph / Facebook
- Twitter Cards
- JSON-LD Structured Data:
  - Homepage: Organization + WebSite schema
  - Articles: Article/BlogPosting schema
  - Breadcrumb: BreadcrumbList schema
- CSS stylesheet link
- Favicon links

**Variabili Jekyll utilizzate:**
- `site.title`, `site.url`, `site.baseurl`, `site.description`, `site.keywords`
- `page.title`, `page.description`, `page.url`, `page.date`, `page.layout`
- `page.section`, `page.subsection`, `page.tags`

### `header.html`

**Responsabilità:**
- Logo LOG_PUCK
- Navigation principale
- Mobile menu (hamburger)
- Dropdown menu (OB-Progetti)
- Active state tracking (basato su `page.url`)

**Classi CSS:**
- `.site-header`, `.logo`, `.main-nav`, `.nav-menu`
- `.nav-link`, `.nav-link.active`
- `.nav-dropdown`, `.dropdown-menu`

**JavaScript:** Gestito in `scripts.html`

### `breadcrumb.html`

**Condizione:** Solo se `page.url != '/'`

**Struttura:**
- Home → Section → Subsection → Title (corrente)

**Variabili:** `page.section`, `page.subsection`, `page.title`

### `footer.html`

**Contenuto:**
- Koan (filosofico)
- Footer navigation (About, Legal, Social)
- Copyright meta

**Classi CSS:** `.site-footer`, `.koan`, `.footer-nav`, `.footer-meta`

### `scripts.html`

**Funzionalità:**
- Mobile menu toggle
- Dropdown toggle (mobile)
- Close menu su click items
- Gestione stato active/open

**Dipendenze:** Nessuna libreria esterna (vanilla JS)

---

## Frontmatter Standard

### Articoli (ob_session)
```yaml
---
title: "Titolo Articolo"
date: 2025-01-12
section: "OB-Session"
layout: "ob_session"
tags:
  - Tag1
  - Tag2
---
```

### Documenti (ob_document)
```yaml
---
title: "Titolo Documento"
date: 2025-01-12
section: "OB-Archives"
layout: "ob_document"
version: "1.0"
tags:
  - Tag1
---
```

### AI Profiles (ob_ai)
```yaml
---
title: "Nome AI"
section: "OB-AI"
layout: "ob_ai"
avatar: "🤖"
profilo: "Descrizione"
epoca: "2025"
style: "Stile comunicativo"
tags:
  - Tag1
---
```

---

## Convenzioni

### Naming
- **Layouts:** `ob_*.html` (kebab-case con prefisso `ob_`)
- **Includes:** `*.html` (kebab-case semplice)
- **Classi CSS:** kebab-case (`.article-page`, `.nav-link`)

### Paths
- Sempre usare `{{ '/path' | relative_url }}` per link interni
- `site.baseurl` è `/log-puck-blog` (GitHub Pages)

### Active States
- Navigation: `{% if page.url contains '/path/' %}active{% endif %}`
- Dropdown items: Stesso pattern con class `active`

---

## Estendere la Struttura

### Aggiungere un nuovo Include

1. Creare file in `_includes/nuovo-componente.html`
2. Usare `{% include nuovo-componente.html %}` nei layout
3. Documentare variabili Jekyll necessarie

### Aggiungere un nuovo Layout

1. Creare `_layouts/ob_nuovo.html`
2. Iniziare con `layout: default`
3. Defininire classi CSS specifiche in `_sass/_layouts.scss`
4. Documentare campi frontmatter richiesti

### Modificare Navigation

1. Modificare `_includes/header.html`
2. Aggiungere/rimuovere voci in `.nav-menu`
3. Aggiornare active states se necessario
4. Testare mobile menu

---

## Note per Collaboratori AI

Quando sviluppi nuove funzionalità HTML:

1. **Mantieni la modularità:** Usa includes per componenti riutilizzabili
2. **Rispetta la struttura:** Layout specifici ereditano sempre da `default`
3. **Segui le convenzioni:** Naming, paths, active states
4. **Documenta frontmatter:** Nuovi layout = nuovi campi frontmatter
5. **Testa mobile:** Tutti i componenti devono essere responsive

**Riferimenti:**
- `SPEC_SCSS.md` per stili CSS
- `SPEC_PROCESSORS.md` per generazione contenuti
