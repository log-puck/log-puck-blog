"""
Documentation Processor: Processa documenti da DB_DOCUMENTATION_ID
"""

import os
from typing import Optional, Dict, Any
from ..api import NotionClient, get_property_value
from ..converters import NotionToMarkdownConverter, JekyllBuilder
from ..generators import FileWriter
from ..config import DB_DOCUMENTATION_ID, OUTPUT_DIR
from ..logger import log


class DocumentationProcessor:
    """Processa documenti (archivio) da DB_DOCUMENTATION_ID"""
    
    def __init__(self, client: NotionClient):
        """
        Inizializza il documentation processor.
        
        Args:
            client: NotionClient per chiamate API
        """
        self.client = client
        self.converter = NotionToMarkdownConverter(client)
        self.file_writer = FileWriter(client)
        self.builder = JekyllBuilder()
    
    def process_documentation(self) -> None:
        """
        Processa documenti da DB_DOCUMENTATION_ID e genera pagine Jekyll.
        
        Filtra per Build Status = Done AND Published = checked.
        Genera file con layout ob_document in ob-archives/{slug}.md
        """
        log("Inizio generazione DOCUMENTATION...")
        
        if not DB_DOCUMENTATION_ID or DB_DOCUMENTATION_ID == "TBD":
            log("DB_DOCUMENTATION_ID non configurato, skip Documentation", "WARN")
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
        
        doc_items = self.client.get_database_data(DB_DOCUMENTATION_ID, filter_done)
        log(f"Trovati {len(doc_items)} documenti da pubblicare.")
        
        generated_count = 0
        
        for item in doc_items:
            props_raw = item.get("properties", {})
            page_id = item.get("id")
            
            # 1. Estrai metadati base da DB_DOCUMENTATION
            name = get_property_value(props_raw.get("Name"))
            date = get_property_value(props_raw.get("Date"))
            slug = get_property_value(props_raw.get("Slug"))
            description = get_property_value(props_raw.get("Description"))
            ai_author = get_property_value(props_raw.get("AI Author"))
            document_type = get_property_value(props_raw.get("Document Type"))
            access_level = get_property_value(props_raw.get("Access Level"))
            version = get_property_value(props_raw.get("Version"))
            last_review = get_property_value(props_raw.get("Last Review"))
            ai_reviewer = get_property_value(props_raw.get("AI Reviewer"))
            
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
            section = "OB-Archives"
            permalink = self.builder.generate_permalink(section, None, None, slug)
            
            # 4. Genera percorso file
            layout_notion = "ob_document"  # Layout fisso per Documentation
            file_path = self.builder.generate_build_path(section, slug, layout_notion, None, None)
            
            # 5. Valida percorso
            try:
                FileWriter.validate_build_path(file_path)
            except ValueError as e:
                log(f"SKIP [INVALID PATH]: {name} - {e}", "WARN")
                continue
            
            # 6. Crea frontmatter
            fm_props = {
                "title": name,
                "slug": slug,
                "date": date,
                "section": section,
                "description": description,
                "permalink": permalink,
                "ai_author": ai_author,
                "version": version,
                "next_review": last_review  # next_review nel frontmatter corrisponde a Last Review in Notion
            }
            
            # 7. Genera frontmatter e scrivi file
            jekyll_layout = layout_notion
            full_content = self.builder.create_frontmatter(fm_props, jekyll_layout) + body_content
            
            # 8. Scrivi file
            if self.file_writer.write_jekyll_file(file_path, full_content, page_id):
                generated_count += 1
        
        log(f"--- DOCUMENTATION: Generati {generated_count} file. ---")
