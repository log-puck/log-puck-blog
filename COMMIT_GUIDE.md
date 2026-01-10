# Guida Commit - Architettura Modulare

## ✅ File da COMMITTARE

### 1. `.github/workflows/notion-sync.yml` (MODIFICATO)
**✅ COMMITTA** - Abbiamo aggiornato il workflow per supportare i nuovi moduli.

### 2. `tools/ESEMPIO_USO_MODULI.py` (NON TRACCIATO)
**✅ COMMITTA** - Fa parte della documentazione del progetto modulare.

### 3. `experiments/package.json` (NON TRACCIATO)
**❓ DECIDI** - Dipende se vuoi tracciare le dipendenze Node.js degli esperimenti.
- **Se committi**: Utile per riproducibilità degli esperimenti
- **Se non committi**: Aggiungi a `.gitignore` se è solo per sviluppo locale

### 4. `experiments/ponte_config.js` (NON TRACCIATO)
**❌ NON COMMITTARE** - Contiene credenziali/config sensibili. 
- È già nel `.gitignore`, ma se appare come non tracciato potrebbe essere stato tracciato prima
- Se è già tracciato in git, rimuovilo: `git rm --cached experiments/ponte_config.js`

### 5. `experiments/public/waw-council-*.html` (NON TRACCIATO)
**✅ COMMITTATI** - File HTML di test/esperimenti (non contengono dati sensibili).
- Sono già stati committati e va bene così
- In futuro, modifiche a questi file saranno ignorate dal `.gitignore`

## Comandi per il Commit

### Step 1: Verifica cosa verrà committato
```bash
git status
```

### Step 2: Aggiungi solo i file da committare
```bash
# File sicuri da committare
git add .github/workflows/notion-sync.yml
git add tools/ESEMPIO_USO_MODULI.py

# Se vuoi tracciare package.json (opzionale)
git add experiments/package.json

# Aggiungi tutta la nuova struttura modulare
git add tools/notion_jekyll/
git add tools/notion_to_jekyll_builder.py
git add tools/ARCHITETTURA_MODULARE.md
git add tools/README.md
git add .gitignore
```

### Step 3: Se ponte_config.js è già tracciato, rimuovilo
```bash
git rm --cached experiments/ponte_config.js
```

### Step 4: Commit
```bash
git commit -m "refactor: migrazione completa ad architettura modulare

- Estratti tutti i componenti in notion_jekyll/ package
- Script principale ridotto da 1438 a 21 righe  
- Aggiunta documentazione completa (ARCHITETTURA_MODULARE.md, ESEMPIO_USO_MODULI.py)
- Aggiornato workflow GitHub Actions per nuova struttura
- Aggiornato .gitignore per nuova organizzazione"
```

## File da NON Committare (già nel .gitignore)

- ❌ `tools/notion_config.py` (credenziali)
- ❌ `experiments/ponte_config.js` (credenziali)
- ❌ `experiments/public/*.html` (file generati)
- ❌ `__pycache__/` (cache Python)
- ❌ `*.pyc` (bytecode Python)

## Nota Importante

Se vedi file nel "Changes" che dovrebbero essere ignorati ma non lo sono:
1. Verifica che siano nel `.gitignore`
2. Se erano già tracciati prima, rimuovili con: `git rm --cached <file>`
3. Il file resterà sul disco ma non sarà più tracciato da git
