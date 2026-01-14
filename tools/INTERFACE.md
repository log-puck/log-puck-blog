# INTERFACE.md — Contratti e Interfacce per Collaboratori AI

**⚠️ IMPORTANTE:** Questo file definisce le interfacce pubbliche necessarie per collaborare su questo progetto. 
Non rivela dettagli implementativi interni.

---

## 📥 Input Richiesti

Quando lavori su questo progetto, assicurati che i dati di input rispettino questi contratti:

### Script/Processori Generici

**Per creare/modificare uno script o processore:**

**⚠️ Campo di applicazione (OBBLIGATORIO):**
- Specificare il campo di applicazione: `Jekyll`, `Notion`, `Data Processing`, `API`, `Build`, etc.
- Ogni campo di applicazione può avere requisiti specifici (vedi esempi sotto)

**Input richiesto (generale):**
- Tipo operazione: `read` (leggere dati), `write` (scrivere dati), `generate` (generare output), `transform` (trasformare dati)
- Fonte dati: Notion Database, File System, API, etc.
- Formato input: JSON, Markdown, YAML, etc.

**Se interagisce con Notion Database:**
- Database ID Notion (stringa, formato UUID)
- Properties Notion (lista completa con dettagli)
- Tipo operazione Notion: `read` (query), `write` (create/update), `sync` (bidirezionale)

**Formato Properties Notion:**
- Ogni property deve avere: `name` (stringa), `type` (stringa: `title`, `rich_text`, `date`, `multi_select`, `checkbox`, `select`, `status`, `number`, `formula` (specificare la formula)).
- Ogni property deve avere l'indicazione `Obbligatoria` se è ritenuta bloccante, altrimenti sarà ritenuta `Facoltativa`.
- Indicare lo stato iniziale per le properties di cui sia necessario avere uno stato iniziale (es: `Published`, type: `checkbox`, stato iniziale `checked/unchecked`, `Build Status`, type: `status`, stato iniziale: `To-do`).

**Output generato (specificare in base al campo di applicazione):**
- Tipo formato output (Markdown, JSON, HTML, YAML, etc.)
- Destinazione output (file system, Notion, API, etc.)
- Se file system: percorso directory/file, naming convention
- Se Markdown/Jekyll: directory destinazione, frontmatter YAML (se richiesto), fonte contenuto (Notion blocks o campo specifico)
- Se JSON/API: struttura dati, endpoint, formato risposta

**Esempi per campo di applicazione:**

**Campo: `Jekyll`**
- Layout Jekyll target (stringa, es: `ob_session`)
- Section (stringa, es: `OB-Session`)
- Path output (stringa, es: `ob-session/`)

**Campo: `Notion` (write)**
- Mapping dati input → properties Notion
- Validazioni dati prima di scrittura
- Gestione errori e retry logic

**Campo: `Data Processing`**
- Formato input/output
- Trasformazioni applicate
- Validazioni dati

### Layout Jekyll

**Per creare/modificare un Layout:**

**Input richiesto:**
- Nome layout (stringa, formato: `ob_*`)
- Layout padre (deve ereditare da `default`)
- Classi CSS principali (array di stringhe)

**Formato:**
- File in `_layouts/nome_layout.html`
- Deve iniziare con `layout: default`
- Classi CSS in formato kebab-case (`.article-page`, `.document-header`)

### Moduli SCSS

**Per creare/modificare un modulo SCSS:**

**Input richiesto:**
- Nome modulo (stringa, formato: `_nome.scss`)
- Responsabilità (stringa, descrizione)
- Classi CSS principali (array di stringhe)

**Formato:**
- File in `_sass/_nome.scss`
- Deve usare variabili CSS (`var(--nome-variabile)`)
- Deve essere importato in `assets/css/main.scss`

### Include HTML

**Per creare/modificare un Include:**

**Input richiesto:**
- Nome file (stringa, formato: `nome.html`)
- Responsabilità (stringa)
- Variabili Jekyll necessarie (array di stringhe)

**Formato:**
- File in `_includes/nome.html`
- Deve essere incluso in `_layouts/default.html` (o layout specifico)

---

## ✅ Validazioni Necessarie

Prima di committare modifiche, verifica:

1. **File chiave presenti:**
   - `_config.yml` esiste
   - `index.html` esiste
   - `Gemfile` esiste

2. **Struttura base:**
   - Directory `_layouts/` esiste
   - Directory `_includes/` esiste
   - Directory `_sass/` esiste

3. **Nessun conflitto CSS:**
   - Se esiste `assets/css/main.scss`, NON creare `assets/css/main.css`
   - `main.css` è generato automaticamente da Jekyll

4. **Processori:**
   - NON usare processori obsoleti (`content.py`, `personas.py`, `projects.py`)
   - Usare solo processori v4.0: `articles.py`, `documentation.py`, `ai_profiles.py`, `waw_council.py`

---

## 🔗 Riferimenti Pubblici

Per dettagli implementativi completi, consulta (locale, non su GitHub):
- `spec/SPEC_HTML.md` - Specifiche HTML dettagliate
- `spec/SPEC_SCSS.md` - Specifiche SCSS dettagliate
- `spec/SPEC_PROCESSORS.md` - Specifiche Python dettagliate

---

## 🚫 Cosa NON Fare

- ❌ NON modificare `_config.yml` senza verifica (baseurl critico)
- ❌ NON creare `main.css` se esiste `main.scss`
- ❌ NON reintrodurre processori obsoleti
- ❌ NON modificare `_layouts/default.html` senza usare includes
- ❌ NON modificare import order in `main.scss` senza motivo
