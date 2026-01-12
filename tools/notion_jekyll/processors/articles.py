"""
Articles Processor: Processa articoli da DB_ARTICLES_ID
"""

import os
from typing import Optional, Dict, Any
from ..api import NotionClient, get_property_value
from ..converters import NotionToMarkdownConverter, JekyllBuilder
from ..generators import FileWriter
from ..config import DB_ARTICLES_ID, OUTPUT_DIR
from ..logger import log


class ArticlesProcessor:
    """Processa articoli (sessioni) da DB_ARTICLES_ID"""
    
    def __init__(self, client: NotionClient):
        """
        Inizializza l'articles processor.
        
        Args:
            client: NotionClient per chiamate API
        """
        self.client = client
        self.converter = NotionToMarkdownConverter(client)
        self.file_writer = FileWriter(client)
        self.builder = JekyllBuilder()
    
    def process_articles(self) -> None:
        """
        Processa articoli da DB_ARTICLES_ID e genera pagine Jekyll.
        
        Filtra per Build Status = Done AND Published = checked.
        Genera file con layout ob_session in ob-session/{slug}.md
        """
        log("Inizio generazione ARTICLES...")
        
        if not DB_ARTICLES_ID or DB_ARTICLES_ID == "TBD":
            log("DB_ARTICLES_ID non configurato, skip Articles", "WARN")
            return
        
        # Filtra per Build Status = Done E Published = checked
        filter_done = {
            "filter": {
                "and": [
                    {
                        "property": "Build Status",
                        "status": {
                            "equals": "Done"
                        }
                    },
                    {
                        "property": "Published",
                        "checkbox": {
                            "equals": True
                        }
                    }
                ]
            }
        }
        
        article_items = self.client.get_database_data(DB_ARTICLES_ID, filter_done)
        log(f"Trovati {len(article_items)} articoli da pubblicare.")
        
        generated_count = 0
        
        for item in article_items:
            props_raw = item.get("properties", {})
            page_id = item.get("id")
            
            # 1. Estrai metadati base da DB_ARTICLES
            name = get_property_value(props_raw.get("Name"))
            date = get_property_value(props_raw.get("Date"))
            slug = get_property_value(props_raw.get("Slug"))
            description = get_property_value(props_raw.get("Description"))
            subtitle = get_property_value(props_raw.get("Subtitle"))
            keywords = get_property_value(props_raw.get("Keywords"))
            tags = get_property_value(props_raw.get("Tags"))
            ai_author = get_property_value(props_raw.get("AI Author"))
            ai_participants = get_property_value(props_raw.get("AI Partecipants"))
            
            # Validazione campi obbligatori
            if not all([name, slug, date]):
                missing = []
                if not name: missing.append("Name")
                if not slug: missing.append("Slug")
                if not date: missing.append("Date")
                log(f"SKIP [MISSING FIELDS]: {name or 'Unknown'} - Mancanti: {', '.join(missing)}", "WARN")
                continue
            
            # 2. Recupero Body Content
            body_content = ""
            try:
                body_content = self.converter.get_page_blocks(page_id)
            except Exception as e:
                log(f"WARN: Impossibile recuperare body per {name}: {e}", "WARN")
                body_content = ""
            
            # Validazione body content
            if not body_content or body_content.strip() == "":
                log(f"SKIP [NO BODY]: {name}", "WARN")
                continue
            
            # 3. Genera permalink
            section = "OB-Session"
            permalink = self.builder.generate_permalink(section, None, None, slug)
            
            # 4. Genera percorso file
            layout_notion = "ob_session"  # Layout fisso per Articles
            file_path = self.builder.generate_build_path(section, slug, layout_notion, None, None)
            
            # 5. Valida percorso
            try:
                FileWriter.validate_build_path(file_path)
            except ValueError as e:
                log(f"SKIP [INVALID PATH]: {name} - {e}", "WARN")
                continue
            
            # 6. Normalizza tags e ai_participants (da multi-select a lista)
            tags_list = tags if isinstance(tags, list) else [tags] if tags else []
            ai_participants_list = ai_participants if isinstance(ai_participants, list) else [ai_participants] if ai_participants else []
            
            # 7. Crea frontmatter
            fm_props = {
                "title": name,
                "slug": slug,
                "date": date,
                "section": section,
                "description": description,
                "permalink": permalink,
                "subtitle": subtitle,
                "keywords": keywords,
                "tags": tags_list,
                "ai_author": ai_author,
                "ai_participants": ai_participants_list
            }
            
            # 8. Genera frontmatter e scrivi file
            jekyll_layout = layout_notion
            full_content = self.builder.create_frontmatter(fm_props, jekyll_layout) + body_content
            
            # 9. Scrivi file
            if self.file_writer.write_jekyll_file(file_path, full_content, page_id):
                generated_count += 1
        
        log(f"--- ARTICLES: Generati {generated_count} file. ---")
