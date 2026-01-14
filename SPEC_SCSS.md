# SPEC_SCSS.md — Specifiche SCSS/CSS per LOG_PUCK Blog

## Panoramica

Questo documento descrive la struttura SCSS modulare del sito LOG_PUCK, inclusi i moduli partial e l'organizzazione del codice CSS.

**Versione:** 4.0 (Modulare)  
**Ultimo aggiornamento:** 2025-01-12

---

## Struttura Modulare

### Architettura

Il sistema CSS è organizzato in moduli SCSS parziali:

```
assets/css/
└── main.scss          # Entry point (18 righe - solo import)

_sass/                 # Directory standard Jekyll per partial SCSS
├── _variables.scss    # CSS Variables (12 righe)
├── _base.scss         # Reset & base styles (22 righe)
├── _header.scss       # Header & Navigation (279 righe)
├── _breadcrumb.scss   # Breadcrumb (31 righe)
├── _hero.scss         # Hero section & Tags (61 righe)
├── _landing.scss      # Landing pages (113 righe)
├── _components.scss   # Cards, buttons, grids (195 righe)
├── _components-content.scss  # Callout, Box-Caos (183 righe)
├── _layouts.scss      # Article, Document, Persona, Projects (568 righe)
├── _footer.scss       # Footer (54 righe)
└── _responsive.scss   # Media queries (26 righe)
```

**Totale:** ~1550 righe (prima erano in un unico file `main.css`)

---

## Entry Point: `main.scss`

### Struttura

```scss
---
---

// Main SCSS Entry Point
// Importa tutti i moduli nell'ordine corretto

@import 'variables';
@import 'base';
@import 'header';
@import 'breadcrumb';
@import 'hero';
@import 'landing';
@import 'components';
@import 'components-content';
@import 'layouts';
@import 'footer';
@import 'responsive';
```

**Note importanti:**
- Frontmatter YAML vuoto (`---\n---`) obbligatorio per Jekyll
- Ordine degli import è critico (variabili prima di tutto)
- Jekyll compila automaticamente `main.scss` → `main.css`

---

## Moduli SCSS

### `_variables.scss`

**Responsabilità:** CSS Variables (Design Tokens)

```scss
:root {
    --bg-main: #fffef7;
    --text-main: #1a1a1a;
    --accent-yellow: #99ff00;
    --accent-yellow-dark: #7acc00;
    --accent-lime: rgba(153, 255, 0, 0.60);
    --accent-magenta: #fa93fa;
    --border-color: #2a2a2a;
    --slot-bg: #f5f3e8;
    --footer-bg: #2a2a2a;
}
```

**Uso:** Sempre preferire variabili CSS invece di valori hardcoded

### `_base.scss`

**Responsabilità:**
- CSS Reset (`* { margin: 0; padding: 0; box-sizing: border-box; }`)
- Body styles (font-family, line-height, colors)
- Main element (z-index)
- Container utility (max-width, margin, padding)

### `_header.scss`

**Responsabilità:**
- Site header (sticky, z-index)
- Logo styles
- Navigation menu (desktop + mobile)
- Dropdown menu (OB-Progetti)
- Mobile hamburger menu
- Active states
- Media queries per mobile (768px)

**Classi principali:**
- `.site-header`, `.logo`, `.main-nav`
- `.nav-menu`, `.nav-link`, `.nav-link.active`
- `.nav-dropdown`, `.dropdown-menu`
- `.nav-toggle` (hamburger)

### `_breadcrumb.scss`

**Responsabilità:**
- Breadcrumb wrapper
- Link styles
- Separator
- Current page styling

**Classi:** `.breadcrumb-wrapper`, `.breadcrumb`, `.separator`, `.current`

### `_hero.scss`

**Responsabilità:**
- Hero section (padding, spacing)
- Tags cloud (display, flex, gap)
- Hero title (clamp per responsive)
- Hero description (max-width, typography)
- Tag component (styling, hover states)

**Classi:** `.hero`, `.tags-cloud`, `.hero-title`, `.hero-description`, `.tag`

### `_landing.scss`

**Responsabilità:**
- Landing page layout
- Landing header (title, description)
- Landing content (typography, spacing)
- wAw project specific styles (CTA links)
- Blockquote, links, lists

**Classi:** `.landing-page`, `.landing-header`, `.landing-title`, `.landing-content`

### `_components.scss`

**Responsabilità:**
- Articles grid (CSS Grid)
- Article cards (hover effects, borders)
- Grid blocks (flex layout)
- CTA buttons (`.btn-enter` con arrow)
- Feed table (grid layout)

**Classi principali:**
- `.articles-grid`, `.article-card`, `.article-card-title`
- `.grid-container`, `.card`
- `.btn-enter`, `.btn-enter::after`
- `.feed-section`, `.feed-row`

### `_components-content.scss`

**Responsabilità:**
- Callout component (insights/lezioni)
- Box-Caos component (caos/osservazione)
- Typography dentro i componenti
- Media queries per mobile

**Classi:** `.callout`, `.box-caos`

### `_layouts.scss`

**Responsabilità:**
- Article page styles (`.article-page`, `.article-content`)
- Document page styles (`.document-page`, `.document-content`)
- Persona/AI page styles (`.persona-page`, `.persona-content`)
- AI landing specific (`.ai-landing`)
- Projects grid (`.projects-grid`, `.project-card`)
- Document task lists (checkbox styling)

**Classi principali:**
- `.article-page`, `.article-header`, `.article-content`
- `.document-page`, `.document-header`, `.document-content`
- `.persona-page`, `.persona-header`, `.persona-content`
- `.projects-grid`, `.project-card`

### `_footer.scss`

**Responsabilità:**
- Site footer (background, padding)
- Koan styling (typography, spacing, pseudo-elements)
- Footer navigation (links)
- Footer meta (copyright)

**Classi:** `.site-footer`, `.koan`, `.footer-nav`, `.footer-meta`

**Nota importante:** `min(520px, 85%)` non funziona in SCSS (conflitto con funzione matematica), usare `max-width: 520px; width: 85%;` invece

### `_responsive.scss`

**Responsabilità:**
- Media queries per mobile (max-width: 768px)
- Breakpoint unificato
- Override styles per mobile

**Breakpoint:** `768px` (mobile/desktop threshold)

---

## Variabili CSS

### Palette Colori

| Variabile | Valore | Uso |
|-----------|--------|-----|
| `--bg-main` | `#fffef7` | Background principale |
| `--text-main` | `#1a1a1a` | Testo principale |
| `--accent-yellow` | `#99ff00` | Accento principale (hover, highlight) |
| `--accent-yellow-dark` | `#7acc00` | Accento giallo scuro |
| `--accent-lime` | `rgba(153, 255, 0, 0.60)` | Accento lime (bordi, CTA) |
| `--accent-magenta` | `#fa93fa` | Accento magenta (hover cards) |
| `--border-color` | `#2a2a2a` | Colore bordi |
| `--slot-bg` | `#f5f3e8` | Background cards/slot |
| `--footer-bg` | `#2a2a2a` | Background footer |

---

## Convenzioni

### Naming
- **File partial:** `_nome-modulo.scss` (underscore prefix)
- **Classi CSS:** kebab-case (`.article-card`, `.nav-link`)
- **Variabili CSS:** kebab-case (`--bg-main`, `--text-main`)

### Organizzazione
- Un modulo = una responsabilità
- Import order: variabili → base → componenti → layouts → responsive
- Media queries: Raggruppate in `_responsive.scss`, non sparse

### Unità
- **Spacing:** `rem` (preferito) o `px` per valori piccoli
- **Font-size:** `rem` o `clamp()` per responsive
- **Breakpoint:** `768px` (standard mobile/desktop)

### Funzioni CSS

**⚠️ Attenzione:** SCSS ha funzioni native che confliggono con CSS:

- ❌ `min(520px, 85%)` → Conflitto con `min()` SCSS
- ✅ `max-width: 520px; width: 85%;` → Soluzione compatibile

---

## Estendere la Struttura

### Aggiungere un nuovo modulo

1. Creare `_sass/_nuovo-modulo.scss`
2. Aggiungere `@import 'nuovo-modulo';` in `main.scss` (ordine corretto)
3. Documentare responsabilità e classi principali

### Aggiungere stili per nuovo layout

1. Aggiungere classi in `_layouts.scss`
2. Seguire naming: `.nome-layout-page`, `.nome-layout-header`, `.nome-layout-content`
3. Aggiungere media queries in `_responsive.scss` se necessario

### Aggiungere nuovo componente

1. Aggiungere stili in `_components.scss` (componenti generici) o `_components-content.scss` (componenti contenuto)
2. Usare variabili CSS (`var(--nome-variabile)`)
3. Documentare classi e uso

---

## Note per Collaboratori AI

Quando sviluppi nuovi stili SCSS:

1. **Usa variabili CSS:** Mai valori hardcoded, sempre `var(--nome-variabile)`
2. **Segui la modularità:** Aggiungi al modulo appropriato o crea nuovo modulo
3. **Rispetta l'ordine:** Import in `main.scss` nell'ordine corretto
4. **Mobile-first:** Aggiungi media queries in `_responsive.scss`
5. **Breakpoint unico:** Usa `768px` per mobile/desktop
6. **Evita conflitti:** Non usare `min()`/`max()` CSS direttamente (conflitto SCSS)

**Riferimenti:**
- `SPEC_HTML.md` per struttura HTML/layouts
- `SPEC_PROCESSORS.md` per generazione contenuti
