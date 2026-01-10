---
title: "wAw Council - Hybrid Form"
slug: "hybrid-form"
date: "2026-01-09"
section: "OB-Archives"
layout: "ob_document"
permalink: /ob-archives/hybrid-form/
description: "Form flessibile con 3 modalità per Context e Ideas."
keywords: "meta-programmazione, context-engineering, Council-AI"
subtitle: "Form flessibile con 3 modalità per Context e Ideas."
tags:
  - Meta Programmazione
  - Context Engineering
  - AI Council
  - Claude
  - Documents
ai_author: "Claude"
show_footer: false
version: "1"
---
# WAW COUNCIL - HYBRID FORM 🦅
Form flessibile con 3 modalità per Context e Ideas.

---

## COSA FA:

Form flessibile con 3 modalità per Context e Ideas.

---

## MODALITÀ CONTEXT:

### 1. STRUCTURED (Preset)
5 campi fissi:
- Project Name
- Tech Stack  
- Current Focus (textarea 3 righe)
- Completed (textarea 3 righe)
- AI Partners (multiselect checkbox - carica da Notion AI Models DB)

**Quando usare:** Quick voting, formato standard

---

### 2. FREE TEXT (Custom)
Textarea grande (10+ righe)

**Quando usare:** 
- Parlare direttamente alle AI
- Spiegare vision progetto
- Contesto non strutturato
- Test come quello di oggi! ✨

**Esempio:**
```
Ciao, benvenuto nel progetto Log_Puck.
Sono un umano e sto cercando di costruire
un sistema collaborativo human/AI...
```

---

## MODALITÀ IDEAS:

### 1. PRESET
Lista hardcoded nel codice

**Pro:** Veloce, zero setup  
**Contro:** Serve modificare codice per cambiare

---

### 2. NOTION (Checkbox)
Carica da DB WAW_IDEAS con checkbox "Include in Next Vote"

**Setup (una volta):**
1. Vai su Notion → WAW_IDEAS
2. Aggiungi campo: "Include in Next Vote" (Checkbox)
3. Spunta 5-8 idee da votare
4. Form le carica automaticamente!

**Pro:** Flessibile, gestisci da Notion  
**Contro:** Richiede setup iniziale del database Notion

---

### 3. CUSTOM
Textarea - una idea per riga

**Quando usare:**
- Test rapidi
- Idee temporanee
- Non vuoi toccare Notion

**Esempio:**
```
Dark mode toggle
SEO optimization
Footer links
New landing page
```

---

## INSTALLAZIONE:

### 1. File già presente
Il file `waw-council-hybrid.html` è già in `experiments/public/`

### 2. Configurazione Notion (Opzionale)

#### Per modalità "Load from Notion" (Ideas):
```
Database: WAW_IDEAS
New field: "Include in Next Vote"
Type: Checkbox
```

#### Per campo "AI Partners":
```
Database: AI Models
Fields necessari:
- Nome AI (Title)
- Status (Select) con opzione "Active"
```

### 3. Configurazione Backend

```
Database: WAW_IDEAS
New field: "Include in Next Vote"
Type: Checkbox
```

### 4. Testa!

```bash
# Avvia server
cd experiments
node ponte-orchestrator-waw.js

# Apri browser
http://localhost:3000/waw-council-hybrid.html
```

---

## USO:

### Quick Voting (Standard):
1. Context: Structured
2. Ideas: Preset
3. Select AI
4. Call Council

### Deep Conversation (Come oggi):
1. Context: Free Text
2. Scrivi messaggio genuino
3. Ideas: Custom o Preset
4. Select AI (tutti!)
5. Call Council
6. MAGIA! ✨

### Notion-Powered:
1. Vai Notion → Spunta idee
2. Context: Structured o Free
3. Ideas: Load from Notion
4. Select AI
5. Call Council

---

## TIPS:

**Free Text Mode:**
- Scrivi come se parlassi a persone
- Spiega vision, non solo task
- Sii onesto e genuino
- Le AI rispondono meglio! 🔥

**Custom Ideas:**
- Una per riga
- Chiare e concise
- Max 6-8 idee per votazione

**AI Selection:**
- Tutti = massima diversità
- Subset = test specifico
- Minimo 3 per consenso valido

**AI Partners (Context):**
- Multiselect checkbox da Notion AI Models DB
- Filtra automaticamente solo AI con Status = "Active"
- Aggiunge contesto al prompt: "AI Partners: Claude, GLM-4, Gemini"
- Opzionale ma consigliato per tracciabilità

---

## FILES GENERATI:

Ogni chiamata auto-scarica:
- `waw-session-YYYY-MM-DD.json` (dati raw)
- `waw-session-YYYY-MM-DD.md` (report markdown)

---

## COSA CAMBIA DAL FORM VECCHIO:

✅ Context textarea più grandi (3 righe)  
✅ Free text mode completo  
✅ Ideas da Notion (opzionale)  
✅ Ideas custom (quick test)  
✅ **AI Partners multiselect** (carica da Notion AI Models DB)  
✅ Toggle tra modalità  
✅ Stessa UI/UX familiare  

---

## FILOSOFIA:

> "se vi si da un contesto XYZ rispondete come le calcolatrici
> se si utilizza il linguaggio, vi si può far vivere"
> — Puck, 06/01/2026

**Questo form lo permette.** 🎯

---

**NOI > IO**  
**wAw 👁**  
**無**

