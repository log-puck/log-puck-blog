"""
Orchestrator: Orchestrazione principale per il processo di generazione Jekyll
"""

from .api import NotionClient, get_property_value
from .processors import ContentProcessor, PersonasProcessor, ProjectsProcessor
from .generators import TagGenerator
from .config import DB_CONTENT_ID, DB_PROJECT_ID
from .logger import log


class JekyllOrchestrator:
    """Orchestratore principale per generazione Jekyll da Notion"""
    
    def __init__(self, client: NotionClient):
        """
        Inizializza l'orchestrator.
        
        Args:
            client: NotionClient per chiamate API
        """
        self.client = client
        self.content_processor = ContentProcessor(client)
        self.personas_processor = PersonasProcessor(client)
        self.projects_processor = ProjectsProcessor(client)
        self.tag_generator = TagGenerator()
    
    def run(self) -> None:
        """
        Esegue il processo completo di generazione:
        1. Processa contenuti da DB CONTENT
        2. Processa personas da DB PERSONAS
        3. Processa progetti da DB PROJECT
        4. Genera pagine tag
        5. Genera top tags data
        """
        log("Avvio GENERATORE Jekyll v4.0 (Modulare)...")
        
        # 1. Processa contenuti da DB CONTENT
        filter_published = {
            "filter": {
                "property": "Status",
                "select": {
                    "equals": "Published"
                }
            }
        }
        
        content_items = self.client.get_database_data(DB_CONTENT_ID, filter_published)
        log(f"Trovati {len(content_items)} contenuti da pubblicare.")
        
        generated_count = 0
        
        for item in content_items:
            # Estrai infra_id se presente per aggiornare status
            props_raw = item.get("properties", {})
            blog_relation_ids = get_property_value(props_raw.get("Blog"))
            infra_id_to_update = blog_relation_ids[0] if blog_relation_ids else None
            
            if self.content_processor.process_content_item(item, infra_id_to_update):
                generated_count += 1
        
        log(f"--- COMPLETATO! Generati {generated_count} file. ---")
        
        # 2. Processa personas
        self.personas_processor.process_personas()
        
        # 3. Processa progetti
        self.projects_processor.process_projects()
        
        # 4. Genera pagine tag
        self.tag_generator.generate_tag_pages()
        
        # 5. Genera top tags data
        self.tag_generator.generate_top_tags_data()
        
        # Cleanup tag orfani (opzionale)
        # self.tag_generator.cleanup_orphan_tag_pages()


def main() -> None:
    """Entry point principale modulare"""
    # Crea client Notion
    client = NotionClient()
    
    # Crea orchestrator
    orchestrator = JekyllOrchestrator(client)
    
    # Esegui processo completo
    orchestrator.run()
