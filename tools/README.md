# Tools - Notion to Jekyll Builder

Strumenti per la conversione automatica di contenuti Notion in file Markdown per Jekyll.

## Architettura Modulare

Il sistema è stato refactorizzato in un'architettura modulare completa. Vedi `SPEC_PROCESSORS.md` nella root del progetto per i dettagli completi.

## Installazione

### 1. Dipendenze Python

Installa le dipendenze necessarie:

```bash
pip install -r ../requirements.txt
```

Oppure manualmente:

```bash
pip install requests pyyaml python-dotenv
```

### 2. Configurazione

Copia il file di esempio e configura le tue credenziali Notion:

```bash
cp notion_config.py.example notion_config.py
# Edita notion_config.py con le tue credenziali
```

**⚠️ IMPORTANTE**: `notion_config.py` è nel `.gitignore` e NON viene committato. 
Non condividere mai le tue credenziali!

### Variabili d'Ambiente (alternativa)

Puoi anche usare variabili d'ambiente invece di `notion_config.py`:

```bash
export NOTION_TOKEN="your_token_here"
export DB_CONTENT_ID="your_db_id"
export DB_PERSONAS_ID="your_personas_db_id"
export DB_PROJECT_ID="your_project_db_id"
```

Questo è utile per GitHub Actions (usa GitHub Secrets).

## Uso

### Esecuzione Locale

```bash
python notion_to_jekyll_builder.py
```

### GitHub Actions

Lo script può essere eseguito automaticamente tramite GitHub Actions.
Vedi `.github/workflows/notion-sync.yml` per la configurazione.

## Struttura Moduli

```
tools/
├── notion_jekyll/          # Package modulare principale
│   ├── api/                # Notion API client
│   ├── converters/         # Convertitori Notion → Markdown
│   ├── generators/         # Generatori file (tag, etc.)
│   └── processors/         # Processori contenuti
├── notion_to_jekyll_builder.py  # Entry point
└── notion_config.py.example     # Template configurazione
```

## File da Committare

✅ **SI committano**:
- Tutti i moduli in `notion_jekyll/`
- `notion_to_jekyll_builder.py`
- `notion_config.py.example` (template)
- `README.md` (questa documentazione)

❌ **NON committare**:
- `notion_config.py` (contiene credenziali)
- `__pycache__/` (cache Python)
- `*.pyc` (bytecode Python)

## Sviluppo

### Test Import Moduli

```bash
cd tools
python3 -c "from notion_jekyll.orchestrator import main; print('OK')"
```

### Aggiungere Nuovi Moduli

1. Crea il modulo nella cartella appropriata (`processors/`, `generators/`, etc.)
2. Aggiorna `__init__.py` della cartella per esportare la classe/funzione
3. Aggiorna l'orchestrator se necessario

Vedi `SPEC_PROCESSORS.md` nella root del progetto per i dettagli completi.

## Troubleshooting

### ModuleNotFoundError

Assicurati che `tools/` sia nel `PYTHONPATH` o esegui lo script dalla directory `tools/`:

```bash
cd tools
python notion_to_jekyll_builder.py
```

### Credenziali Non Trovate

- Verifica che `notion_config.py` esista e contenga le credenziali corrette
- Oppure verifica che le variabili d'ambiente siano impostate
- Controlla che le credenziali siano valide in Notion

### Errori di Import

Se vedi errori di import, verifica che tutti i `__init__.py` esistano in ogni sottocartella.
