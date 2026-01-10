"""
Configurazione centralizzata per Notion to Jekyll Builder
"""

import os
from typing import Dict, Optional

# ============================================================================
# CARICAMENTO CREDENZIALI
# ============================================================================

def load_config() -> Dict[str, Optional[str]]:
    """
    Carica configurazione da variabili d'ambiente o notion_config.py.
    
    Returns:
        Dict con NOTION_API_KEY, DB_CONTENT_ID, DB_PERSONAS_ID, DB_PROJECT_ID
    """
    NOTION_API_KEY = None
    DB_CONTENT_ID = None
    DB_PERSONAS_ID = None
    DB_PROJECT_ID = None
    
    # Prova a caricare da notion_config.py (per sviluppo locale)
    try:
        import notion_config
        NOTION_API_KEY = getattr(notion_config, 'NOTION_API_KEY', None)
        DB_CONTENT_ID = getattr(notion_config, 'DB_CONTENT_ID', None)
        DB_PERSONAS_ID = getattr(notion_config, 'DB_PERSONAS_ID', None)
        DB_PROJECT_ID = getattr(notion_config, 'DB_PROJECT_ID', None)
    except ImportError:
        pass
    
    # Override con variabili d'ambiente se presenti (priorità alle env vars)
    NOTION_API_KEY = os.getenv("NOTION_TOKEN") or os.getenv("NOTION_API_KEY") or NOTION_API_KEY
    DB_CONTENT_ID = os.getenv("DB_CONTENT_ID") or DB_CONTENT_ID
    DB_PERSONAS_ID = os.getenv("DB_PERSONAS_ID") or DB_PERSONAS_ID
    DB_PROJECT_ID = os.getenv("DB_PROJECT_ID") or DB_PROJECT_ID
    
    # Validazione
    if not NOTION_API_KEY:
        raise ValueError("NOTION_API_KEY o NOTION_TOKEN deve essere impostato")
    if not all([DB_CONTENT_ID, DB_PERSONAS_ID, DB_PROJECT_ID]):
        raise ValueError("DB_CONTENT_ID, DB_PERSONAS_ID e DB_PROJECT_ID devono essere impostati")
    
    return {
        "NOTION_API_KEY": NOTION_API_KEY,
        "DB_CONTENT_ID": DB_CONTENT_ID,
        "DB_PERSONAS_ID": DB_PERSONAS_ID,
        "DB_PROJECT_ID": DB_PROJECT_ID,
    }

# Carica configurazione al caricamento del modulo
_config = load_config()
NOTION_API_KEY = _config["NOTION_API_KEY"]
DB_CONTENT_ID = _config["DB_CONTENT_ID"]
DB_PERSONAS_ID = _config["DB_PERSONAS_ID"]
DB_PROJECT_ID = _config["DB_PROJECT_ID"]

# ============================================================================
# COSTANTI
# ============================================================================

OUTPUT_DIR = "."

NOTION_FIELDS = {
    "title": "Title",
    "slug": "Slug",
    "date": "Date",
    "layout": "Layout",
    "section": "Section",
    "subsection": "Subsection",
    "description": "Description",
    "keywords": "Keywords",
    "tags": "Tags",
    "subtitle": "Subtitle",
    "show_footer": "Show Footer",
    "footer_text": "Footer Text",
    "version": "version",
    "next_review": "next_review",
    "internal_section": "Internal Section",
    "ai_author": "AI Author",
    "ai_participants": "AI Partecipants",
    "project_status": "Project Status"
}

LAYOUT_MAP = {
    "session": "ob_session",
    "document": "ob_document",
    "landing": "ob_landing",
    "ai": "ob_ai",
    "musica": "ob_musica",
    "giochi": "ob_giochiAI",
    "project": "ob_progetti",
    "archive": "ob_archive",
    "tag": "ob_tag"
}

NOTION_HEADERS = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}
