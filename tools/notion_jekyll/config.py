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
        Dict con NOTION_API_KEY e tutti i Database IDs
    """
    NOTION_API_KEY = None
    DB_ARTICLES_ID = None
    DB_DOCUMENTATION_ID = None
    DB_AI_PROFILES_ID = None
    DB_PROJECT_DATA_ID = None
    DB_MUSICA_ID = None
    DB_STUDI_MUSICA_ID = None
    WAW_COUNCIL_ID = None
    
    # Prova a caricare da notion_config.py (per sviluppo locale)
    try:
        import notion_config
        NOTION_API_KEY = getattr(notion_config, 'NOTION_API_KEY', None)
        # Nuovi DB IDs (mappatura dai nomi in notion_config.py)
        DB_ARTICLES_ID = getattr(notion_config, 'ARTICLES_ID', None)
        DB_DOCUMENTATION_ID = getattr(notion_config, 'DOCUMENT_ID', None)  # DOCUMENT_ID in notion_config
        DB_AI_PROFILES_ID = getattr(notion_config, 'AI_PROFILES_ID', None)
        DB_PROJECT_DATA_ID = getattr(notion_config, 'PROJECT_DATA_ID', None)
        DB_MUSICA_ID = getattr(notion_config, 'MUSICA_ID', None)
        DB_STUDI_MUSICA_ID = getattr(notion_config, 'STUDI_MUSICA_ID', None)
        WAW_COUNCIL_ID = getattr(notion_config, 'WAW_COUNCIL_ID', None)
    except ImportError:
        pass
    
    # Override con variabili d'ambiente se presenti (priorità alle env vars)
    NOTION_API_KEY = os.getenv("NOTION_TOKEN") or os.getenv("NOTION_API_KEY") or NOTION_API_KEY
    DB_ARTICLES_ID = os.getenv("DB_ARTICLES_ID") or os.getenv("ARTICLES_ID") or DB_ARTICLES_ID
    DB_DOCUMENTATION_ID = os.getenv("DB_DOCUMENTATION_ID") or os.getenv("DOCUMENT_ID") or DB_DOCUMENTATION_ID
    DB_AI_PROFILES_ID = os.getenv("DB_AI_PROFILES_ID") or os.getenv("AI_PROFILES_ID") or DB_AI_PROFILES_ID
    DB_PROJECT_DATA_ID = os.getenv("DB_PROJECT_DATA_ID") or os.getenv("PROJECT_DATA_ID") or DB_PROJECT_DATA_ID
    DB_MUSICA_ID = os.getenv("DB_MUSICA_ID") or os.getenv("MUSICA_ID") or DB_MUSICA_ID
    DB_STUDI_MUSICA_ID = os.getenv("DB_STUDI_MUSICA_ID") or os.getenv("STUDI_MUSICA_ID") or DB_STUDI_MUSICA_ID
    WAW_COUNCIL_ID = os.getenv("WAW_COUNCIL_ID") or WAW_COUNCIL_ID
    
    # Validazione
    if not NOTION_API_KEY:
        raise ValueError("NOTION_API_KEY o NOTION_TOKEN deve essere impostato")
    
    # Validazione DB IDs obbligatori
    required_dbs = {
        "DB_ARTICLES_ID": DB_ARTICLES_ID,
        "DB_DOCUMENTATION_ID": DB_DOCUMENTATION_ID,
        "DB_AI_PROFILES_ID": DB_AI_PROFILES_ID,
        "DB_PROJECT_DATA_ID": DB_PROJECT_DATA_ID,
        "DB_MUSICA_ID": DB_MUSICA_ID,
        "DB_STUDI_MUSICA_ID": DB_STUDI_MUSICA_ID,
        "WAW_COUNCIL_ID": WAW_COUNCIL_ID
    }
    
    missing = [name for name, value in required_dbs.items() if not value]
    if missing:
        raise ValueError(f"Database IDs mancanti: {', '.join(missing)}")
    
    return {
        "NOTION_API_KEY": NOTION_API_KEY,
        "DB_ARTICLES_ID": DB_ARTICLES_ID,
        "DB_DOCUMENTATION_ID": DB_DOCUMENTATION_ID,
        "DB_AI_PROFILES_ID": DB_AI_PROFILES_ID,
        "DB_PROJECT_DATA_ID": DB_PROJECT_DATA_ID,
        "DB_MUSICA_ID": DB_MUSICA_ID,
        "DB_STUDI_MUSICA_ID": DB_STUDI_MUSICA_ID,
        "WAW_COUNCIL_ID": WAW_COUNCIL_ID
    }

# Carica configurazione al caricamento del modulo
_config = load_config()
NOTION_API_KEY = _config["NOTION_API_KEY"]
DB_ARTICLES_ID = _config["DB_ARTICLES_ID"]
DB_DOCUMENTATION_ID = _config["DB_DOCUMENTATION_ID"]
DB_AI_PROFILES_ID = _config["DB_AI_PROFILES_ID"]
DB_PROJECT_DATA_ID = _config["DB_PROJECT_DATA_ID"]
DB_MUSICA_ID = _config["DB_MUSICA_ID"]
DB_STUDI_MUSICA_ID = _config["DB_STUDI_MUSICA_ID"]
WAW_COUNCIL_ID = _config["WAW_COUNCIL_ID"]

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
    # Nota: ob_council non ancora aggiunto (useremo ob_progetti per test)
}

NOTION_HEADERS = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}
