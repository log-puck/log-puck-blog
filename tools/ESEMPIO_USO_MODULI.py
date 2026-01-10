#!/usr/bin/env python3
"""
Esempio di come usare i moduli modulari invece dello script monolitico

Questo esempio mostra come utilizzare i nuovi moduli estratti,
dimostrando i vantaggi della struttura modulare.
"""

import sys
import os

# Aggiungi tools/ al path per importare i moduli
script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir not in sys.path:
    sys.path.insert(0, script_dir)

# ============================================================================
# ESEMPIO 1: Usare il NotionClient
# ============================================================================

from notion_jekyll.api import NotionClient, get_property_value
from notion_jekyll.config import DB_CONTENT_ID
from notion_jekyll.logger import log

def esempio_notion_client():
    """Esempio di utilizzo del NotionClient modulare"""
    
    # Crea client (usa configurazione automatica da config.py)
    client = NotionClient()
    
    # Query database con filtro
    filter_published = {
        "filter": {
            "property": "Status",
            "select": {
                "equals": "Published"
            }
        }
    }
    
    try:
        content_items = client.get_database_data(DB_CONTENT_ID, filter_published)
        log(f"✅ Trovati {len(content_items)} contenuti", "INFO")
        
        # Processa il primo item come esempio
        if content_items:
            item = content_items[0]
            props = item.get("properties", {})
            title = get_property_value(props.get("Title"))
            log(f"📄 Primo contenuto: {title}", "INFO")
            
            # Esempio di altre proprietà
            date = get_property_value(props.get("Date"))
            section = get_property_value(props.get("Section"))
            log(f"   Data: {date}, Sezione: {section}", "DEBUG")
    except Exception as e:
        log(f"❌ Errore: {e}", "ERROR")


# ============================================================================
# ESEMPIO 2: Utilizzo modulare e testabile
# ============================================================================

def esempio_uso_modulare():
    """
    Mostra i vantaggi dell'approccio modulare:
    
    1. Testabilità: Puoi mockare NotionClient per test senza chiamate API reali
    2. Riutilizzo: Puoi importare solo quello che ti serve
    3. Flessibilità: Puoi sostituire componenti facilmente
    """
    
    # Esempio: Usa solo il logger senza importare tutto il resto
    from notion_jekyll.logger import log
    
    log("🔧 Logging modulare: import solo quello che serve", "INFO")
    
    # Esempio: Usa solo la config senza il client
    from notion_jekyll.config import NOTION_API_KEY, LAYOUT_MAP
    
    log(f"📋 Layout disponibili: {list(LAYOUT_MAP.keys())}", "INFO")
    
    # Esempio: Usa solo get_property_value senza tutto il client
    from notion_jekyll.api.properties import get_property_value
    
    # Simula una proprietà Notion per test
    fake_prop = {
        "type": "title",
        "title": [{"plain_text": "Test Title"}]
    }
    
    title = get_property_value(fake_prop)
    log(f"✅ Estrazione proprietà: {title}", "INFO")


# ============================================================================
# ESEMPIO 3: Vantaggi per testing e sviluppo
# ============================================================================

class MockNotionClient:
    """Mock client per test senza chiamate API reali"""
    
    def get_database_data(self, database_id, filter_body=None):
        return [
            {
                "id": "fake-id-123",
                "properties": {
                    "Title": {
                        "type": "title",
                        "title": [{"plain_text": "Test Content"}]
                    }
                }
            }
        ]
    
    def get_page(self, page_id):
        return {"id": page_id, "properties": {}}

def esempio_testing():
    """Mostra come la modularità facilita i test"""
    
    log("🧪 Esempio di testing modulare", "INFO")
    
    # Puoi sostituire il client reale con un mock per i test
    mock_client = MockNotionClient()
    test_data = mock_client.get_database_data("fake-db-id")
    
    log(f"✅ Test senza chiamate API: {len(test_data)} items mock", "INFO")
    log("   (In un test reale, useresti unittest.mock o pytest)", "DEBUG")


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("ESEMPI DI UTILIZZO MODULI NOTION_JEKyll")
    print("=" * 60)
    print()
    
    # Esempio 1: NotionClient (richiede credenziali Notion)
    print("📡 ESEMPIO 1: NotionClient")
    print("-" * 60)
    try:
        esempio_notion_client()
    except ValueError as e:
        log(f"⚠️  Saltato: {e}", "WARN")
        log("   (Richiede credenziali Notion configurate)", "DEBUG")
    print()
    
    # Esempio 2: Uso modulare
    print("🔧 ESEMPIO 2: Utilizzo Modulare")
    print("-" * 60)
    esempio_uso_modulare()
    print()
    
    # Esempio 3: Testing
    print("🧪 ESEMPIO 3: Testing Modulare")
    print("-" * 60)
    esempio_testing()
    print()
    
    print("=" * 60)
    print("✅ Esempi completati!")
    print()
    print("💡 VANTAGGI della struttura modulare:")
    print("   • Testabilità: ogni componente testabile separatamente")
    print("   • Riutilizzo: import solo quello che serve")
    print("   • Manutenibilità: modifiche localizzate")
    print("   • Scalabilità: facile aggiungere nuovi componenti")
    print("=" * 60)
