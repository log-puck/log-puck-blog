"""
Timeline Processor
Genera timeline.json da Done-List Notion per Workflow Tracking Dashboard
"""

import json
from datetime import datetime
from typing import Dict, List, Optional
from ..api import NotionClient, get_property_value
from ..config import DB_DONE_LIST_ID
from ..logger import log


class TimelineProcessor:
    """Processor per generazione timeline lavori completati"""
    
    def __init__(self, client: NotionClient):
        self.client = client
        self.categories = ["Infrastructure", "Content", "Feature", "Fix", "Design"]
    
    def auto_categorize(self, title: str, description: str) -> str:
        """
        Auto-detect category from keywords
        
        Args:
            title: Task title
            description: Task description
            
        Returns:
            Category string (Infrastructure|Content|Feature|Fix|Design)
        """
        text = f"{title} {description}".lower()
        
        # Infrastructure keywords
        if any(word in text for word in [
            'server', 'script', 'database', 'db', 'api', 
            'deployment', 'infrastructure', 'hetzner', 'pm2',
            'notion', 'integration', 'python', 'node', 'orchestrator',
            'processor', 'jekyll', 'build', 'config'
        ]):
            return 'Infrastructure'
        
        # Content keywords
        elif any(word in text for word in [
            'article', 'articolo', 'content', 'blog', 
            'documentation', 'doc', 'post', 'write', 'writing',
            'session', 'ob-session', 'markdown', 'testo'
        ]):
            return 'Content'
        
        # Feature keywords
        elif any(word in text for word in [
            'feature', 'new', 'implement', 'add', 'create',
            'dashboard', 'tool', 'system', 'workflow', 'council',
            'waw', 'voting', 'timeline', 'automation'
        ]):
            return 'Feature'
        
        # Fix keywords
        elif any(word in text for word in [
            'fix', 'bug', 'error', 'repair', 'correct',
            'debug', 'issue', 'problem', 'risolv', 'aggiust'
        ]):
            return 'Fix'
        
        # Design keywords
        elif any(word in text for word in [
            'design', 'ui', 'ux', 'visual', 'style',
            'css', 'scss', 'layout', 'mockup', 'aesthetic',
            'frontend', 'responsive', 'mobile'
        ]):
            return 'Design'
        
        # Default fallback
        else:
            return 'General'
    
    def process_timeline(self) -> None:
        """
        Processa Done-List da Notion e genera timeline.json
        
        Output: _data/timeline.json
        """
        log("📋 Starting Timeline generation...")
        
        if not DB_DONE_LIST_ID or DB_DONE_LIST_ID == "TBD":
            log("DB_DONE_LIST_ID non configurato, skip Timeline", "WARN")
            return
        
        try:
            # Query Done-List con sorting (NO filters - leggi tutto)
            # get_database_data accetta filter_body che può contenere sorts
            query_body = {
                "sorts": [{
                    "property": "Created time",
                    "direction": "descending"
                }]
            }
            pages = self.client.get_database_data(DB_DONE_LIST_ID, query_body)
            
            if not pages:
                log("⚠️ Warning: Done-List is empty")
                pages = []
            
            # Process tasks
            tasks = []
            category_counts = {cat: 0 for cat in self.categories}
            category_counts["General"] = 0  # Include General for fallback
            
            for idx, page in enumerate(pages):
                try:
                    # Estrai properties (pattern corretto come altri processors)
                    props_raw = page.get("properties", {})
                    
                    # Extract properties usando pattern corretto
                    title = get_property_value(props_raw.get("Name")) or ""
                    description = get_property_value(props_raw.get("Descrizione")) or ""
                    notion_url = get_property_value(props_raw.get("URL")) or page.get("url", "")
                    
                    # Created time: Notion lo restituisce come property "Created time" (created_time type)
                    created_time_prop = props_raw.get("Created time")
                    if created_time_prop and created_time_prop.get("type") == "created_time":
                        created_time = created_time_prop.get("created_time", "")
                    else:
                        # Fallback: usa created_time direttamente dal page object se disponibile
                        created_time = page.get("created_time", "")
                    
                    # Auto-categorize
                    category = self.auto_categorize(title, description)
                    
                    # Increment counter
                    if category in category_counts:
                        category_counts[category] += 1
                    
                    # Build task object
                    task = {
                        "id": page.get("id", ""),
                        "date": created_time.split('T')[0] if created_time else "",
                        "category": category,
                        "title": title,
                        "description": description,
                        "notion_url": notion_url,
                        "is_latest": (idx == 0)  # First item is latest
                    }
                    
                    tasks.append(task)
                    
                except Exception as e:
                    log(f"⚠️ Error processing page {page.get('id', 'unknown')}: {str(e)}")
                    continue
            
            # Prepare timeline data
            timeline_data = {
                "tasks": tasks,
                "categories": self.categories,
                "summary": {
                    "total": len(tasks),
                    "by_category": {
                        cat: category_counts[cat] 
                        for cat in self.categories
                    }
                },
                "last_updated": datetime.now().isoformat()
            }
            
            # Write to _data/timeline.json (root del progetto)
            output_path = "_data/timeline.json"
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(timeline_data, f, indent=2, ensure_ascii=False)
            
            # Log summary
            log(f"✅ Timeline: Generated {len(tasks)} tasks")
            log(f"   By category:")
            for cat in self.categories:
                count = category_counts[cat]
                if count > 0:
                    log(f"   - {cat}: {count}")
            
            log(f"--- Timeline: Output written to {output_path} ---")
            
        except Exception as e:
            log(f"❌ Timeline Error: {str(e)}")
            raise
