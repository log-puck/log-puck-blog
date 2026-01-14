# Standard di Nomenclatura - LOG_PUCK Blog

**Versione:** 1.0  
**Data:** 2026-01-14  
**Scopo:** Definire standard chiari e univoci per naming conventions del progetto

---

## 📋 Standard Generale

### Database IDs Notion

**Python (`tools/notion_jekyll/config.py` e `.env` per Python):**
- **Pattern:** `DB_*_ID` (DB all'inizio)
- **Convenzione:** `DB_{NOME}_ID`
- **Esempi:**
  - `DB_ARTICLES_ID`
  - `DB_DOCUMENTATION_ID`
  - `DB_AI_PROFILES_ID`
  - `DB_WAW_COUNCIL_ID`
  - `DB_DONE_LIST_ID`
  - `DB_MUSICA_ID`
  - `DB_STUDI_MUSICA_ID`

**JavaScript/Node (`experiments/ponte_config.js`):**
- **Pattern:** `*_ID` (senza prefisso `DB_`)
- **Convenzione:** `{NOME}_ID`
- **Note:** Alcuni possono avere `_DB_ID` alla fine per chiarezza (opzionale)
- **Esempi:**
  - `WAW_COUNCIL_DB_ID`
  - `WAW_IDEAS_DB_ID`
  - `ARTICLES_ID`
  - `DONE_LIST_ID`

**Perché due convenzioni diverse?**
- Python: Prefisso `DB_` chiarisce che è un Database ID Notion
- JavaScript: Pattern più corto, alcuni nomi mantengono `_DB_ID` per chiarezza opzionale

---

## 🎯 Mapping Completo Python

### Variabili d'Ambiente (`.env`)

**Standard definitivo per Python (da usare nel `.env`):**

```bash
# Pattern: DB_*_ID
DB_ARTICLES_ID=...
DB_AI_PROFILES_ID=...
DB_PROJECT_DATA_ID=...
DB_DOCUMENTATION_ID=...      # Nota: "DOCUMENTATION" non "DOCUMENT"
DB_WAW_COUNCIL_ID=...
DB_MUSICA_ID=...
DB_STUDI_MUSICA_ID=...
DB_DONE_LIST_ID=...
```

**Retrocompatibilità supportata (ma non consigliato):**
- `ARTICLES_ID` → mappato a `DB_ARTICLES_ID`
- `DOCUMENT_ID` → mappato a `DB_DOCUMENTATION_ID`
- `WAW_COUNCIL_DB_ID` → mappato a `DB_WAW_COUNCIL_ID`
- etc.

---

## 📝 Altri Standard di Nomenclatura

### Sections (Sezioni Jekyll)

**Pattern:** `OB-{Nome}` (plurale inglese quando possibile)

**Esempi:**
- `OB-Session` → path: `ob-session/`
- `OB-Archives` → path: `ob-archives/`
- `OB-AI` → path: `ob-ai/`
- `OB-Progetti` → path: `ob-progetti/`

**Regole:**
- Plurale inglese quando possibile (`Archives`, `Sessions`)
- Eccezioni: nomi propri italiani (`Progetti`)
- Verificare sempre contro codebase esistente con `grep`

### Layout Jekyll

**Pattern:** `ob_{nome}.html`

**Esempi:**
- `ob_session.html`
- `ob_document.html`
- `ob_ai.html`
- `ob_workflow.html`

**Regole:**
- Prefisso `ob_` obbligatorio
- Snake_case (underscore)
- Nome in lowercase

### Classi CSS

**Pattern:** Kebab-case (trattini)

**Esempi:**
- `.workflow-page`
- `.timeline-item`
- `.article-header`
- `.category-label`

**Regole:**
- Lowercase
- Trattini (`-`) per separare parole
- BEM-like quando utile: `.block__element--modifier`

### File SCSS

**Pattern:** `_{nome}.scss`

**Esempi:**
- `_variables.scss`
- `_workflow-timeline.scss`
- `_base.scss`

**Regole:**
- Prefisso `_` obbligatorio (partial SCSS)
- Kebab-case per il nome
- Import in `assets/css/main.scss`

### Processori Python

**Pattern:** `{nome}.py` (classe: `{Nome}Processor`)

**Esempi:**
- File: `articles.py` → Classe: `ArticlesProcessor`
- File: `timeline.py` → Classe: `TimelineProcessor`
- File: `waw_council.py` → Classe: `WAWCouncilProcessor`

**Regole:**
- File: snake_case
- Classe: PascalCase
- Metodi: snake_case (`process_articles()`)

---

## ✅ Checklist per Nuovi Database IDs

Quando aggiungi un nuovo Database ID:

- [ ] **Python:**
  - [ ] Variabile in `tools/notion_config.py`: `DB_{NOME}_ID`
  - [ ] Aggiunta a `tools/notion_jekyll/config.py` `load_config()`
  - [ ] Aggiunta a mapping `required_dbs` (se necessario)
  - [ ] Export finale in `config.py`
  
- [ ] **JavaScript (se necessario):**
  - [ ] Variabile in `experiments/ponte_config.js`: `{NOME}_ID` o `{NOME}_DB_ID`

- [ ] **`.env`:**
  - [ ] Variabile: `DB_{NOME}_ID` (per Python)
  
- [ ] **Documentazione:**
  - [ ] Aggiornare `tools/INTERFACE.md` se necessario
  - [ ] Aggiornare questo file se introduce nuovo pattern

---

## 🔄 Retrocompatibilità

**Policy:** Manteniamo retrocompatibilità per 1-2 versioni, poi rimuoviamo.

**Attualmente supportato (ma deprecato):**
- `ARTICLES_ID` → `DB_ARTICLES_ID`
- `WAW_COUNCIL_DB_ID` → `DB_WAW_COUNCIL_ID`
- `DOCUMENT_ID` → `DB_DOCUMENTATION_ID`

**Prossimi passi:** Rimuovere supporto retrocompatibilità in versione futura.

---

## 📌 Quick Reference

**Per nuovi collaboratori:**

```
Python Database IDs    → DB_*_ID
JavaScript Database IDs → *_ID o *_DB_ID
Sections               → OB-{Nome}
Layouts                → ob_{nome}.html
CSS Classes            → .kebab-case
SCSS Files             → _{nome}.scss
Python Classes         → PascalCase
Python Files/Functions → snake_case
```

---

**Standard Documentati - Versione 1.0**
