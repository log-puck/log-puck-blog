"""
Processors: Processori contenuti Notion
"""

# TODO: Processor vecchi commentati per migrazione (usano vecchi DB IDs)
# from .content import ContentProcessor
# from .personas import PersonasProcessor
# from .projects import ProjectsProcessor
from .articles import ArticlesProcessor
from .documentation import DocumentationProcessor
from .ai_profiles import AIProfilesProcessor
from .waw_council import WAWCouncilProcessor

__all__ = ["ArticlesProcessor", "DocumentationProcessor", "AIProfilesProcessor", "WAWCouncilProcessor"]  # TODO: Aggiungere altri nuovi processor quando creati
