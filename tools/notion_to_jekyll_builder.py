"""
Notion to Jekyll Builder
Converte contenuti da Notion a file Markdown per Jekyll
"""

import requests
import os
import datetime
from notion_config import NOTION_API_KEY, DB_CONTENT_ID, DB_PERSONAS_ID, DB_PROJECT_ID

# ============================================================================
# 1. CONFIGURAZIONE
# ============================================================================

OUTPUT_DIR = "."

LAYOUT_MAP = {
    "session": "ob_session",
    "document": "ob_document",
    "landing": "ob_landing",
    "ai": "ob_ai",
    "musica": "ob_musicaAI",
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

def log(message, level="INFO"):
    """Logging con timestamp."""
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] [{level}] {message}")

# ============================================================================
# 3. NOTION API UTILITIES
# ============================================================================

def get_notion_data(database_id, filter_body=None):
    """
    Query un database Notion con paginazione completa.
    
    Args:
        database_id: ID del database Notion
        filter_body: Filtro opzionale per la query
        
    Returns:
        Lista di risultati dalla query
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

def get_page_by_id(page_id):
    """
    Recupera una pagina Notion per ID.
    
    Args:
        page_id: ID della pagina Notion
        
    Returns:
        Dati della pagina o None se errore
    """
    url = f"https://api.notion.com/v1/pages/{page_id}"
    response = requests.get(url, headers=NOTION_HEADERS)
    if response.status_code == 200:
        return response.json()
    return None

def get_property_value(prop):
    """
    Estrae il valore 'pulito' da un oggetto proprietà Notion.
    
    Gestisce: title, rich_text, select, multi_select, date, relation, checkbox
    
    Args:
        prop: Oggetto proprietà Notion
        
    Returns:
        Valore estratto o None
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
        return prop.get("select", {}).get("name", "")
    elif prop_type == "multi_select":
        return [tag.get("name") for tag in prop.get("multi_select", [])]
    elif prop_type == "date":
        date_obj = prop.get("date")
        if date_obj:
            return date_obj.get("start") 
        return None
    elif prop_type == "relation":
        return [rel.get("id") for rel in prop.get("relation", [])]
    elif prop_type == "checkbox":
        return prop.get("checkbox", False)
    return None

def update_infra_status(infra_page_id, status, error_log=""):
    """
    Aggiorna lo status di build in Notion.
    
    Args:
        infra_page_id: ID della pagina infra
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

def get_latest_session_id(session_ids):
    """
    Restituisce l'ID della sessione con Date più recente.
    
    Args:
        session_ids: Lista di ID sessione
        
    Returns:
        ID della sessione più recente o None
    """
    if not session_ids:
        return None
    
    if len(session_ids) == 1:
        return session_ids[0]

    log(f"Trovate {len(session_ids)} sessioni collegate. Ricerca più recente...", "DEBUG")
    
    candidates = []
    for sid in session_ids:
        url = f"https://api.notion.com/v1/pages/{sid}"
        response = requests.get(url, headers=NOTION_HEADERS)
        if response.status_code == 200:
            page_data = response.json()
            date_prop = page_data.get("properties", {}).get("Date")
            date_val = get_property_value(date_prop)
            
            if not date_val:
                date_val = page_data.get("created_time")
                
            candidates.append({'id': sid, 'date': date_val})
    
    candidates.sort(key=lambda x: x['date'], reverse=True)
    
    if candidates:
        latest = candidates[0]
        log(f"Sessione più recente selezionata: {latest['id']} (Data: {latest['date']})", "DEBUG")
        return latest['id']
    
    return session_ids[0]

def get_page_blocks(page_id):
    """
    Recupera tutti i blocchi di una pagina Notion e converte in Markdown.
    
    Args:
        page_id: ID della pagina Notion
        
    Returns:
        Contenuto Markdown della pagina
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
    if content_md.startswith("```markdown"):
        content_md = content_md.replace("```markdown\n", "", 1)
    if content_md.endswith("```"):
        content_md = content_md.rstrip("```").rstrip()
    
    return content_md

def extract_ai_metadata(session_page):
    """
    Estrae AI Author e AI Partecipanti da una pagina sessione.
    
    Args:
        session_page: Dati della pagina sessione Notion
        
    Returns:
        Tuple (ai_author, ai_participants)
    """
    ai_author = None
    ai_participants = []
    
    if not session_page:
        return ai_author, ai_participants
    
    session_props = session_page.get('properties', {})
    
    # AI Author (single relation)
    author_ids = get_property_value(session_props.get('AI Author'))
    if author_ids:
        author_page = get_page_by_id(author_ids[0])
        if author_page:
            ai_author = get_property_value(author_page['properties'].get('Nome AI'))
    
    # AI Partecipanti (multi relation)
    participant_ids = get_property_value(session_props.get('AI Partecipanti'))
    if participant_ids:
        for pid in participant_ids:
            p_page = get_page_by_id(pid)
            if p_page:
                p_name = get_property_value(p_page['properties'].get('Nome AI'))
                if p_name:
                    ai_participants.append(p_name)
    
    return ai_author, ai_participants

# ============================================================================
# 5. FILE GENERATION UTILITIES
# ============================================================================

def generate_build_path(section, slug, layout_val, subsection=None):
    """
    Genera il percorso file secondo la Routing Matrix.
    
    Args:
        section: Sezione (OB-Session, OB-AI, etc.)
        slug: Slug del contenuto
        layout_val: Valore layout Notion
        subsection: Sottosezione opzionale
        
    Returns:
        Percorso file completo
    """
    safe_slug = slug.strip().lower().replace(" ", "-")
    
    dir_map = {
        "OB-Session": "ob-session",
        "OB-AI": "ob-ai",
        "OB-Progetti": "ob-progetti",
        "OB-Archives": "ob-archives"
    }
    base_dir = dir_map.get(section, "uncategorized")
    
    sub_path = ""
    
    if subsection and subsection != "Default":
        sub_sub = subsection.lower().replace(" ", "-")
        if "musica" in sub_sub:
            sub_sub = "musica"
        elif "giochi" in sub_sub:
            sub_sub = "giochiAI"
            
        if sub_path == "":
            sub_path = f"{sub_sub}/"
        else:
            sub_path = f"{sub_path}{sub_sub}/"
        
    filename = f"{safe_slug}.md"
    return os.path.join(OUTPUT_DIR, base_dir, sub_path, filename)

def create_frontmatter(props, layout_name):
    """
    Crea il frontmatter YAML per Jekyll.
    
    Args:
        props: Dizionario con le proprietà
        layout_name: Nome del layout Jekyll
        
    Returns:
        Stringa frontmatter YAML
    """
    fm = "---\n"
    fm += f'title: "{props.get("title", "Untitled")}"\n'
    fm += f'slug: "{props.get("slug", "")}"\n'
    fm += f'date: "{props.get("date", "")}"\n'
    fm += f'section: "{props.get("section", "")}"\n'
    
    # Includi subsection solo se non è "Default"
    if props.get("subsection") and props.get("subsection") != "Default":
        fm += f'subsection: "{props.get("subsection")}"\n'
        
    fm += f'layout: "{layout_name}"\n'
    
    if props.get("permalink"):
        fm += f'permalink: {props.get("permalink")}\n'
    
    # Description viene da "Description" in Notion
    if props.get("description"):
        fm += f'description: "{props.get("description")}"\n'
    
    if props.get("keywords"):
        fm += f'keywords: "{props.get("keywords")}"\n'
    
    # Campi SEO aggiuntivi per landing pages
    if props.get("tagline"):
        fm += f'tagline: "{props.get("tagline")}"\n'
    # keywords_seo rimosso (doppione di keywords)
    
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
    
    # Debug per show_footer e footer_text
    show_footer_val = props.get("show_footer")
    if props.get("title") == "OB-Progetti":
        log(f"DEBUG [create_frontmatter] show_footer_val: {show_footer_val} (type: {type(show_footer_val)}, is not None: {show_footer_val is not None})", "DEBUG")
    
    if show_footer_val is not None:
        fm += f'show_footer: {str(show_footer_val).lower()}\n'
    
    footer_text_val = props.get("footer_text")
    if props.get("title") == "OB-Progetti":
        log(f"DEBUG [create_frontmatter] footer_text_val: {footer_text_val} (type: {type(footer_text_val)})", "DEBUG")
    
    if footer_text_val:
        fm += f'footer_text: "{footer_text_val}"\n'
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

def write_jekyll_file(file_path, content, infra_id_to_update=None):
    """
    Scrive un file Jekyll Markdown con gestione errori.
    
    Args:
        file_path: Percorso del file da scrivere
        content: Contenuto completo (frontmatter + body)
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

def validate_build_path(file_path):
    """
    Valida che il percorso non contenga cartelle con underscore.
    
    Args:
        file_path: Percorso da validare
        
    Raises:
        ValueError se il percorso contiene cartelle con underscore
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

def process_content_item(item, infra_id_to_update=None):
    """
    Processa un singolo item da DB CONTENT e genera il file Jekyll.
    
    Args:
        item: Item Notion da DB CONTENT
        infra_id_to_update: ID pagina infra per aggiornare status (opzionale)
        
    Returns:
        True se processato con successo, False altrimenti
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
    permalink = get_property_value(props_raw.get("Permalink"))
    
    # Campi aggiuntivi per landing pages
    tagline = get_property_value(props_raw.get("Tagline"))
    
    # show_footer e footer_text vengono da DB PROJECT tramite relazione
    # Segui relazione a DB PROJECT se presente
    show_footer = None
    footer_text = None
    db_project_ids = get_property_value(props_raw.get("DB PROJECT"))
    
    if db_project_ids:
        # Prendi il primo progetto collegato
        project_id = db_project_ids[0]
        project_page = get_page_by_id(project_id)
        
        if project_page:
            project_props = project_page.get("properties", {})
            # Estrai show_footer e footer_text da DB PROJECT
            show_footer = get_property_value(project_props.get("Show Footer"))
            footer_text = get_property_value(project_props.get("Footer Text"))
            
            # Debug: log campi estratti
            if title == "OB-Progetti":
                log(f"DEBUG [OB-Progetti] Relazione DB PROJECT trovata: {project_id}", "DEBUG")
                log(f"DEBUG [OB-Progetti] show_footer da DB PROJECT: {show_footer}", "DEBUG")
                log(f"DEBUG [OB-Progetti] footer_text da DB PROJECT: {footer_text}", "DEBUG")
    else:
        # Debug: nessuna relazione trovata
        if title == "OB-Progetti":
            log(f"DEBUG [OB-Progetti] Nessuna relazione DB PROJECT trovata", "DEBUG")
    
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
    
    # 4. Estrai AI metadata da sessione (se presente)
    ai_author = None
    ai_participants = []
    session_ids = get_property_value(props_raw.get("DB OB-SESSIONS"))
    
    if session_ids:
        latest_sid = get_latest_session_id(session_ids)
        session_page = get_page_by_id(latest_sid)
        ai_author, ai_participants = extract_ai_metadata(session_page)
    
    # Validazione body content
    if not body_content:
        log(f"SKIP [NO BODY]: {title}", "WARN")
        if infra_id_to_update:
            update_infra_status(infra_id_to_update, "error", "No content found")
        return False

    # 5. Genera percorso file
    jekyll_layout = LAYOUT_MAP.get(layout_notion, "default")
    
    if build_path_override:
        file_path = build_path_override
    else:
        file_path = generate_build_path(section, slug, layout_notion, subsection)

    # 5. Valida percorso
    try:
        validate_build_path(file_path)
    except ValueError:
        if infra_id_to_update:
            update_infra_status(infra_id_to_update, "error", "Invalid build path")
        return False

    # 6. Crea frontmatter e scrivi file
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
        "ai_author": ai_author,
        "ai_participants": ai_participants,
        "tagline": tagline,
        "show_footer": show_footer,
        "footer_text": footer_text
    }
    
    # Debug: verifica valori passati a create_frontmatter
    if title == "OB-Progetti":
        log(f"DEBUG [OB-Progetti] fm_props['show_footer']: {fm_props.get('show_footer')} (type: {type(fm_props.get('show_footer'))})", "DEBUG")
        log(f"DEBUG [OB-Progetti] fm_props['footer_text']: {fm_props.get('footer_text')} (type: {type(fm_props.get('footer_text'))})", "DEBUG")
    
    # Rimuovi eventuale --- iniziale dal body (può essere rimasto da Notion)
    if body_content.strip().startswith("---"):
        body_content = body_content.strip()[3:].lstrip() + "\n"
    
    full_content = create_frontmatter(fm_props, jekyll_layout) + body_content
    
    # Debug: verifica frontmatter generato
    if title == "OB-Progetti":
        frontmatter_only = full_content.split("---\n")[1] if "---\n" in full_content else ""
        if "show_footer" in frontmatter_only:
            log(f"DEBUG [OB-Progetti] ✅ show_footer presente nel frontmatter generato", "DEBUG")
        else:
            log(f"DEBUG [OB-Progetti] ❌ show_footer NON presente nel frontmatter generato", "DEBUG")
        if "footer_text" in frontmatter_only:
            log(f"DEBUG [OB-Progetti] ✅ footer_text presente nel frontmatter generato", "DEBUG")
        else:
            log(f"DEBUG [OB-Progetti] ❌ footer_text NON presente nel frontmatter generato", "DEBUG")
    
    return write_jekyll_file(file_path, full_content, infra_id_to_update)

def process_personas():
    """
    Genera pagine AI personas da DB CONTENT (Section=OB-AI) 
    collegato a DB PERSONAS per i dati specifici.
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
        description = get_property_value(props.get("Meta Description")) or ""
        keywords = get_property_value(props.get("Keywords SEO")) or ""
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
        
        # Genera frontmatter
        frontmatter = f"""---
layout: ob_ai
title: "{title}"
slug: "{slug}"
date: {date_str}
section: "OB-AI"
nome: "{nome}"
profilo: "{profilo}"
epoca: "{epoca}"
style: "{stile}"
avatar: "{avatar}"
description: "{description}"
keywords: "{keywords}"
tags: {tags}
---

"""
        
        # Path file
        filepath = os.path.join("ob-ai", f"{slug}.md")
        
        # Scrivi file
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(frontmatter + body_content)
            log(f"✅ [OK] Persona: {nome} → {filepath}", "INFO")
            personas_count += 1
        except Exception as e:
            log(f"ERROR writing {filepath}: {str(e)}", "ERROR")
    
    log(f"--- PERSONAS: Generati {personas_count} file. ---")

# ============================================================================
# 6. TAG PAGES GENERATION
# ============================================================================

def get_all_tags_from_files():
    """
    Scansiona tutti i file .md generati e raccoglie tutti i tag unici.
    
    Returns:
        set: Set di tag unici trovati
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
                        
                        # Cerca sezione tags nel frontmatter
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
                                if line_stripped and not line_stripped.startswith("- ") and ":" in line_stripped:
                                    in_tags_section = False
                                    continue
                                
                                # Tag in formato lista YAML: - Tag Name
                                if line_stripped.startswith("- "):
                                    tag = line_stripped[2:].strip().strip('"').strip("'")
                                    if tag:
                                        tags_set.add(tag)
                                
        except Exception as e:
            log(f"Errore lettura {filepath}: {str(e)}", "WARN")
    
    return tags_set

def generate_tag_slug(tag):
    """Converte un tag in slug per URL."""
    return tag.lower().replace(" ", "-").replace("_", "-")

def generate_tag_pages():
    """
    Genera pagine tag per tutti i tag trovati nei file esistenti.
    Crea file in tags/tag-slug.md
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

def generate_top_tags_data():
    """
    Genera file _data/top_tags.yml con i 5 tag più popolari.
    Questo file viene letto da Jekyll per mostrare i top tag nella homepage.
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
                            
                            # Cerca sezione tags nel frontmatter
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
                                                    tag_counts[tag] = tag_counts.get(tag, 0) + 1
                                        in_tags_section = False
                                    # Se non c'è array inline, continua a leggere le righe successive
                                    continue
                                
                                # Se siamo nella sezione tags, processa le righe
                                if in_tags_section:
                                    # Fine sezione tags (nuova chiave YAML)
                                    if line_stripped and not line_stripped.startswith("- ") and ":" in line_stripped and not line_stripped.startswith("#"):
                                        in_tags_section = False
                                        continue
                                    
                                    # Tag in formato lista YAML: - Tag Name
                                    if line_stripped.startswith("- "):
                                        tag = line_stripped[2:].strip().strip('"').strip("'")
                                        if tag:
                                            tag_counts[tag] = tag_counts.get(tag, 0) + 1
                                    # Se la riga è vuota o solo spazi, continua (potrebbe essere parte della lista)
                                    elif not line_stripped:
                                        continue
                                    # Altrimenti, fine sezione tags
                                    else:
                                        in_tags_section = False
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

def cleanup_orphan_tag_pages():
    """
    Rimuove pagine tag che non hanno più contenuti associati.
    Utile dopo aver rimosso tag da alcuni contenuti.
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

def process_projects():
    """
    Processa items da DB_PROJECT e genera pagine progetti.
    Supporta relazioni a DB_CONTENT, AI_MODELS, PERSONAS.
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
        
        # 1. Estrai metadati base
        name = get_property_value(props_raw.get("Name"))
        date = get_property_value(props_raw.get("Date"))
        subsection = get_property_value(props_raw.get("Subsection"))
        internal_section = get_property_value(props_raw.get("Internal Section"))
        project_status = get_property_value(props_raw.get("Project Status"))
        show_footer = props_raw.get("Show Footer", {}).get("checkbox", False)
        footer_text = get_property_value(props_raw.get("Footer Text"))
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
        
        # 3. Estrai dati da DB_CONTENT
        title = get_property_value(content_props.get("Title"))
        slug = get_property_value(content_props.get("Slug"))
        section = get_property_value(content_props.get("Section"))
        layout_notion = get_property_value(content_props.get("Layout"))
        description = get_property_value(content_props.get("Description"))
        keywords = get_property_value(content_props.get("Keywords"))
        tags = get_property_value(content_props.get("Tags"))
        permalink = get_property_value(content_props.get("Permalink"))
        
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
        log(f"DEBUG: Tentativo lettura body da content_id: {content_id}", "DEBUG")
        body_content = get_page_blocks(content_id)
        log(f"DEBUG: Body recuperato, lunghezza: {len(body_content) if body_content else 0} caratteri", "DEBUG")
        
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
        
        # 7. Genera percorso file
        jekyll_layout = LAYOUT_MAP.get(layout_notion, "default")
        
        # Build path considerando Internal Section
        if internal_section and internal_section != "Default":
            internal_path = internal_section.lower().replace(" ", "-")
            file_path = os.path.join(OUTPUT_DIR, "ob-progetti", subsection.lower(), internal_path, f"{slug}.md")
        else:
            file_path = os.path.join(OUTPUT_DIR, "ob-progetti", subsection.lower(), f"{slug}.md")
        
        # 8. Valida percorso
        try:
            validate_build_path(file_path)
        except ValueError:
            continue
        
        # 9. Crea frontmatter con tutti i campi
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
        
        # Rimuovi eventuale --- iniziale dal body (può essere rimasto da Notion)
        if body_content.strip().startswith("---"):
            body_content = body_content.strip()[3:].lstrip() + "\n"
        
        full_content = create_frontmatter(fm_props, jekyll_layout) + body_content
        
        # 10. Scrivi file
        if write_jekyll_file(file_path, full_content):
            generated_count += 1
    
    log(f"--- PROGETTI: Generati {generated_count} file. ---")

# ============================================================================
# 9. MAIN ENTRY POINT
# ============================================================================

def main():
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
