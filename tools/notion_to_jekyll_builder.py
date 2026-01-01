import requests
import os
import json
import datetime
from pathlib import Path

# --- CONFIGURAZIONE ---
NOTION_API_KEY = "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"
DB_CONTENT_ID = "2d46f0146d118046949bf3b441fa2627"
OUTPUT_DIR = "." 

# Mapping Layout Notion -> Layout Jekyll
LAYOUT_MAP = {
    "session": "ob_session",
    "document": "ob_document",
    "landing": "ob_landing",
    "ai": "ob_ai",
    "music": "ob_music",
    "game": "ob_game"
}

headers = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

def log(message, level="INFO"):
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] [{level}] {message}")

def get_notion_data(database_id, filter_body=None):
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

        response = requests.post(url, headers=headers, json=payload)
        if response.status_code != 200:
            log(f"Errore API Notion: {response.text}", "ERROR")
            raise Exception(f"API Error: {response.status_code}")

        data = response.json()
        results.extend(data.get("results", []))
        has_more = data.get("has_more", False)
        start_cursor = data.get("next_cursor", None)
    return results

def get_page_by_id(page_id):
    url = f"https://api.notion.com/v1/pages/{page_id}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    return None

def get_latest_session_id(session_ids):
    """
    Riceve una lista di ID sessione e restituisce l'ID della sessione con Date più recente.
    """
    if not session_ids:
        return None
    
    if len(session_ids) == 1:
        return session_ids[0]

    log(f"Trovate {len(session_ids)} sessioni collegate. Ricerca più recente...", "DEBUG")
    
    candidates = []
    for sid in session_ids:
        url = f"https://api.notion.com/v1/pages/{sid}"
        response = requests.get(url, headers=headers)
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

def update_infra_status(infra_page_id, status, error_log=""):
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

    response = requests.patch(url, headers=headers, json=payload)
    if response.status_code != 200:
        log(f"Errore aggiornamento status infra {infra_page_id}: {response.text}", "WARN")

def get_property_value(prop):
    """Helper per estrarre il valore 'pulito' da un oggetto proprietà Notion."""
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
    
def get_page_blocks(page_id):
    """Recupera i blocchi (contenuto corpo) di una pagina Notion."""
    url = f"https://api.notion.com/v1/blocks/{page_id}/children"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return ""
        
    data = response.json()
    blocks = data.get("results", [])
    content_md = ""
    
    def get_text(prop):
        rich_text_list = prop.get("rich_text", [])
        if rich_text_list:
            return rich_text_list[0].get("plain_text", "")
        return ""
    
    for block in blocks:
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
                
    return content_md

def generate_build_path(section, slug, layout_val, subsection=None):
    """
    Implementa la Routing Matrix.
    """
    safe_slug = slug.strip().lower().replace(" ", "-")
    
    # Mapping Base Directory
    dir_map = {
        "OB-Session": "ob-session",
        "OB-AI": "ob-ai",
        "OB-Progetti": "ob-progetti",
        "OB-Archives": "ob-archives"
    }
    base_dir = dir_map.get(section, "uncategorized")
    
    sub_path = ""
    
    # Logica Layout (sostituisce Type)
    if layout_val == "document":
        sub_path = "docs/"
    elif layout_val == "landing":
        sub_path = "landing/"
    
    # Logica Subsection (per OB-Progetti)
    if subsection and subsection != "Default":
        sub_sub = subsection.lower().replace(" ", "-")
        # Normalizziamo i nomi
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
            
    fm += "---\n"
    return fm

def main():
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
        props_raw = item.get("properties", {})
        
        # 1. Metadati
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
        
        if not all([slug, date, layout_notion, section]):
            log(f"SKIP [MISSING FIELDS]: {title}", "WARN")
            continue

        # 2. Recupero Infra (Blog Relation)
        blog_relation_ids = get_property_value(props_raw.get("Blog"))
        infra_page = None
        build_path_override = None
        infra_id_to_update = None
        
        if blog_relation_ids:
            infra_id = blog_relation_ids[0]
            infra_id_to_update = infra_id
            infra_page = get_page_by_id(infra_id)
            
            if infra_page:
                bp_prop = infra_page.get("properties", {}).get("Build Path")
                if bp_prop:
                    raw_path = get_property_value(bp_prop)
                    if raw_path:
                        if raw_path.endswith(".html"):
                            raw_path = raw_path[:-5] + ".md"
                        build_path_override = os.path.join(OUTPUT_DIR, raw_path)

        # 3. Recupero Body (Con Logica Multi-Sessione)
        session_ids = get_property_value(props_raw.get("DB OB-SESSIONS"))
        
        body_content = ""
        source_name = ""
        
        if session_ids:
            latest_sid = get_latest_session_id(session_ids)
            body_content = get_page_blocks(latest_sid)
            source_name = "OB-SESSION (Latest)"
        else:
            raw_content = get_property_value(props_raw.get("Content"))
            if raw_content:
                body_content = raw_content
                source_name = "DB CONTENT"
        
        if not body_content:
            err_msg = f"SKIP [NO BODY]: {title}"
            log(err_msg, "WARN")
            if infra_id_to_update:
                update_infra_status(infra_id_to_update, "error", "No content found")
            continue

        # 4. Layout & Path
        jekyll_layout = LAYOUT_MAP.get(layout_notion, "default")
        
        if build_path_override:
            file_path = build_path_override
        else:
            file_path = generate_build_path(section, slug, layout_notion, subsection)

        # 5. Controllo Anti-Underscore
        path_components = os.path.normpath(file_path).split(os.sep)
        folders = path_components[:-1]
        
        if any(folder.startswith("_") for folder in folders):
            error_msg = f"⛔ ERRORE: Build Path '{file_path}' contiene cartella con '_'. Jekyll la ignorerebbe."
            log(error_msg, "ERROR")
            
            if infra_id_to_update:
                update_infra_status(infra_id_to_update, "error", "Folder starts with _")
            
            raise ValueError(error_msg)

        # 6. Build File
        fm_props = {
            "title": title,
            "slug": slug,
            "date": date,
            "section": section,
            "subsection": subsection,
            "meta_title": meta_title,
            "meta_description": meta_desc,
            "keywords_seo": keys_seo,
            "tags": tags
        }
        
        full_content = create_frontmatter(fm_props, jekyll_layout) + body_content
        
        try:
            target_dir = os.path.dirname(file_path)
            if not os.path.exists(target_dir):
                os.makedirs(target_dir)
                
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(full_content)
            
            print(f"✅ [OK] Generato: {file_path}")
            
            generated_count += 1
            
            if infra_id_to_update:
                update_infra_status(infra_id_to_update, "ok")
                
        except Exception as e:
            log(f"ERROR writing {file_path}: {str(e)}", "ERROR")
            if infra_id_to_update:
                update_infra_status(infra_id_to_update, "error", str(e))

    log(f"--- COMPLETATO! Generati {generated_count} file. ---")

if __name__ == "__main__":
    main()