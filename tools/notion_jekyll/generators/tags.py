"""
Tag Generator: Genera pagine tag e top tags data
"""

import os
import re
from typing import List, Set
from ..logger import log


class TagGenerator:
    """Genera pagine tag e file YAML per top tags"""
    
    @staticmethod
    def extract_tags_from_frontmatter(frontmatter: str) -> List[str]:
        """
        Estrae tutti i tag da un frontmatter YAML.
        
        Supporta formati:
        - tags: ["tag1", "tag2"]
        - tags: tag1, tag2
        - tags: "tag1, tag2"
        
        Args:
            frontmatter: Stringa frontmatter YAML (senza i separatori ---)
            
        Returns:
            Lista di tag estratti (lista di stringhe)
        """
        tags_set = set()
        in_tags_section = False
        
        for line in frontmatter.split("\n"):
            line_stripped = line.strip()
            
            # Inizio sezione tags
            if line_stripped.startswith("tags:"):
                in_tags_section = True
                # Gestisci formato inline: tags: ['tag1', 'tag2']
                if "[" in line:
                    tags_match = re.search(r'\[(.*?)\]', line)
                    if tags_match:
                        tags_str = tags_match.group(1)
                        for tag in tags_str.split(","):
                            tag = tag.strip().strip('"').strip("'")
                            if tag:
                                tags_set.add(tag)
                    in_tags_section = False
                continue
            
            # Se siamo nella sezione tags, processa le righe
            if in_tags_section:
                # Fine sezione tags (nuova chiave o fine frontmatter)
                if line_stripped and not line_stripped.startswith("- ") and ":" in line_stripped and not line_stripped.startswith("#"):
                    in_tags_section = False
                    continue
                
                # Tag in formato lista YAML: - Tag Name
                if line_stripped.startswith("- "):
                    tag = line_stripped[2:].strip().strip('"').strip("'")
                    if tag:
                        tags_set.add(tag)
                # Se la riga è vuota o solo spazi, continua (potrebbe essere parte della lista)
                elif not line_stripped:
                    continue
                # Altrimenti, fine sezione tags
                else:
                    in_tags_section = False
        
        return list(tags_set)
    
    @staticmethod
    def get_all_tags_from_files() -> Set[str]:
        """
        Scansiona tutti i file .md generati e raccoglie tutti i tag unici.
        
        Cerca in: ob-session, ob-ai, ob-progetti, ob-archives
        
        Returns:
            Set di tag unici trovati (set di stringhe)
        """
        tags_set = set()
        md_files = []
        
        # Cerca in tutte le cartelle di contenuto
        content_dirs = ["ob-session", "ob-ai", "ob-progetti", "ob-archives"]
        
        for dir_name in content_dirs:
            if os.path.exists(dir_name):
                for root, dirs, files in os.walk(dir_name):
                    for file in files:
                        if file.endswith(".md"):
                            md_files.append(os.path.join(root, file))
        
        # Leggi ogni file e estrai tag dal frontmatter
        for filepath in md_files:
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                    
                    # Estrai frontmatter
                    if content.startswith("---"):
                        parts = content.split("---", 2)
                        if len(parts) >= 3:
                            frontmatter = parts[1]
                            # Estrai tag usando funzione comune
                            file_tags = TagGenerator.extract_tags_from_frontmatter(frontmatter)
                            tags_set.update(file_tags)
                                
            except Exception as e:
                log(f"Errore lettura {filepath}: {str(e)}", "WARN")
        
        return tags_set
    
    @staticmethod
    def generate_tag_slug(tag: str) -> str:
        """Converte un tag in slug per URL."""
        return tag.lower().replace(" ", "-").replace("_", "-")
    
    def generate_tag_pages(self) -> None:
        """
        Genera pagine tag per tutti i tag trovati nei file esistenti.
        
        Crea file in tags/tag-slug.md con layout ob_tag.
        Ogni pagina tag mostra tutti i contenuti con quel tag.
        """
        log("Inizio generazione TAG PAGES...")
        
        # Crea directory tags se non esiste
        tags_dir = "tags"
        if not os.path.exists(tags_dir):
            os.makedirs(tags_dir)
            log(f"Creata directory {tags_dir}")
        
        # Raccogli tutti i tag
        all_tags = self.get_all_tags_from_files()
        
        if not all_tags:
            log("Nessun tag trovato nei file", "WARN")
            return
        
        log(f"Trovati {len(all_tags)} tag unici")
        
        generated_count = 0
        
        for tag in all_tags:
            tag_slug = self.generate_tag_slug(tag)
            filepath = os.path.join(tags_dir, f"{tag_slug}.md")
            
            # Frontmatter per pagina tag
            frontmatter = f"""---
layout: ob_tag
tag_name: "{tag}"
title: "Tag: {tag}"
permalink: /tags/{tag_slug}/
description: "Tutti i contenuti con tag '{tag}'"
---

"""
            
            try:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(frontmatter)
                generated_count += 1
            except Exception as e:
                log(f"ERROR writing {filepath}: {str(e)}", "ERROR")
        
        log(f"--- TAG PAGES: Generati {generated_count} file. ---")
    
    def generate_top_tags_data(self) -> None:
        """
        Genera file _data/top_tags.yml con i 5 tag più popolari.
        
        Questo file viene letto da Jekyll per mostrare i top tag nella homepage.
        Conta quante volte ogni tag appare nei contenuti e ordina per popolarità.
        """
        log("Inizio generazione TOP TAGS data...")
        
        # Crea directory _data se non esiste
        data_dir = "_data"
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
            log(f"Creata directory {data_dir}")
        
        all_tags = self.get_all_tags_from_files()
        
        if not all_tags:
            log("Nessun tag trovato, creo file vuoto", "WARN")
            top_tags = []
        else:
            # Conta occorrenze di ogni tag
            tag_counts = {}
            md_files = []
            
            # Cerca in tutte le cartelle di contenuto
            content_dirs = ["ob-session", "ob-ai", "ob-progetti", "ob-archives"]
            
            for dir_name in content_dirs:
                if os.path.exists(dir_name):
                    for root, dirs, files in os.walk(dir_name):
                        for file in files:
                            if file.endswith(".md"):
                                md_files.append(os.path.join(root, file))
            
            # Conta occorrenze
            for filepath in md_files:
                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        content = f.read()
                        
                        if content.startswith("---"):
                            parts = content.split("---", 2)
                            if len(parts) >= 3:
                                frontmatter = parts[1]
                                # Estrai tag usando funzione comune
                                file_tags = self.extract_tags_from_frontmatter(frontmatter)
                                # Conta occorrenze
                                for tag in file_tags:
                                    tag_counts[tag] = tag_counts.get(tag, 0) + 1
                except Exception as e:
                    log(f"Errore lettura {filepath}: {str(e)}", "WARN")
            
            # Ordina per count e prendi top 5
            sorted_tags = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)
            top_5 = sorted_tags[:5]
            
            # Crea lista per YAML con slug
            top_tags = [{"name": tag, "count": count, "slug": self.generate_tag_slug(tag)} for tag, count in top_5]
            
            tag_list = ', '.join([f"{t['name']} ({t['count']})" for t in top_tags])
            log(f"Top 5 tag: {tag_list}")
        
        # Scrivi file YAML
        filepath = os.path.join(data_dir, "top_tags.yml")
        try:
            import yaml
            with open(filepath, "w", encoding="utf-8") as f:
                yaml.dump(top_tags, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
            log(f"✅ [OK] Top tags data: {filepath}", "INFO")
        except ImportError:
            # Se PyYAML non è disponibile, scrivi YAML manualmente
            with open(filepath, "w", encoding="utf-8") as f:
                f.write("# Top 5 most popular tags\n")
                f.write("# Generated automatically by notion_to_jekyll_builder.py\n\n")
                for tag_data in top_tags:
                    f.write(f"- name: \"{tag_data['name']}\"\n")
                    f.write(f"  count: {tag_data['count']}\n")
                    f.write(f"  slug: \"{tag_data['slug']}\"\n")
            log(f"✅ [OK] Top tags data (manual YAML): {filepath}", "INFO")
        except Exception as e:
            log(f"ERROR writing {filepath}: {str(e)}", "ERROR")
    
    def cleanup_orphan_tag_pages(self) -> None:
        """
        Rimuove pagine tag che non hanno più contenuti associati.
        
        Utile dopo aver rimosso tag da alcuni contenuti.
        Scansiona tags/*.md e rimuove quelli senza contenuti associati.
        """
        log("Inizio cleanup TAG PAGES orfane...")
        
        tags_dir = "tags"
        if not os.path.exists(tags_dir):
            return
        
        # Raccogli tutti i tag attualmente usati
        active_tags = self.get_all_tags_from_files()
        active_tag_slugs = {self.generate_tag_slug(tag) for tag in active_tags}
        
        # Controlla ogni file tag
        removed_count = 0
        for filename in os.listdir(tags_dir):
            if filename.endswith(".md"):
                tag_slug = filename[:-3]  # Rimuovi .md
                
                # Verifica se il tag è ancora attivo
                if tag_slug not in active_tag_slugs:
                    filepath = os.path.join(tags_dir, filename)
                    try:
                        os.remove(filepath)
                        log(f"🗑️  Rimosso tag page orfano: {tag_slug}", "INFO")
                        removed_count += 1
                    except Exception as e:
                        log(f"ERROR rimozione {filepath}: {str(e)}", "ERROR")
        
        if removed_count > 0:
            log(f"--- CLEANUP: Rimosse {removed_count} pagine tag orfane. ---")
        else:
            log("--- CLEANUP: Nessuna pagina tag orfana trovata. ---")
