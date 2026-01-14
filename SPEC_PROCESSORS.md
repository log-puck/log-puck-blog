# SPEC_PROCESSORS.md — Specifiche Processori Python per LOG_PUCK Blog

## Panoramica

Questo documento descrive la struttura modulare Python per la generazione di contenuti Jekyll da database Notion.

**Versione:** 4.0 (Modulare)  
**Ultimo aggiornamento:** 2025-01-12  
**Linguaggio:** Python 3.x

---

## Struttura Modulare

### Architettura Package

```
tools/notion_jekyll/
├── __init__.py
├── orchestrator.py          # Entry point principale
├── config.py                # Configurazione (DB IDs, paths)
├── logger.py                # Logging utility
│
├── api/
│   ├── __init__.py
│   ├── client.py            # NotionClient (API wrapper)
│   └── properties.py        # Property extractors
│
├── processors/
│   ├── __init__.py
│   ├── articles.py          # ArticlesProcessor
│   ├── documentation.py     # DocumentationProcessor
│   ├── ai_profiles.py       # AIProfilesProcessor
│   └── waw_council.py       # WAWCouncilProcessor
│
├── converters/
│   ├── __init__.py
│   ├── jekyll_builder.py    # Frontmatter & path generation
│   └── notion_to_markdown.py # Notion blocks → Markdown
│
└── generators/
    ├── __init__.py
    ├── tags.py              # TagGenerator (tag pages, top tags)
    └── file_writer.py       # File I/O utilities
```

---

## Entry Point: `orchestrator.py`

### Classe `JekyllOrchestrator`

**Responsabilità:** Coordinare tutti i processori e generatori

```python
class JekyllOrchestrator:
    def __init__(self, client: NotionClient):
        self.client = client
        self.articles_processor = ArticlesProcessor(client)
        self.documentation_processor = DocumentationProcessor(client)
        self.ai_profiles_processor = AIProfilesProcessor(client)
        self.waw_council_processor = WAWCouncilProcessor(client)
        self.tag_generator = TagGenerator()
    
    def run(self) -> None:
        # 1. Processa Articles
        self.articles_processor.process_articles()
        
        # 2. Processa Documentation
        self.documentation_processor.process_documentation()
        
        # 3. Processa AI Profiles
        self.ai_profiles_processor.process_ai_profiles()
        
        # 4. Processa WAW Council
        self.waw_council_processor.process_waw_council()
        
        # 5. Genera tag pages
        self.tag_generator.generate_tag_pages()
        
        # 6. Genera top tags data
        self.tag_generator.generate_top_tags_data()
        
        # 7. Cleanup tag orfani
        self.tag_generator.cleanup_orphan_tag_pages()
```

**Uso:**
```python
from notion_jekyll.api import NotionClient
from notion_jekyll.orchestrator import JekyllOrchestrator

client = NotionClient(api_key="...")
orchestrator = JekyllOrchestrator(client)
orchestrator.run()
```

---

## Processori

### Struttura Standard di un Processor

Tutti i processori seguono questo pattern:

```python
from ..api import NotionClient, get_property_value
from ..converters import JekyllBuilder
from ..generators import FileWriter
from ..logger import log

class NomeProcessor:
    """Processor per [DESCRIZIONE]"""
    
    def __init__(self, client: NotionClient):
        self.client = client
        self.builder = JekyllBuilder()
        self.writer = FileWriter()
    
    def process_nome(self) -> None:
        """Processa [tipo contenuto] da Notion e genera file Jekyll"""
        log(f"Inizio generazione [TIPO]...")
        
        # 1. Query Notion database
        pages = self.client.query_database(
            database_id=CONFIG.DB_NOME_ID,
            filter={
                "and": [
                    {"property": "Published", "checkbox": {"equals": True}},
                    {"property": "Build Status", "select": {"equals": "Done"}}
                ]
            }
        )
        
        # 2. Processa ogni pagina
        generated_count = 0
        for page in pages:
            # 3. Estrai properties
            title = get_property_value(page, "Title", "title")
            # ... altre properties
            
            # 4. Genera frontmatter
            frontmatter = self.builder.create_frontmatter(
                title=title,
                layout="ob_nome",
                section="OB-Section",
                # ... altre opzioni
            )
            
            # 5. Genera markdown content
            content = self.client.get_page_content(page_id=page["id"])
            
            # 6. Genera path/file
            file_path = self.builder.generate_file_path(
                section="OB-Section",
                slug=slug,
                filename=filename
            )
            
            # 7. Scrivi file
            self.writer.write_jekyll_file(
                file_path=file_path,
                frontmatter=frontmatter,
                content=content
            )
            
            # 8. Aggiorna status Notion (opzionale)
            self.client.update_page_status(
                page_id=page["id"],
                status="Published"
            )
            
            generated_count += 1
        
        log(f"--- [TIPO]: Generati {generated_count} file. ---")
```

---

## Processori Esistenti

### `ArticlesProcessor`

**Database:** `DB_ARTICLES_ID`  
**Layout:** `ob_session`  
**Section:** `OB-Session`  
**Path:** `./ob-session/`  
**Metodo:** `process_articles()`

**Properties Notion:**
- `Title` (title)
- `Date` (date)
- `Description` (rich_text)
- `Tags` (multi_select)
- `Published` (checkbox)
- `Build Status` (select)

**Campi frontmatter:**
- `title`, `date`, `layout`, `section`, `tags`

### `DocumentationProcessor`

**Database:** `DB_DOCUMENTATION_ID`  
**Layout:** `ob_document`  
**Section:** `OB-Archives`  
**Path:** `./ob-archives/`  
**Metodo:** `process_documentation()`

**Properties Notion:**
- `Title` (title)
- `Date` (date)
- `Description` (rich_text)
- `Version` (rich_text)
- `Tags` (multi_select)
- `Section` (select) → sempre "OB-Archives"
- `Published` (checkbox)
- `Build Status` (select)

**Campi frontmatter:**
- `title`, `date`, `layout`, `section`, `tags`, `version`

### `AIProfilesProcessor`

**Database:** `DB_AI_PROFILES_ID`  
**Layout:** `ob_ai`  
**Section:** `OB-AI`  
**Path:** `./ob-ai/`  
**Metodo:** `process_ai_profiles()`

**Properties Notion:**
- `Title` (title)
- `Avatar` (rich_text)
- `Profilo` (rich_text)
- `Epoca` (rich_text)
- `Style` (rich_text)
- `Tags` (multi_select)
- `Published` (checkbox)
- `Build Status` (select)

**Campi frontmatter custom:**
- `title`, `layout`, `section`, `tags`
- `avatar`, `profilo`, `epoca`, `style` (custom fields)

### `WAWCouncilProcessor`

**Database:** `WAW_COUNCIL_ID`  
**Layout:** `ob_progetti` (test) → futuro `ob_council`  
**Section:** `OB-Progetti`  
**Subsection:** `wAw`  
**Path:** `./ob-progetti/waw/council/`  
**Metodo:** `process_waw_council()`

**Properties Notion:**
- `Title` (title)
- `Date` (date)
- `Session Number` (number)
- `Tags` (multi_select)
- `Published` (checkbox)
- `Build Status` (select)

**Campi frontmatter:**
- `title`, `date`, `layout`, `section`, `subsection`, `tags`

---

## Configurazione: `config.py`

### Database IDs

```python
# Notion Database IDs
# NOTA: I Database IDs reali sono in config.py (non commitare valori reali qui)
DB_ARTICLES_ID = "TBD"  # Impostare in config.py o variabili d'ambiente
DB_DOCUMENTATION_ID = "TBD"
DB_AI_PROFILES_ID = "TBD"
WAW_COUNCIL_ID = "TBD"
DB_PROJECT_DATA_ID = "TBD"
DB_MUSICA_ID = "TBD"
DB_STUDI_MUSICA_ID = "TBD"
```

### Path Mapping

```python
SECTION_DIR_MAP = {
    "OB-Session": "ob-session",
    "OB-Archives": "ob-archives",
    "OB-AI": "ob-ai",
    "OB-Progetti": "ob-progetti"
}
```

### Layout Mapping

```python
LAYOUT_MAP = {
    "ob_session": "ob_session",
    "ob_document": "ob_document",
    "ob_ai": "ob_ai",
    "ob_progetti": "ob_progetti"
}
```

---

## Converters

### `JekyllBuilder`

**Responsabilità:**
- Generazione frontmatter YAML
- Generazione file paths
- Mapping sezioni → directory

**Metodi principali:**

```python
def create_frontmatter(
    title: str,
    layout: str,
    section: str,
    date: Optional[str] = None,
    tags: Optional[List[str]] = None,
    **kwargs
) -> str:
    """Genera frontmatter YAML"""
    
def generate_file_path(
    section: str,
    slug: str,
    filename: Optional[str] = None
) -> str:
    """Genera path file Jekyll"""
```

**Campi custom supportati:**
- `avatar`, `profilo`, `epoca`, `style` (AI Profiles)
- `version`, `next_review` (Documents)

### `NotionToMarkdown`

**Responsabilità:**
- Conversione Notion blocks → Markdown
- Supporto rich text, code blocks, lists

---

## Generators

### `TagGenerator`

**Responsabilità:**
- Genera pagine tag (`tags/*.md`)
- Genera `_data/top_tags.yml`
- Cleanup tag orfani

**Metodi:**
- `generate_tag_pages()`: Scansiona contenuti, genera pagine tag
- `generate_top_tags_data()`: Genera top 5 tags per `_data/top_tags.yml`
- `cleanup_orphan_tag_pages()`: Rimuove tag pages senza contenuti associati

### `FileWriter`

**Responsabilità:**
- Scrittura file Jekyll (frontmatter + content)
- Gestione directory (crea se non esistono)
- Encoding UTF-8

---

## API Client

### `NotionClient`

**Responsabilità:**
- Wrapper Notion API
- Query database
- Get page content
- Update page properties

**Metodi principali:**

```python
def query_database(
    database_id: str,
    filter: Optional[Dict] = None
) -> List[Dict]:
    """Query Notion database con filtri"""
    
def get_page_content(page_id: str) -> str:
    """Estrae contenuto markdown da pagina Notion"""
    
def update_page_status(
    page_id: str,
    status: str = "Published"
) -> None:
    """Aggiorna status pagina Notion"""
```

**Filtri standard:**
```python
filter = {
    "and": [
        {"property": "Published", "checkbox": {"equals": True}},
        {"property": "Build Status", "select": {"equals": "Done"}}
    ]
}
```

---

## Convenzioni

### Naming
- **Classi:** `NomeProcessor` (PascalCase)
- **Metodi:** `process_nome()` (snake_case)
- **File:** `nome_processor.py` (snake_case)

### Filtering
- **Sempre filtrare:** `Published = True` AND `Build Status = Done`
- **Errori:** Se build fallisce, aggiornare status a "In Review"

### Paths
- **Directory:** Usare `SECTION_DIR_MAP` per mapping sezioni
- **Filename:** Generare da slug/title (lowercase, hyphens)
- **Encoding:** Sempre UTF-8

### Frontmatter
- **Layout:** Sempre specificare (`ob_session`, `ob_document`, etc.)
- **Section:** Sempre specificare (`OB-Session`, `OB-Archives`, etc.)
- **Tags:** Lista YAML, sempre presente (anche se vuota)

---

## Creare un Nuovo Processor

### Template

```python
from ..api import NotionClient, get_property_value
from ..converters import JekyllBuilder
from ..generators import FileWriter
from ..config import DB_NUOVO_ID, SECTION_DIR_MAP
from ..logger import log

class NuovoProcessor:
    """Processor per [DESCRIZIONE]"""
    
    def __init__(self, client: NotionClient):
        self.client = client
        self.builder = JekyllBuilder()
        self.writer = FileWriter()
    
    def process_nuovo(self) -> None:
        """Processa [tipo] da Notion"""
        log(f"Inizio generazione [TIPO]...")
        
        # Query Notion
        pages = self.client.query_database(
            database_id=DB_NUOVO_ID,
            filter={
                "and": [
                    {"property": "Published", "checkbox": {"equals": True}},
                    {"property": "Build Status", "select": {"equals": "Done"}}
                ]
            }
        )
        
        generated_count = 0
        for page in pages:
            # Estrai properties
            title = get_property_value(page, "Title", "title")
            # ... altre properties
            
            # Genera frontmatter
            frontmatter = self.builder.create_frontmatter(
                title=title,
                layout="ob_nuovo",
                section="OB-Section",
                # ... altre opzioni
            )
            
            # Genera content
            content = self.client.get_page_content(page_id=page["id"])
            
            # Genera path
            file_path = self.builder.generate_file_path(
                section="OB-Section",
                slug=slug,
                filename=filename
            )
            
            # Scrivi file
            self.writer.write_jekyll_file(
                file_path=file_path,
                frontmatter=frontmatter,
                content=content
            )
            
            generated_count += 1
        
        log(f"--- [TIPO]: Generati {generated_count} file. ---")
```

### Steps

1. **Creare file:** `tools/notion_jekyll/processors/nuovo.py`
2. **Definire classe:** `NuovoProcessor`
3. **Implementare metodo:** `process_nuovo()`
4. **Aggiungere DB ID:** In `config.py`
5. **Registrare in orchestrator:**
   - Import in `processors/__init__.py`
   - Istanziazione in `orchestrator.py`
   - Chiamata in `orchestrator.run()`

---

## Note per Collaboratori AI

Quando sviluppi nuovi processori:

1. **Segui il pattern:** Usa template standard
2. **Filtri obbligatori:** Sempre `Published = True` AND `Build Status = Done`
3. **Error handling:** Log errors, aggiorna status Notion se fallisce
4. **Documentazione:** Documenta properties Notion richieste
5. **Testing:** Testa con database Notion reale
6. **Integrazione:** Registra in orchestrator dopo implementazione

**Riferimenti:**
- `SPEC_HTML.md` per layouts e frontmatter
- `SPEC_SCSS.md` per stili CSS
- Processori esistenti come esempi (`articles.py`, `documentation.py`)
