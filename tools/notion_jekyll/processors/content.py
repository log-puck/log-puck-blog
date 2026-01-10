"""
Content Processor: Processa contenuti da DB CONTENT
"""

import os
from typing import Optional, Dict, Any
from ..api import NotionClient, get_property_value
from ..converters import NotionToMarkdownConverter, JekyllBuilder
from ..generators import FileWriter
from ..config import OUTPUT_DIR, NOTION_FIELDS
from ..logger import log


class ContentProcessor:
    """Processa contenuti da DB CONTENT e genera file Jekyll"""
    
    def __init__(self, client: NotionClient):
        """
        Inizializza il content processor.
        
        Args:
            client: NotionClient per chiamate API
        """
        self.client = client
        self.converter = NotionToMarkdownConverter(client)
        self.file_writer = FileWriter(client)
        self.builder = JekyllBuilder()
    
    def process_content_item(self, item: Dict[str, Any], infra_id_to_update: Optional[str] = None) -> bool:
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
        description = get_property_value(props_raw.get("Description"))
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
                self.client.update_page_status(infra_id_to_update, "error", "Missing required fields")
            return False
        
        # 2. Recupero Build Path Override (se presente)
        build_path_override = None
        blog_relation_ids = get_property_value(props_raw.get("Blog"))
        if blog_relation_ids:
            infra_id = blog_relation_ids[0]
            infra_page = self.client.get_page(infra_id)
            if infra_page:
                bp_prop = infra_page.get("properties", {}).get("Build Path")
                if bp_prop:
                    raw_path = get_property_value(bp_prop)
                    if raw_path:
                        if raw_path.endswith(".html"):
                            raw_path = raw_path[:-5] + ".md"
                        build_path_override = os.path.join(OUTPUT_DIR, raw_path)
        
        # 3. Recupero Body Content
        page_id = item.get("id")
        body_content = self.converter.get_page_blocks(page_id)
        
        # 4. Estrai AI metadata direttamente da DB CONTENT
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
                self.client.update_page_status(infra_id_to_update, "error", "No content found")
            return False
        
        # 5. Genera permalink automaticamente (se non c'è build_path_override)
        permalink = None
        if not build_path_override:
            permalink = self.builder.generate_permalink(section, subsection, internal_section, slug)
        
        # 6. Genera percorso file
        jekyll_layout = self.builder.get_jekyll_layout(layout_notion, section, slug)
        
        if build_path_override:
            file_path = build_path_override
        else:
            file_path = self.builder.generate_build_path(section, slug, layout_notion, subsection, internal_section)
        
        # 7. Valida percorso
        try:
            FileWriter.validate_build_path(file_path)
        except ValueError:
            if infra_id_to_update:
                self.client.update_page_status(infra_id_to_update, "error", "Invalid build path")
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
        
        # Pulisci il body content (già fatto in converter.get_page_blocks)
        full_content = self.builder.create_frontmatter(fm_props, jekyll_layout) + body_content
        
        return self.file_writer.write_jekyll_file(file_path, full_content, infra_id_to_update)
