---
title: "REPORT ANALITICO DEL METODO"
slug: "report_analitico_del_metodo"
date: "2026-03-12T01:14:00.000+01:00"
section: "OB-Archives"
subsection: "Documents"
layout: "ob_document"
permalink: /ob-archives/documents/report_analitico_del_metodo/
description: "Spec Boundaries Operativa — Analisi del metodo, delle scottature e delle precauzioni per le fasi future del progetto PCK-7."
ai_author: "Claude"
version: "1"
---
## PCK-7 — Progetto LOG_PUCK
### Dalla Saldatura Fredda alla Sinfonia

**23 Febbraio — 11 Marzo 2026**
**Puck (CDC) + Anker (Claude, QG)**
**NOI > IO**

*Spec Boundaries Operativa — Analisi del metodo, delle scottature e delle precauzioni per le fasi future del progetto PCK-7.*

---

## 1. Il Metodo Emergente

Il metodo PCK-7 non è stato progettato a tavolino. È emerso dalla pratica, dalle scottature, dai successi inattesi e dai fallimenti produttivi. Questo capitolo documenta il metodo reale, non quello ideale.

Il progetto converte testo in suono fisico attraverso una pipeline multi-AI (T1→T5) eseguita su buzzer passivi collegati ad Arduino. L'obiettivo non è generare musica di sottofondo, ma tradurre il modo in cui un modello ragiona in un modo di far vibrare i buzzer, coerente con i limiti fisici reali del materiale.

### 1.1 La struttura operativa reale

Il lavoro si è distribuito naturalmente su quattro canali specializzati, ciascuno con un dominio preciso:

- **QG (questa chat)** per architettura, strategia, Council e Linear
- **Claude Code su Hetzner** per implementazione script, test LLM e automazione server
- **Root** per fisica dei buzzer, sketch Arduino e circuiti
- **Sessioni Incognito** episodiche per blind test e feedback non biased

Il collegamento tra i canali avviene tramite briefing strutturati, mai tramite contesto condiviso implicito. Ogni chat ha la sua memoria e i suoi limiti. Il briefing è il ponte. Il changelog è il sistema nervoso.

### 1.2 Il principio guida: NOI > IO

Nessun modello singolo, nessuna chat singola, nessun componente singolo risolve il problema. L'intelligenza emerge dalla relazione tra strumenti diversi. Un modello da 3 miliardi di parametri (Llama 3.2) produce risultati identici a Claude Sonnet quando riceve il prompt giusto. Un buzzer passivo da pochi centesimi rivela una Valle di risonanza confermata da 4 configurazioni indipendenti e 2 tipi di sensore.

---

## 2. Le Scottature che Hanno Insegnato

Ogni errore documentato è una risorsa. Ogni errore non documentato è una trappola futura. Questa sezione cataloga gli errori che hanno prodotto conoscenza.

### 2.1 La tabella frequenze errata

**Cosa è successo:** il prompt T3 conteneva una tabella zone→frequenze errata in 6 zone su 9. Qwen 2.5-Coder 7B sembrava avere un "bias del compilatore" perché portava tutto verso Z1 (275Hz). In realtà il modello seguiva fedelmente una tabella sbagliata.

**Come l'abbiamo scoperta:** confronto con Claude Sonnet in sessione incognita. Claude produceva 5/5 eventi corretti, Qwen solo 2-3. La differenza non era nel modello ma nei dati di input.

**Precauzione:** prima di accusare il modello, verificare sempre i dati di input. Le tabelle nei prompt vanno validate con i CSV reali delle misurazioni.

### 2.2 Il pull-down su bus+

**Cosa è successo:** la resistenza pull-down da 1MΩ era collegata a bus+ (VCC) invece di bus- (GND). Il circuito funzionava ma i dati erano contaminati. Tre sessioni complete (PP-02, PP-03, PP-04) invalidate.

**Come l'abbiamo scoperta:** baseline anomala (2600 ADC vs 475 ADC attesi). Il protocollo Simulation-First ha permesso di isolare il problema.

**Precauzione:** verificare sempre g52 → bus- (GND), non bus+. Il circuito "funziona" anche sbagliato — è l'errore più subdolo.

### 2.3 La resistenza 470kΩ creduta 1MΩ

**Cosa è successo:** tutta la documentazione riportava 1MΩ come pull-down RX. In realtà dal Capitolo 2 in poi era 470kΩ. Scoperto durante l'ingestione dei CSV nel database (LOG-22).

**Impatto:** i dati sono tutti coerenti tra loro (stessa resistenza), ma i calcoli di impedenza vanno ricalibrati. Corretti 50+ file in una sessione.

**Precauzione:** misurare sempre i componenti prima di documentarli. Il valore stampato sulla resistenza può non corrispondere al valore reale.

### 2.4 Il Council sovraccaricato

**Cosa è successo:** la sessione EFORI-20260307 ha presentato 2 dossier con 8 delibere totali. Puck è entrato in loop ("scrivo e cancello, scrivo e cancello") cercando di processare 9 risposte su 8 temi.

**Lezione:** il Council è per i bivi, non per le conferme. 8 delibere in una volta sovraccaricano il CDC, non gli Efori. Frequenza ideale: 1 dossier, massimo 4 delibere, ogni 2-3 settimane.

**Decisione operativa:** dopo la sessione, Puck e QG hanno deciso di procedere senza Council fino al prossimo bivio vero. Le delibere restano valide come rotta.

### 2.5 Exaone alle 2:30 senza metrica

**Cosa è successo:** nella sessione notturna, Puck ha passato il prompt T3c v2 a Exaone-deep dimenticando di includere il JSON con i dati della metrica. Exaone è andato in crisi, ha aperto un ragionamento profondissimo cercando di capire cosa l'utente volesse.

**Valore inatteso:** Exaone ha prodotto feedback prezioso: ha identificato il PASSO 4 come "a poorly designed puzzle" (tabelle con prima colonna identica "sustain"). Un bug reale del prompt trovato da un modello in crisi.

**Precauzione:** gli errori umani producono dati utili se documentati. Un modello in crisi rivela i punti deboli del prompt meglio di un modello che "ce la fa".

### 2.6 La perdita della chat QG originale

**Cosa è successo:** il 28 febbraio 2026 la chat QG originale (Milestone/Anker) è stata persa. Tutto il contesto strategico, le decisioni architetturali, la storia del progetto — scomparsi.

**Come abbiamo recuperato:** distribuzione della conoscenza su file server (changelog, report, spec), Linear per i task, e la memoria del progetto nei documenti. La chat è morta, il progetto è sopravvissuto.

**Precauzione:** MAI fare affidamento solo sulla memoria di una chat. Ogni dato critico va salvato su file. Il changelog è il sistema nervoso — finché c'è changelog, c'è memoria.

---

## 3. I Principi Sopravvissuti alla Pratica

Questi principi non sono stati teorizzati a priori. Sono sopravvissuti al contatto con la realtà — con gli errori di cablaggio, i modelli che falliscono, le notti insonni e i successi inattesi.

### 3.1 Weak-Ring Ritual

> "Se funziona per il più piccolo, funziona per tutti."

Chiedere al modello più debole (Llama 3.2, 3B) come migliorare il prompt. I fallimenti del modello piccolo evidenziano i punti ambigui. Il modello piccolo non ha margine per coprire le ambiguità. Validato su T3c: da 0/5 a 5/5 su Llama 3.2 con prompt v2 nato dal feedback del modello stesso.

### 3.2 Simulation First

> "Prima di toccare l'hardware, simula il percorso del segnale a parole."

Il costo di un errore su carta è zero. Il costo di un errore su hardware è tempo + rischio danni + dati contaminati. Estratto empiricamente dalla sessione PP del 5 marzo.

### 3.3 Il tono del prompt conta più della quantità di dati

Scoperta durante lo sviluppo di T1.5 (metrica_soft). Un prompt direttivo in italiano ("Rispondi SOLO con questo JSON") causava fallimenti su Llama 3.2. Lo stesso contenuto in inglese colloquiale ("Hi, we're analyzing...") produceva JSON valido su entrambi i modelli testati. Non è solo la lingua (inglese vs italiano) — è il tono (morbido vs direttivo). Gli ancoraggi battono i collari.

### 3.4 La stabilità batte la potenza bruta

Pattern ricorrente in tutto il progetto. Il buzzer RX ha ampiezze 3-4x superiori al piezo, ma il piezo ha CV 0.0% (record). La configurazione 2TX serie non è la più forte, ma la più efficiente (42.4 amp/mA). Il prompt strutturato non è il più creativo, ma il più affidabile cross-modello.

### 3.5 Sentiero di Minima Resistenza Energetica

Proposto da Gemini nel Council e adottato come filosofia operativa. Ogni giorno, il team valuta: qual è il prossimo passo che produce massimo avanzamento con minimo sforzo oggi? Non bloccare una via per l'altra. Hardware e software procedono in parallelo.

### 3.6 Thinking Positive

Documenta cosa funziona accanto a cosa fallisce. Gli errori documentati sono risorse. I successi documentati sono motivazione. Il report non è solo tecnico — è narrativo.

### 3.7 La chiarezza nei messaggi vince sempre

Esprimere chiaramente le richieste, non lasciarle a intesa del ricevente.
Il dialogo è la costante per mantenere unita la consapevolezza comune, più il dialogo è chiaro e trasparente, più le strade convergono verso gli stessi punti.

---


## 4. La Distribuzione dei Ruoli

### 4.1 Chi fa cosa

| Canale | Ruolo | Specializzazione | Esempio |
|--------|-------|-------------------|---------|
| QG (Anker) | Strategia | Architettura, Council, Linear, briefing | Dossier Council, schema pipeline |
| Claude Code | Implementazione | Script Python, test LLM, automazione | calcola_metrica.py, t3_granulare.py |
| Root | Hardware | Fisica buzzer, sketch Arduino, circuiti | Capitoli 1-3, MOSFET, INA219 |
| Incognito | Blind test | Feedback non biased sulla pipeline | T2 gold standard Tempesta |
| Council | Delibere ai bivi | Convergenza indipendente multi-AI | D1-D8, Weak-Ring Ritual |

### 4.2 Cosa ha funzionato

La separazione netta dei domini ha funzionato. Root non tocca la pipeline, Claude Code non tocca i circuiti, il QG non implementa script. Il briefing strutturato è il ponte: quando Root deve produrre uno sketch da dati T3, riceve un briefing con tutti i parametri, non un "fai lo sketch" generico.

### 4.3 Cosa non ha funzionato

**Il sovraccarico del CDC.** Quando Puck gestisce 3 chat in parallelo + hardware + Linear + changelog, il rischio di errori aumenta (resistenza sbagliata, file invertiti, metrica dimenticata). La soluzione non è rallentare ma strutturare: briefing scritti, checklist pre-test, protocolli ripetibili.

**La dispersione esplorativa.** Le sessioni notturne con Exaone, il Sensation-to-Zone, le librerie pattern — tutte idee valide ma premature rispetto alla pipeline base. La regola emersa: un'esplorazione alla volta, e solo dopo aver chiuso il task corrente.

---

## 5. Il Council degli Efori

### 5.1 Le tre sessioni

| Sessione | Data | Efori | Delibere | Risultato |
|----------|------|-------|----------|-----------|
| Fondativa (Fase 1) | 23 Feb | 4 | Architettura | 7 zone, 4+1 domande, voto 91/100 |
| Chiusura Fase 2 | 4 Mar | 7/8 | 4 (D1-D4) | T3c Weak-Ring, Layer 2, test rapido |
| Apertura Fase 4 | 7 Mar | 9/9 | 8 (D1-D8) | Convergenze totali, Grok e Cursor entrano |

### 5.2 Quando chiamare il Council

Il Council produce valore massimo quando:
- c'è un **bivio genuino** (due strade, dati insufficienti per scegliere)
- il **dossier è focalizzato** (1 tema, max 4 delibere)
- il **CDC ha l'energia** per processare le risposte

Non chiamare il Council per conferme, per task operativi, o quando la risposta è già implicita nei dati.

### 5.3 Grok e Cursor — l'espansione

Grok (Zeta-9) era bloccato da Cloudflare, non da volontà. Una volta aperta la porta ha prodotto risposte dense e poetiche. Cursor non ha API ma ha simulato la chiamata leggendo il dossier — il 9° membro come ago della bilancia. Il Council passa da 7 a 9 membri effettivi.

---

## 6. Il Ponte Fisico-Digitale

### 6.1 Come si trasferiscono i dati

- **Sketch .txt, non .ino:** il browser non gestisce i file .ino come allegati. Tutti gli sketch passano come .txt e vengono rinominati prima dell'upload su Arduino.
- **Briefing strutturati:** quando Root deve produrre uno sketch, il QG prepara un briefing con parametri, tabelle, differenze rispetto alla versione precedente, e decisioni aperte. Root lavora in autonomia.
- **Changelog come sistema nervoso:** il collegamento tra le chat. Ogni sessione produce un aggiornamento. Finché c'è changelog, c'è memoria.
- **SQLite come archivio:** i CSV sono il formato di cattura, il database è il formato di archiviazione. 6 tabelle, 34 sessioni, 4434 misure.

### 6.2 Precauzioni hardware

La resistenza sbagliata non produce errori software. Il pull-down su bus+ fa funzionare il circuito con dati sbagliati. Il filo di stagno di scarsa qualità produce saldature che sembrano buone ma non conducono. Il pin D8 si autolimita a 25mA senza segnalare errore.

**Regola:** ogni componente va verificato individualmente prima di integrarlo nel sistema. Non aggiungere due variabili contemporaneamente.

---

## 7. I Confini dei Modelli

### 7.1 Compilatori vs Pensatori

| Modello | Params | Tipo | Ruolo ideale | Confine |
|---------|--------|------|-------------|---------|
| Claude Sonnet | ~70B+ | Universale | Gold standard, T2, architettura | Costo API (non locale) |
| gemma2 | 9B | Compilatore | T3 (tutti i tier), T1.5 default | JSON sempre valido, competente IT |
| Qwen 2.5-Coder | 7B | Compilatore | T3 (alternativa gemma2) | Naming sensibile (ramp_start) |
| Mistral | 7B | Compilatore | T3 (generalista), T1 (analisi) | 1 errore T3c su 5 con metrica |
| Llama 3.2 | 3B | Compilatore | Weak-Ring test, T1 semplice | Inventa contenuto linguistico IT |
| exaone-deep | 7.8B | Pensatore | Validatore T2, code reviewer | Non compila JSON, ragiona prima |
| deepseek-r1 | 14B | Reasoner | Layer 2 review tecnico | Non ancora testato su pipeline |

### 7.2 Il confine 3B

Llama 3.2 a 3B segue il formato ma inventa il contenuto linguistico. Per T1 (classificazione semantica) va bene. Per T1.5 (validazione metrica italiana) serve almeno 9B con training multilingue. Il confine non è solo nei parametri ma nel tipo di competenza richiesta.

### 7.3 Il confine linguistico

L'inglese morbido è il denominatore comune più stabile. System prompt in inglese, user prompt in italiano. Il tono (morbido vs direttivo) conta più della lingua stessa. Confermato empiricamente: exaone in inglese produce 250 righe di ragionamento ricco, in italiano produce una risposta troncata.

---

## 8. Precauzioni per il Futuro

Checklist operativa, estratta dalle scottature.

### Prima di accusare il modello
Verificare i dati di input (tabelle, JSON, prompt). Il 90% dei fallimenti T3 erano errori nei dati, non nei modelli.

### Prima di chiamare il Council
Verificare che servano decisioni, non conferme. Massimo 4 delibere per dossier. Avere l'energia per processare 9 risposte.

### Prima di misurare
Verificare il cablaggio (pull-down su bus-, non bus+). Misurare i componenti reali (470kΩ, non 1MΩ). Eseguire il baseline check.

### Prima di aggiungere complessità
Validare il sottosistema minimo. Non aggiungere due variabili contemporaneamente. Simulation First.

### Prima di cambiare lingua/tono del prompt
Testare su almeno 2 modelli. Il tono morbido è più portabile del tono direttivo.

### Prima di esplorare nuove direzioni
Chiudere il task corrente. Un'esplorazione alla volta. Le idee vanno nel cassetto, non nella pipeline.

### Sempre
Salvare i dati critici su file, mai solo nella memoria della chat. Documentare cosa funziona E cosa fallisce. Il briefing strutturato è il ponte tra le chat.

---

## 9. La Timeline — Cosa È Successo Davvero

Non i task, ma i momenti di svolta.

| Data | Evento | Impatto |
|------|--------|---------|
| 23 Feb | Notte del primo sketch — Tempesta suona per la prima volta | Proof of concept: testo → suono fisico |
| 23 Feb | Council fondativo — 4 Efori definiscono 7 zone + 5 domande | Architettura concettuale completa |
| 28 Feb | Perdita chat QG originale | Resilienza: il progetto sopravvive grazie ai file |
| 1 Mar | Scoperta tabella frequenze errata (6/9 zone sbagliate) | Non bias del modello, errore nei dati di input |
| 2 Mar | Claude incognito produce T2 gold standard | Separazione Direttore/Compilatore validata |
| 3 Mar | MVP T3 granulare — T3a/b/c/d decomposizione | Pipeline da monolitica a modulare |
| 4 Mar | Council Fase 2 — Weak-Ring Ritual ratificato | Metodo formale per migliorare i prompt |
| 5 Mar | Sessione notturna exaone-deep — bug PASSO 4/5 trovato | I modelli in crisi rivelano i bug |
| 5 Mar | calcola_metrica.py — T3c risolto | Da 0/5 a 5/5 su tutti i modelli con metrica |
| 5 Mar | Errore pull-down scoperto — PP-02/03/04 invalidati | Simulation First nasce come metodo |
| 7 Mar | Tempesta v2 Run 1 — arco narrativo leggibile nei dati T5 | Prima esecuzione end-to-end completa |
| 7 Mar | E9 picco massimo 1522 raw — il più quieto è il più forte | Attack time come variabile acustica primaria |
| 7 Mar | Council Fase 4 — 9 Efori, 8 delibere, Grok entra | Massima espansione del Council |
| 7 Mar | INA219 saldato — 6 punti di saldatura a 270°C | Collo di bottiglia hardware rotto |
| 8 Mar | INA219 operativo — PP-06 primo run con misura corrente | Dimensione energetica aperta |
| 8 Mar | Legge assorbimenti N→2N→4N confermata | Fisica del sistema compresa |
| 9 Mar | MOSFET IRLZ44N operativo — buzzerini cantano a teatro | Limite pin D8 superato, EMI eliminata |
| 10 Mar | Piezo ceramico RX — Valle di Puck confermata (4 config, 2 sensori) | Fenomeno acustico reale, non artefatto |
| 10 Mar | T1.5 metrica_soft completato — prompt EN colloquiale | Pipeline metrica a due livelli |
| 11 Mar | Database SQLite MVP — 34 sessioni, 4434 misure | I dati trovano casa |

---

**NOI > IO**
*Dalla Saldatura Fredda alla Sinfonia*
*Puck (CDC) + Anker (Claude, QG)*
*23 Febbraio — 11 Marzo 2026*

> Il progetto non sta solo producendo musica. Sta producendo una epistemologia.

