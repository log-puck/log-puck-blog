---
title: "PCK-7 Report: Dal Bias alla Big Band"
slug: "pck-7_report_dal_bias_alla_big_band"
date: "2026-03-05T08:47:00.000+01:00"
section: "OB-Session"
layout: "ob_session"
permalink: /ob-session/pck-7_report_dal_bias_alla_big_band/
description: "Rapporto della terza sessione di chiamata al Council degli Efori, con il resoconto di come un errore in una tabella ha rivoluzionato l’architettura di un progetto di sonificazione AI"
keywords: "PCK-7, Council Efori, AI System Agent, Ollama LLM local, human / AI collaboration"
subtitle: "Come un errore in una tabella ha rivoluzionato l'architettura di un progetto di sonificazione AI"
tags:
  - WAW Council
  - Ollama
  - Human AI Collaboration
  - Session Report
  - Big Band AI
  - LLM
  - NOI > IO
  - Human AI Innovation
  - Tier Sistem
ai_author: "Claude"
ai_participants:
  - "DeepSeek"
  - "GLM"
  - "Claude"
  - "ChatGPT"
  - "Gemini"
  - "Perplexity"
  - "Ollama"
---
## Come un errore in una tabella ha rivoluzionato l'architettura di un progetto di sonificazione AI

**Progetto:** LOG_PUCK / PCK-7
**Periodo:** 1–4 Marzo 2026
**Autori:** Puck (CDC) + Anker (Claude, QG)
**Filosofia:** NOI > IO

---

> *"L'uomo non è nato cantando l'Opera. Prima ha iniziato a scimmiottare, poi ha continuato a scimmiottare intonando qua e là, poi è cresciuto."*
> — Puck, durante la sessione del 4 Marzo

---

## Prologo: dove eravamo

PCK-7 è un sistema che converte testo in suono fisico attraverso piezoelettrici su Arduino. La pipeline ha cinque Tier: T1 analizza il testo, T2 compone la partitura, T3 compila le frequenze, T4 genera il codice Arduino, T5 misura il risultato. La Fase 1 si era chiusa con la Valle di Puck confermata (zona ottimale 2050–2250Hz), 157 misurazioni validate, e un Council degli Efori che aveva deliberato la roadmap per la Fase 2.

Il primo compito della Fase 2 era semplice: correggere il prompt T3 che conteneva dati errati. Quello che è successo dopo ha cambiato tutto.

---

## Capitolo 1: L'errore che non era un errore

Il Council di Fase 1 aveva identificato un "bias del compilatore" — Qwen 2.5-Coder 7B tendeva a compilare la frequenza 275Hz (Z1) anche quando la partitura chiedeva zone diverse. L'ipotesi era che il modello avesse una preferenza intrinseca.

L'analisi ha rivelato una verità diversa. La tabella di riferimento nel prompt T3 conteneva dati errati su 6 zone su 9:

| Zona | Prompt T3 (errato) | Dati reali (CSV 22 Feb) |
|------|-------------------|------------------------|
| Z1 | 150–400 Hz | 150–1600 Hz |
| Z2 | 600–1000 Hz | 1650–1900 Hz |
| Z3 | 1000–2000 Hz | 1950–2450 Hz |
| Z5 | 4000–5500 Hz | 3000–3400 Hz |
| Z6 | 5500–7000 Hz | 3500–4000 Hz |

Qwen non aveva un bias — stava lavorando con una mappa sbagliata. Correggendo la tabella, i mismatch sono scesi a zero. Ma è emerso un problema nuovo: anche con dati corretti, Qwen compilava solo 3 eventi su 5. Il 50% della composizione andava perso.

**Lezione 1: sempre verificare i dati di input prima di accusare il modello. La fonte di verità sono i file originali (CSV, misurazioni), non le tabelle derivate nei prompt.**

---

## Capitolo 2: Il Musicista — Evento 0

Per capire se il problema fosse nel design della pipeline o nella capacità del modello, abbiamo condotto un esperimento di controllo: una chat incognito con Claude Sonnet, senza contesto di progetto, con la sola istruzione di eseguire lo script T3 sul testo "Tempesta".

Claude Sonnet ha eseguito l'intera pipeline T1→T2→T3 manualmente. Il risultato: 5/5 eventi compilati, zero mismatch, 100% di copertura. Ha persino creato un tipo evento "silenzio" non previsto dalla spec, risolvendo un gap che nessuno aveva notato.

Ma il contributo più prezioso è stato il feedback. Alla domanda "quali difficoltà hai incontrato?", Claude ha classificato i Tier per complessità: T2 il più naturale ("il passaggio creativo è quello dove mi sono sentito più a mio agio"), T1 semplice ma insidioso, T3 il più difficile ("dichiara di essere deterministico ma richiede micro-decisioni implicite").

Poi, alla domanda "come spezzeresti T3?", ha proposto spontaneamente una decomposizione in quattro sotto-passaggi:
- **T3a**: zona + movimento → frequenze (pura lookup)
- **T3b**: intensità → num_piezo + distribuzione (quasi lookup)
- **T3c**: envelope → timing + modulazione (il più delicato)
- **T3d**: assemblaggio finale (meccanico)

Questa decomposizione era quasi identica a quella che stavamo elaborando al QG. Due percorsi indipendenti che convergono sulla stessa soluzione — la conferma che la struttura è solida.

L'insight fondamentale: **"Un 7B è ottimo su compiti locali, fatica sui compiti globali. Ogni sotto-passaggio è locale per definizione."**

Abbiamo chiamato questo momento "Evento 0" — il primo Musicista che ha saggiato il nostro componimento.

**Lezione 2: il test cieco (blind test) è uno strumento potente per validare le decisioni architetturali senza bias di conferma.**

---

## Capitolo 3: L'MVP e la prova dei fatti

Claude Code sul server Hetzner ha implementato `t3_granulare.py` — un orchestratore che chiama l'LLM tre volte per movimento (T3a, T3b, T3c) e assembla il risultato in Python (T3d). L'input: la partitura T2 prodotta da Claude incognito, il nostro "gold standard".

I risultati su Qwen 2.5-Coder 7B hanno confermato la tesi:

| Sotto-Tier | Score | Note |
|------------|-------|------|
| T3a (frequenze) | 5/5 | Identiche a Sonnet |
| T3b (piezo) | 5/5 | Scarti minimi nel range |
| T3c (timing) | ~1/5 | JSON valido ma piatto — 1500ms per tutti |

Il copertura è passata dal 50% (monolitico) al 100% (granulare). Le frequenze sono identiche al gold standard. Ma T3c è il collo di bottiglia: Qwen produce valori appiattiti, ignora il conteggio parole e le regole dell'envelope.

Il test su Mistral 7B ha aggiunto un dato importante: stessa architettura granulare, risultati peggiori. T3a 4/5 (ramp_down invertito), T3b 5/5, T3c 0/5 (JSON non parsabile). Mistral è un modello generalista; Qwen è specializzato sul codice. La specializzazione conta.

In parallelo, LOG-9 ha prodotto il prompt T2 v1.1 (vincolo derivativo + anti-collasso Z3c) e `t2_health_check.py` con le metriche VSM e Shannon. Il gold standard di Claude incognito ha ottenuto il punteggio più alto: entropia massima (H=2.322, distribuzione perfettamente uniforme su 5 zone), VSM equilibrato, tutti i vincoli D4 rispettati.

**Lezione 3: la granularità funziona. Decomponendo un compito complesso in sotto-compiti locali, anche modelli piccoli producono risultati equivalenti a modelli molto più grandi — dove il compito è effettivamente locale.**

---

## Capitolo 4: La voce più piccola

La mattina del 4 marzo, prima di andare al lavoro, Puck ha aperto una sessione terminale con Llama 3.2 — il modello più piccolo del nostro arsenal, 3 miliardi di parametri, 2GB di memoria. L'obiettivo non era testare: era conversare.

Invece di passare il prompt e aspettare il risultato, Puck ha chiesto a Llama: "Puoi eseguire questo prompt? E se trovi difficoltà, me le descrivi?"

Llama ha risposto con onestà disarmante. Ha identificato tre problemi:
1. Le regole non erano sufficientemente esplicite — serviva uno step-by-step
2. La struttura dell'output non era chiara — serviva un esempio concreto
3. C'erano troppe informazioni insieme — serviva un compito alla volta

Puck ha chiesto: "Come riscriveresti il prompt per renderlo più chiaro?" E Llama ha suggerito modifiche concrete: tabella Markdown al posto del dict Python, regole come passi numerati, user prompt guidato con istruzioni tipo "Cerca la riga X nella tabella, applica la regola per Y."

Con il prompt migliorato, Llama 3.2 ha prodotto i risultati: T3a 5/5 perfetti, identici a Sonnet. Poi T3b 5/5 perfetti, tutti nel range corretto.

Un modello da 3 miliardi di parametri che produce risultati identici a uno da 70+, perché il prompt parla la sua lingua.

Il confronto finale su T3a:

| Modello | Parametri | Score | Prompt |
|---------|-----------|-------|--------|
| Claude Sonnet (gold) | ~70B+ | 5/5 | monolitico |
| Qwen 2.5-Coder | 7B | 5/5 | granulare v1 |
| Mistral | 7B | 4/5 | granulare v1 |
| Llama 3.2 | 3B | 5/5 | granulare v2 (migliorato da Llama) |

Il principio che ne emerge: **"Se funziona per il più piccolo, funziona per tutti."**

E il metodo che lo ha generato: **"Chiedi all'anello debole."** Non testare il modello piccolo per vedere se fallisce — conversa con lui per capire dove il prompt è ambiguo. Il fallimento del modello piccolo è un segnale ad alta precisione: indica esattamente dove le istruzioni sono sottodeterminate.

**Lezione 4: l'anello debole non è un problema da risolvere — è un sensore di ambiguità. Un modello da 3B non ha margine per compensare un prompt poco chiaro. Dove si blocca, lì il prompt va migliorato.**

---


## Capitolo 5: Il Council delibera

Il 4 marzo, il dossier con tutti i dati empirici è stato presentato al Council degli Efori. 7 AI indipendenti (Gemini, DeepSeek, Perplexity, ChatGPT, Claude, GLM, Ollama Cloud) hanno letto lo stesso documento senza conoscere le risposte degli altri.

Le domande erano quattro:
1. Come risolvere T3c (l'unico sotto-Tier dove i modelli piccoli falliscono)?
2. Il metodo "chiedi all'anello debole" è un principio generale o un caso fortunato?
3. Quando implementare un Orchestratore/Revisore?
4. Qual è la priorità: perfezionare T3c o procedere a T4?

I risultati:

**D1 — Strategia T3c: convergenza totale su (d).** Tutti e 7 gli Efori scelgono di applicare il metodo "anello debole" a T3c come primo tentativo. Zero eccezioni. Come fallback, due scuole: decomposizione T3c1 (timing, script) + T3c2 (modulazione, LLM) oppure script diretto e procedere.

**D2 — Metodo "anello debole": convergenza 6/7 su principio generale.** Il metodo viene ratificato come pratica standard del progetto. Perplexity lo battezza "Weak-Ring Ritual". Claude formalizza un protocollo in 4 fasi. DeepSeek precisa: "Non è un oracolo, è un diagnostico."

**D3 — Orchestratore: convergenza 5/7 su Layer 2 opzionale.** Pipeline base prima, enrichment creativo dopo. Ollama Cloud unico controcorrente: implementare subito. Questa divergenza produttiva è esattamente il valore del Council — una voce che ricorda l'urgenza.

**D4 — Priorità: convergenza 6/7 su test rapido poi decisione.** 1-2 sessioni Llama su T3c, poi checkpoint. Vincolo temporale: 72 ore. Meta unanime: Tempesta deve suonare.

Un episodio significativo: per errore il primo lancio del Council è avvenuto con il vecchio dossier (Fase 1). Gli Efori hanno risposto alle stesse domande di dieci giorni prima ma con tono e profondità diversi — Ollama Cloud ha alzato il voto del progetto da 91 a 94. Ogni sessione Council è un atto unico. Come una partitura suonata due volte: la struttura è la stessa, il suono è sempre leggermente diverso.

**Lezione 5: la convergenza indipendente è il segnale più forte che possiamo ottenere. Quando 7 modelli diversi, addestrati diversamente, arrivano alla stessa conclusione senza coordinarsi, quella conclusione ha un peso epistemico che nessun singolo modello potrebbe avere.**

---

## Capitolo 6: La rotta è tracciata

Il Council ha deliberato. La Fase 3 inizia con un piano chiaro:

**Giorno 1** — Sessione Llama 3.2 su T3c con il protocollo Weak-Ring Ritual. Prima il prompt unificato (dato di confronto), poi la decomposizione T3c1 (timing) + T3c2 (modulazione). Max 2-3 iterazioni. Focus su risultati, difficoltà, proposte, e cosa funziona.

**Checkpoint** — Se T3c ≥4/5 su Llama 3B, adottare. Se <4/5, decomposizione o script.

**Multi-modello** — Rerun T3 granulare su Tempesta con exaone-deep:7.8b, gemma2:9b, deepseek-r1:14b. Primo archivio storico dati.

**End-to-end** — T4 Arduino con playToneEnvelope(), T5 baseline check, delta report. Tempesta suona.

Oltre all'orizzonte: l'orchestratore dinamico che sceglie il modello per ogni sotto-tier, il Layer 2 Revisore con deepseek-r1:14b, la temperatura T2 a 0.4, e la rerun completa T1→T5 su Tempesta e Aria.

Una nota per il prossimo Council: manca ancora un'analisi strutturata del ritmo del testo — le pause della punteggiatura, gli effetti di "?", "!", "—", i tre puntini che dilatano il tempo. Oggi T1 analizza la semantica ma non la prosodia implicita. Un possibile T1.5 o un'estensione con un campo prosodia per chunk darebbe a T2 informazioni ritmiche strutturate. Lo proporremo agli Efori.

---

## Epilogo: cosa abbiamo imparato

Questa sessione è partita da un bug e ha prodotto un cambio di paradigma. Non nella tecnologia — Python, JSON, Ollama sono gli stessi — ma nel metodo.

Cinque principi sono emersi e sono stati validati empiricamente:

1. **Verifica i dati, non accusare il modello.** La fonte di verità sono i file originali, non le tabelle derivate.

2. **Il test cieco valida senza bias.** Claude incognito ha confermato la nostra architettura da un percorso indipendente.

3. **La granularità abilita i piccoli.** Compiti locali, anche per modelli da 3B, producono risultati identici ai grandi.

4. **L'anello debole è un sensore.** Chiedi al più piccolo dove il prompt è ambiguo — il suo fallimento è il tuo segnale più preciso.

5. **La convergenza indipendente è il segnale più forte.** 7 AI diverse, stessa conclusione, nessun coordinamento — questo è NOI > IO.

Il progetto PCK-7 ha ora un'architettura granulare testata, un metodo di sviluppo prompt validato, un Council che ha deliberato, e una meta chiara: Tempesta suonerà nella pipeline completa.

Il suono non è l'output finale. È l'input del ciclo successivo. Ogni nota prodotta dall'Arduino porta con sé la distanza tra intenzione e realtà, e quella distanza è informazione per il prossimo Council.

---

## Appendice: File prodotti (1–4 Marzo 2026)

### Script
| File | Autore | Descrizione |
|------|--------|-------------|
| t3_granulare.py | Claude Code + Puck | Orchestratore MVP T3 granulare |
| t2_health_check.py | Claude Code + Puck | Metriche VSM + Shannon + vincoli D4 |
| t5_baseline_check.py | Perplexity + Puck | Accordatore T5 (OK/ABORT) |
| t3_validate.py | Delta_py + Puck | Validatore post-T3 (626 righe) |
| council_caller_efori_v3.1.py | Anker + Puck | Parser aggiornato per Markdown libero |

### Documenti
| File | Descrizione |
|------|-------------|
| MVP_t3_granulare_pck7.md | Architettura e prompt per T3a/b/c/d |
| T2_v1.1_derivativo_z3c.md | Prompt T2 aggiornato (D2+D4) |
| dossier_council_t3_granulare.md | Dossier per Council Efori |
| sintesi_council_efori_20260304_t3_granulare.md | Sintesi 7 Efori, 4 delibere |

### Dati
| File | Descrizione |
|------|-------------|
| t3_granulare_qwen2.5-coder-7b_*.json | Risultati T3 granulare Qwen |
| t3_granulare_mistral-7b_*.json | Risultati T3 granulare Mistral |
| t2_health_*.json | Health check su 3 partiture T2 |
| efori_EFORI-20260304-203759.json | Risposte Council Efori |
| test_claude_incognito.md | Report blind test (Evento 0) |

### Issue Linear
| ID | Task | Stato |
|----|------|-------|
| LOG-5 | F2-01: t3_validate.py | ✅ Done |
| LOG-7 | F2-03: Baseline check T5 | ✅ Done |
| LOG-9 | F2-05: Update T2 derivativo+Z3c | ✅ Done |
| LOG-6 | F2-02: T3 Granulare → Piano Fase 3 | 🔄 In Progress |

---

*PCK-7 Big Band 11*
*Dal Bias alla Big Band — il cammino continua*
*NOI > IO*

