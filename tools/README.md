# Notion to Jekyll Builder

Script Python che converte contenuti da Notion a file Markdown per Jekyll.

## Panoramica

Questo script legge contenuti da database Notion (DB CONTENT, DB PERSONAS, DB PROJECT) e genera file Markdown con frontmatter YAML per Jekyll.

## Struttura dello Script

### 1. Configurazione (Righe 11-50)

**Costanti:**
- `OUTPUT_DIR`: Directory di output (default: ".")
- `NOTION_FIELDS`: Mappa nomi campi Notion (centralizzata per facilitare manutenzione)
  - Contiene mapping tra nomi interni e nomi reali dei campi in Notion
  - Facilita refactoring e manutenzione quando i nomi campi cambiano
- `LAYOUT_MAP`: Mappa layout Notion -> layout Jekyll
  - Converte valori layout da Notion (es. "session", "document") in nomi layout Jekyll (es. "ob_session", "ob_document")

### 2. Logging (Righe 57-65)

**Funzioni:**
- `log(message: str, level: str = "INFO") -> None`
  - Logging con timestamp
  - Livelli: INFO, DEBUG, ERROR, WARNING

### 3. Notion API Utilities (Righe 66-231)

**Funzioni:**
- `get_notion_data(database_id: str, filter_body: Optional[Dict] = None) -> List[Dict]`
  - Query database Notion con paginazione completa
  - Restituisce lista di risultati

- `get_page_by_id(page_id: str) -> Optional[Dict]`
  - Recupera una pagina Notion per ID
  - Restituisce dati pagina o None se errore

- `get_property_value(prop: Optional[Dict]) -> Union[str, List, bool, int, float, None]`
  - Estrae valore 'pulito' da proprietà Notion
  - Supporta: title, rich_text, select, multi_select, date, relation, checkbox, number

- `update_infra_status(infra_page_id: Optional[str], status: str, error_log: str = "") -> None`
  - Aggiorna status di build in Notion
  - Status: "ok" o "error"

### 4. Content Processing Utilities (Righe 232-325)

**Funzioni:**
- `get_page_blocks(page_id: str) -> str`
  - Recupera tutti i blocchi di una pagina Notion e converte in Markdown
  - Supporta: paragraph, heading_1/2/3, code, bulleted_list_item, numbered_list_item, image

- `clean_markdown_content(content: str) -> str`
  - Pulisce contenuto markdown rimuovendo wrapper e separatori frontmatter
  - Rimuove ```markdown, ```html, e --- iniziali

### 5. File Generation Utilities (Righe 326-621)

**Funzioni:**
- `normalize_slug(slug: Optional[str]) -> str`
  - Normalizza slug rimuovendo .md e preparandolo per l'uso
  - Lowercase, spazi sostituiti con -

- `normalize_subsection(subsection: Optional[str]) -> str`
  - Normalizza nome subsection per percorso file
  - Converte "MusicaAI" -> "musica", "GiochiAI" -> "giochiAI"

- `generate_permalink(section: str, subsection: Optional[str] = None, internal_section: Optional[str] = None, slug: Optional[str] = None) -> str`
  - Genera permalink automatico basato su section, subsection, internal_section, slug
  - Esempio: `/ob-progetti/waw/council/`

- `get_jekyll_layout(layout_notion: Optional[str], section: Optional[str] = None, slug: Optional[str] = None) -> str`
  - Determina layout Jekyll da usare
  - Auto-rileva landing progetti: section == "OB-Progetti" e slug == "index" -> "ob_progetti"

- `generate_build_path(section: str, slug: Optional[str], layout_val: Optional[str], subsection: Optional[str] = None, internal_section: Optional[str] = None) -> str`
  - Genera percorso file secondo Routing Matrix
  - Esempio: `ob-progetti/waw/council/session-2026-01-04.md`

- `create_frontmatter(props: Dict[str, Any], layout_name: str) -> str`
  - Crea frontmatter YAML per Jekyll
  - Include automaticamente filter_section per ob_landing
  - Include custom_class: "ai-landing" per OB-AI landing

- `write_jekyll_file(file_path: str, content: str, infra_id_to_update: Optional[str] = None) -> bool`
  - Scrive file Jekyll Markdown con gestione errori
  - Crea directory necessarie se non esistono
  - Aggiorna status in Notion se infra_id fornito

- `validate_build_path(file_path: str) -> None`
  - Valida che percorso non contenga cartelle con underscore
  - Previene creazione file in cartelle riservate Jekyll

### 6. Content Processors (Righe 622-913)

**Funzioni:**
- `process_content_item(item: Dict[str, Any], infra_id_to_update: Optional[str] = None) -> bool`
  - Processa singolo item da DB CONTENT e genera file Jekyll
  - Estrae proprietà, genera frontmatter, recupera body, scrive file
  - Restituisce True se successo

- `process_personas() -> None`
  - Genera pagine AI personas da DB CONTENT (Section=OB-AI) collegato a DB PERSONAS
  - Recupera personas da DB PERSONAS, trova contenuto in DB CONTENT, genera pagine

- `process_projects() -> None`
  - Processa items da DB_PROJECT e genera pagine progetti
  - Supporta relazioni a DB_CONTENT, AI_MODELS, PERSONAS
  - Genera pagine per progetti principali e subsections

### 7. Tag Pages Generation (Righe 914-1155)

**Funzioni:**
- `get_all_tags_from_files() -> set`
  - Scansiona tutti i file .md generati e raccoglie tag unici
  - Cerca in: ob-session, ob-ai, ob-progetti, ob-archives
  - Restituisce set di tag unici

- `extract_tags_from_frontmatter(frontmatter: str) -> List[str]`
  - Estrae tutti i tag da frontmatter YAML
  - Supporta: `tags: ["tag1", "tag2"]`, `tags: tag1, tag2`, `tags: "tag1, tag2"`

- `generate_tag_slug(tag: str) -> str`
  - Converte tag in slug per URL
  - Esempio: "AI Tools" -> "ai-tools"

- `generate_tag_pages() -> None`
  - Genera pagine tag per tutti i tag trovati nei file esistenti
  - Crea file in `tags/tag-slug.md` con layout ob_tag

- `generate_top_tags_data() -> None`
  - Genera file `_data/top_tags.yml` con i 5 tag più popolari
  - Usato da Jekyll per mostrare top tag nella homepage

- `cleanup_orphan_tag_pages() -> None`
  - Rimuove pagine tag che non hanno più contenuti associati
  - Utile dopo rimozione tag da contenuti

### 8. Main Entry Point (Righe 1330-1410)

**Funzioni:**
- `main() -> None`
  - Entry point principale del generatore
  - Orchestrazione completa:
    1. Processa contenuti da DB CONTENT
    2. Processa personas da DB PERSONAS
    3. Processa progetti da DB PROJECT
    4. Genera pagine tag
    5. Genera top tags data

## Flusso di Esecuzione

1. **Setup**: Carica configurazione e costanti
2. **DB CONTENT**: Query contenuti con Status="Published"
3. **Process Content**: Per ogni contenuto:
   - Estrae proprietà da Notion
   - Genera frontmatter
   - Recupera body content
   - Scrive file Markdown
   - Aggiorna status in Notion
4. **Personas**: Processa personas da DB PERSONAS
5. **Projects**: Processa progetti da DB PROJECT
6. **Tags**: Genera pagine tag e top tags data

## Dipendenze

Le dipendenze sono gestite tramite `requirements.txt` nella root del repository:

- `requests>=2.31.0`: Per chiamate API Notion
- `pyyaml>=6.0`: Per generazione file YAML (opzionale, ha fallback manuale)
- `python-dotenv>=1.0.0`: Per gestione variabili d'ambiente (opzionale)

**Dipendenze standard Python:**
- `os`, `datetime`: Utilities standard Python
- `typing`: Per type hints (Optional, List, Dict, Any, Union)
- `notion_config`: Configurazione Notion locale (API key, database IDs) - file `tools/notion_config.py`

### Installazione

```bash
# Dalla root del repository
pip install -r requirements.txt
```

## Script Correlati

### `test_tag_generation.py`

Script di test standalone per generazione pagine tag. Non richiede connessione a Notion API.

**Funzionalità:**
- Scansiona tutti i file `.md` nelle cartelle di contenuto
- Estrae tag dai frontmatter
- Genera pagine tag in `tags/`
- Genera file `_data/top_tags.yml` con i top 5 tag

**Uso:**
```bash
python tools/test_tag_generation.py
```

**Differenze con lo script principale:**
- Non richiede dipendenze Notion API
- Testa solo la logica di generazione tag
- Utile per debug locale senza chiamate API

## Esecuzione

### Esecuzione Locale

```bash
# Assicurati di avere le dipendenze installate
pip install -r requirements.txt

# Esegui lo script dalla root del repository
python tools/notion_to_jekyll_builder.py
```

**Nota:** Lo script deve essere eseguito dalla root del repository per generare i file nella posizione corretta (non da dentro `tools/`).

### GitHub Actions

Lo script è configurato per eseguirsi automaticamente tramite GitHub Actions (`.github/workflows/notion-sync.yml`):

- **Trigger**: Ogni 6 ore (cron) o manuale (workflow_dispatch)
- **Processo**: 
  1. Installa dipendenze da `requirements.txt`
  2. Esegue lo script
  3. Committa e pusha i cambiamenti generati

## Note

- Lo script genera file relativi alla directory corrente (root del repository)
- Crea automaticamente directory necessarie
- Aggiorna status build in Notion se infra_id fornito
- Supporta paginazione per query Notion grandi
- Gestisce errori gracefully con logging
- Le dipendenze sono specificate in `requirements.txt` nella root

## Type Hints

Tutte le funzioni hanno type hints completi per:
- Parametri di input
- Valori di ritorno
- Tipi opzionali (Optional)
- Union types per valori multipli

## Docstring

Tutte le funzioni hanno docstring dettagliate con:
- Descrizione funzionalità
- Args: Parametri con tipo e descrizione
- Returns: Tipo e descrizione valore di ritorno
- Esempi dove utile
- Note su comportamento speciale
