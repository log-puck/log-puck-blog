"""
File Writer: Scrive file Jekyll e valida path
"""

import os
from typing import Optional
from ..logger import log
from ..api import NotionClient


class FileWriter:
    """Gestisce la scrittura di file Jekyll e validazione path"""
    
    def __init__(self, client: Optional[NotionClient] = None):
        """
        Inizializza il file writer.
        
        Args:
            client: NotionClient opzionale per aggiornare status (se None, non aggiorna status)
        """
        self.client = client
    
    def write_jekyll_file(self, file_path: str, content: str, infra_id_to_update: Optional[str] = None) -> bool:
        """
        Scrive un file Jekyll Markdown con gestione errori.
        
        Crea le directory necessarie se non esistono.
        Aggiorna lo status in Notion se infra_id_to_update è fornito.
        
        Args:
            file_path: Percorso del file da scrivere (relativo o assoluto)
            content: Contenuto completo (frontmatter YAML + body markdown)
            infra_id_to_update: ID pagina infra per aggiornare status (opzionale)
            
        Returns:
            True se successo, False altrimenti
        """
        try:
            target_dir = os.path.dirname(file_path)
            if target_dir and not os.path.exists(target_dir):
                os.makedirs(target_dir)
            
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            
            log(f"✅ [OK] Generato: {file_path}", "INFO")
            
            if infra_id_to_update and self.client:
                self.client.update_page_status(infra_id_to_update, "ok")
            
            return True
            
        except Exception as e:
            log(f"ERROR writing {file_path}: {str(e)}", "ERROR")
            if infra_id_to_update and self.client:
                self.client.update_page_status(infra_id_to_update, "error", str(e))
            return False
    
    @staticmethod
    def validate_build_path(file_path: str) -> None:
        """
        Valida che il percorso non contenga cartelle con underscore.
        
        Jekyll tratta le cartelle con underscore come speciali (es. _layouts, _includes).
        Questa funzione previene la creazione accidentale di file in cartelle riservate.
        
        Args:
            file_path: Percorso da validare
            
        Raises:
            ValueError: Se il percorso contiene cartelle con underscore
        """
        path_components = os.path.normpath(file_path).split(os.sep)
        folders = path_components[:-1]
        
        if any(folder.startswith("_") for folder in folders):
            error_msg = f"⛔ ERRORE: Build Path '{file_path}' contiene cartella con '_'. Jekyll la ignorerebbe."
            log(error_msg, "ERROR")
            raise ValueError(error_msg)
