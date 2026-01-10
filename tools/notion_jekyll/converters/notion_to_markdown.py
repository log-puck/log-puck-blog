"""
Notion to Markdown Converter
Converte blocchi Notion in Markdown
"""

import requests
from typing import Dict, Any
from ..api import NotionClient
from ..logger import log


class NotionToMarkdownConverter:
    """Converte contenuti Notion in Markdown"""
    
    def __init__(self, client: NotionClient):
        """
        Inizializza il converter.
        
        Args:
            client: NotionClient per fare chiamate API
        """
        self.client = client
    
    def get_page_blocks(self, page_id: str) -> str:
        """
        Recupera tutti i blocchi di una pagina Notion e converte in Markdown.
        
        Supporta: paragraph, heading_1/2/3, code, bulleted_list_item, numbered_list_item, image
        
        Args:
            page_id: ID della pagina Notion
            
        Returns:
            Contenuto Markdown della pagina (stringa)
        """
        all_blocks = []
        has_more = True
        start_cursor = None
        
        while has_more:
            url = f"https://api.notion.com/v1/blocks/{page_id}/children"
            params = {}
            if start_cursor:
                params["start_cursor"] = start_cursor
            
            response = requests.get(url, headers=self.client.headers, params=params)
            if response.status_code != 200:
                log(f"Errore recupero blocchi per {page_id}: {response.text}", "ERROR")
                break
            
            data = response.json()
            all_blocks.extend(data.get("results", []))
            has_more = data.get("has_more", False)
            start_cursor = data.get("next_cursor", None)
        
        content_md = ""
        
        def get_text(prop):
            """Concatena tutti i rich_text elements."""
            rich_text_list = prop.get("rich_text", [])
            return "".join([rt.get("plain_text", "") for rt in rich_text_list])
        
        for block in all_blocks:
            block_type = block.get("type")
            block_data = block.get(block_type, {})
            
            if block_type == "paragraph":
                text = get_text(block_data)
                content_md += f"{text}\n\n"
            elif block_type == "heading_1":
                text = get_text(block_data)
                content_md += f"# {text}\n\n"
            elif block_type == "heading_2":
                text = get_text(block_data)
                content_md += f"## {text}\n\n"
            elif block_type == "heading_3":
                text = get_text(block_data)
                content_md += f"### {text}\n\n"
            elif block_type == "code":
                text = get_text(block_data)
                lang = block_data.get("language", "")
                if lang.lower() == "markdown":
                    content_md += f"{text}\n\n"
                else:
                    content_md += f"```{lang}\n{text}\n```\n\n"
            elif block_type == "bulleted_list_item":
                text = get_text(block_data)
                content_md += f"- {text}\n"
            elif block_type == "numbered_list_item":
                text = get_text(block_data)
                content_md += f"1. {text}\n"
            elif block_type == "image":
                url_img = block_data.get("external", {}).get("url")
                if not url_img:
                    url_img = block_data.get("file", {}).get("url")
                if url_img:
                    content_md += f"![image]({url_img})\n\n"
        
        # Pulisci il markdown
        content_md = self.clean_markdown_content(content_md)
        
        return content_md
    
    @staticmethod
    def clean_markdown_content(content: str) -> str:
        """
        Pulisce il contenuto markdown rimuovendo wrapper e separatori frontmatter.
        
        Args:
            content: Contenuto markdown da pulire
            
        Returns:
            Contenuto pulito
        """
        if not content:
            return content
        
        # Rimuovi wrapper markdown se presente
        if content.startswith("```markdown"):
            content = content.replace("```markdown\n", "", 1)
        if content.startswith("```html"):
            content = content.replace("```html\n", "", 1)
        if content.endswith("```"):
            content = content.rstrip("```").rstrip()
        
        # Rimuovi eventuale --- iniziale (può essere rimasto da Notion)
        if content.strip().startswith("---"):
            content = content.strip()[3:].lstrip() + "\n"
        
        return content
