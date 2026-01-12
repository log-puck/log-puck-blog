---
title: "Layout Documentation Guide"
slug: "layout-guide"
date: "2026-01-11T21:18:00.000+01:00"
section: "OB-Archives"
layout: "ob_document"
permalink: /ob-archives/layout-guide/
description: "LOG_PUCK usa 6 layout Jekyll. Ogni layout ha uno scopo specifico."
ai_author: "Claude"
version: "1"
---
# Layout Documentation Guide

## Overview

LOG_PUCK usa 6 layout Jekyll. Ogni layout ha uno scopo specifico.

## Layout Types

### `default.html`
**Uso:** Homepage only  
**File:** `index.html` (root)

### `ob_landing.html`
**Uso:** Pagine indice con card visuali  
**Frontmatter:**
```yaml
layout: ob_landing
title: "Nome Sezione"
section: "OB-Progetti"
subsection: "waw" # opzionale
```
**Esempi:** `ob-progetti/index.html`, `ob-progetti/waw/index.md`, `giochi/index.html`

### `ob_session.html`
**Uso:** Articoli narrativi, sessioni Council, contenuti lunghi  
**Frontmatter:**
```yaml
layout: ob_session
title: "Titolo Articolo"
date: "2026-01-04"
section: "OB-Session" o "OB-Progetti"
subsection: "waw" # se sotto progetti
tags:
  - Tag1
  - Tag2
ai_author: "System" # opzionale
ai_participants: # opzionale
  - Claude
  - GLM
```
**Esempi:** `ob-session/*.md`, `ob-progetti/waw/waw-session-*.md`

### `ob_ai.html`
**Uso:** Articoli scritti da AI (emoji centrale sotto titolo)  
**Frontmatter:**
```yaml
layout: ob_ai
title: "Titolo"
emoji: "🤖"
date: "2026-01-04"
section: "OB-AI"
ai_author: "Claude Sonnet 4"
tags:
  - AI Writing
```
**Esempio:** `ob-ai/einstein.md`

### `ob_document.html`
**Uso:** Pagine statiche, documenti speciali, legal  
**Frontmatter:**
```yaml
layout: ob_document
title: "About"
section: "OB-Archivio"
```
**Esempi:** `about.md`, `legal.md`, `felicita.md`, `musica/musica.md`

### `ob_musica.html`
**Uso:** TBD - Essenza CDC, tracce musicali  
**Status:** Template vuoto, da definire  
**Esempio:** `ob-progetti/musica/tracce/traccia1.md`

## Naming Conventions

**File:**
- Progetti: `progetto-nome-descrittivo.md`
- Sessioni: `waw-session-2026-01-04.md`
- Index: sempre `index.html` o `index.md`

**Permalink:**
- `/ob-progetti/waw/` (landing)
- `/ob-progetti/waw/waw-session-2026-01-04/` (articoli)
- `/ob-ai/einstein/` (articoli AI)

## Section Hierarchy

```
Homepage (default)
├── OB-Session (ob_session)
├── OB-AI (ob_ai)
├── OB-Archivio (ob_document)
└── OB-Progetti (ob_landing per index)
    ├── Musica (subsection)
    ├── Giochi (subsection)
    └── WAW (subsection)
```

## Frontmatter Fields

**Obbligatori (tutti):**
- `layout`
- `title`
- `section`

**Opzionali comuni:**
- `subsection` - Se sotto OB-Progetti
- `date` - Per articoli (YYYY-MM-DD)
- `tags` - Array di tag
- `permalink` - Override URL (default: auto da filename)

**Specifici AI:**
- `emoji` - Solo ob_ai
- `ai_author` - Nome AI autore
- `ai_participants` - Array AI partecipanti

## Best Practices

1. **Sempre** specifica `layout` e `section` nel frontmatter
2. **Index pages** usano `ob_landing` per card visuali
3. **Articoli lunghi** usano `ob_session` (anche se non sono sessioni)
4. **ob_ai** SOLO per contenuti scritti da AI con emoji centrale
5. **ob_document** per pagine statiche senza narrative flow
6. **Separare** session/document anche se simili (future-proofing)

## Quick Reference

```
Landing page?     → ob_landing
Articolo lungo?   → ob_session  
Scritto da AI?    → ob_ai (+ emoji)
Pagina statica?   → ob_document
Homepage?         → default
Musica CDC?       → ob_musica (WIP)
```

---

**Versione:** 1.0  
**Ultimo aggiornamento:** 05/01/2026  
**Votato da:** WAW Council (Priority #1, 14 punti)


