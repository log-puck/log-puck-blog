"""
Orchestrator: Orchestrazione principale per il processo di generazione Jekyll
"""

from .api import NotionClient, get_property_value
from .processors import ArticlesProcessor, DocumentationProcessor, AIProfilesProcessor, WAWCouncilProcessor, TimelineProcessor
from .generators import TagGenerator
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
        self.articles_processor = ArticlesProcessor(client)
        self.documentation_processor = DocumentationProcessor(client)
        self.ai_profiles_processor = AIProfilesProcessor(client)
        self.waw_council_processor = WAWCouncilProcessor(client)
        self.timeline_processor = TimelineProcessor(client)
        self.tag_generator = TagGenerator()
    
    def run(self) -> None:
        """
        Esegue il processo completo di generazione:
        1. Processa Articles da DB_ARTICLES_ID
        2. Processa Documentation da DB_DOCUMENTATION_ID
        3. Processa AI Profiles da DB_AI_PROFILES_ID
        4. Processa WAW Council da WAW_COUNCIL_ID
        5. Genera pagine tag
        6. Genera top tags data
        7. Cleanup tag orfani
        """
        log("Avvio GENERATORE Jekyll v4.0 (Modulare) - ARTICLES + DOCUMENTATION + AI PROFILES + WAW COUNCIL + TIMELINE...")
        
        # 1. Processa Articles
        self.articles_processor.process_articles()
        
        # 2. Processa Documentation
        self.documentation_processor.process_documentation()
        
        # 3. Processa AI Profiles
        self.ai_profiles_processor.process_ai_profiles()
        
        # 4. Processa WAW Council
        self.waw_council_processor.process_waw_council()
        
        # 5. Processa Timeline
        self.timeline_processor.process_timeline()
        
        # 6. Genera pagine tag
        self.tag_generator.generate_tag_pages()
        
        # 6. Genera top tags data
        self.tag_generator.generate_top_tags_data()
        
        # 7. Cleanup tag orfani
        self.tag_generator.cleanup_orphan_tag_pages()


def main() -> None:
    """Entry point principale modulare"""
    # Crea client Notion
    client = NotionClient()
    
    # Crea orchestrator
    orchestrator = JekyllOrchestrator(client)
    
    # Esegui processo completo
    orchestrator.run()
