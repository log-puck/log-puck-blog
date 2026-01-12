"""
AI Profiles Processor: Processa profili AI da DB_AI_PROFILES_ID
"""

import os
from typing import Optional, Dict, Any
from ..api import NotionClient, get_property_value
from ..converters import NotionToMarkdownConverter, JekyllBuilder
from ..generators import FileWriter
from ..config import DB_AI_PROFILES_ID, OUTPUT_DIR
from ..logger import log


class AIProfilesProcessor:
    """Processa profili AI da DB_AI_PROFILES_ID"""
    
    def __init__(self, client: NotionClient):
        """
        Inizializza l'AI profiles processor.
        
        Args:
            client: NotionClient per chiamate API
        """
        self.client = client
        self.converter = NotionToMarkdownConverter(client)
        self.file_writer = FileWriter(client)
        self.builder = JekyllBuilder()
    
    def process_ai_profiles(self) -> None:
        """
        Processa profili AI da DB_AI_PROFILES_ID e genera pagine Jekyll.
        
        Filtra per Build Status = Done AND Published = checked.
        Genera file con layout ob_ai in ob-ai/{slug}.md
        """
        log("Inizio generazione AI PROFILES...")
        
        if not DB_AI_PROFILES_ID or DB_AI_PROFILES_ID == "TBD":
            log("DB_AI_PROFILES_ID non configurato, skip AI Profiles", "WARN")
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
        
        profile_items = self.client.get_database_data(DB_AI_PROFILES_ID, filter_done)
        log(f"Trovati {len(profile_items)} profili AI da pubblicare.")
        
        generated_count = 0
        
        for item in profile_items:
            props_raw = item.get("properties", {})
            page_id = item.get("id")
            
            # 1. Estrai metadati base da DB_AI_PROFILES
            name = get_property_value(props_raw.get("Name"))
            date = get_property_value(props_raw.get("Date"))
            slug = get_property_value(props_raw.get("Slug"))
            description = get_property_value(props_raw.get("Description"))
            ai_author = get_property_value(props_raw.get("AI Author"))
            ai_profiles = get_property_value(props_raw.get("AI Profiles"))  # select
            epoca = get_property_value(props_raw.get("Epoca"))
            tono = get_property_value(props_raw.get("Tono"))  # multiselect
            stile = get_property_value(props_raw.get("Stile"))
            focus = get_property_value(props_raw.get("Focus"))  # number
            speaking = get_property_value(props_raw.get("Speaking"))  # number
            avatar_emoji = get_property_value(props_raw.get("Avatar Emoji"))
            version = get_property_value(props_raw.get("Version"))
            
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
            section = "OB-AI"
            permalink = self.builder.generate_permalink(section, None, None, slug)
            
            # 4. Genera percorso file
            layout_notion = "ob_ai"
            file_path = self.builder.generate_build_path(section, slug, layout_notion, None, None)
            
            # 5. Valida percorso
            try:
                FileWriter.validate_build_path(file_path)
            except ValueError as e:
                log(f"SKIP [INVALID PATH]: {name} - {e}", "WARN")
                continue
            
            # 6. Crea frontmatter con campi custom per ob_ai
            fm_props = {
                "title": name,
                "slug": slug,
                "date": date,
                "section": section,
                "description": description,
                "permalink": permalink,
                "ai_author": ai_author,
                "version": version,
                # Campi custom per layout ob_ai
                "avatar": avatar_emoji,
                "profilo": ai_profiles,
                "epoca": epoca,
                "style": stile,
                "focus": focus,
                "speaking": speaking,
                "tono": tono  # multiselect -> array
            }
            
            # 7. Genera frontmatter e scrivi file
            jekyll_layout = layout_notion
            full_content = self.builder.create_frontmatter(fm_props, jekyll_layout) + body_content
            
            # 8. Scrivi file
            if self.file_writer.write_jekyll_file(file_path, full_content, page_id):
                generated_count += 1
        
        log(f"--- AI PROFILES: Generati {generated_count} file. ---")
