"""
Notion to Jekyll Builder
Converte contenuti da Notion a file Markdown per Jekyll

VERSIONE MODULARE v4.0
Questo script ora usa l'architettura modulare in notion_jekyll/
"""

import sys
import os

# Aggiungi tools/ al path per importare i moduli
script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir not in sys.path:
    sys.path.insert(0, script_dir)

# Importa e esegui l'orchestrator modulare
from notion_jekyll.orchestrator import main

if __name__ == "__main__":
    main()
