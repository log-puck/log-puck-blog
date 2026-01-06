"""
Notion to Jekyll Builder
Converte contenuti da Notion a file Markdown per Jekyll
"""

import requests
import os
import datetime
from notion_config import NOTION_API_KEY, DB_CONTENT_ID, DB_PERSONAS_ID

# ============================================================================
# 1. CONFIGURAZIONE
# ============================================================================

OUTPUT_DIR = "."

LAYOUT_MAP = {
    "session": "ob_session",
    "document": "ob_document",
    "landing": "ob_landing",
    "ai": "ob_ai",
    "music": "ob_music",
    "game": "ob_game"
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
    
    Gestisce: title, rich_text, select, multi_select, date, relation
    
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
    
    if props.get("subsection"):
        fm += f'subsection: "{props.get("subsection")}"\n'
        
    fm += f'layout: "{layout_name}"\n'
    
    if props.get("meta_title"):
        fm += f'meta_title: "{props.get("meta_title")}"\n'
    if props.get("meta_description"):
        fm += f'meta_description: "{props.get("meta_description")}"\n'
    if props.get("keywords_seo"):
        fm += f'keywords_seo: "{props.get("keywords_seo")}"\n'
    
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
    meta_title = get_property_value(props_raw.get("Meta Title"))
    meta_desc = get_property_value(props_raw.get("Meta Description"))
    keys_seo = get_property_value(props_raw.get("Keywords SEO"))
    tags = get_property_value(props_raw.get("Tags"))
    
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
    session_ids = get_property_value(props_raw.get("DB OB-SESSIONS"))
    body_content = ""
    ai_author = None
    ai_participants = []
    
    if session_ids:
        latest_sid = get_latest_session_id(session_ids)
        body_content = get_page_blocks(latest_sid)
        
        # Estrai AI metadata dalla sessione
        session_page = get_page_by_id(latest_sid)
        ai_author, ai_participants = extract_ai_metadata(session_page)
    else:
        raw_content = get_property_value(props_raw.get("Content"))
        if raw_content:
            body_content = raw_content
        else:
            # Fallback: prova a estrarre da proprietà "Body" con rich_text
            body_rich_text = props_raw.get("Body", {}).get("rich_text", [])
            if body_rich_text:
                body_content = "".join([rt.get("plain_text", "") for rt in body_rich_text])
    
    # Validazione body content
    if not body_content:
        log(f"SKIP [NO BODY]: {title}", "WARN")
        if infra_id_to_update:
            update_infra_status(infra_id_to_update, "error", "No content found")
        return False

    # 4. Genera percorso file
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
        "meta_title": meta_title,
        "meta_description": meta_desc,
        "keywords_seo": keys_seo,
        "tags": tags,
        "ai_author": ai_author,
        "ai_participants": ai_participants
    }
    
    full_content = create_frontmatter(fm_props, jekyll_layout) + body_content
    
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
        meta_title = get_property_value(props.get("Meta Title")) or title
        meta_desc = get_property_value(props.get("Meta Description")) or ""
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
meta_title: "{meta_title}"
meta_description: "{meta_desc}"
keywords_seo: "{keywords}"
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
# 7. MAIN ENTRY POINT
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

if __name__ == "__main__":
    main()
