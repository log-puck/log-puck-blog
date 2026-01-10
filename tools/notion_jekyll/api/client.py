"""
Notion API Client
"""

import requests
import datetime
from typing import Optional, List, Dict, Any
from ..config import NOTION_HEADERS
from ..logger import log


class NotionClient:
    """Client per interagire con Notion API"""
    
    def __init__(self, headers: Optional[Dict[str, str]] = None):
        """
        Inizializza il client Notion.
        
        Args:
            headers: Headers HTTP personalizzati (default: usa NOTION_HEADERS da config)
        """
        self.headers = headers or NOTION_HEADERS
    
    def get_database_data(self, database_id: str, filter_body: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Query un database Notion con paginazione completa.
        
        Args:
            database_id: ID del database Notion
            filter_body: Filtro opzionale per la query
            
        Returns:
            Lista di risultati dalla query
            
        Raises:
            Exception: Se la chiamata API fallisce
        """
        results = []
        url = f"https://api.notion.com/v1/databases/{database_id}/query"
        has_more = True
        start_cursor = None
        
        while has_more:
            payload = {}
            if start_cursor:
                payload["start_cursor"] = start_cursor
            if filter_body:
                payload.update(filter_body)
            
            response = requests.post(url, headers=self.headers, json=payload)
            if response.status_code != 200:
                log(f"Errore API Notion: {response.text}", "ERROR")
                raise Exception(f"API Error: {response.status_code}")
            
            data = response.json()
            results.extend(data.get("results", []))
            has_more = data.get("has_more", False)
            start_cursor = data.get("next_cursor", None)
        
        return results
    
    def get_page(self, page_id: str) -> Optional[Dict[str, Any]]:
        """
        Recupera una pagina Notion per ID.
        
        Args:
            page_id: ID della pagina Notion
            
        Returns:
            Dati della pagina (dict) o None se errore
        """
        url = f"https://api.notion.com/v1/pages/{page_id}"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        return None
    
    def update_page_status(self, page_id: str, status: str, error_log: str = "") -> None:
        """
        Aggiorna lo status di build in Notion.
        
        Args:
            page_id: ID della pagina infra
            status: "ok" o "error"
            error_log: Messaggio di errore opzionale
        """
        url = f"https://api.notion.com/v1/pages/{page_id}"
        
        notion_status_name = "In progress"
        if status == "ok":
            notion_status_name = "Done"
        elif status == "error":
            notion_status_name = "In progress"
        
        payload = {
            "properties": {
                "Build Status": {
                    "status": {
                        "name": notion_status_name
                    }
                },
                "Last Build": {
                    "date": {
                        "start": datetime.datetime.now().isoformat()
                    }
                }
            }
        }
        
        if error_log:
            payload["properties"]["Error Log"] = {
                "rich_text": [
                    {
                        "text": {
                            "content": error_log
                        }
                    }
                ]
            }
        
        response = requests.patch(url, headers=self.headers, json=payload)
        if response.status_code != 200:
            log(f"Errore aggiornamento status infra {page_id}: {response.text}", "WARN")
