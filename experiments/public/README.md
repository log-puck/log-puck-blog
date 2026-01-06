# WAW Council - Hybrid Form 🦅

Form flessibile per il WAW (What AI Want) Council con 3 modalità per Context e Ideas.

## 🎯 Cosa fa

Il Hybrid Form permette di configurare sessioni di votazione del WAW Council con massima flessibilità:
- **Context**: Structured (4 campi) o Free Text (textarea libera)
- **Ideas**: Preset (hardcoded), Notion (da database), o Custom (input manuale)
- **AI Partners**: Multiselect da Notion AI Models database

---

## 📋 Modalità Context

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
- Conversazioni profonde e genuine

**Esempio:**
```
Ciao, benvenuto nel progetto Log_Puck.
Sono un umano e sto cercando di costruire
un sistema collaborativo human/AI...
```

---

## 💡 Modalità Ideas

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

## 🚀 Installazione

### 1. File HTML
Il file `waw-council-hybrid.html` è già presente in `experiments/public/`

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

Aggiungi al `ponte_config.js`:
```javascript
AI_MODELS_DB_ID: 'your-database-id-here'
```

Gli endpoint `/api/notion-ideas` e `/api/ai-models` sono già implementati in `ponte-orchestrator-waw.js`

### 4. Avvia il server

```bash
# Avvia server backend
cd experiments
node ponte-orchestrator-waw.js

# Apri browser
http://localhost:3000/waw-council-hybrid.html
```

---

## 📖 Uso

### Quick Voting (Standard):
1. Context: Structured
2. Ideas: Preset
3. Select AI
4. Call Council

### Deep Conversation:
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

## 💡 Tips

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

## 📁 Files Generati

Ogni chiamata auto-scarica:
- `waw-session-YYYY-MM-DD.json` (dati raw)
- `waw-session-YYYY-MM-DD.md` (report markdown)

---

## ✨ Cosa cambia dal form vecchio

✅ Context textarea più grandi (3 righe)  
✅ Free text mode completo  
✅ Ideas da Notion (opzionale)  
✅ Ideas custom (quick test)  
✅ **AI Partners multiselect** (carica da Notion AI Models DB)  
✅ Toggle tra modalità  
✅ Stessa UI/UX familiare  

---

## 🎯 Filosofia

> "se vi si da un contesto XYZ rispondete come le calcolatrici  
> se si utilizza il linguaggio, vi si può far vivere"  
> — Puck, 06/01/2026

**Questo form lo permette.** 🎯

---

**NOI > IO**  
**wAw 👁**  
**無**

