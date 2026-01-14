"""
Jekyll Builder: Genera frontmatter, permalink, path per Jekyll
"""

import os
from typing import Optional, Dict, Any
from ..config import LAYOUT_MAP, OUTPUT_DIR


class JekyllBuilder:
    """Builder per generare componenti Jekyll (frontmatter, path, permalink)"""
    
    @staticmethod
    def normalize_slug(slug: Optional[str]) -> str:
        """
        Normalizza lo slug rimuovendo .md se presente e preparandolo per l'uso.
        
        Args:
            slug: Slug originale (può contenere .md o meno)
            
        Returns:
            Slug normalizzato (senza .md, lowercase, spazi sostituiti con -)
        """
        if not slug:
            return ""
        # Rimuovi .md se presente
        if slug.endswith(".md"):
            slug = slug[:-3]
        # Normalizza: lowercase, rimuovi spazi, sostituisci con -
        return slug.strip().lower().replace(" ", "-")
    
    @staticmethod
    def normalize_subsection(subsection: Optional[str]) -> str:
        """
        Normalizza il nome della subsection per il percorso file.
        
        Converte "MusicaAI" -> "musica", "GiochiAI" -> "giochiAI", etc.
        
        Args:
            subsection: Nome subsection originale (può essere None)
            
        Returns:
            Nome subsection normalizzato (lowercase, spazi sostituiti con -), stringa vuota se None
        """
        if not subsection:
            return ""
        
        sub_sub = subsection.lower().replace(" ", "-")
        if "musica" in sub_sub:
            sub_sub = "musica"
        elif "giochi" in sub_sub:
            sub_sub = "giochiAI"
        elif sub_sub == "documents":
            sub_sub = "documents"  # Mantieni "documents" per OB-Archives
        
        return sub_sub
    
    @staticmethod
    def generate_permalink(section: str, subsection: Optional[str] = None, internal_section: Optional[str] = None, slug: Optional[str] = None) -> Optional[str]:
        """
        Genera il permalink automatico basato su section, subsection, internal_section e slug.
        
        Esempi:
        - section="OB-Session", slug="test" -> "/ob-session/test/"
        - section="OB-Progetti", subsection="wAw", slug="index" -> "/ob-progetti/waw/"
        - section="OB-Progetti", subsection="wAw", internal_section="Council", slug="index" -> "/ob-progetti/waw/council/"
        
        Args:
            section: Sezione (OB-Session, OB-AI, OB-Progetti, OB-Archives)
            subsection: Sottosezione opzionale (wAw, MusicaAI, etc.)
            internal_section: Sezione interna opzionale (Council, Metabolism, Evolution, etc.)
            slug: Slug del contenuto (None per index.md, che genera permalink senza /index/)
            
        Returns:
            Permalink generato o None se non valido
        """
        permalink_parts = []
        
        if section:
            section_slug = section.lower().replace(" ", "-")
            permalink_parts.append(section_slug)
        
        if subsection:
            subsection_slug = JekyllBuilder.normalize_subsection(subsection)
            permalink_parts.append(subsection_slug)
        
        if internal_section:
            internal_slug = internal_section.lower().replace(" ", "-")
            permalink_parts.append(internal_slug)
        
        # Per file index.md, non aggiungere slug
        if slug and slug != "index":
            permalink_parts.append(slug)
        
        if permalink_parts:
            return "/" + "/".join(permalink_parts) + "/"
        
        return None
    
    @staticmethod
    def get_jekyll_layout(layout_notion: Optional[str], section: Optional[str] = None, slug: Optional[str] = None) -> str:
        """
        Determina il layout Jekyll da usare, con auto-rilevamento per landing progetti.
        
        Mappa layout Notion -> layout Jekyll usando LAYOUT_MAP.
        Auto-rileva landing progetti: se section == "OB-Progetti" e slug == "index", usa "ob_progetti".
        
        Args:
            layout_notion: Valore layout da Notion (session, document, landing, etc.)
            section: Sezione (per auto-rilevamento progetti)
            slug: Slug (per auto-rilevamento progetti)
            
        Returns:
            Nome layout Jekyll (es. "ob_session", "ob_document", "ob_progetti", "default")
        """
        jekyll_layout = LAYOUT_MAP.get(layout_notion, "default")
        
        # Auto-rileva landing di progetti: se section == "OB-Progetti" e slug == "index", usa layout ob_progetti
        # Questo include anche le landing di subsection (es. council/index, metabolism/index, evolution/index)
        if section == "OB-Progetti" and slug == "index":
            jekyll_layout = "ob_progetti"
        
        return jekyll_layout
    
    @staticmethod
    def generate_build_path(section: str, slug: Optional[str], layout_val: Optional[str], subsection: Optional[str] = None, internal_section: Optional[str] = None) -> str:
        """
        Genera il percorso file secondo la Routing Matrix.
        
        Esempi:
        - section="OB-Session", slug="test" -> "ob-session/test.md"
        - section="OB-Progetti", subsection="wAw", slug="index" -> "ob-progetti/waw/index.md"
        - section="OB-Progetti", subsection="wAw", internal_section="Council", slug="session-2026-01-04" -> "ob-progetti/waw/council/session-2026-01-04.md"
        
        Args:
            section: Sezione (OB-Session, OB-AI, OB-Progetti, OB-Archives)
            slug: Slug del contenuto (normalizzato automaticamente)
            layout_val: Valore layout Notion (non usato ma mantenuto per compatibilità)
            subsection: Sottosezione opzionale (wAw, MusicaAI, etc.)
            internal_section: Sezione interna (Council, Metabolism, Evolution, tracce, etc.)
            
        Returns:
            Percorso file completo relativo (es. "ob-session/test.md")
        """
        safe_slug = JekyllBuilder.normalize_slug(slug)
        
        dir_map = {
            "OB-Session": "ob-session",
            "OB-AI": "ob-ai",
            "OB-Progetti": "ob-progetti",
            "OB-Archives": "ob-archives"
        }
        base_dir = dir_map.get(section, "uncategorized")
        
        sub_path = ""
        
        if subsection:
            sub_sub = JekyllBuilder.normalize_subsection(subsection)
            if sub_path == "":
                sub_path = f"{sub_sub}/"
            else:
                sub_path = f"{sub_path}{sub_sub}/"
        
        # Aggiungi Internal Section se presente (es. Council, Metabolism, Evolution, tracce)
        if internal_section:
            internal_path = internal_section.lower().replace(" ", "-")
            sub_path = f"{sub_path}{internal_path}/"
        
        filename = f"{safe_slug}.md"
        return os.path.join(OUTPUT_DIR, base_dir, sub_path, filename)
    
    @staticmethod
    def create_frontmatter(props: Dict[str, Any], layout_name: str) -> str:
        """
        Crea il frontmatter YAML per Jekyll.
        
        Include automaticamente:
        - filter_section per layout ob_landing
        - custom_class: "ai-landing" per OB-AI landing
        
        Args:
            props: Dizionario con le proprietà (title, slug, date, section, subsection, description, keywords, tags, etc.)
            layout_name: Nome del layout Jekyll (es. "ob_session", "ob_landing")
            
        Returns:
            Stringa frontmatter YAML formattata (inizia con "---" e termina con "---")
        """
        fm = "---\n"
        fm += f'title: "{props.get("title", "Untitled")}"\n'
        fm += f'slug: "{props.get("slug", "")}"\n'
        fm += f'date: "{props.get("date", "")}"\n'
        fm += f'section: "{props.get("section", "")}"\n'
        
        # Includi subsection se presente
        if props.get("subsection"):
            fm += f'subsection: "{props.get("subsection")}"\n'
        
        fm += f'layout: "{layout_name}"\n'
        
        # Per layout ob_landing, aggiungi automaticamente filter_section (uguale a section)
        # Controlla che non sia già presente per evitare duplicati
        if layout_name == "ob_landing" and props.get("section") and "filter_section" not in str(fm):
            fm += f'filter_section: "{props.get("section")}"\n'
        
        # Per OB-AI landing, aggiungi automaticamente custom_class per stili CSS specifici
        if layout_name == "ob_landing" and props.get("section") == "OB-AI":
            fm += f'custom_class: "ai-landing"\n'
        
        if props.get("permalink"):
            fm += f'permalink: {props.get("permalink")}\n'
        
        # Description viene da "Description" in Notion
        if props.get("description"):
            fm += f'description: "{props.get("description")}"\n'
        
        if props.get("keywords"):
            fm += f'keywords: "{props.get("keywords")}"\n'
        
        # Campi display opzionali
        if props.get("subtitle"):
            fm += f'subtitle: "{props.get("subtitle")}"\n'
        
        if props.get("tags"):
            fm += "tags:\n"
            for tag in props.get("tags"):
                fm += f"  - {tag}\n"
        
        if props.get("ai_author"):
            fm += f'ai_author: "{props.get("ai_author")}"\n'
        
        if props.get("ai_participants"):
            fm += "ai_participants:\n"
            for participant in props.get("ai_participants"):
                fm += f'  - "{participant}"\n'
        
        # Project-specific fields
        if props.get("project_status"):
            fm += f'project_status: "{props.get("project_status")}"\n'
        
        # Campi footer (progetti)
        show_footer_val = props.get("show_footer")
        if show_footer_val is not None:
            fm += f'show_footer: {str(show_footer_val).lower()}\n'
        
        if props.get("footer_text"):
            fm += f'footer_text: "{props.get("footer_text")}"\n'
        
        # Campi documenti
        # version è number in Notion, convertiamo a stringa
        if props.get("version") is not None:
            version_val = props.get("version")
            # Se è number, converti a stringa mantenendo il formato (es. 1.0)
            if isinstance(version_val, (int, float)):
                fm += f'version: "{version_val}"\n'
            else:
                fm += f'version: "{version_val}"\n'
        
        if props.get("next_review"):
            # Formatta next_review come data
            next_review_val = props.get("next_review")
            if isinstance(next_review_val, str):
                fm += f'next_review: "{next_review_val}"\n'
            else:
                fm += f'next_review: "{next_review_val}"\n'
        if props.get("use_supabase_data"):
            fm += f'use_supabase_data: {str(props.get("use_supabase_data")).lower()}\n'
        if props.get("supabase_table"):
            fm += f'supabase_table: "{props.get("supabase_table")}"\n'
        if props.get("ai_models"):
            fm += "ai_models:\n"
            for model in props.get("ai_models"):
                fm += f'  - "{model}"\n'
        if props.get("personas"):
            fm += "personas:\n"
            for persona in props.get("personas"):
                fm += f'  - "{persona}"\n'
        
        # Campi AI Profiles (ob_ai layout)
        if props.get("avatar"):
            fm += f'avatar: "{props.get("avatar")}"\n'
        if props.get("profilo"):
            fm += f'profilo: "{props.get("profilo")}"\n'
        if props.get("epoca"):
            fm += f'epoca: "{props.get("epoca")}"\n'
        if props.get("style"):
            fm += f'style: "{props.get("style")}"\n'
        if props.get("focus") is not None:
            focus_val = props.get("focus")
            if isinstance(focus_val, (int, float)):
                fm += f'focus: {focus_val}\n'
            else:
                fm += f'focus: "{focus_val}"\n'
        if props.get("speaking") is not None:
            speaking_val = props.get("speaking")
            if isinstance(speaking_val, (int, float)):
                fm += f'speaking: {speaking_val}\n'
            else:
                fm += f'speaking: "{speaking_val}"\n'
        if props.get("tono"):
            fm += "tono:\n"
            for t in props.get("tono"):
                fm += f'  - "{t}"\n'
        
        fm += "---\n"
        return fm
