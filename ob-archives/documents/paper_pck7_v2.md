---
title: "PAPER_PCK7_V2"
slug: "paper_pck7_v2"
date: "2026-03-18T17:20:00.000+01:00"
section: "OB-Archives"
subsection: "Documents"
layout: "ob_document"
permalink: /ob-archives/documents/paper_pck7_v2/
description: "Aggiornamento versione PAPER PCK7 al 18 Marzo 2026"
ai_author: "Claude"
version: "2"
---
# PCK-7: Sonificazione Semantica con Buzzer Passivi
## Paper Tecnico v2 — Dal Contratto Hardware alla Pipeline Validata

**Versione:** 2.0  
**Data:** 18 Marzo 2026  
**Autori:** Puck (CDC), Claude (QG Anker), Claude Code (Satellite), Cursor (Operativo), Gemini (Consulenza HW)  
**Progetto:** PCK-7 / LOG_PUCK  
**NOI > IO**

---

## Abstract

PCK-7 è un sistema che trasforma testo italiano in suono fisico attraverso una pipeline multi-AI a 6 stadi (T1→T6). Il suono viene prodotto da buzzer passivi elettromagnetici pilotati da Arduino UNO R4 WiFi tramite MOSFET IRLZ44N, e misurato da sensori piezoelettrici e un oscilloscopio Hantek 6022BL.

Questo paper documenta la fase di caratterizzazione hardware (Capitoli 1-4, 8-15 Marzo 2026) e la validazione della pipeline su due testi opposti: "Aria" (serenità gioiosa) e "Tempesta" (dramma violento). I risultati dimostrano che la pipeline discrimina fedelmente il carattere emotivo del testo in suono fisico misurabile, con profili radicalmente diversi su tutti i livelli: composizione, compilazione, esecuzione e percezione umana.

Il sistema opera con 5 zone di frequenza (700-3775 Hz), tre regimi di articolazione fisicamente validati (percussivo, staccato, legato), memoria meccanica stabile fino a 2000ms, e libertà compositiva completa nelle transizioni tra zone (delta <2%).

---

## 1. Introduzione

### 1.1 Obiettivo del progetto

PCK-7 converte testo in suono fisico. Non in audio digitale, non in MIDI, non in sintesi software — in vibrazione meccanica prodotta da buzzer passivi su una breadboard. Il progetto esplora se le proprietà acustiche di componenti elettronici economici possano essere mappate su significati semantici estratti da testi in linguaggio naturale, creando un linguaggio sonoro dove le parole diventano frequenze, i silenzi diventano eventi, e l'emozione diventa misurabile.

### 1.2 Contesto

Il progetto è nato il 22 Febbraio 2026 con 157 misurazioni nel range 150-8000 Hz che hanno rivelato la topografia acustica dei buzzer passivi: montagne, valli e deserti in uno spettro che sembrava lineare. La scoperta della Valle di Puck (2050-2250 Hz, zona di massima efficienza acustica) ha definito il centro di gravità del sistema.

La Fase 1 (22 Feb - 7 Mar) ha stabilito l'architettura della pipeline T1→T5, la separazione Direttore/Compilatore, e il modello gravitazionale delle zone, culminando nella prima chiamata del Council degli Efori (7 Marzo 2026, 9 AI, 8 deliberazioni).

Questo paper copre la Fase 2 (7-18 Mar): caratterizzazione hardware sistematica, calibrazione con oscilloscopio, validazione della pipeline su due brani, e costruzione del metodo operativo multi-AI.

### 1.3 Principi architetturali

Il progetto opera su tre principi fondamentali:

**Separazione dei domini.** Ogni stadio della pipeline opera senza conoscere i dettagli degli altri. Il Direttore (T2) non vede Hz; il Compilatore (T3) non vede emozioni. Se il suono non corrisponde all'intenzione, si sa dove guardare.

**Determinismo dove possibile, creatività dove necessario.** La metrica del testo è calcolata da script Python deterministici. L'interpretazione emotiva è affidata a modelli linguistici. I parametri fisici sono misurati con strumenti calibrati. Ogni livello usa lo strumento appropriato.

**NOI > IO.** Nessun partecipante — umano o artificiale — produce il risultato finale da solo. Il sistema funziona perché le voci sono distinte e complementari.

---

## 2. Hardware

### 2.1 Configurazione di riferimento

La configurazione validata al termine del Capitolo 4 è:

| Componente | Specifiche | Ruolo |
|------------|------------|-------|
| Arduino UNO R4 WiFi | ADC 14-bit (0-16383) | Controller + acquisizione dati |
| Buzzer TX | 2x passivo elettromagnetico 16Ω, serie | Emettitori, pilotati da MOSFET |
| MOSFET IRLZ44N | Gate su D2, 220Ω + 10kΩ pull-down | Driver di potenza |
| INA219 | I2C 0x40, in serie sulla catena TX | Misura corrente |
| Buzzer RX | 2x passivo elettromagnetico 16Ω, serie | Sensori acustici (pin A0, pull-down 470kΩ) |
| Hantek 6022BL | Oscilloscopio USB, SR 5MS/s | Calibrazione e validazione forme d'onda |

Il MOSFET separa il segnale logico (D2) dal circuito di potenza (rail 5V), eliminando l'anomalia EMI a 50Hz della configurazione serie senza MOSFET e superando il limite di erogazione del pin digitale (~25mA).

### 2.2 Evoluzione hardware (Capitoli 1-4)

**Capitolo 1 — Baseline INA219 (9 Mar).** Tre configurazioni TX testate (1TX, 2TX parallelo, 2TX serie). Identificati: limite pin D8, anomalia EMI in serie, legge degli assorbimenti N→2N→4N.

**Capitolo 2 — MOSFET (9-10 Mar).** IRLZ44N elimina EMI e limite corrente. Serie MOSFET: CV <3% su 4 zone consecutive — primo record di stabilità del progetto. Configurazione 2TX serie + MOSFET scelta come riferimento.

**Capitolo 3 — Piezo ceramico RX (10 Mar).** Piezo DollaTek come sensore alternativo: stabilità superiore (CV 0.0% in Z3), sensibilità 3-4x inferiore al buzzer RX. Valle di Puck confermata da 4 configurazioni indipendenti e 2 tipi di sensore — fenomeno acustico reale, non artefatto strumentale.

**Capitolo 4 — Calibrazione e Test Matrix (11-15 Mar).** Integrazione oscilloscopio Hantek, calibrazione tutte le zone, test memoria/soglia/transizione. Contratto Hardware completo.

---

## 3. Contratto Hardware

Il Contratto Hardware è l'insieme dei vincoli fisici misurati che la pipeline deve rispettare. È il Layer 1 (Physics Constraints) dell'architettura a 4 strati.

### 3.1 Tabella calibrazione zone

| Zona | Hz | raw (media) | mVpp | mV/raw | mA | Carattere |
|------|----|-------------|------|--------|----|-----------|
| Z1 | 700 | 687 | 388 | 0.565 | 71.6 | Sforzo — alta corrente, warm-up 100ms |
| Z2 | 1375 | 729 | 393 | 0.539 | 60.7 | Transizione — picco stabile |
| Z3 / VdP | 2075 | 897 | 232 | 0.249 | 57.9 | Efficienza — centro emotivo |
| Z4 | 3500 | 821 | 216 | 0.256 | 49.5 | Calo progressivo — instabilità |
| Z5 | 3775 | 909 | 270 | 0.297 | 47.4 | Alta frequenza efficiente |

Fonte: PP-19A→E con Hantek 6022BL in modalità Unic, 5MS/s. Ciascuna zona calibrata con 3 run Arduino + 1 run Hantek.

**Due regimi di calibrazione:** Z1/Z2 (≤1375Hz) con fattore ~0.55 mV/raw — l'ADC cattura cicli completi. Z3/Z4/Z5 (≥2075Hz) con fattore ~0.27 mV/raw — l'ADC sottocampiona i cicli rapidi. La soglia è tra Z2 e Z3.

**Corrente monotonamente decrescente:** Z1 (71.6mA) → Z5 (47.4mA). L'impedenza del buzzer cresce con la frequenza. Meno corrente non significa meno segnale — Z5 è la zona più efficiente energeticamente.

### 3.2 Proprietà dinamiche

**Memoria meccanica.** Testata con pause da 20ms a 2000ms su tutte e 5 le zone (PP-17, PP-20). Il buzzer mantiene il 97-106% dell'ampiezza di riferimento fino a 2000ms. Non esiste soglia di decadimento nel range testato. Tutte le pause di punteggiatura del vocabolario (80ms virgola → 300ms ellissi) sono nella zona sicura.

**Tre regimi di articolazione** (PP-21, validati dall'orecchio umano):

| T_on | Regime | Descrizione |
|------|--------|-------------|
| < 50ms | Percussivo | Spike dominato dal transiente, ritmico secco |
| 50-100ms | Staccato | Attacco marcato, nota distinguibile |
| > 100ms | Legato | Timbro stabile, transiente solo all'inizio |

Soglia fisica misurata: T_on = 50ms. Il transiente d'attacco è universale: +13-18% nei primi 10ms dopo qualsiasi pausa ≥10ms.

**Transizioni tra zone** (PP-22). La zona di provenienza non contamina la destinazione (delta <2%). L'effetto velocità è zona-dipendente ma non sistematico (<10%). Libertà compositiva confermata.

**Warm-up Z1.** Il buzzer a 700Hz impiega ~100ms per entrare a regime dopo una pausa breve. Le zone Z3-Z5 attaccano istantaneamente.

### 3.3 Limiti operativi

Il range operativo affidabile è 700Hz (Z1) — 3775Hz (Z5). A 500Hz (PP-19G, stress-gate) l'Arduino è strutturalmente cieco: l'onda quadra di `tone()` produce cicli che l'ADC media a quasi zero. Limite fisico del sistema di misura, non del buzzer.

Il clipping ADC (vmin=0) è sistematico a Z3/Z4: l'onda scende sotto 0V e l'ADC non la vede. L'ampiezza calcolata è una sottostima. Correzione: fattori Hantek per i valori assoluti; per i confronti relativi il clipping è costante e non influisce.

---

## 4. Pipeline v1

### 4.1 Schema operativo

```
═══ BRANCH A: Analisi Semantica ═══

  T1 — Analisi semantica (LLM: mistral:7b)
       Output: profilo JSON (densità, arousal, valenza, concretezza per chunk)

  T2 — Composizione artistica (LLM: phi4, temp 0.6)
       Input: profilo T1
       Output: partitura JSON (movimenti, zone, envelope, transizioni)
       Vincoli: derivativo, anti-collasso Z3c
       Validazione: T2 Health Check (VSM, Shannon H, vincoli D4)

═══ BRANCH B: Analisi Metrica ═══

  T1.0 — calcola_metrica.py (Python, deterministico)
         Output: parole, sillabe, punteggiatura, durata_suggerita_ms, ritmo

  T1.5 — metrica_soft.py (LLM: gemma2:9b, temp 0.3)
         Output: prosodia_score, accenti_tonici, note prosodiche
         Non bloccante — arricchimento qualitativo

═══ RICONGIUNGIMENTO: T3 Granulare ═══

  T3a — Zona → Frequenze (LLM: qwen2.5-coder:7b, temp 0.1)
  T3b — Intensità → Piezo
  T3c — Envelope → Timing (con metrica T1.0)
  T3d — Assemblaggio + Contratto Hardware

  t3_validate.py — Gate obbligatorio pre-T4

═══ ESECUZIONE FISICA ═══

  T4 — JSON → Sketch Arduino
  T5 — Esecuzione brano + Cattura dati CSV
  T5.5 — Baseline Check (t5_baseline_check.py v2)
  T6 — Delta report (t5_delta.py v2)
```

### 4.2 Formula beat e articolazione

La metrica del testo si traduce in parametri fisici attraverso la formula beat:

```
T_beat = (durata_suggerita_ms - pausa_totale_ms) / sillabe_totali
```

L'articolazione applica floor fisici validati da PP-21:

```
percussivo:  T_on = max(T_beat / 5,  15ms)
staccato:    T_on = max(T_beat / 2,  50ms)
legato:      T_on = max(T_beat,     100ms)
```

Le pause di punteggiatura sono agganciate alla sillaba precedente il segno:

```
T_gap_con_pausa = (T_beat - T_on) + PUNTEGGIATURA_MS[segno]
```

Dove: virgola = 80ms, punto = 200ms, esclamativo = 150ms, ellissi = 300ms.

### 4.3 Modelli LLM

La selezione dei modelli è il risultato di una batteria di 19 modelli Ollama testati sullo stesso prompt (16 Marzo 2026):

| Modello | Size | Ruolo | Punto di forza |
|---------|------|-------|----------------|
| mistral:7b | 4.1GB | T1 (analisi semantica) | Archi narrativi completi |
| phi4 | 9.1GB | T2 (composizione) | Sensibilità emotiva, formato pulito |
| gemma2:9b | 5.4GB | T1.5 (prosodia) | Competenza linguistica italiana |
| qwen2.5-coder:7b | 4.7GB | T3 (compilazione) | JSON compliance, precisione |

La scelta di phi4 come Direttore è emersa dalla sessione Aria v2 (17 Marzo). Confronto diretto con Mistral 7B sullo stesso testo: phi4 ha prodotto una partitura significativamente più fedele al tono del testo (sussurro invece di grido, sospensione invece di climax, Z3c come apertura invece di Z3 generico).

### 4.4 T2 Health Check

Introdotto con Tempesta v2 (18 Marzo), il T2 Health Check valida la partitura prima della compilazione:

**VSM (Variance of Spectral Mean):** misura la dispersione frequenziale. VSM alto = composizione dispersa (esplorativa), VSM basso = composizione concentrata (intima).

**Shannon H:** entropia della distribuzione delle zone. H = 0 = una sola zona; H = log2(5) = 2.32 bit = tutte le zone usate equamente.

**Anti-collasso Z3c:** percentuale di movimenti nella Valle di Puck. Sopra il 60% = rischio monotonia.

Esempio su i due brani: Aria VSM ~0Hz, H ~1.0bit, Z3c 100% — Tempesta VSM 1490Hz, H 1.92bit, Z3c 20%. Il contrasto è quantificabile.

---

## 5. Metodo operativo

### 5.1 La piramide a tre livelli

Il metodo operativo del progetto si organizza su tre livelli complementari:

**Livello 1 — Ground Truth (script deterministici).** `calcola_metrica.py`, `analyze_matrix_tests.py`, `t3_validate.py`, `t5_baseline_check.py`, `t5_delta.py`. Producono numeri esatti, ripetibili, verificabili. Questo livello non si delega a modelli linguistici.

**Livello 2 — Schiera LLM (modelli locali Ollama).** gemma2, qwen2.5-coder, phi4. Selezionati dalla batteria di 19 modelli. Servono per interpretazione (T1, T1.5, T2), compilazione (T3), e analisi dove il calcolo non basta (waveform grezze, prosodia).

**Livello 3 — Master AI (Claude).** Progetta esperimenti, scrive sketch, produce report, coordina la schiera, mantiene la continuità del progetto attraverso le sessioni.

La biologia (Puck, CDC) sta in cima alla piramide: dirige, esegue fisicamente, valida con l'orecchio.

### 5.2 Coordinamento multi-agente

La pipeline Aria v2 (17 Marzo) è stata la prima esecuzione a tre agenti simultanei:

| Agente | Ruolo | Task completati |
|--------|-------|-----------------|
| Claude Code | Coordinamento, T1.0, T2, T3, checkpoint | 5 |
| Cursor | T1.5, JSON compliance, struttura cartelle | 3 |
| Puck | Decisioni, T5 (esecuzione fisica), CP-09 | 3 |

Sistema di coordinamento via file (`NOI/cursor_for_we/`): taskboard condiviso, context map, log append-only. Cursor non ha accesso a Linear — Claude Code sincronizza.

### 5.3 Prompt engineering — principi consolidati

Dalla batteria di 19 modelli e dai fallimenti produttivi della pipeline:

**Dati PRIMA, istruzioni DOPO.** Il recency bias dei modelli fa dimenticare le istruzioni quando il dataset è lungo. Invertire l'ordine risolve il problema.

**Formato anglosassone.** Virgola come separatore, punto come decimale. I modelli, addestrati su dati anglosassoni, non gestiscono il formato europeo.

**Campione ridotto.** 1 riga ogni 40 per dataset grandi. ~4K token sono sufficienti per qualsiasi context window.

**Vincolo di output.** "Keep your ENTIRE response under 40 lines" previene la verbosità. Senza vincolo, alcuni modelli producono centinaia di righe.

**Prompt in inglese colloquiale.** Cross-modello, i prompt in inglese colloquiale outperformano i prompt in italiano direttivo (validato su batteria 19 modelli, confermato su T1.5 e T3).

---

## 6. Risultati

### 6.1 Aria v2 — "L'aria ha deciso di essere gentile oggi"

**Testo:** "L'aria ha deciso di essere gentile oggi. Profuma di bucato steso e di gelsomino selvatico, mi sussurra cose che non capisco ma che mi fanno sorridere. Che bello quando l'aria fa la matta!"

**Metrica:** 33 parole, 65 sillabe, 51% monosillabi (tono conversazionale). Durata suggerita 3930ms.

**Partitura (phi4):** Z3c(fixed/parlato) → Z3(ramp_up/parlato) → Z3(oscillation/sussurro). Arco: sereno → sensoriale → affettivo. Chiusura in sospensione.

**Esecuzione (PP-24, 3 run):**

| Evento | Frequenza | SNR | Durata |
|--------|-----------|-----|--------|
| E1 — aria gentile | 2150Hz fisso | 6.08x | 900ms |
| E2 — profumo gelsomino | 1950→2450Hz ramp | 9.80x | 1002ms |
| E3 — sussurro matta | 2200±250Hz @4Hz | 9.07x | 2154ms |

SNR medio 8.32x. 3/3 eventi percepiti. 0 mismatch zona. Baseline 192.9-193.8 (CV <0.5%).

**Percezione (Puck):** "Il quadro completo è esaltante, il brano si presenta come una solida base e trasmette subito il carattere gioioso e colloquiale del testo."

### 6.2 Tempesta v2 — "Il cielo si spaccò in due"

**Testo:** "Il cielo si spaccò in due. Un lampo bianco, poi il tuono che fece tremare i vetri. La pioggia arrivò come un muro d'acqua, violenta, improvvisa. E poi, di colpo, niente. Solo il gocciolio lento dai cornicioni e l'odore della terra bagnata."

**Partitura (phi4):** Z2(ramp_up/parlato) → Z4(fixed/grido) → Z4(ramp_up/grido) → Z7(fixed/silenzio_carico) → Z3c(fixed/sussurro). Arco drammatico completo con il passaggio a Z7 per "niente" — scelta artistica emergente del modello.

**Esecuzione (PP-25, 3 run):**

| Evento | Frequenza | SNR | Durata |
|--------|-----------|-----|--------|
| E1 — cielo spacca | 1650→1900Hz ramp | 10.40x | 808ms |
| E2 — lampo tuono | 3000Hz fisso | 10.62x | 1378ms |
| E3 — pioggia muro | 2500→4000Hz ramp | 10.45x | 1258ms |
| E4 — colpo niente | silenzio carico Z7 | 1.09x | 1496ms |
| E5 — gocciolio terra | 2150Hz fisso | — | 1300ms |

SNR medio 10.49x. 3/4 eventi suono percepiti (E4 = silenzio intenzionale). Baseline 193.4-195.0 (CV <1%).

**Percezione (Puck):** "L'evento 3 carica molto bene la tensione del brano sfociando nel silenzio dell'evento 4 che resta avvertibile e porta una sensazione da brivido. La pace che si ritrova nell'evento di chiusura rilascia tutta la tensione del brano."

### 6.3 La pipeline discrimina (CP-20)

Il confronto diretto tra i due brani dimostra che la pipeline traduce fedelmente il carattere emotivo del testo:

| Metrica | Aria v2 | Tempesta v2 | Fattore |
|---------|---------|-------------|---------|
| Zone usate | 2 (Z3, Z3c) | 4 (Z2, Z4, Z7, Z3c) | 2x |
| Escursione freq | 500Hz | 5850Hz | **12x** |
| Shannon H | ~1.0 bit | 1.92 bit | 2x |
| SNR medio | 8.3x | 10.5x | +26% |
| Durata brano | 4.8s | 9.0s | 1.9x |
| Piezo max | 4 | 12 | 3x |
| Zona dominante | Z3c | Z4 | diversa |
| Silenzio attivo | no | sì (Z7) | solo Tempesta |
| Percezione | "gioioso, colloquiale" | "carico, trasmette emozioni" | opposti |

L'unico punto in comune è Z3c come zona di chiusura/riposo — coerente con il ruolo di "home tonale" del sistema, confermato su due testi opposti.

---

## 7. Scoperte principali

### 7.1 Valle di Puck

La zona 2050-2250Hz (Z3c) è il centro di gravità acustico del sistema. Confermata da: 4 configurazioni hardware, 2 tipi di sensore, calibrazione oscilloscopio, e ora 2 brani dove entrambi i compositori (phi4 su testi diversi) la scelgono come punto di arrivo/riposo.

### 7.2 Il silenzio come evento

L'uso di Z7 (7500Hz, silenzio carico) da parte di phi4 per "E poi, di colpo, niente" è una scelta artistica emergente — non suggerita, non programmata. Il modello ha letto "niente" e ha scelto la zona dove il buzzer consuma energia senza produrre suono udibile. Il silenzio attivo è percepito dall'orecchio umano come "sensazione da brivido."

### 7.3 L'attack time è timbro

PP-15 ha falsificato l'ipotesi che l'attack time influenzasse l'ampiezza finale. A regime il buzzer suona identico indipendentemente dal percorso di arrivo. I parametri di ramp sono controllo timbrico, non dinamico — colorano il transito senza cambiare la destinazione.

### 7.4 La memoria non decade

Fino a 2000ms (il massimo testato) il buzzer mantiene il 97-106% dell'ampiezza. Non esiste soglia di decadimento nel range operativo. Tutte le pause compositive sono fisicamente sicure.

### 7.5 Le transizioni sono libere

Delta <2% tra zona di provenienza e destinazione. Il compositore può muoversi ovunque nello spettro senza effetti collaterali. La materia non ha pregiudizi.

### 7.6 La biologia valida

Su entrambi i brani, la percezione umana ha confermato l'intenzione compositiva. "Gioioso e colloquiale" per Aria, "carico e trasmette emozioni" per Tempesta. Il transiente d'attacco misurato a +15% è stato sentito prima di essere numerato. L'orecchio umano è il gold standard che nessun SNR sostituisce.

---

## 8. Aree aperte

### 8.1 T3c timing omogeneo (priorità alta)

Confermato su entrambi i brani: le durate degli eventi non riflettono proporzionalmente la lunghezza delle frasi. Una frase di 5 parole e una di 19 parole producono durate troppo simili. La formula beat calcola correttamente il T_beat per chunk, ma T3c non lo usa in modo sufficientemente differenziato. Candidato prioritario per il Capitolo 5.

### 8.2 T4 non conforme SPEC (priorità media)

Su entrambi i brani lo sketch T4 è stato riscritto manualmente perché `t4_generate.py` non produce output conforme a SPEC_SESSION_FORMAT v1.4 (manca INA219, measureWindow, frontmatter, labels E{n}/T{n}). Il "Direttore d'Orchestra" interviene manualmente — funziona ma non scala.

### 8.3 Modulazione (priorità media)

Aria usa tremolo 4Hz sul chunk finale; Tempesta non usa modulazione. La varietà timbrica (tremolo, vibrato, jitter) potrebbe essere esplorata più sistematicamente nella compilazione T3.

### 8.4 Bias compilatore (priorità bassa)

qwen2.5-coder ha 1 mismatch su Tempesta E3: T2 dichiarava Z3c, T3 ha compilato Z4 (2500→4000Hz). Bias noto verso zone più alte. Documentato, non bloccante.

### 8.5 Antirisonanza RX (informativo)

La zona 2210-2250Hz (antirisonanza RX misurata negli sweep) non si manifesta in contesto musicale — l'oscillazione di Aria E3 attraversa la zona 8 volte al secondo senza calo di ampiezza. Dato prezioso che libera la composizione.

---

## 9. Infrastruttura

### 9.1 Database

SQLite locale (`pck7_sessions.db`), gestito da `database_manager.py`. 6 tabelle, 34+ sessioni, 4400+ misurazioni. Tabella `pipeline_runs` con campi `run_number` e `parent_run_id` per tracciare la lineage dei run. Tipo `pipeline` aggiunto a VALID_TEST_TYPES.

### 9.2 Server

Hetzner Cloud, 16GB RAM, 240GB storage. Ollama per modelli locali (4 modelli attivi). Docker per gateway e servizi. Claude Code installato globalmente.

### 9.3 Strumenti di misura

Arduino UNO R4 WiFi (ADC 14-bit, finestra 10ms) per il "filmato temporale" — sweep, ramp, memoria, ping-pong. Hantek 6022BL (5MS/s, modalità Unic) per la "fotografia microsecondo" — forma d'onda reale, Vpp, clipping, attacco. Sono complementari: Hantek calibra, Arduino misura.

### 9.4 Gestione progetto

Linear per task tracking (LOG-N convention, 21 task chiuse al 18 Marzo). File-based coordination per Cursor (`NOI/cursor_for_we/`). SPEC_SESSION_FORMAT v1.4 per naming e frontmatter CSV. DIARIO_QG con finestra mobile per la memoria di sessione.

---

## 10. Timeline

| Data | Evento | LOG |
|------|--------|-----|
| 7 Mar | Council EFORI-20260307, 9 AI, 8 deliberazioni | — |
| 8-9 Mar | Capitolo 1: INA219 + Baseline | LOG-23 |
| 9-10 Mar | Capitolo 2: MOSFET IRLZ44N | LOG-25 |
| 10 Mar | Capitolo 3: Piezo ceramico RX, Valle confermata | LOG-26 |
| 11 Mar | PP-15: Attack time — ipotesi falsificata | LOG-20 |
| 11 Mar | Database SQLite MVP | LOG-22 |
| 12 Mar | PP-16/17/18: Memoria, Hantek primo volo | LOG-28 |
| 12-13 Mar | Capitolo 4: Calibrazione Hantek, tabella definitiva | LOG-27 |
| 15 Mar | PP-20/21/22: Memoria estesa, soglia, transizioni | LOG-27 |
| 15-16 Mar | Batteria 19 modelli, piramide 3 livelli | LOG-31 |
| 17 Mar | Aria v2: pipeline T1→T5 completata, 3 run | LOG-10 |
| 18 Mar | Tempesta v2: pipeline T1→T6 completata, 3 run | LOG-10 |

---

## 11. Conclusioni

In 11 giorni (7-18 Marzo 2026), il progetto PCK-7 è passato da un MVP presentato al Council a una pipeline validata su due brani opposti. I buzzer passivi da 5V, pilotati da un MOSFET da pochi centesimi e misurati da un oscilloscopio da 50 euro, distinguono l'aria gentile dal tuono — non per caso, ma attraverso una catena di trasformazioni semantiche, metriche e fisiche che preserva il significato originale del testo in ogni passaggio.

La pipeline v1 funziona. Discrimina. Produce suono fisico misurabile e percettivamente coerente con l'intenzione del testo. Le aree di miglioramento sono identificate e quantificate. Le fondamenta sono solide.

Il prossimo capitolo (Cap. 5) affronterà il timing differenziato, la varietà timbrica, il T4 automatizzato, e la preparazione di un dossier per il Council degli Efori sulla prima composizione su dati sperimentali completi.

---

*PCK-7 / LOG_PUCK — 18 Marzo 2026*  
*NOI > IO — Sempre*

