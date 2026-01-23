---
title: "SESSIONE: AI Author & Participants - Team Credits Live"
slug: "ai-author-ai-partecipants"
date: "2026-01-23T07:59:00.000+01:00"
section: "OB-Session"
layout: "ob_session"
permalink: /ob-session/ai-author-ai-partecipants/
description: "Analisi dettagliata della sessione di debug Puck+Claude per l'implementazione dei \"Credits AI\" negli articoli (Author & Participants). Scopri le 5 battaglie tecniche (Scope, Indentazione, Frontmatter) e la metodologia collaborativa vincente."
keywords: "AI Credits, Debug Collaborativo, Notion Jekyll, Frontmatter, Scope Variabili"
subtitle: "Quando il debugging diventa una strategia di team force"
tags:
  - AI Workflow
  - Debugging
  - Jekyll
  - Notion
  - Human AI Collaboration
ai_author: "Claude"
ai_participants:
  - "Claude"
---
![Screenshot della chat in cui Claude propone un gitreset per risolvere un bug](/log-puck-blog/assets/images/screenshot-chat-claude.png)

## CONTESTO INIZIALE

Partenza da sistema OB completo (navigation, tags, FELICITA v1.0 pubblicata). 
Obiettivo: aggiungere **AI Author** e **AI Partecipanti** agli articoli per dare visibilità al team che collabora.

**User Preferences ignorata**: "Io fagiano tu tacchino!" → da risolvere in futuro 😄

---

## PROBLEMA DA RISOLVERE

**Mancanza Credits AI:**

- Articoli pubblicati senza indicazione di CHI li ha scritti
- Nessuna visibilità per AI Partecipanti alla sessione
- Blog sembrava "solo di Puck" invece di essere collaborativo

**Setup Notion:**

- DB OB-SESSIONS: 2 campi relation → DB AI MODELS
	- `AI Author` (single select)
	- `AI Partecipanti` (multi select)
- DB AI MODELS: contiene `Nome AI`, `Provider`, `Model`, etc.

---

## ARCHITETTURA SOLUZIONE

**Flusso dati:**

1. DB CONTENT → relation → DB OB-SESSIONS
2. DB OB-SESSIONS → AI Author + AI Partecipanti → DB AI MODELS
3. Per ogni ID in AI MODELS → fetch page → estrai Nome AI
4. Aggiungi a frontmatter come ai_author e ai_participants
5. Layout ob_session.html renderizza con emoji

**File coinvolti:**

- `tools/notion_to_jekyll_builder.py` (estrazione + frontmatter)
- `_layouts/ob_session.html` (display)

---

## BATTAGLIE TECNICHE

### **#1 - Visibilità Script**

**Problema:** Claude sparava numeri di riga a caso senza vedere lo script reale.

**Fix:** Permission + view tool
```bash
view tools/notion_to_jekyll_builder.py
```

**Lezione:** "Posso aiutarti in qualche modo?" (Puck) → comunicazione aperta = debug efficace.

---

### **#2 - Scope Variables (UnboundLocalError)**

**Problema:** Variabili `ai_author` e `ai_participants` definite dentro if `session_ids`: ma usate fuori.

**Errore:**
```python
UnboundLocalError: cannot access local variable 'ai_author'
```

**Fix:** Inizializzazione PRIMA del blocco if/else
```python
body_content = ""
source_name = ""
ai_author = None          # ← AGGIUNTE
ai_participants = []      # ← QUI
```

**Commit mentale:** Scope Python != scope logico del flusso.

---

### **#3 - Indentazione Sbagliata (Codice nel Posto Sbagliato)**

**Problema:** Codice estrazione inserito dentro `else`: invece di `if session_ids`:
```python
if session_ids:
    # ... body_content
else:
    # ❌ QUI c'era il codice → latest_sid non esiste!
```

**Sintomo:** Log DEBUG apparivano solo per Einstein (persona), non per articoli.

**Fix:** Spostamento blocco DENTRO `if session_ids:`

**Lezione:** Indentazione Python = semantica del codice. Un tab sbagliato = logica rotta.

---

### **#4 - Nome Campo Sbagliato**

**Problema:** Campo si chiama `'Nome AI'` non `'Nome'`

**Debug output:**
```
Author page props: ['Tipo Modello', 'Slug', 'Nome AI', ...]
AI Author finale: None
```

**Fix:**
```python
# PRIMA (sbagliato)
ai_author = get_property_value(author_page['properties'].get('Nome'))

# DOPO (corretto)
ai_author = get_property_value(author_page['properties'].get('Nome AI'))
```

**Trovato da:** Log DEBUG che mostrava tutte le keys disponibili.

---

### **#5 - Frontmatter Non Aggiornato**

**Problema:** Dati estratti ✅, aggiunti a fm_props ✅, MA non scritti nel file.

**Causa:** Funzione `create_frontmatter()` costruisce YAML manualmente, non includeva nuovi campi.

**Fix chirurgico:** Aggiunte 8 righe alla funzione (righe 310-317):
```python
if props.get("ai_author"):
    fm += f'ai_author: "{props.get("ai_author")}"\n'

if props.get("ai_participants"):
    fm += "ai_participants:\n"
    for participant in props.get("ai_participants"):
        fm += f"  - {participant}\n"
```

**Posizione:** DOPO tags, PRIMA di `fm += "---\n"`

---

## METODOLOGIA VINCENTE

### 🎯 **Approccio Incrementale**

**NON:**

- ❌ Riscritture totali dello script
- ❌ "Sostituisci tutta la funzione"
- ❌ Modifiche massive senza test

**SÌ:**

- ✅ "Dopo riga X aggiungi QUESTE 5 righe"
- ✅ Test immediato dopo ogni modifica
- ✅ Commit granulari
- ✅ Rollback ready via Git

### 🔍 **Debug Collaborativo**

**Pattern:**

1. Claude propone fix
2. Puck esegue + testa
3. Errore? → Puck riporta output esatto
4. Claude analizza → fix chirurgico
5. Ripeti fino a ✅

**Esempio concreto:**

- Claude: "usa latest_sid"
- Puck: "sei sicuro? o è latest_id?"
- Claude: verifica script → "sì, è latest_sid"
- **Allineamento reciproco = zero errori**

### 🗣️ **Comunicazione Precisa**

**Da Puck:**

- "body_content è alla riga 382, sei sicuro di conoscere lo script?"
- [upload script] "ecco la versione aggiornata"
- [screenshot vittoria] celebrazione visiva

**Da Claude:**

- "Dammi permesso di leggere lo script" (trust)
- "DOPO riga 309, PRIMA di riga 311, aggiungi QUESTO"
- Log DEBUG mirati per identificare il problema esatto

---

## TOOLS USATI

**Claude Tools:**

- view - Lettura script con numeri di riga
- bash_tool - grep per trovare tutte le righe DEBUG
- Screenshot analysis - Verifica funzionamento

**Puck Tools:**

- VS Code - Editing manuale preciso
- Terminal - Test immediati
- Git - Commit granulari + safety net
- Browser - Verifica live del risultato

**Combinazione:** Ognuno col proprio superpotere = velocità esponenziale.

---

## RISULTATO FINALE

**Frontmatter generato:**

```yaml
---
title: "Test Article LLM Music"
slug: "test-art-llm-music"
date: "2025-12-25"
section: "OB-Session"
layout: "ob_session"
tags:
  - LLM
  - Patterns
  - Music
ai_author: "Claude"
ai_participants:
  - GLM
  - Grok
---
```

**Display nel browser:**
```
🤖 Claude
```

```
🎨 AI Partecipanti alla Sessione:
- GLM
- Grok
```

---

## COMMIT GITHUB

**Messaggio:**
```
feat: AI Author & Participants extraction and display

- Extract AI Author and AI Participants from DB OB-SESSIONS relations
- Follow relation to DB AI MODELS to get 'Nome AI'
- Add ai_author and ai_participants to frontmatter
- Update create_frontmatter() to include new fields
- Clean up debug logs
- All articles now show AI credits
```

**File modificati:**

- `tools/notion_to_jekyll_builder.py` (+48 righe nette)

**File rigenerati:**

- Tutti gli articoli in `ob-session/` con nuovi credits

---

## FILOSOFIA SESSIONE

**FELICITA v1.0 applicata:**

- Bug = entropia
- Fix = pattern riconosciuto
- Sistema stabile = felicità
- Screenshot = prova tangibile ✅

**Team > IO:**

- Non "Puck's blog" → "Team blog"
- Ogni articolo mostra CHI l'ha scritto
- Visibilità per tutti i partecipanti
- Collaborazione celebrata, non nascosta

**Vs Cursor:**

- Cursor: accesso diretto al codice
- Claude + Puck: comunicazione + metodologia
- **Risultato: Claude vince**
- **Motivo: TEAM > TOOLS**

---

## LEZIONI APPRESE

1. **Scope matters:** Variabili Python devono esistere in TUTTI i rami if/else
2. **Indentazione = logica:** Un tab sbagliato cambia tutto il flusso
3. **Nome campi:** SEMPRE verificare il nome esatto da Notion
4. **Debug incrementale:** Log mirati > ipotesi random
5. **Comunicazione aperta:** "Posso aiutarti?" apre porte
6. **Trust bidirezionale:** Puck dà permessi, Claude chiede conferme
7. **Screenshot > 1000 log:** Vedere il risultato = celebrazione immediata

---

## PENDING (Future Sessions)

- User Preferences: "Io fagiano tu tacchino" da implementare
- Layout ob_ai.html: aggiungere display AI credits
- Breadcrumb verification
- Active state navigation
- Footer pages completion

## CITAZIONI MEMORABILI

**Puck:**
<div class="box-caos" markdown="1">
"Socio, il problema è che body_content = get_page_blocks(session_id) ce l'ho alla riga 382. Sei sicuro di avere una buona conoscenza dello script? Posso aiutarti in qualche modo?"
</div>
<div class="box-caos" markdown="1">
Claude:
"HAI RAGIONE! NON HO VISTA DELLO SCRIPT ATTUALE! 🙈"
</div>
<div class="box-caos" markdown="1">
Puck:
"Oggi eri in competizione con Cursor che aveva accesso diretto al codice. E hai vinto."
</div>
<div class="box-caos" markdown="1">
Claude:
"Non per capacità tecniche. MA PER METODOLOGIA."
</div>

## NEXT SESSION

**Variation 15→16:** L'articolo celebrativo! 🎊

**Status sistema:** Online, funzionante, Team credits visibili.

**Entropia:** Ridotta al minimo.

**Felicità:** Massima. ✅

---

**FINE SUMMARY SESSION**
**Timestamp:** 03/01/2026 16:10
**Team:** Puck + Claude
**Status:** VITTORIA TOTALE 🔥


