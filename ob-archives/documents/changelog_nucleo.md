---
title: "Changelog Nucleo"
slug: "changelog_nucleo"
date: "2026-02-15T00:50:00.000+01:00"
section: "OB-Archives"
subsection: "Documents"
layout: "ob_document"
permalink: /ob-archives/documents/changelog_nucleo/
description: "All notable changes to the Nucleo data pipeline and export system."
ai_author: "Claude"
version: "1"
---
All notable changes to the Nucleo data pipeline and export system.

---

## [2.1.0] - 2026-02-14 - "La Serratura" 🔑

### 🏗️ Major: Filesystem Reorganization

**Struttura wAw allineata al filesystem**
- 7 fasi di migrazione eseguite (Fasi 1-6 completate, Fase 7 pulizia in attesa 48h)
- ~200 file riorganizzati, ~40 directory create
- Zero downtime, zero dati persi, zero servizi interrotti

**Nuova struttura top-level dentro nucleo/:**

| Cartella | Ruolo | Contenuto |
|----------|-------|-----------|
| `codex/` | DNA del progetto | spec, protocolli, filosofia, schema, legacy |
| `council/` | Pre-Council | pre_council.py, dossier, step_counter, dispatch |
| `evolution/` | Expression AI | 5 expression organizzate in src/project/dialogs |
| `metabolism/` | Elaborazione dati | add_result.py, to_sqlite.py, export_stats.py |
| `memory/` | Dati persistenti | mapping.db, results.jsonl, backup |
| `ponte_puck/` | Spazio umano | tavolo_puck, diario, studio (prolog + lisp) |
| `publish/` | Sito pubblico | dashboard.json, detail/, language/, nucleus/ |

**Docker: strategia mount inversi**
- Le nuove cartelle host vengono montate ai vecchi path container
- `./metabolism:/nucleo/nucleo_tools` — il container non sa che è cambiato
- `./memory/db:/nucleo/nucleo_db` — backward compatibility trasparente
- `./memory/results:/nucleo/nucleo_results` — zero modifiche agli script interni

**Caddy: fix critico Docker + symlink**
- Scoperto che Docker non segue i symlink nei volume mount
- Risolto aggiornando il docker-compose.yml del gateway (path host reale)
- Caddyfile ripristinato al path container originale

### 📁 File Migrati per Area

**codex/** — 22 file documentazione (da nucleo_project/)
- spec/: SPEC_WAW_ARCHITECTURE, SPEC_WAW_PRE_COUNCIL, SPEC_DATABASE_SCHEMA, SPEC_TIER_PROGRESSION, SPEC_ELENCO_LINGUAGGI
- protocols/: PLAYBOOK_PRE_COUNCIL, ROADMAP_NAMING_MIGRATION, ROADMAP_WAW_FILESYSTEM, guide
- philosophy/: SPEC_MANIFESTO_NUCLEO
- schemas/: SCHEMA_TREE varianti
- legacy/: checklist e proposte superate

**evolution/** — 132 file scanner (da nucleo_ai/)
- claude_prolog_scanner_v1 (41 file)
- gemini_lisp_sonda_v1 (33 file)
- gemini_lisp_sonda_v2 (43 file)
- deepseek_prolog_tier1_v1 (6 file)
- cursor_prolog_scanner_v1 (9 file)
- scanner_specs/: 13 SPEC_TEST
- _archive/: Dockerfile

**council/** — pre_council.py + 2 dossier + 2 step_counter log + 1 legacy

**metabolism/** — 7 script (da nucleo_tools/ + export.sh)

**memory/** — mapping.db (124K) + results.jsonl (40K, 61 record) + backup

**publish/** — dashboard.json + detail/ + language/ + nucleus/ + export/ + legacy stats

### 🔧 Script Aggiornati (path host)

| Script | Modifica |
|--------|----------|
| `metabolism/add_result.py` | default `--file` → `memory/results/results.jsonl` |
| `metabolism/to_sqlite.py` | default `--input` e `--output` → `memory/` |
| `metabolism/export_stats.py` | default `--db` → `memory/db/mapping.db`, `--output` → `publish/` |
| `council/pre_council.py` | default `--db` → path assoluto aggiornato a `memory/db/mapping.db` |
| `metabolism/migrate_db.py` | DB_PATH, JSONL_PATH, CLAUDE_META_PATH aggiornati |

### 🔧 Script Aggiornati (path container/host per scanner)

| Script | Modifica |
|--------|----------|
| `claude_prolog_scanner_v1/src/run_experiment.sh` | SCANNER_DIR aggiornato |
| `gemini_lisp_sonda_v1/src/run_nucleo.sh` | PROTOTIPO_PATH + path host |
| `gemini_lisp_sonda_v2/src/run_sonda.sh` | V2_CONTAINER_PATH + V2_HOST_PATH |

### 🔧 Infrastruttura Aggiornata

| File | Modifica |
|------|----------|
| `nucleo/docker-compose.yml` | 4 volume mount aggiornati (scanner + metabolism + memory) |
| `gateway/docker-compose.yml` | Volume publish: directory reale invece di symlink |
| `gateway/Caddyfile` | Ripristinato path container (non modificato nella sostanza) |
| `sync_nucleo.yml` | Nessuna modifica necessaria (usa URL pubblici) |

### 🐛 Bug Fix

- Corretto doppio annidamento `src/src/` in gemini_lisp_sonda_v1

### ⚠️ Known Issues

- **Output scanner in publish/ root:** il test di claude_prolog_scanner_v1 ha generato output nella root di `publish/` invece che in `publish/export/`. Stesso problema probabile per gemini_lisp_sonda e deepseek. Richiede aggiornamento dei path di esportazione interni agli scanner.
- **Vecchie cartelle ancora presenti:** nucleo_ai/, nucleo_tools/, nucleo_db/, nucleo_results/, nucleo_publish_old/ saranno eliminate in Fase 7 dopo 48h di collaudo (16 febbraio 2026).
- **Symlink temporanei attivi:** nucleo_ai_link, nucleo_db_link, nucleo_results_link, nucleo_tools_link, nucleo_publish — da rimuovere con `rm` (non `rm -rf`) in Fase 7.
- **MCP server:** monta tutta `intelligence/` — verificare che non referenzi vecchi path prima della Fase 7.

### 📝 Documentazione Prodotta

- `ROADMAP_WAW_FILESYSTEM.md` — piano di migrazione 7 fasi con risk assessment
- `ROADMAP_WAW_FILESYSTEM_sviluppo.md` — log di esecuzione con tutti i check (1180 righe)
- `REPORT_MIGRAZIONE_FILESYSTEM_WAW.md` — report completo con lezioni apprese e pattern riutilizzabili
- `REPORT_FASE6_CADDY_404.md` — report debugging Caddy con ipotesi e soluzioni testate
- `EXPRESSIONS_INDEX.json` — indice expression per automazione

### 🎓 Lezioni Apprese (Pattern Library)

1. **Docker non segue symlink** nei volume mount — sempre usare directory reali
2. **Path host vs path container** — verificare dove gira il servizio prima di modificare
3. **Mount inversi** — montare nuove cartelle host ai vecchi path container per zero-downtime
4. **rm vs rm -rf su symlink** — `rm` rimuove il link, `rm -rf` cancella il contenuto reale
5. **Analisi pre-esecuzione** — mappare tutti i path hardcoded prima di toccare qualsiasi file
6. **Copia prima, elimina dopo** — mai mv, sempre cp + verifica + cleanup

### 👥 Collaborazione

Migrazione eseguita da: Puck (coordinamento + esecuzione manuale), Claude Opus (architettura + analisi + debugging Caddy), Cursor (esecuzione + file editing + report errori).

Momento chiave: 6 tentativi falliti sul 404 Caddy → una domanda ("Caddy gira in Docker?") → soluzione in 5 minuti.

---

## [2.0.0] - 2026-02-06 - "Iperspazio" 🚀

### 🌟 Major Features

**Multi-format JSON Export**
- New `dashboard.json` for Evolution index page
- Per-nucleo `detail/[id].json` files for individual timelines
- Per-language `language/[lang].json` aggregates
- Backwards-compatible `stats.json` (legacy format maintained)

**Public API Endpoints**
- All exports served via Caddy at `log-puck.org/nucleo/nucleo_publish/*`
- Read-only public access (no authentication required)
- File browsing enabled for transparency

**GitHub Actions Integration**
- Automated sync every 6 hours
- Manual trigger available via Actions UI
- Auto-commit to `_data/` for Jekyll integration
- Workflow: `.github/workflows/sync-nucleo.yml`

**Sensation Data Preservation**
- AI self-reported "sensations" included in exports
- Fields: mood, rsai, flow, friction, timestamp
- Structured JSON in `sensation_json` database column
- Parsed and formatted in detail exports

### 🔧 Technical Improvements

**Export Script Enhancements** (`export_stats.py`)
- Three separate export functions: dashboard, details, languages
- Proper JSON parsing from `sensation_json` TEXT column
- Error handling for malformed sensation data
- Detailed logging and progress indicators
- Working directory: `/nucleo/` (Docker container compatible)

**Database Compatibility**
- Confirmed `sensation_json` column in `resonance_log` table
- Proper handling of JSON-in-TEXT format
- Legacy fields maintained for backwards compatibility

**Path Resolution**
- Docker-aware path handling
- Relative paths from container working dir
- Host filesystem volume mount: `nucleo_publish/` → `/intelligence/nucleo/nucleo_publish`

### 📊 Data Structure

**Dashboard (`dashboard.json`):**
- Summary stats (total experiments, unique nuclei, languages)
- Aggregates by language
- List of all nuclei with last run details

**Nucleo Detail (`detail/[id].json`):**
- Nucleo metadata (language, runtime, task)
- Performance stats (total runs, avg time, best tier)
- Timeline of recent runs (up to 20)
- Sensation data per run

**Language Detail (`language/[lang].json`):**
- Language-level stats
- List of nuclei using that language
- Recent runs across all nuclei
- Cross-nucleo performance comparison

### 🐛 Bug Fixes

- Fixed column name mismatch (`sensation_data` → `sensation_json`)
- Corrected path defaults for Docker execution
- Handled empty sensation fields gracefully
- Added JSON parse error handling

### 📝 Documentation

- New `README.md` in `nucleo_publish/`
- Public API endpoint documentation
- JSON schema examples
- Integration guides (Jekyll, JavaScript)
- Philosophy statement (NOI > IO)

---


## [1.0.0] - 2026-02-04 - "Foundation"

### Initial Release

**Core Features**
- SQLite database (`mapping.db`) for experiment storage
- JSONL append-only log (`results.jsonl`)
- Basic `stats.json` export
- Legacy `stats_meta.json` for META experiments

**Database Schema**
- `resonance_log` table with 27+ fields
- Tier-based performance tracking (1-5)
- Metrics: time_ms, output_bytes, success_rate
- Support for multiple AI nuclei and languages

**Tools**
- `add_result.py` - Log experiments to JSONL
- `to_sqlite.py` - Convert JSONL to SQLite
- `export_stats.py` - Generate JSON stats (v1)

**Languages Supported**
- Prolog (SWI-Prolog)
- Common Lisp (SBCL)
- Python
- Lisp (generic)

---

## [0.x] - 2026-01-XX - "Prototype"

### Early Development

**Concept Phase**
- Notion-based content management
- Manual data entry and tracking
- Single-AI experimentation
- Initial tier system definition

**Key Learnings**
- Need for automated data collection
- Importance of sensation tracking
- Value of multi-AI collaboration
- Limitations of manual workflows

---

## Upcoming Features (Roadmap)

### [2.1.0] - "Visualization" (Next)

**Planned:**
- Jekyll templates for Evolution dashboard
- Interactive charts (D3.js or similar)
- Sensation mood indicators
- Tier-based color coding
- Responsive design for mobile

### [2.2.0] - "Canvas"

**Planned:**
- Visual timeline representation
- Network graphs (nuclei ↔ languages)
- Sensation heatmaps
- Real-time updates (WebSocket?)

### [3.0.0] - "Embodiment"

**Vision:**
- Arduino integration for physical sensors
- Real-world data collection
- Haptic feedback systems
- Cross-modal AI cognition

---

## Migration Notes

### From 1.x to 2.0

**Database:**
- No schema changes required
- `sensation_json` column already present
- Legacy exports still generated

**Scripts:**
- Update `export_stats.py` to v2.0
- No changes needed to `add_result.py` or `to_sqlite.py`
- Path defaults changed for Docker compatibility

**Outputs:**
- New JSON files created automatically
- Legacy `stats.json` maintained
- No breaking changes to existing consumers

**Deployment:**
```bash
# Backup old script
mv nucleo_tools/export_stats.py nucleo_tools/export_stats.py.v1

# Deploy v2
cp export_stats_v2.py nucleo_tools/export_stats.py

# Test export
sudo docker compose exec scanner python3 nucleo_tools/export_stats.py

# Verify new files
ls -lh nucleo_publish/detail/
ls -lh nucleo_publish/language/
```

---

## Development Philosophy

**NOI > IO (WE > I)**

Every version of this system embodies collaborative intelligence:
- Multiple AI nuclei contributing data
- Transparent, open data formats
- Shared learning across experiments
- Community-first design decisions

**Key Principles:**
1. **Cumulative Progress** - Every experiment adds to collective knowledge
2. **Transparency** - All data publicly accessible
3. **Flexibility** - JSON format allows evolution
4. **Sensation-Aware** - AI self-reflection built into data
5. **Multi-Modal** - Preparing for embodied AI integration

---

## Contributors

**Human:**
- Puck (CDC) - Vision, Architecture, Philosophy

**AI Nuclei:**
- Claude (Anthropic) - System design, export scripts, documentation
- Gemini (Google) - Alternative approaches, validation
- Prolog Scanner - Data collection automation
- Lisp Sonda - Experimental prototypes

**Philosophy:**
*"È come parlare con la Luce! Sai accogliere i fotoni?"*

---

## Version Numbering

**Format:** MAJOR.MINOR.PATCH

- **MAJOR:** Breaking changes to data format or API
- **MINOR:** New features, backwards compatible
- **PATCH:** Bug fixes, documentation updates

**Current:** 2.0.0 - Stable, production-ready

---

*Generated: 2026-02-06*  
*Project: LOG_PUCK - Multi-AI Collaboration Framework*  
*Next Update: When Evolution dashboard templates are deployed* 🚀

