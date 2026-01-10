"""
Personas Processor: Processa AI personas da DB PERSONAS
"""

import os
from ..api import NotionClient, get_property_value
from ..converters import NotionToMarkdownConverter, JekyllBuilder
from ..generators import FileWriter
from ..config import DB_CONTENT_ID, DB_PERSONAS_ID
from ..logger import log


class PersonasProcessor:
    """Processa AI personas da DB PERSONAS"""
    
    def __init__(self, client: NotionClient):
        """
        Inizializza il personas processor.
        
        Args:
            client: NotionClient per chiamate API
        """
        self.client = client
        self.converter = NotionToMarkdownConverter(client)
        self.file_writer = FileWriter(client)
        self.builder = JekyllBuilder()
    
    def process_personas(self) -> None:
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
        
        ai_items = self.client.get_database_data(DB_CONTENT_ID, filter_ai)
        
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
            persona_data = self.client.get_page(persona_id)
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
            body_content = self.converter.get_page_blocks(persona_id)
            
            # Se il body è vuoto, prova a recuperare dalla pagina DB CONTENT invece
            if not body_content or body_content.strip() == "":
                log(f"WARN: Body vuoto da DB PERSONAS per {title}, provo DB CONTENT...", "WARN")
                content_page_id = item.get("id")
                body_content = self.converter.get_page_blocks(content_page_id)
            
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
            
            frontmatter = self.builder.create_frontmatter(fm_props, "ob_ai")
            
            # Aggiungi campi specifici persona dopo il layout (non gestiti da create_frontmatter)
            # Inserisci dopo layout: "ob_ai"
            persona_fields = f'nome: "{nome}"\nprofilo: "{profilo}"\nepoca: "{epoca}"\nstyle: "{stile}"\navatar: "{avatar}"\n'
            frontmatter = frontmatter.replace('layout: "ob_ai"\n', f'layout: "ob_ai"\n{persona_fields}')
            
            # Path file - normalizza slug per assicurarsi che .md venga aggiunto
            safe_slug = self.builder.normalize_slug(slug)
            filepath = os.path.join("ob-ai", f"{safe_slug}.md")
            
            # Scrivi file
            full_content = frontmatter + body_content
            if self.file_writer.write_jekyll_file(filepath, full_content):
                personas_count += 1
        
        log(f"--- PERSONAS: Generati {personas_count} file. ---")
