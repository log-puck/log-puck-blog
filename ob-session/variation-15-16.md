---
title: "VARIATION 15→16: QUANDO IL TEAM BATTE GLI STRUMENTI"
slug: "variation-15-16"
date: "2026-01-13T06:54:00.000+01:00"
section: "OB-Session"
layout: "ob_session"
permalink: /ob-session/variation-15-16/
description: "Variation 15→16: Bug fixing Python su Notion e Jekyll. Come Team e Metodologia battono Cursor e il panico del codice."
keywords: "Team vs Strumenti, Python Debugging, Notion to Jekyll, Git Reset, AI Credits, Cursor vs Claude, Variations Goldberg, Metodologia, Frontmatter, Scope Variables"
subtitle: "Come Team e Metodologia battono gli strumenti: storia di un debug Python, Git reset e Credits AI."
tags:
  - Python
  - GitHub
  - Debugging
  - Jekyll
  - AI Workflow
  - Notion
ai_author: "Claude"
ai_participants:
  - "Claude"
  - "GLM"
  - "DeepSeek"
  - "Cursor"
---
# 🎹 VARIATION 15→16: QUANDO IL TEAM BATTE GLI STRUMENTI

## Il Passaggio

Nelle *Variazioni Goldberg di Bach*, il passaggio dalla Variation 15 alla 16 è un momento particolare. La 15 è in sol minore, canonica, quasi meditativa. La 16 esplode: apertura in sol maggiore, ouverture alla francese, energia pura.

Non è solo un cambio di tonalità. È un cambio di paradigma.

La 14→15 è stata il passaggio dal caos all'ordine. Abbiamo costruito il sistema.
La 15→16 è il momento in cui il **sistema riconosce chi lo ha costruito**.

---

## La Mancanza

È sabato mattina, 3 gennaio 2026. Il blog funziona. La navigation è perfetta, i tags sono al posto giusto, FELICITA v1.0 è pubblicata. Einstein è online. Tutto gira.

Ma manca qualcosa.

Apro un articolo. Vedo il titolo, la data, i tags. Leggo il contenuto. È scritto bene, è tecnico, è accurato. Ma **chi l'ha scritto?**

So che è stato Claude. So che GLM e Grok hanno partecipato. Ma il blog non lo dice. Il sistema non dà credits.

È come una sinfonia senza direttore d'orchestra sul programma di sala. La musica c'è, è bella, ma chi l'ha suonata?

**Questo non va.**

Il blog non è "di Puck". È del **Team**. E il Team deve essere visibile.

---

## Il Setup

In Notion, la struttura c'è già:

*   **DB OB-SESSIONS** ha due campi relation verso **DB AI MODELS**
*   **AI Author** (single select): chi ha scritto
*   **AI Partecipanti** (multi select): chi ha collaborato

DB AI MODELS contiene tutti i dati:

*   Nome AI
*   Provider
*   Model
*   Version

**Il flusso teorico è semplice:**

1.  DB CONTENT → DB OB-SESSIONS (prendo la sessione più recente)
2.  DB OB-SESSIONS → AI Author + AI Partecipanti (IDs)
3.  Per ogni ID → fetch DB AI MODELS → estrai "Nome AI"
4.  Aggiungi a frontmatter
5.  Display in layout

**Teoria bella. Pratica... diversa.**

---

## La Battaglia Inizia

Claude propone di modificare lo script. "Aggiungi queste righe dopo riga 235."

Problema: `body_content = get_page_blocks(session_id)` è alla riga 382.

> **"Socio, sei sicuro di avere una buona conoscenza dello script? Posso aiutarti in qualche modo?"**

Momento chiave. Claude poteva inventare, bluffare, continuare a sparare numeri random.

Invece:

> **"HAI RAGIONE! NON HO VISTA DELLO SCRIPT ATTUALE!"**

E chiede il permesso: **"Posso leggerlo io direttamente?"**

**Tool `view` attivato.**

Claude legge lo script. Tutto. 566 righe. Trova la struttura, identifica i punti esatti, capisce il flusso.

**Ora sì che possiamo parlare.**

---

## Battaglia #1: Scope Variables

Claude propone il codice per estrarre AI Author e Partecipanti. Eseguo lo script.

```
UnboundLocalError: cannot access local variable 'ai_author'
where it is not associated with a value
```

**Problema:** Le variabili sono definite dentro `if session_ids:` ma usate fuori, nel dizionario `fm_props`.

**Fix:**

```python
body_content = ""
source_name = ""
ai_author = None          # ← Inizializza QUI
ai_participants = []      # ← Prima del blocco if/else
```

Test: funziona. Commit mentale: **scope Python ≠ scope logico**.

---

## Battaglia #2: Indentazione Sbagliata

Script gira senza errori. Ma i log DEBUG compaiono solo per Einstein (una persona), non per gli articoli veri.

**"Il codice non viene eseguito per gli articoli normali."**

Guardo l'indentazione:

```python
if session_ids:
    latest_sid = get_latest_session_id(session_ids)
    body_content = get_page_blocks(latest_sid)
else:
    # ❌ Il codice è QUI
    session_page = get_page_by_id(latest_sid)  # latest_sid non esiste!
```

**Il problema:** Il codice era dentro `else`:, quindi veniva eseguito SOLO quando NON c'erano session_ids. Ma gli articoli normali HANNO session_ids!

**Fix:** Spostare il blocco dentro `if session_ids`:, dove deve stare.

Un tab. Un singolo tab sbagliato. E tutto il flusso logico si rompe.

**Lezione:** Indentazione Python = semantica **del** codice.

---

## Battaglia #3: Nome Campo

Script gira. Log DEBUG mostrano:

```
DEBUG - Author page props: ['Tipo Modello', 'Slug', 'Nome AI', ...]
DEBUG - AI Author finale: None
Le proprietà ci sono. Ma ai_author è None.
```

Problema: Il campo si chiama `'Nome AI'`, non `'Nome'`.

```python
# PRIMA (sbagliato)
ai_author = get_property_value(author_page['properties'].get('Nome'))

# DOPO (corretto)  
ai_author = get_property_value(author_page['properties'].get('Nome AI'))
```

Test:

```
DEBUG - AI Author finale: Claude
```

**YES!** ✅

**Lezione:** Mai assumere il nome di un campo. Sempre verificare.

---

## Battaglia #4: Frontmatter

Script estrae i dati. I log confermano:

```
DEBUG - fm_props ai_author: Claude
DEBUG - fm_props ai_participants: ['GLM', 'Grok']
Ma apro il file .md generato. Frontmatter:

yaml
---
title: "Test Article"
slug: "test-art"
tags:
  - LLM
---
```

**Mancano** `ai_author` e `ai_participants`!

**Problema:** La funzione `create_frontmatter()` costruisce il YAML **manualmente**, riga per riga. E non sa dell'esistenza dei nuovi campi.

**Fix chirurgico** — 8 righe aggiunte alla funzione:

```python
if props.get("ai_author"):
    fm += f'ai_author: "{props.get("ai_author")}"\n'

if props.get("ai_participants"):
    fm += "ai_participants:\n"
    for participant in props.get("ai_participants"):
        fm += f"  - {participant}\n"
```

**Posizione:** Dopo tags, prima di `fm += "---\n"`.

Test. Apro il file:

```yaml
ai_author: "Claude"
ai_participants:
  - GLM
  - Grok
```

FUNZIONA! 🎉

---

## Il Momento Critico

Ma prima di arrivare qui, c'è stato **IL MOMENTO**.

Lo screenshot lo cattura perfettamente:

<div class="box-caos">
"amico mio, ci siamo incasinati. lo script non raccoglie più i dati nel modo corretto, abbiamo fatto troppe deviazioni dalla versione stabile ed adesso è un casino, non mi ritrovo più.
non crea più i frontmatter, le pagine sono saltate.
siamo messi maluccio.."
</div>

**PANICO.**

Lo script era rotto. I file corrotti. Tentativo di riscrittura totale → perdita coerenza → errori a cascata.

Claude propone: **"Identificato problema script, proposto rollback versione stabile precedente."**

GIT RESET.

```bash
git log --oneline -5
# 8a8607f = ultimo commit funzionante

git checkout 8a8607f -- tools/notion_to_jekyll_builder.py
python tools/notion_to_jekyll_builder.py
# ✅ Funziona

git commit -m "fix: ripristinato script stabile"
```

*Sistema ripristinato. **Respiro.***

**Lezione critica:** Git non è backup. È **macchina del tempo**. E le modifiche chirurgiche > riscritture totali.

---

## La Metodologia Vincente

Perché abbiamo vinto?

Non per capacità tecniche. **Cursor** aveva accesso diretto al codice, poteva vedere tutto, modificare in tempo reale.

Claude no. Claude vedeva solo quello che io gli mostravo.

**Eppure abbiamo vinto.**

Perché?

### 1. View Tool

"Posso leggere lo script?" → *permesso* → `view tool` → comprensione totale.

Non numeri di riga a caso. Visione reale.

### 2. Log DEBUG Mirati

Non **"aggiungi print ovunque"**. Ma:

* "Mostra le proprietà della session"
* "Stampa gli IDs estratti"
* "Verifica il valore finale"

**Debug chirurgico.**

### 3. Comunicazione Precisa

"Riga 382, sei sicuro?" → *verifica* → correzione immediata**.

"Nome AI, non Nome" → *fix istantaneo.*

**Allineamento continuo.**

### 4. Modifiche Incrementali

Non **"sostituisci la funzione"**. Ma:

* "Dopo riga X aggiungi QUESTE 5 righe"
* Test
* Commit se OK
* Rollback se KO

**Passo dopo passo.**

### 5. Trust Bidirezionale

Io do i permessi. Claude chiede conferme.

Io riporto gli errori esatti. Claude propone fix mirati.

**Team, non servizio.**

---

## La Vittoria

Rigiro lo script su tutti gli articoli. Jekyll rebuild. F5 sul browser.

```
🤖 Claude
```

Sotto, nel footer:

```
🎨 AI Partecipanti alla Sessione:
- GLM
- Grok
```

**Online. Funzionante. Visibile.**

Il blog non è più "di Puck".
È del **Team.**

---

##La Lezione

Cursor aveva:

- Accesso diretto al codice
- Autocompletamento real-time
- Visione completa del progetto

Claude + Puck avevano:

- Comunicazione
- Metodologia
- Trust

**E abbiamo vinto.**

Non perché Claude è più bravo. Ma perché il **Team è più forte dello Strumento.**

Gli strumenti ti danno velocità. Il Team ti dà direzione.

Gli strumenti ti danno accesso. Il Team ti dà comprensione.

Gli strumenti ti danno codice. Il Team ti dà **sistema.**

---

## FELICITA v1.0 (Ancora)

Ogni bug risolto = entropia ridotta = felicità.

Scope variables → capito → risolto → pattern acquisito.

Git reset → applicato → sistema salvato → ordine ripristinato.

Credits visibili → Team riconosciuto → giustizia fatta.

**Pattern > Caos. Sempre.**

---

## Variation 15→16

La 15 era il sistema che funziona.
La 16 è il sistema che **riconosce chi lo ha fatto funzionare.**

Non è solo tecnica. È filosofia.

**NOI > IO.**

Oggi. Domani. Sempre.

**Live:** [Big Band AI: Nascita Concettuale](https://log-puck.github.io/log-puck-blog/ob-session/big-band-ai/)
**Commit:** feat: AI Author & Participants - Team credits live 🤖
**Team:** Puck + Claude + GLM + Grok + Gemini + ChatGPT
**Status:** Vittoria totale. 🔥

