"""
Orchestrator: Orchestrazione principale per il processo di generazione Jekyll
"""

from .api import NotionClient, get_property_value
# TODO: Processor vecchi da sostituire nella migrazione
# from .processors import ContentProcessor, PersonasProcessor, ProjectsProcessor
from .processors import ArticlesProcessor, DocumentationProcessor, AIProfilesProcessor, WAWCouncilProcessor
from .generators import TagGenerator
# from .config import DB_CONTENT_ID, DB_PROJECT_ID  # Vecchi DB IDs, da rimuovere
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
        # TODO: Processor vecchi da sostituire nella migrazione
        # self.content_processor = ContentProcessor(client)
        # self.personas_processor = PersonasProcessor(client)
        # self.projects_processor = ProjectsProcessor(client)
        self.articles_processor = ArticlesProcessor(client)
        self.documentation_processor = DocumentationProcessor(client)
        self.ai_profiles_processor = AIProfilesProcessor(client)
        self.waw_council_processor = WAWCouncilProcessor(client)
        self.tag_generator = TagGenerator()
    
    def run(self) -> None:
        """
        Esegue il processo completo di generazione:
        1. Processa contenuti da DB CONTENT
        2. Processa personas da DB PERSONAS
        3. Processa progetti da DB PROJECT
        4. Processa WAW Council da WAW_COUNCIL_ID
        5. Genera pagine tag
        6. Genera top tags data
        """
        log("Avvio GENERATORE Jekyll v4.0 (Modulare) - TEST ARTICLES + DOCUMENTATION + AI PROFILES + WAW COUNCIL...")
        
        # TODO: Processor vecchi commentati per migrazione
        # Processa progetti (DA SOSTITUIRE con nuovi processor)
        
        # 1. Processa Articles (ATTIVO per test)
        self.articles_processor.process_articles()
        
        # 2. Processa Documentation (ATTIVO per test)
        self.documentation_processor.process_documentation()
        
        # 3. Processa AI Profiles (ATTIVO per test)
        self.ai_profiles_processor.process_ai_profiles()
        
        # 4. Processa WAW Council (ATTIVO per test)
        self.waw_council_processor.process_waw_council()
        
        # 5. Genera pagine tag
        self.tag_generator.generate_tag_pages()
        
        # 6. Genera top tags data
        self.tag_generator.generate_top_tags_data()
        
        # 7. Cleanup tag orfani (rimuove tag non più utilizzati)
        self.tag_generator.cleanup_orphan_tag_pages()


def main() -> None:
    """Entry point principale modulare"""
    # Crea client Notion
    client = NotionClient()
    
    # Crea orchestrator
    orchestrator = JekyllOrchestrator(client)
    
    # Esegui processo completo
    orchestrator.run()
