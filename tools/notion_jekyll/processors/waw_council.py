"""
WAW Council Processor: Processa sessioni WAW Council da WAW_COUNCIL_ID
"""

import os
from typing import Optional, Dict, Any
from ..api import NotionClient, get_property_value
from ..converters import NotionToMarkdownConverter, JekyllBuilder
from ..generators import FileWriter
from ..config import WAW_COUNCIL_ID, OUTPUT_DIR
from ..logger import log


class WAWCouncilProcessor:
    """Processa sessioni WAW Council da WAW_COUNCIL_ID"""
    
    def __init__(self, client: NotionClient):
        """
        Inizializza il WAW Council processor.
        
        Args:
            client: NotionClient per chiamate API
        """
        self.client = client
        self.converter = NotionToMarkdownConverter(client)
        self.file_writer = FileWriter(client)
        self.builder = JekyllBuilder()
    
    def process_waw_council(self) -> None:
        """
        Processa sessioni WAW Council da WAW_COUNCIL_ID e genera pagine Jekyll.
        
        Filtra per Build Status = Done e genera file con layout ob_progetti
        (inizialmente per test, poi si passerà a ob_council).
        """
        log("Inizio generazione WAW COUNCIL...")
        
        if not WAW_COUNCIL_ID or WAW_COUNCIL_ID == "TBD":
            log("WAW_COUNCIL_ID non configurato, skip WAW Council", "WARN")
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
        
        council_items = self.client.get_database_data(WAW_COUNCIL_ID, filter_done)
        log(f"Trovati {len(council_items)} sessioni WAW Council da pubblicare.")
        
        generated_count = 0
        
        for item in council_items:
            props_raw = item.get("properties", {})
            page_id = item.get("id")
            
            # 1. Estrai metadati base da WAW_COUNCIL
            name = get_property_value(props_raw.get("Name"))
            date = get_property_value(props_raw.get("Date"))
            slug = get_property_value(props_raw.get("Slug"))
            description = get_property_value(props_raw.get("Description"))
            
            # Campi WAW specifici
            project_name = get_property_value(props_raw.get("Project Name"))
            tech_stack = get_property_value(props_raw.get("Tech Stack"))
            context = get_property_value(props_raw.get("Context"))
            current_focus = get_property_value(props_raw.get("Current Focus"))
            completed = get_property_value(props_raw.get("Completed"))
            ideas_completed = get_property_value(props_raw.get("Ideas Completed"))
            ideas_voted = get_property_value(props_raw.get("Ideas Voted"))
            ai_participants = get_property_value(props_raw.get("AI Partecipants"))
            winner_idea = get_property_value(props_raw.get("Winner Idea"))
            winner_score = get_property_value(props_raw.get("Winner Score"))
            
            # Validazione campi obbligatori
            if not all([name, slug, date]):
                missing = []
                if not name: missing.append("Name")
                if not slug: missing.append("Slug")
                if not date: missing.append("Date")
                log(f"SKIP [MISSING FIELDS]: {name or 'Unknown'} - Mancanti: {', '.join(missing)}", "WARN")
                continue
            
            # 2. Recupero Body Content (se presente)
            # NOTA: WAW_COUNCIL non ha body nella pagina, ma può avere Markdown (file)
            # Per ora lasciamo body vuoto o proviamo a recuperare dalla pagina
            body_content = ""
            
            # Prova a recuperare blocchi dalla pagina (potrebbe essere vuoto)
            try:
                body_content = self.converter.get_page_blocks(page_id)
            except Exception as e:
                log(f"WARN: Impossibile recuperare body per {name}: {e}", "WARN")
                body_content = ""
            
            # Se body è vuoto, usa descrizione come placeholder
            if not body_content or body_content.strip() == "":
                if description:
                    body_content = f"{description}\n\n"
                else:
                    body_content = ""
            
            # 3. Genera permalink
            section = "OB-Progetti"
            subsection = "wAw"
            internal_section = "Council"
            permalink = self.builder.generate_permalink(section, subsection, internal_section, slug)
            
            # 4. Genera percorso file
            layout_notion = "ob_progetti"  # Layout fisso per test (poi ob_council)
            file_path = self.builder.generate_build_path(section, slug, layout_notion, subsection, internal_section)
            
            # 5. Valida percorso
            try:
                FileWriter.validate_build_path(file_path)
            except ValueError as e:
                log(f"SKIP [INVALID PATH]: {name} - {e}", "WARN")
                continue
            
            # 6. Crea frontmatter per layout ob_progetti
            # NOTA: Per ora usiamo ob_progetti (test), poi si passerà a ob_council quando creato
            # ob_progetti usa solo: title, subtitle, subsection, show_footer, footer_text
            fm_props = {
                "title": name,
                "slug": slug,
                "date": date,
                "section": section,
                "subsection": subsection,
                "description": description,  # Per ob_progetti può essere usato come subtitle
                "permalink": permalink
            }
            
            # 7. Genera frontmatter con create_frontmatter (gestisce tutto automaticamente)
            jekyll_layout = layout_notion
            full_content = self.builder.create_frontmatter(fm_props, jekyll_layout) + body_content
            
            # NOTA: Campi WAW custom (project_name, tech_stack, context, etc.) saranno aggiunti
            # quando creeremo il layout ob_council dedicato. Per ora ob_progetti non li usa.
            
            # 8. Scrivi file
            if self.file_writer.write_jekyll_file(file_path, full_content, page_id):
                generated_count += 1
        
        log(f"--- WAW COUNCIL: Generati {generated_count} file. ---")
