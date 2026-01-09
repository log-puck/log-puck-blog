"""
Notion to Jekyll Builder
Converte contenuti da Notion a file Markdown per Jekyll
"""

import requests
import os
import datetime
from typing import Optional, List, Dict, Any, Union
from notion_config import NOTION_API_KEY, DB_CONTENT_ID, DB_PERSONAS_ID, DB_PROJECT_ID

# ============================================================================
# 1. CONFIGURAZIONE
# ============================================================================

OUTPUT_DIR = "."

# Costanti per nomi campi Notion (centralizzate per facilitare manutenzione)
NOTION_FIELDS = {
    "title": "Title",
    "slug": "Slug",
    "date": "Date",
    "layout": "Layout",
    "section": "Section",
    "subsection": "Subsection",
    "description": "Description",
    "keywords": "Keywords",
    "tags": "Tags",
    "subtitle": "Subtitle",
    "show_footer": "Show Footer",
    "footer_text": "Footer Text",
    "version": "version",
    "next_review": "next_review",
    "internal_section": "Internal Section",
    "ai_author": "AI Author",
    "ai_participants": "AI Partecipants",
    "project_status": "Project Status"
}

LAYOUT_MAP = {
    "session": "ob_session",
    "document": "ob_document",
    "landing": "ob_landing",
    "ai": "ob_ai",
    "musica": "ob_musica",
    "giochi": "ob_giochiAI",
    "project": "ob_progetti",
    "archive": "ob_archive",
    "tag": "ob_tag"
}

NOTION_HEADERS = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

# ============================================================================
# 2. UTILITY BASE
# ============================================================================

def log(message: str, level: str = "INFO") -> None:
    """
    Logging con timestamp.
    
    Args:
        message: Messaggio da loggare
        level: Livello di log (INFO, DEBUG, ERROR, WARNING)
    """
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] [{level}] {message}")

# ============================================================================
# 3. NOTION API UTILITIES
# ============================================================================

def get_notion_data(database_id: str, filter_body: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
    """
    Query un database Notion con paginazione completa.
    
    Args:
        database_id: ID del database Notion
        filter_body: Filtro opzionale per la query (dict con proprietà filter)
        
    Returns:
        Lista di risultati dalla query (lista di dict con proprietà Notion)
        
    Raises:
        Exception: Se la chiamata API fallisce
    """
    results = []
    url = f"https://api.notion.com/v1/databases/{database_id}/query"
    has_more = True
    start_cursor = None

    while has_more:
        payload = {}
        if start_cursor:
            payload["start_cursor"] = start_cursor
        if filter_body:
            payload.update(filter_body)

        response = requests.post(url, headers=NOTION_HEADERS, json=payload)
        if response.status_code != 200:
            log(f"Errore API Notion: {response.text}", "ERROR")
            raise Exception(f"API Error: {response.status_code}")

        data = response.json()
        results.extend(data.get("results", []))
        has_more = data.get("has_more", False)
        start_cursor = data.get("next_cursor", None)
    return results

def get_page_by_id(page_id: str) -> Optional[Dict[str, Any]]:
    """
    Recupera una pagina Notion per ID.
    
    Args:
        page_id: ID della pagina Notion
        
    Returns:
        Dati della pagina (dict) o None se errore
    """
    url = f"https://api.notion.com/v1/pages/{page_id}"
    response = requests.get(url, headers=NOTION_HEADERS)
    if response.status_code == 200:
        return response.json()
    return None

def get_property_value(prop: Optional[Dict[str, Any]]) -> Union[str, List[str], bool, int, float, None]:
    """
    Estrae il valore 'pulito' da un oggetto proprietà Notion.
    
    Gestisce: title, rich_text, select, multi_select, date, relation, checkbox, number
    
    Args:
        prop: Oggetto proprietà Notion (dict con campo "type" e dati specifici)
        
    Returns:
        Valore estratto:
        - str per title, rich_text, select, date
        - List[str] per multi_select, relation (lista di ID)
        - bool per checkbox
        - int/float per number
        - None se prop è None o tipo non supportato
    """
    if not prop:
        return None
        
    prop_type = prop.get("type")
    
    if prop_type == "title":
        title_list = prop.get("title", [])
        if title_list:
            return title_list[0].get("plain_text", "")
        return ""
    elif prop_type == "rich_text":
        rich_text_list = prop.get("rich_text", [])
        if rich_text_list:
            return rich_text_list[0].get("plain_text", "")
        return ""
    elif prop_type == "select":
        select_obj = prop.get("select")
        if select_obj:
            return select_obj.get("name", "")
        return ""
    elif prop_type == "multi_select":
        return [tag.get("name") for tag in prop.get("multi_select", [])]
    elif prop_type == "date":
        date_obj = prop.get("date")
        if date_obj:
            return date_obj.get("start")
        return None
    elif prop_type is None:
        # Campo esiste ma non ha tipo (campo vuoto o non configurato)
        return None
    elif prop_type == "relation":
        return [rel.get("id") for rel in prop.get("relation", [])]
    elif prop_type == "checkbox":
        return prop.get("checkbox", False)
    elif prop_type == "number":
        return prop.get("number")
    return None

def update_infra_status(infra_page_id: Optional[str], status: str, error_log: str = "") -> None:
    """
    Aggiorna lo status di build in Notion.
    
    Args:
        infra_page_id: ID della pagina infra (None se non presente)
        status: "ok" o "error"
        error_log: Messaggio di errore opzionale
    """
    url = f"https://api.notion.com/v1/pages/{infra_page_id}"
    
    notion_status_name = "In progress"
    if status == "ok":
        notion_status_name = "Done"
    elif status == "error":
        notion_status_name = "In progress"
        
    payload = {
        "properties": {
            "Build Status": {
                "status": {
                    "name": notion_status_name
                }
            },
            "Last Build": {
                "date": {
                    "start": datetime.datetime.now().isoformat()
                }
            }
        }
    }
    
    if error_log:
        payload["properties"]["Error Log"] = {
            "rich_text": [
                {
                    "text": {
                        "content": error_log
                    }
                }
            ]
        }

    response = requests.patch(url, headers=NOTION_HEADERS, json=payload)
    if response.status_code != 200:
        log(f"Errore aggiornamento status infra {infra_page_id}: {response.text}", "WARN")

# ============================================================================
# 4. CONTENT PROCESSING UTILITIES
# ============================================================================

def get_page_blocks(page_id: str) -> str:
    """
    Recupera tutti i blocchi di una pagina Notion e converte in Markdown.
    
    Supporta: paragraph, heading_1/2/3, code, bulleted_list_item, numbered_list_item
    
    Args:
        page_id: ID della pagina Notion
        
    Returns:
        Contenuto Markdown della pagina (stringa)
    """
    all_blocks = []
    has_more = True
    start_cursor = None
    
    while has_more:
        url = f"https://api.notion.com/v1/blocks/{page_id}/children"
        params = {}
        if start_cursor:
            params["start_cursor"] = start_cursor
            
        response = requests.get(url, headers=NOTION_HEADERS, params=params)
        if response.status_code != 200:
            log(f"Errore recupero blocchi per {page_id}: {response.text}", "ERROR")
            break
            
        data = response.json()
        all_blocks.extend(data.get("results", []))
        has_more = data.get("has_more", False)
        start_cursor = data.get("next_cursor", None)
    
    content_md = ""
    
    def get_text(prop):
        """Concatena tutti i rich_text elements."""
        rich_text_list = prop.get("rich_text", [])
        return "".join([rt.get("plain_text", "") for rt in rich_text_list])
    
    for block in all_blocks:
        block_type = block.get("type")
        block_data = block.get(block_type, {})
        
        if block_type == "paragraph":
            text = get_text(block_data)
            content_md += f"{text}\n\n"
        elif block_type == "heading_1":
            text = get_text(block_data)
            content_md += f"# {text}\n\n"
        elif block_type == "heading_2":
            text = get_text(block_data)
            content_md += f"## {text}\n\n"
        elif block_type == "heading_3":
            text = get_text(block_data)
            content_md += f"### {text}\n\n"
        elif block_type == "code":
            text = get_text(block_data)
            lang = block_data.get("language", "")
            if lang.lower() == "markdown":
                content_md += f"{text}\n\n"
            else:
                content_md += f"```{lang}\n{text}\n```\n\n"
        elif block_type == "bulleted_list_item":
            text = get_text(block_data)
            content_md += f"- {text}\n"
        elif block_type == "numbered_list_item":
            text = get_text(block_data)
            content_md += f"1. {text}\n"
        elif block_type == "image":
            url_img = block_data.get("external", {}).get("url")
            if not url_img:
                url_img = block_data.get("file", {}).get("url")
            if url_img:
                content_md += f"![image]({url_img})\n\n"
    
    # Rimuovi markdown wrapper se presente
    content_md = clean_markdown_content(content_md)
    
    return content_md

def clean_markdown_content(content: str) -> str:
    """
    Pulisce il contenuto markdown rimuovendo wrapper e separatori frontmatter.
    
    Args:
        content: Contenuto markdown da pulire
        
    Returns:
        Contenuto pulito
    """
    if not content:
        return content
    
    # Rimuovi wrapper markdown se presente
    if content.startswith("```markdown"):
        content = content.replace("```markdown\n", "", 1)
    if content.startswith("```html"):
        content = content.replace("```html\n", "", 1)
    if content.endswith("```"):
        content = content.rstrip("```").rstrip()
    
    # Rimuovi eventuale --- iniziale (può essere rimasto da Notion)
    if content.strip().startswith("---"):
        content = content.strip()[3:].lstrip() + "\n"
    
    return content

# ============================================================================
# 5. FILE GENERATION UTILITIES
# ============================================================================

def normalize_slug(slug: Optional[str]) -> str:
    """
    Normalizza lo slug rimuovendo .md se presente e preparandolo per l'uso.
    
    Args:
        slug: Slug originale (può contenere .md o meno)
        
    Returns:
        Slug normalizzato (senza .md, lowercase, spazi sostituiti con -)
    """
    if not slug:
        return ""
    # Rimuovi .md se presente
    if slug.endswith(".md"):
        slug = slug[:-3]
    # Normalizza: lowercase, rimuovi spazi, sostituisci con -
    return slug.strip().lower().replace(" ", "-")

def normalize_subsection(subsection: Optional[str]) -> str:
    """
    Normalizza il nome della subsection per il percorso file.
    
    Converte "MusicaAI" -> "musica", "GiochiAI" -> "giochiAI", etc.
    
    Args:
        subsection: Nome subsection originale (può essere None)
        
    Returns:
        Nome subsection normalizzato (lowercase, spazi sostituiti con -), stringa vuota se None
    """
    if not subsection:
        return ""
    
    sub_sub = subsection.lower().replace(" ", "-")
    if "musica" in sub_sub:
        sub_sub = "musica"
    elif "giochi" in sub_sub:
        sub_sub = "giochiAI"
    
    return sub_sub

def generate_permalink(section: str, subsection: Optional[str] = None, internal_section: Optional[str] = None, slug: Optional[str] = None) -> str:
    """
    Genera il permalink automatico basato su section, subsection, internal_section e slug.
    
    Esempi:
    - section="OB-Session", slug="test" -> "/ob-session/test/"
    - section="OB-Progetti", subsection="wAw", slug="index" -> "/ob-progetti/waw/"
    - section="OB-Progetti", subsection="wAw", internal_section="Council", slug="index" -> "/ob-progetti/waw/council/"
    
    Args:
        section: Sezione (OB-Session, OB-AI, OB-Progetti, OB-Archives)
        subsection: Sottosezione opzionale (wAw, MusicaAI, etc.)
        internal_section: Sezione interna opzionale (Council, Metabolism, Evolution, etc.)
        slug: Slug del contenuto (None per index.md, che genera permalink senza /index/)
        
    Returns:
        Permalink generato o None se non valido
    """
    permalink_parts = []
    
    if section:
        section_slug = section.lower().replace(" ", "-")
        permalink_parts.append(section_slug)
    
    if subsection:
        subsection_slug = normalize_subsection(subsection)
        permalink_parts.append(subsection_slug)
    
    if internal_section:
        internal_slug = internal_section.lower().replace(" ", "-")
        permalink_parts.append(internal_slug)
    
    # Per file index.md, non aggiungere slug
    if slug and slug != "index":
        permalink_parts.append(slug)
    
    if permalink_parts:
        return "/" + "/".join(permalink_parts) + "/"
    
    return None

def get_jekyll_layout(layout_notion: Optional[str], section: Optional[str] = None, slug: Optional[str] = None) -> str:
    """
    Determina il layout Jekyll da usare, con auto-rilevamento per landing progetti.
    
    Mappa layout Notion -> layout Jekyll usando LAYOUT_MAP.
    Auto-rileva landing progetti: se section == "OB-Progetti" e slug == "index", usa "ob_progetti".
    
    Args:
        layout_notion: Valore layout da Notion (session, document, landing, etc.)
        section: Sezione (per auto-rilevamento progetti)
        slug: Slug (per auto-rilevamento progetti)
        
    Returns:
        Nome layout Jekyll (es. "ob_session", "ob_document", "ob_progetti", "default")
    """
    jekyll_layout = LAYOUT_MAP.get(layout_notion, "default")
    
    # Auto-rileva landing di progetti: se section == "OB-Progetti" e slug == "index", usa layout ob_progetti
    # Questo include anche le landing di subsection (es. council/index, metabolism/index, evolution/index)
    if section == "OB-Progetti" and slug == "index":
        jekyll_layout = "ob_progetti"
    
    return jekyll_layout

def generate_build_path(section: str, slug: Optional[str], layout_val: Optional[str], subsection: Optional[str] = None, internal_section: Optional[str] = None) -> str:
    """
    Genera il percorso file secondo la Routing Matrix.
    
    Esempi:
    - section="OB-Session", slug="test" -> "ob-session/test.md"
    - section="OB-Progetti", subsection="wAw", slug="index" -> "ob-progetti/waw/index.md"
    - section="OB-Progetti", subsection="wAw", internal_section="Council", slug="session-2026-01-04" -> "ob-progetti/waw/council/session-2026-01-04.md"
    
    Args:
        section: Sezione (OB-Session, OB-AI, OB-Progetti, OB-Archives)
        slug: Slug del contenuto (normalizzato automaticamente)
        layout_val: Valore layout Notion (non usato ma mantenuto per compatibilità)
        subsection: Sottosezione opzionale (wAw, MusicaAI, etc.)
        internal_section: Sezione interna (Council, Metabolism, Evolution, tracce, etc.)
        
    Returns:
        Percorso file completo relativo (es. "ob-session/test.md")
    """
    safe_slug = normalize_slug(slug)
    
    dir_map = {
        "OB-Session": "ob-session",
        "OB-AI": "ob-ai",
        "OB-Progetti": "ob-progetti",
        "OB-Archives": "ob-archives"
    }
    base_dir = dir_map.get(section, "uncategorized")
    
    sub_path = ""
    
    if subsection:  # Rimossi controlli per "Default"
        sub_sub = normalize_subsection(subsection)
        if sub_path == "":
            sub_path = f"{sub_sub}/"
        else:
            sub_path = f"{sub_path}{sub_sub}/"
    
    # Aggiungi Internal Section se presente (es. Council, Metabolism, Evolution, tracce)
    if internal_section:
        internal_path = internal_section.lower().replace(" ", "-")
        sub_path = f"{sub_path}{internal_path}/"
        
    filename = f"{safe_slug}.md"
    return os.path.join(OUTPUT_DIR, base_dir, sub_path, filename)

def create_frontmatter(props: Dict[str, Any], layout_name: str) -> str:
    """
    Crea il frontmatter YAML per Jekyll.
    
    Include automaticamente:
    - filter_section per layout ob_landing
    - custom_class: "ai-landing" per OB-AI landing
    
    Args:
        props: Dizionario con le proprietà (title, slug, date, section, subsection, description, keywords, tags, etc.)
        layout_name: Nome del layout Jekyll (es. "ob_session", "ob_landing")
        
    Returns:
        Stringa frontmatter YAML formattata (inizia con "---" e termina con "---")
    """
    fm = "---\n"
    fm += f'title: "{props.get("title", "Untitled")}"\n'
    fm += f'slug: "{props.get("slug", "")}"\n'
    fm += f'date: "{props.get("date", "")}"\n'
    fm += f'section: "{props.get("section", "")}"\n'
    
    # Includi subsection se presente
    if props.get("subsection"):
        fm += f'subsection: "{props.get("subsection")}"\n'
        
    fm += f'layout: "{layout_name}"\n'
    
    # Per layout ob_landing, aggiungi automaticamente filter_section (uguale a section)
    # Controlla che non sia già presente per evitare duplicati
    if layout_name == "ob_landing" and props.get("section") and "filter_section" not in str(fm):
        fm += f'filter_section: "{props.get("section")}"\n'
    
    # Per OB-AI landing, aggiungi automaticamente custom_class per stili CSS specifici
    if layout_name == "ob_landing" and props.get("section") == "OB-AI":
        fm += f'custom_class: "ai-landing"\n'
    
    if props.get("permalink"):
        fm += f'permalink: {props.get("permalink")}\n'
    
    # Description viene da "Description" in Notion
    if props.get("description"):
        fm += f'description: "{props.get("description")}"\n'
    
    if props.get("keywords"):
        fm += f'keywords: "{props.get("keywords")}"\n'
    
    # Campi display opzionali
    if props.get("subtitle"):
        fm += f'subtitle: "{props.get("subtitle")}"\n'
    
    if props.get("tags"):
        fm += "tags:\n"
        for tag in props.get("tags"):
            fm += f"  - {tag}\n"
    
    if props.get("ai_author"):
        fm += f'ai_author: "{props.get("ai_author")}"\n'
    
    if props.get("ai_participants"):
        fm += "ai_participants:\n"
        for participant in props.get("ai_participants"):
            fm += f'  - "{participant}"\n'
    
    # Project-specific fields
    if props.get("project_status"):
        fm += f'project_status: "{props.get("project_status")}"\n'
    
    # Campi footer (progetti)
    show_footer_val = props.get("show_footer")
    if show_footer_val is not None:
        fm += f'show_footer: {str(show_footer_val).lower()}\n'
    
    if props.get("footer_text"):
        fm += f'footer_text: "{props.get("footer_text")}"\n'
    
    # Campi documenti
    # version è number in Notion, convertiamo a stringa
    if props.get("version") is not None:
        version_val = props.get("version")
        # Se è number, converti a stringa mantenendo il formato (es. 1.0)
        if isinstance(version_val, (int, float)):
            fm += f'version: "{version_val}"\n'
        else:
            fm += f'version: "{version_val}"\n'
    
    if props.get("next_review"):
        # Formatta next_review come data
        next_review_val = props.get("next_review")
        if isinstance(next_review_val, str):
            fm += f'next_review: "{next_review_val}"\n'
        else:
            fm += f'next_review: "{next_review_val}"\n'
    if props.get("use_supabase_data"):
        fm += f'use_supabase_data: {str(props.get("use_supabase_data")).lower()}\n'
    if props.get("supabase_table"):
        fm += f'supabase_table: "{props.get("supabase_table")}"\n'
    if props.get("ai_models"):
        fm += "ai_models:\n"
        for model in props.get("ai_models"):
            fm += f'  - "{model}"\n'
    if props.get("personas"):
        fm += "personas:\n"
        for persona in props.get("personas"):
            fm += f'  - "{persona}"\n'
            
    fm += "---\n"
    return fm

def write_jekyll_file(file_path: str, content: str, infra_id_to_update: Optional[str] = None) -> bool:
    """
    Scrive un file Jekyll Markdown con gestione errori.
    
    Crea le directory necessarie se non esistono.
    Aggiorna lo status in Notion se infra_id_to_update è fornito.
    
    Args:
        file_path: Percorso del file da scrivere (relativo o assoluto)
        content: Contenuto completo (frontmatter YAML + body markdown)
        infra_id_to_update: ID pagina infra per aggiornare status (opzionale)
        
    Returns:
        True se successo, False altrimenti
    """
    try:
        target_dir = os.path.dirname(file_path)
        if target_dir and not os.path.exists(target_dir):
            os.makedirs(target_dir)
            
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        
        log(f"✅ [OK] Generato: {file_path}", "INFO")
        
        if infra_id_to_update:
            update_infra_status(infra_id_to_update, "ok")
        
        return True
        
    except Exception as e:
        log(f"ERROR writing {file_path}: {str(e)}", "ERROR")
        if infra_id_to_update:
            update_infra_status(infra_id_to_update, "error", str(e))
        return False

def validate_build_path(file_path: str) -> None:
    """
    Valida che il percorso non contenga cartelle con underscore.
    
    Jekyll tratta le cartelle con underscore come speciali (es. _layouts, _includes).
    Questa funzione previene la creazione accidentale di file in cartelle riservate.
    
    Args:
        file_path: Percorso da validare
        
    Raises:
        ValueError: Se il percorso contiene cartelle con underscore
    """
    path_components = os.path.normpath(file_path).split(os.sep)
    folders = path_components[:-1]
    
    if any(folder.startswith("_") for folder in folders):
        error_msg = f"⛔ ERRORE: Build Path '{file_path}' contiene cartella con '_'. Jekyll la ignorerebbe."
        log(error_msg, "ERROR")
        raise ValueError(error_msg)

# ============================================================================
# 6. CONTENT PROCESSORS
# ============================================================================

def process_content_item(item: Dict[str, Any], infra_id_to_update: Optional[str] = None) -> bool:
    """
    Processa un singolo item da DB CONTENT e genera il file Jekyll.
    
    Estrae tutte le proprietà da Notion, genera frontmatter, recupera body content,
    e scrive il file Markdown. Aggiorna lo status in Notion se infra_id è fornito.
    
    Args:
        item: Item Notion da DB CONTENT (dict con properties)
        infra_id_to_update: ID pagina infra per aggiornare status (opzionale)
        
    Returns:
        True se file generato con successo, False altrimenti
    """
    props_raw = item.get("properties", {})
    
    # 1. Estrai metadati base
    title = get_property_value(props_raw.get("Title"))
    slug = get_property_value(props_raw.get("Slug"))
    date = get_property_value(props_raw.get("Date"))
    layout_notion = get_property_value(props_raw.get("Layout"))
    section = get_property_value(props_raw.get("Section"))
    subsection = get_property_value(props_raw.get("Subsection"))
    # Description è stato rinominato da "Meta Description"
    description = get_property_value(props_raw.get("Description"))
    # Keywords è stato rinominato da "Keywords SEO"
    keywords = get_property_value(props_raw.get("Keywords"))
    tags = get_property_value(props_raw.get("Tags"))
    
    # Campi display opzionali
    subtitle = get_property_value(props_raw.get("Subtitle"))
    
    # Campi footer (letti direttamente da DB CONTENT)
    show_footer = get_property_value(props_raw.get("Show Footer"))
    footer_text = get_property_value(props_raw.get("Footer Text"))
    
    # Campi documenti opzionali
    version = get_property_value(props_raw.get("version"))
    next_review = get_property_value(props_raw.get("next_review"))
    
    # Internal Section (per percorsi progetti: Council, Metabolism, Evolution, etc.)
    internal_section = get_property_value(props_raw.get("Internal Section"))
    
    # Validazione campi obbligatori
    if not all([slug, date, layout_notion, section]):
        log(f"SKIP [MISSING FIELDS]: {title}", "WARN")
        if infra_id_to_update:
            update_infra_status(infra_id_to_update, "error", "Missing required fields")
        return False

    # 2. Recupero Build Path Override (se presente)
    build_path_override = None
    blog_relation_ids = get_property_value(props_raw.get("Blog"))
    if blog_relation_ids:
        infra_id = blog_relation_ids[0]
        infra_page = get_page_by_id(infra_id)
        if infra_page:
            bp_prop = infra_page.get("properties", {}).get("Build Path")
            if bp_prop:
                raw_path = get_property_value(bp_prop)
                if raw_path:
                    if raw_path.endswith(".html"):
                        raw_path = raw_path[:-5] + ".md"
                    build_path_override = os.path.join(OUTPUT_DIR, raw_path)

    # 3. Recupero Body Content
    # Body sempre dalla pagina DB_CONTENT stessa
    page_id = item.get("id")
    body_content = get_page_blocks(page_id)
    
    # 4. Estrai AI metadata direttamente da DB CONTENT
    # AI Author è select (singolo valore), AI Partecipants è multi-select (lista)
    ai_author = get_property_value(props_raw.get("AI Author"))
    ai_participants = get_property_value(props_raw.get("AI Partecipants"))
    
    # ai_author è già un singolo valore (select), non serve conversione
    # ai_participants è una lista (multi-select)
    if not isinstance(ai_participants, list):
        ai_participants = [ai_participants] if ai_participants else []
    
    # Validazione body content
    if not body_content:
        log(f"SKIP [NO BODY]: {title}", "WARN")
        if infra_id_to_update:
            update_infra_status(infra_id_to_update, "error", "No content found")
        return False

    # 5. Genera permalink automaticamente (se non c'è build_path_override)
    permalink = None
    if not build_path_override:
        permalink = generate_permalink(section, subsection, internal_section, slug)
    
    # 6. Genera percorso file
    jekyll_layout = get_jekyll_layout(layout_notion, section, slug)
    
    if build_path_override:
        file_path = build_path_override
    else:
        file_path = generate_build_path(section, slug, layout_notion, subsection, internal_section)

    # 7. Valida percorso
    try:
        validate_build_path(file_path)
    except ValueError:
        if infra_id_to_update:
            update_infra_status(infra_id_to_update, "error", "Invalid build path")
        return False

    # 8. Crea frontmatter e scrivi file
    fm_props = {
        "title": title,
        "slug": slug,
        "date": date,
        "section": section,
        "subsection": subsection,
        "description": description,
        "keywords": keywords,
        "tags": tags,
        "permalink": permalink,
        "subtitle": subtitle,
        "ai_author": ai_author,
        "ai_participants": ai_participants,
        "show_footer": show_footer,
        "footer_text": footer_text,
        "version": version,
        "next_review": next_review
    }
    
    # Pulisci il body content
    body_content = clean_markdown_content(body_content)
    
    full_content = create_frontmatter(fm_props, jekyll_layout) + body_content
    
    return write_jekyll_file(file_path, full_content, infra_id_to_update)

def process_personas() -> None:
    """
    Genera pagine AI personas da DB CONTENT (Section=OB-AI) 
    collegato a DB PERSONAS per i dati specifici.
    
    Recupera tutte le personas da DB PERSONAS, trova il contenuto collegato in DB CONTENT,
    e genera le pagine Jekyll con i dati combinati.
    """
    log("Inizio generazione PERSONAS...")
    
    filter_ai = {
        "filter": {
            "and": [
                {"property": "Section", "select": {"equals": "OB-AI"}},
                {"property": "Status", "select": {"equals": "Published"}}
            ]
        }
    }
    
    ai_items = get_notion_data(DB_CONTENT_ID, filter_ai)
    
    if not ai_items:
        log("Nessuna persona OB-AI trovata", "WARN")
        return
    
    personas_count = 0
    
    for item in ai_items:
        props = item["properties"]
        
        # Dati da DB CONTENT
        title = get_property_value(props.get("Title"))
        slug = get_property_value(props.get("Slug"))
        date_str = get_property_value(props.get("Date"))
        description = get_property_value(props.get("Description")) or ""
        keywords = get_property_value(props.get("Keywords")) or ""
        tags = get_property_value(props.get("Tags")) or []
        
        if not slug:
            log(f"Slug mancante per: {title}", "WARN")
            continue
        
        # Segui relation a DB PERSONAS
        personas_relation = get_property_value(props.get("DB PERSONAS"))
        
        if not personas_relation:
            log(f"Nessuna relation a DB PERSONAS per: {title}", "WARN")
            continue
        
        persona_id = personas_relation[0]
        
        # Fetch dati da DB PERSONAS
        persona_data = get_page_by_id(persona_id)
        if not persona_data:
            log(f"Errore fetch persona {persona_id}", "ERROR")
            continue
            
        persona_props = persona_data.get("properties", {})
        
        nome = get_property_value(persona_props.get("Nome"))
        profilo = get_property_value(persona_props.get("Profilo")) or ""
        epoca = get_property_value(persona_props.get("Epoca")) or ""
        stile = get_property_value(persona_props.get("Stile")) or ""
        avatar = get_property_value(persona_props.get("Avatar Emoji")) or "🤖"
        
        # Fetch BODY dalla pagina Notion di DB PERSONAS
        body_content = get_page_blocks(persona_id)
        
        # Se il body è vuoto, prova a recuperare dalla pagina DB CONTENT invece
        if not body_content or body_content.strip() == "":
            log(f"WARN: Body vuoto da DB PERSONAS per {title}, provo DB CONTENT...", "WARN")
            content_page_id = item.get("id")
            body_content = get_page_blocks(content_page_id)
        
        # Pulisci il body content
        body_content = clean_markdown_content(body_content)
        
        # Genera frontmatter usando create_frontmatter()
        fm_props = {
            "title": title,
            "slug": slug,
            "date": date_str,
            "section": "OB-AI",
            "description": description,
            "keywords": keywords,
            "tags": tags
        }
        
        frontmatter = create_frontmatter(fm_props, "ob_ai")
        
        # Aggiungi campi specifici persona dopo il layout (non gestiti da create_frontmatter)
        # Inserisci dopo layout: "ob_ai"
        persona_fields = f'nome: "{nome}"\nprofilo: "{profilo}"\nepoca: "{epoca}"\nstyle: "{stile}"\navatar: "{avatar}"\n'
        frontmatter = frontmatter.replace('layout: "ob_ai"\n', f'layout: "ob_ai"\n{persona_fields}')
        
        # Path file - normalizza slug per assicurarsi che .md venga aggiunto
        safe_slug = normalize_slug(slug)
        filepath = os.path.join("ob-ai", f"{safe_slug}.md")
        
        # Scrivi file
        full_content = frontmatter + body_content
        if write_jekyll_file(filepath, full_content):
            personas_count += 1
    
    log(f"--- PERSONAS: Generati {personas_count} file. ---")

# ============================================================================
# 6. TAG PAGES GENERATION
# ============================================================================

def get_all_tags_from_files() -> set:
    """
    Scansiona tutti i file .md generati e raccoglie tutti i tag unici.
    
    Cerca in: ob-session, ob-ai, ob-progetti, ob-archives
    
    Returns:
        Set di tag unici trovati (set di stringhe)
    """
    tags_set = set()
    md_files = []
    
    # Cerca in tutte le cartelle di contenuto
    content_dirs = ["ob-session", "ob-ai", "ob-progetti", "ob-archives"]
    
    for dir_name in content_dirs:
        if os.path.exists(dir_name):
            for root, dirs, files in os.walk(dir_name):
                for file in files:
                    if file.endswith(".md"):
                        md_files.append(os.path.join(root, file))
    
    # Leggi ogni file e estrai tag dal frontmatter
    for filepath in md_files:
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
                
                # Estrai frontmatter
                if content.startswith("---"):
                    parts = content.split("---", 2)
                    if len(parts) >= 3:
                        frontmatter = parts[1]
                        # Estrai tag usando funzione comune
                        file_tags = extract_tags_from_frontmatter(frontmatter)
                        tags_set.update(file_tags)
                                
        except Exception as e:
            log(f"Errore lettura {filepath}: {str(e)}", "WARN")
    
    return tags_set

def extract_tags_from_frontmatter(frontmatter: str) -> List[str]:
    """
    Estrae tutti i tag da un frontmatter YAML.
    
    Supporta formati:
    - tags: ["tag1", "tag2"]
    - tags: tag1, tag2
    - tags: "tag1, tag2"
    
    Args:
        frontmatter: Stringa frontmatter YAML (senza i separatori ---)
        
    Returns:
        Lista di tag estratti (lista di stringhe)
    """
    tags_set = set()
    in_tags_section = False
    
    for line in frontmatter.split("\n"):
        line_stripped = line.strip()
        
        # Inizio sezione tags
        if line_stripped.startswith("tags:"):
            in_tags_section = True
            # Gestisci formato inline: tags: ['tag1', 'tag2']
            if "[" in line:
                import re
                tags_match = re.search(r'\[(.*?)\]', line)
                if tags_match:
                    tags_str = tags_match.group(1)
                    for tag in tags_str.split(","):
                        tag = tag.strip().strip('"').strip("'")
                        if tag:
                            tags_set.add(tag)
                in_tags_section = False
            continue
        
        # Se siamo nella sezione tags, processa le righe
        if in_tags_section:
            # Fine sezione tags (nuova chiave o fine frontmatter)
            if line_stripped and not line_stripped.startswith("- ") and ":" in line_stripped and not line_stripped.startswith("#"):
                in_tags_section = False
                continue
            
            # Tag in formato lista YAML: - Tag Name
            if line_stripped.startswith("- "):
                tag = line_stripped[2:].strip().strip('"').strip("'")
                if tag:
                    tags_set.add(tag)
            # Se la riga è vuota o solo spazi, continua (potrebbe essere parte della lista)
            elif not line_stripped:
                continue
            # Altrimenti, fine sezione tags
            else:
                in_tags_section = False
    
    return tags_set

def generate_tag_slug(tag: str) -> str:
    """Converte un tag in slug per URL."""
    return tag.lower().replace(" ", "-").replace("_", "-")

def generate_tag_pages() -> None:
    """
    Genera pagine tag per tutti i tag trovati nei file esistenti.
    
    Crea file in tags/tag-slug.md con layout ob_tag.
    Ogni pagina tag mostra tutti i contenuti con quel tag.
    """
    log("Inizio generazione TAG PAGES...")
    
    # Crea directory tags se non esiste
    tags_dir = "tags"
    if not os.path.exists(tags_dir):
        os.makedirs(tags_dir)
        log(f"Creata directory {tags_dir}")
    
    # Raccogli tutti i tag
    all_tags = get_all_tags_from_files()
    
    if not all_tags:
        log("Nessun tag trovato nei file", "WARN")
        return
    
    log(f"Trovati {len(all_tags)} tag unici")
    
    generated_count = 0
    
    for tag in all_tags:
        tag_slug = generate_tag_slug(tag)
        filepath = os.path.join(tags_dir, f"{tag_slug}.md")
        
        # Frontmatter per pagina tag
        # Nota: permalink senza baseurl, Jekyll lo aggiunge automaticamente con relative_url
        frontmatter = f"""---
layout: ob_tag
tag_name: "{tag}"
title: "Tag: {tag}"
permalink: /tags/{tag_slug}/
description: "Tutti i contenuti con tag '{tag}'"
---

"""
        
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(frontmatter)
            """
            log(f"✅ [OK] Tag page: {tag} → {filepath}", "INFO")
            """
            generated_count += 1
        except Exception as e:
            log(f"ERROR writing {filepath}: {str(e)}", "ERROR")
    
    log(f"--- TAG PAGES: Generati {generated_count} file. ---")

def generate_top_tags_data() -> None:
    """
    Genera file _data/top_tags.yml con i 5 tag più popolari.
    
    Questo file viene letto da Jekyll per mostrare i top tag nella homepage.
    Conta quante volte ogni tag appare nei contenuti e ordina per popolarità.
    """
    log("Inizio generazione TOP TAGS data...")
    
    # Crea directory _data se non esiste
    data_dir = "_data"
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        log(f"Creata directory {data_dir}")
    
    # Raccogli tutti i tag
    all_tags = get_all_tags_from_files()
    
    if not all_tags:
        log("Nessun tag trovato, creo file vuoto", "WARN")
        top_tags = []
    else:
        # Conta occorrenze di ogni tag
        tag_counts = {}
        md_files = []
        
        # Cerca in tutte le cartelle di contenuto
        content_dirs = ["ob-session", "ob-ai", "ob-progetti", "ob-archives"]
        
        for dir_name in content_dirs:
            if os.path.exists(dir_name):
                for root, dirs, files in os.walk(dir_name):
                    for file in files:
                        if file.endswith(".md"):
                            md_files.append(os.path.join(root, file))
        
        # Conta occorrenze
        for filepath in md_files:
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                    
                    if content.startswith("---"):
                        parts = content.split("---", 2)
                        if len(parts) >= 3:
                            frontmatter = parts[1]
                            # Estrai tag usando funzione comune
                            file_tags = extract_tags_from_frontmatter(frontmatter)
                            # Conta occorrenze
                            for tag in file_tags:
                                tag_counts[tag] = tag_counts.get(tag, 0) + 1
            except Exception as e:
                log(f"Errore lettura {filepath}: {str(e)}", "WARN")
        
        # Ordina per count e prendi top 5
        sorted_tags = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)
        top_5 = sorted_tags[:5]
        
        # Crea lista per YAML con slug
        top_tags = [{"name": tag, "count": count, "slug": generate_tag_slug(tag)} for tag, count in top_5]
        
        tag_list = ', '.join([f"{t['name']} ({t['count']})" for t in top_tags])
        log(f"Top 5 tag: {tag_list}")
    
    # Scrivi file YAML
    filepath = os.path.join(data_dir, "top_tags.yml")
    try:
        import yaml
        with open(filepath, "w", encoding="utf-8") as f:
            yaml.dump(top_tags, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
        log(f"✅ [OK] Top tags data: {filepath}", "INFO")
    except ImportError:
        # Se PyYAML non è disponibile, scrivi YAML manualmente
        with open(filepath, "w", encoding="utf-8") as f:
            f.write("# Top 5 most popular tags\n")
            f.write("# Generated automatically by notion_to_jekyll_builder.py\n\n")
            for i, tag_data in enumerate(top_tags, 1):
                f.write(f"- name: \"{tag_data['name']}\"\n")
                f.write(f"  count: {tag_data['count']}\n")
                f.write(f"  slug: \"{generate_tag_slug(tag_data['name'])}\"\n")
        log(f"✅ [OK] Top tags data (manual YAML): {filepath}", "INFO")
    except Exception as e:
        log(f"ERROR writing {filepath}: {str(e)}", "ERROR")

def cleanup_orphan_tag_pages() -> None:
    """
    Rimuove pagine tag che non hanno più contenuti associati.
    
    Utile dopo aver rimosso tag da alcuni contenuti.
    Scansiona tags/*.md e rimuove quelli senza contenuti associati.
    """
    log("Inizio cleanup TAG PAGES orfane...")
    
    tags_dir = "tags"
    if not os.path.exists(tags_dir):
        return
    
    # Raccogli tutti i tag attualmente usati
    active_tags = get_all_tags_from_files()
    active_tag_slugs = {generate_tag_slug(tag) for tag in active_tags}
    
    # Controlla ogni file tag
    removed_count = 0
    for filename in os.listdir(tags_dir):
        if filename.endswith(".md"):
            tag_slug = filename[:-3]  # Rimuovi .md
            
            # Verifica se il tag è ancora attivo
            if tag_slug not in active_tag_slugs:
                filepath = os.path.join(tags_dir, filename)
                try:
                    os.remove(filepath)
                    log(f"🗑️  Rimosso tag page orfano: {tag_slug}", "INFO")
                    removed_count += 1
                except Exception as e:
                    log(f"ERROR rimozione {filepath}: {str(e)}", "ERROR")
    
    if removed_count > 0:
        log(f"--- CLEANUP: Rimosse {removed_count} pagine tag orfane. ---")
    else:
        log("--- CLEANUP: Nessuna pagina tag orfana trovata. ---")

# ============================================================================
# 8. PROJECT PROCESSING
# ============================================================================

def process_projects() -> None:
    """
    Processa items da DB_PROJECT e genera pagine progetti.
    
    Supporta relazioni a DB_CONTENT, AI_MODELS, PERSONAS.
    Genera pagine per progetti principali e loro subsections (Council, Metabolism, Evolution).
    """
    log("Inizio generazione PROGETTI...")
    
    if not DB_PROJECT_ID or DB_PROJECT_ID == "TBD":
        log("DB_PROJECT_ID non configurato, skip progetti", "WARN")
        return
    
    filter_ready = {
        "filter": {
            "property": "Status",
            "select": {
                "equals": "Ready for CONTENT"
            }
        }
    }
    
    project_items = get_notion_data(DB_PROJECT_ID, filter_ready)
    log(f"Trovati {len(project_items)} progetti da pubblicare.")
    
    generated_count = 0
    
    for item in project_items:
        props_raw = item.get("properties", {})
        
        # 1. Estrai metadati base da DB_PROJECT
        name = get_property_value(props_raw.get("Name"))
        date = get_property_value(props_raw.get("Date"))
        subsection = get_property_value(props_raw.get("Subsection"))
        use_supabase = props_raw.get("Use Supabase Data", {}).get("checkbox", False)
        supabase_table = get_property_value(props_raw.get("Supabase Table"))
        
        # 2. Segui relation CONTENT Item
        content_relation_ids = get_property_value(props_raw.get("CONTENT Item"))
        
        if not content_relation_ids:
            log(f"SKIP [NO CONTENT]: {name}", "WARN")
            continue
        
        content_id = content_relation_ids[0]
        content_page = get_page_by_id(content_id)
        
        if not content_page:
            log(f"ERROR fetching content page for: {name}", "ERROR")
            continue
        
        content_props = content_page.get("properties", {})
        
        # 3. Estrai dati da DB_CONTENT (ora include anche Internal Section, Project Status, Show Footer, Footer Text)
        title = get_property_value(content_props.get("Title"))
        slug = get_property_value(content_props.get("Slug"))
        section = get_property_value(content_props.get("Section"))
        layout_notion = get_property_value(content_props.get("Layout"))
        description = get_property_value(content_props.get("Description"))
        keywords = get_property_value(content_props.get("Keywords"))
        tags = get_property_value(content_props.get("Tags"))
        # Permalink viene generato automaticamente, non letto da Notion
        permalink = None
        
        # Campi spostati da DB_PROJECT a DB_CONTENT
        internal_section = get_property_value(content_props.get("Internal Section"))
        project_status = get_property_value(content_props.get("Project Status"))
        show_footer = get_property_value(content_props.get("Show Footer"))
        footer_text = get_property_value(content_props.get("Footer Text"))
        
        # Validazione campi obbligatori
        if not all([slug, date, layout_notion, section]):
            missing = []
            if not slug: missing.append("Slug")
            if not date: missing.append("Date")
            if not layout_notion: missing.append("Layout")
            if not section: missing.append("Section")
            log(f"SKIP [MISSING FIELDS]: {name} - Mancanti: {', '.join(missing)}", "WARN")
            continue
        
        # 4. Recupero Body Content
        # Per progetti, il body è nella pagina DB_CONTENT direttamente
        body_content = get_page_blocks(content_id)
        
        if not body_content:
            log(f"SKIP [NO BODY]: {name}", "WARN")
            continue
        
        # 5. Segui relations AI Participants
        ai_models = []
        ai_participant_ids = get_property_value(props_raw.get("AI Participants"))
        if ai_participant_ids:
            for ai_id in ai_participant_ids:
                ai_page = get_page_by_id(ai_id)
                if ai_page:
                    ai_name = get_property_value(ai_page['properties'].get('Name'))
                    if ai_name:
                        ai_models.append(ai_name)
        
        # 6. Segui relations DB PERSONAS
        personas = []
        persona_ids = get_property_value(props_raw.get("DB PERSONAS"))
        if persona_ids:
            for p_id in persona_ids:
                p_page = get_page_by_id(p_id)
                if p_page:
                    p_name = get_property_value(p_page['properties'].get('Nome'))
                    if p_name:
                        personas.append(p_name)
        
        # 7. Genera permalink automaticamente
        permalink = generate_permalink(section, subsection, internal_section, slug)
        
        # 8. Genera percorso file
        jekyll_layout = get_jekyll_layout(layout_notion, section, slug)
        
        # Build path usando generate_build_path per consistenza
        file_path = generate_build_path(section, slug, layout_notion, subsection, internal_section)
        
        # 9. Valida percorso
        try:
            validate_build_path(file_path)
        except ValueError:
            continue
        
        # 10. Crea frontmatter con tutti i campi
        fm_props = {
            "title": title,
            "slug": slug,
            "date": date,
            "section": section,
            "subsection": subsection,
            "description": description,
            "keywords": keywords,
            "tags": tags,
            "permalink": permalink,
            "project_status": project_status,
            "show_footer": show_footer,
            "footer_text": footer_text,
            "use_supabase_data": use_supabase,
            "supabase_table": supabase_table,
            "ai_models": ai_models,
            "personas": personas
        }
        
        # Pulisci il body content
        body_content = clean_markdown_content(body_content)
        
        full_content = create_frontmatter(fm_props, jekyll_layout) + body_content
        
        # 11. Scrivi file
        if write_jekyll_file(file_path, full_content):
            generated_count += 1
    
    log(f"--- PROGETTI: Generati {generated_count} file. ---")

# ============================================================================
# 9. MAIN ENTRY POINT
# ============================================================================

def main() -> None:
    """Entry point principale del generatore."""
    log("Avvio GENERATORE Jekyll v3.0 (Simplified Layout)...")
    
    filter_published = {
        "filter": {
            "property": "Status",
            "select": {
                "equals": "Published"
            }
        }
    }
    
    content_items = get_notion_data(DB_CONTENT_ID, filter_published)
    log(f"Trovati {len(content_items)} contenuti da pubblicare.")
    
    generated_count = 0
    
    for item in content_items:
        # Estrai infra_id se presente per aggiornare status
        props_raw = item.get("properties", {})
        blog_relation_ids = get_property_value(props_raw.get("Blog"))
        infra_id_to_update = blog_relation_ids[0] if blog_relation_ids else None
        
        if process_content_item(item, infra_id_to_update):
            generated_count += 1

    log(f"--- COMPLETATO! Generati {generated_count} file. ---")
    
    # Processa anche le personas
    process_personas()
    
    # Processa progetti da DB_PROJECT
    process_projects()
    
    # Genera pagine tag
    generate_tag_pages()
    
    # Genera top tags data per homepage
    generate_top_tags_data()
    
    # Cleanup tag orfani (opzionale, commenta se non vuoi rimozione automatica)
    # cleanup_orphan_tag_pages()

if __name__ == "__main__":
    main()
