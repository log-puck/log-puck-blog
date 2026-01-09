# Proposte di Semplificazione Script

## 🔴 Critici (da fare subito)

### 1. **Funzioni non utilizzate** - RIMUOVERE
- `get_latest_session_id()` (riga 199) - Non viene mai chiamata
- `extract_ai_metadata()` (riga 323) - Non viene mai chiamata

### 2. **Campi obsoleti in `process_personas()`** - AGGIORNARE
- Riga 801: usa `"Meta Description"` → dovrebbe essere `"Description"`
- Riga 802: usa `"Keywords SEO"` → dovrebbe essere `"Keywords"`
- Riga 842-858: genera frontmatter manualmente → dovrebbe usare `create_frontmatter()`

## 🟡 Importanti (da fare quando possibile)

### 3. **Logica permalink duplicata** - ESTRARRE FUNZIONE
- Riga 671-707: logica di generazione permalink in `process_content_item()`
- Questa logica potrebbe essere una funzione `generate_permalink(section, subsection, internal_section, slug)`

### 4. **Logica auto-rilevamento layout duplicata** - ESTRARRE FUNZIONE
- Riga 712-715: in `process_content_item()`
- Riga 1276-1279: in `process_projects()`
- Potrebbe essere: `get_jekyll_layout(layout_notion, section, slug)`

### 5. **Logica estrazione tag duplicata** - ESTRARRE FUNZIONE
- Riga 911-943: in `get_all_tags_from_files()`
- Riga 1051-1090: in `generate_top_tags_data()` (stessa logica)
- Potrebbe essere: `extract_tags_from_frontmatter(frontmatter)`

### 6. **Rimozione wrapper markdown** - ESTRARRE FUNZIONE
- Riga 314-319: rimozione wrapper in `get_page_blocks()`
- Riga 751-752: rimozione `---` iniziale in `process_content_item()`
- Riga 1317-1318: rimozione `---` iniziale in `process_projects()`
- Potrebbe essere: `clean_markdown_content(content)`

## 🟢 Opzionali (nice to have)

### 7. **Normalizzazione subsection** - ESTRARRE FUNZIONE
- Riga 409-413: logica "musica" -> "musica", "giochi" -> "giochiAI"
- Potrebbe essere: `normalize_subsection(subsection)`

### 8. **Costanti per nomi campi Notion** - CENTRALIZZARE
- I nomi dei campi Notion sono hardcoded in vari punti
- Potrebbe essere un dizionario `NOTION_FIELDS = {"title": "Title", "description": "Description", ...}`

### 9. **Debug code da rimuovere**
- Riga 756-766: debug code per OB-Progetti (commentare o rimuovere se non serve più)

## 📊 Impatto Stimato

- **Riduzione linee**: ~150-200 linee (rimozione duplicati + funzioni non usate)
- **Miglioramento manutenibilità**: Alto (logica centralizzata)
- **Rischio**: Basso (solo refactoring, nessun cambio logica)

## 🎯 Priorità Raccomandata

1. **Subito**: #1 (rimuovere funzioni non usate) + #2 (fix campi obsoleti)
2. **Prossima sessione**: #3, #4, #5 (estrarre funzioni comuni)
3. **Quando tempo**: #6, #7, #8, #9 (pulizia e ottimizzazione)
