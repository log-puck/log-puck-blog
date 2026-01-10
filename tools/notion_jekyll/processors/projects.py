"""
Projects Processor: Processa progetti da DB_PROJECT
"""

import os
from typing import Optional
from ..api import NotionClient, get_property_value
from ..converters import NotionToMarkdownConverter, JekyllBuilder
from ..generators import FileWriter
from ..config import DB_PROJECT_ID, OUTPUT_DIR
from ..logger import log


class ProjectsProcessor:
    """Processa progetti da DB_PROJECT"""
    
    def __init__(self, client: NotionClient):
        """
        Inizializza il projects processor.
        
        Args:
            client: NotionClient per chiamate API
        """
        self.client = client
        self.converter = NotionToMarkdownConverter(client)
        self.file_writer = FileWriter(client)
        self.builder = JekyllBuilder()
    
    def process_projects(self) -> None:
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
        
        project_items = self.client.get_database_data(DB_PROJECT_ID, filter_ready)
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
            content_page = self.client.get_page(content_id)
            
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
            body_content = self.converter.get_page_blocks(content_id)
            
            if not body_content:
                log(f"SKIP [NO BODY]: {name}", "WARN")
                continue
            
            # 5. Segui relations AI Participants
            ai_models = []
            ai_participant_ids = get_property_value(props_raw.get("AI Participants"))
            if ai_participant_ids:
                for ai_id in ai_participant_ids:
                    ai_page = self.client.get_page(ai_id)
                    if ai_page:
                        ai_name = get_property_value(ai_page['properties'].get('Name'))
                        if ai_name:
                            ai_models.append(ai_name)
            
            # 6. Segui relations DB PERSONAS
            personas = []
            persona_ids = get_property_value(props_raw.get("DB PERSONAS"))
            if persona_ids:
                for p_id in persona_ids:
                    p_page = self.client.get_page(p_id)
                    if p_page:
                        p_name = get_property_value(p_page['properties'].get('Nome'))
                        if p_name:
                            personas.append(p_name)
            
            # 7. Genera permalink automaticamente
            permalink = self.builder.generate_permalink(section, subsection, internal_section, slug)
            
            # 8. Genera percorso file
            jekyll_layout = self.builder.get_jekyll_layout(layout_notion, section, slug)
            
            # Build path usando generate_build_path per consistenza
            file_path = self.builder.generate_build_path(section, slug, layout_notion, subsection, internal_section)
            
            # 9. Valida percorso
            try:
                FileWriter.validate_build_path(file_path)
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
            
            full_content = self.builder.create_frontmatter(fm_props, jekyll_layout) + body_content
            
            # 11. Scrivi file
            if self.file_writer.write_jekyll_file(file_path, full_content):
                generated_count += 1
        
        log(f"--- PROGETTI: Generati {generated_count} file. ---")
