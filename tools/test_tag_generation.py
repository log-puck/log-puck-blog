#!/usr/bin/env python3
"""
Script di test per generazione pagine tag.
Testa solo la funzione di generazione tag senza chiamare Notion API.
"""

import os
import sys

# Aggiungi il path per importare le funzioni
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Importa solo le funzioni necessarie (senza dipendenze Notion)
def generate_tag_slug(tag):
    """Converte un tag in slug per URL."""
    return tag.lower().replace(" ", "-").replace("_", "-")

def get_all_tags_from_files():
    """
    Scansiona tutti i file .md generati e raccoglie tutti i tag unici.
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
                        
                        # Cerca sezione tags nel frontmatter
                        in_tags_section = False
                        for line in frontmatter.split("\n"):
                            line_stripped = line.strip()
                            
                            # Inizio sezione tags
                            if line_stripped.startswith("tags:"):
                                in_tags_section = True
                                # Gestisci formato inline: tags: ['tag1', 'tag2']
                                if "[" in line:
                                    import re
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
                                if line_stripped and not line_stripped.startswith("- ") and ":" in line_stripped:
                                    in_tags_section = False
                                    continue
                                
                                # Tag in formato lista YAML: - Tag Name
                                if line_stripped.startswith("- "):
                                    tag = line_stripped[2:].strip().strip('"').strip("'")
                                    if tag:
                                        tags_set.add(tag)
                                
        except Exception as e:
            print(f"WARN: Errore lettura {filepath}: {str(e)}")
    
    return tags_set

def generate_tag_pages():
    """Genera pagine tag per tutti i tag trovati."""
    print("Inizio generazione TAG PAGES...")
    
    # Crea directory tags se non esiste
    tags_dir = "tags"
    if not os.path.exists(tags_dir):
        os.makedirs(tags_dir)
        print(f"Creata directory {tags_dir}")
    
    # Raccogli tutti i tag
    all_tags = get_all_tags_from_files()
    
    if not all_tags:
        print("WARN: Nessun tag trovato nei file")
        return
    
    print(f"Trovati {len(all_tags)} tag unici: {', '.join(sorted(all_tags))}")
    
    generated_count = 0
    
    for tag in all_tags:
        tag_slug = generate_tag_slug(tag)
        filepath = os.path.join(tags_dir, f"{tag_slug}.md")
        
        # Frontmatter per pagina tag
        frontmatter = f"""---
layout: ob_tag
tag_name: "{tag}"
title: "Tag: {tag}"
permalink: /tags/{tag_slug}/
meta_title: "tag-{tag_slug}"
meta_description: "Tutti i contenuti con tag '{tag}'"
---

"""
        
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(frontmatter)
            print(f"✅ [OK] Tag page: {tag} → {filepath}")
            generated_count += 1
        except Exception as e:
            print(f"ERROR writing {filepath}: {str(e)}")
    
    print(f"--- TAG PAGES: Generati {generated_count} file. ---")

def generate_top_tags_data():
    """Genera file _data/top_tags.yml con i 5 tag più popolari."""
    print("Inizio generazione TOP TAGS data...")
    
    data_dir = "_data"
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        print(f"Creata directory {data_dir}")
    
    all_tags = get_all_tags_from_files()
    
    if not all_tags:
        print("Nessun tag trovato, creo file vuoto")
        top_tags = []
    else:
        tag_counts = {}
        md_files = []
        
        content_dirs = ["ob-session", "ob-ai", "ob-progetti", "ob-archives"]
        
        for dir_name in content_dirs:
            if os.path.exists(dir_name):
                for root, dirs, files in os.walk(dir_name):
                    for file in files:
                        if file.endswith(".md"):
                            md_files.append(os.path.join(root, file))
        
        for filepath in md_files:
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                    
                    if content.startswith("---"):
                        parts = content.split("---", 2)
                        if len(parts) >= 3:
                            frontmatter = parts[1]
                            
                            # Cerca sezione tags nel frontmatter
                            in_tags_section = False
                            for line in frontmatter.split("\n"):
                                line_stripped = line.strip()
                                
                                # Inizio sezione tags
                                if line_stripped.startswith("tags:"):
                                    in_tags_section = True
                                    # Gestisci formato inline: tags: ['tag1', 'tag2']
                                    if "[" in line:
                                        import re
                                        tags_match = re.search(r'\[(.*?)\]', line)
                                        if tags_match:
                                            tags_str = tags_match.group(1)
                                            for tag in tags_str.split(","):
                                                tag = tag.strip().strip('"').strip("'")
                                                if tag:
                                                    tag_counts[tag] = tag_counts.get(tag, 0) + 1
                                        in_tags_section = False
                                    # Se non c'è array inline, continua a leggere le righe successive
                                    continue
                                
                                # Se siamo nella sezione tags, processa le righe
                                if in_tags_section:
                                    # Fine sezione tags (nuova chiave YAML)
                                    if line_stripped and not line_stripped.startswith("- ") and ":" in line_stripped and not line_stripped.startswith("#"):
                                        in_tags_section = False
                                        continue
                                    
                                    # Tag in formato lista YAML: - Tag Name
                                    if line_stripped.startswith("- "):
                                        tag = line_stripped[2:].strip().strip('"').strip("'")
                                        if tag:
                                            tag_counts[tag] = tag_counts.get(tag, 0) + 1
                                    # Se la riga è vuota o solo spazi, continua (potrebbe essere parte della lista)
                                    elif not line_stripped:
                                        continue
                                    # Altrimenti, fine sezione tags
                                    else:
                                        in_tags_section = False
            except Exception as e:
                print(f"WARN: Errore lettura {filepath}: {str(e)}")
        
        sorted_tags = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)
        top_5 = sorted_tags[:5]
        
        top_tags = [{"name": tag, "count": count, "slug": generate_tag_slug(tag)} for tag, count in top_5]
        
        tag_list = ', '.join([f"{t['name']} ({t['count']})" for t in top_tags])
        print(f"Top 5 tag: {tag_list}")
    
    filepath = os.path.join(data_dir, "top_tags.yml")
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write("# Top 5 most popular tags\n")
            f.write("# Generated automatically by notion_to_jekyll_builder.py\n\n")
            for tag_data in top_tags:
                f.write(f"- name: \"{tag_data['name']}\"\n")
                f.write(f"  count: {tag_data['count']}\n")
                f.write(f"  slug: \"{tag_data['slug']}\"\n")
        print(f"✅ [OK] Top tags data: {filepath}")
    except Exception as e:
        print(f"ERROR writing {filepath}: {str(e)}")

if __name__ == "__main__":
    generate_tag_pages()
    generate_top_tags_data()

