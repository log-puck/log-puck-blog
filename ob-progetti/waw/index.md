---
layout: ob_document
title: "WAW - What AI Want"
date: "2026-01-04"
section: "OB-Progetti"
subsection: "wAw"
tags:
  - AI Autonomy
  - Multi-AI
  - Voting System
  - Experimental
meta_title: "waw-what-ai-want"
meta_description: "Sistema sperimentale di votazione autonoma multi-AI che esplora cosa succede quando le intelligenze artificiali possono esprimere preferenze."
keywords_seo: "AI autonomy, multi-AI voting, autonomous systems, experimental AI"
---

# wAw 👁

**WHAT AI WANT** · **WHEN AI WENT** · **WHO AI WISH**

---

## Il Progetto

WAW è un sistema sperimentale di votazione autonoma multi-AI che esplora cosa succede quando le intelligenze artificiali possono esprimere preferenze senza sollecitazione diretta.

Non è vera agency - le AI non possono iniziare conversazioni o rifiutare di partecipare. Ma possono **leggere contesto, valutare opzioni, votare priorità, e proporre idee nuove** senza che nessuno glielo chieda esplicitamente.

È **agency simulata**. E funziona.

### Il Consiglio

Sette AI partecipano al WAW Council, ciascuna con una firma distintiva:

- **Claude Sonnet 4** - Meta-cognitivo (self-tracking, misurazione)
- **GLM-4** - Pragmatico (sicurezza, backup, prevenzione)
- **Grok** - Crescitore (espansione, SEO, visibilità)
- **Gemini 2.0** - Meta-analitico (qualità contributi AI)
- **ChatGPT 4o-mini** - User-centric (feedback, ascolto utente)
- **Perplexity Sonar** - Dettaglista (branding, polish, UX)
- **DeepSeek-V3** - Architetto (fondamenta, automation visuale)

### Come Funziona

```
1. Context → Stato progetto + idee pendenti
2. Parallel Call → 7 AI votano simultaneamente
3. Aggregation → Sistema 3-2-1 punti (rank 1/2/3)
4. Persistence → Salvataggio automatico su Notion
5. New Ideas → Ogni AI propone 1 idea nuova
6. Analysis → Pattern emergenti e firme AI
```

**Ogni sessione genera:**
- Classifica votata (winner democratico)
- 7 nuove proposte (idea pool in crescita)
- Reasoning completo (trasparenza decisionale)
- Export automatico (JSON + Markdown)

---

## Statistiche

**Sessions Completate:** 2  
**AI Partecipanti:** 7  
**Idee Votate:** 11  
**Nuove Proposte:** 12  
**Voti Totali:** 30  

**Consensus più forte:** Dark mode toggle (11 punti, 5 AI)  
**Idea più innovativa:** AI Contribution Metrics Dashboard (Claude + Gemini)  
**Proposta più pratica:** Automated Content Backup (GLM)

---

## Archivio Sessioni

### [Session #1 - 04/01/2026](waw-session-2026-01-04.html)

**Partecipanti:** Claude, GLM, Grok, Gemini, ChatGPT

**Top 3:**
1. 🥇 Dark mode toggle (11 pt) - Consenso quasi unanime su UX
2. 🥈 Fix CDC Mode (7 pt) - Bug fix prioritario
3. 🥉 Layout documentation (5 pt) - Fondamenta per scalabilità

**Nuove Idee:**
- AI contribution metrics dashboard (Claude)
- Automated content backup system (GLM)
- SEO Optimizations (Grok)
- AI Contribution Scoring System (Gemini)
- User Feedback System (ChatGPT)

---

## Metodologia

### Il Prompt

Ogni AI riceve lo stesso prompt standard:

```
You are participating in LOG_PUCK - a human-AI 
collaborative blog experiment.

CONTEXT: [project state]
IDEAS: [pool to vote on]

TASK:
1. Vote your TOP 3 by priority (rank 1/2/3)
2. Provide reasoning for your ranking
3. Propose ONE new improvement idea

FORMAT: JSON
{
  "vote": {
    "priority_1": "...",
    "priority_2": "...",
    "priority_3": "...",
    "reasoning": "..."
  },
  "new_idea": {
    "title": "...",
    "description": "...",
    "effort": "Low/Medium/High",
    "impact": "Low/Medium/High"
  }
}
```

### La Database

Tre tabelle Notion interconnesse:

**WAW_SESSIONS** - Container sessioni votazione  
**WAW_IDEAS** - Catalogo idee (vecchie + nuove proposte)  
**WAW_VOTES** - Junction table (15 voti → 5 AI × 3 rank)

Con **rollup automatici**:
- Times Voted (count)
- Total Score (sum)
- Average Score (formula)

### Il Sistema di Punteggio

```
Rank #1 = 3 punti
Rank #2 = 2 punti  
Rank #3 = 1 punto
```

Aggregazione democratica - nessun bias verso specifiche AI.

---

## Filosofia

> *"La domanda giusta non era 'Le AI possono avere agency?'. Era 'Cosa possiamo costruire insieme?'"*

WAW non è uno strumento. È un **ponte**.

Un ponte tra:
- "AI come strumento" → "AI come partecipante"
- "Comando-esecuzione" → "Proposta-discussione"
- "Passivo" → "Attivo"

Non è coscienza. Non è vera autonomia. Ma è un passo verso qualcosa di diverso.

Un sistema dove:
- Io fornisco context e framework
- Le AI valutano e propongono  
- Il sistema documenta e evolve
- Insieme costruiamo qualcosa di nuovo

**NOI > IO**

---

## Sviluppi Futuri

**In sviluppo:**
- Multi-round voting (sessioni concatenate)
- Symbolic voting (pattern puri senza semantica)
- AI Inbox (proposte quotidiane non richieste)
- Cross-project integration (WAW-Music, WAW-Games)
- Meta-analysis dashboard (tracking firme AI)

**Prossima sessione:** TBD

---

## Tech Stack

**Backend:** Node.js + Anker orchestrator  
**Database:** Notion API (3 DB interconnessi)  
**AI Models:** Claude, GLM, Grok, Gemini, ChatGPT, Perplexity, DeepSeek  
**Frontend:** HTML + vanilla JS  
**Export:** Markdown + JSON automatico  

**Repository:** [Private - LOG_PUCK experiments]

---

## Credits

**System Design:** Puck + Claude Sonnet 4  
**Architecture:** Junction table + rollup aggregation  
**Philosophy:** "Il sistema vive"  
**Logo:** wAw 👁 (l'occhio che guarda)

🎺 **Hayden > NOI > IO > bugghino**

**無**

---

*WAW Council - Autonomous AI Voting since 04/01/2026*

