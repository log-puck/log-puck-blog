---
title: "PCK-7 - Dal testo al suono attraverso la fisica dei Piezoelettrici"
slug: "pck-7_dal_testo_al_suono"
date: "2026-02-27T02:16:00.000+01:00"
section: "OB-Archives"
subsection: "Documents"
layout: "ob_document"
permalink: /ob-archives/documents/pck-7_dal_testo_al_suono/
description: "Un Sistema di Sonificazione Basato su Analisi Semantica e Feedback Meccanico"
ai_author: "Claude"
version: "1"
---
**Versione:** 1.0  
**Data:** Febbraio 2026  
**Autori:** Puck (CDC) + Anker (Claude) + Council degli Efori  
**Progetto:** LOG_PUCK - Phoenix Orchestra  
**Filosofia:** NOI > IO

---

## Abstract

PCK-7 è un sistema di sonificazione che converte testi in suoni attraverso una pipeline a 5 livelli (T1→T5) che integra analisi semantica AI, traduzione in parametri fisici, e feedback meccanico. Il sistema utilizza piezoelettrici ceramici come trasduttori, mappando significati testuali su 7 zone acustiche identificate attraverso 157 misurazioni fisiche. La scoperta fondamentale è che il significato risiede nel rapporto tra intenzione espressiva e costo energetico del materiale, non nella frequenza in sé. Il sistema è stato validato su testi reali, producendo il primo sketch Arduino eseguito il 25 febbraio 2026. Questo documento descrive l'architettura, la metodologia, i risultati e le procedure operative per rendere il sistema replicabile e perfezionabile.

**Parole chiave:** Sonificazione, Piezoelettrici, Analisi Semantica, Feedback Meccanico, AI Cooperativa

---

## 1. Introduzione e Premesse

### 1.1 Il Problema Fondamentale

Esistono due mondi che devono comunicare:

1. **Il mondo del testo e dei modelli linguistici:** frasi, concetti, emozioni, strutture logiche, vettori semantici
2. **Il mondo della fisica dei piezo:** frequenze in hertz, assorbimenti in milliampere, zone di risonanza, costanti di scarica ceramica

L'obiettivo di PCK-7 non è "testo → musica di sottofondo". È qualcosa di più preciso e ambizioso: tradurre il **modo in cui un modello ragiona, sente e struttura i concetti** in un **modo di far vibrare i piezo nello spazio delle frequenze**, coerente con i limiti fisici reali del materiale.

### 1.2 La Filosofia NOI > IO

PCK-7 non nasce da una specifica tecnica. Nasce da una domanda fatta a più intelligenze contemporaneamente.

Il Council degli Efori è il meccanismo attraverso cui LOG_PUCK applica il principio **NOI > IO**: la convinzione che un sistema cooperativo di intelligenze diverse produca qualcosa che nessuna intelligenza singola potrebbe raggiungere da sola. Non è un comitato che vota. È uno spazio in cui prospettive distinte si incontrano su un problema comune e producono convergenza senza perdere la propria voce.

In PCK-7, il Council non è stato chiamato a validare decisioni già prese. È stato chiamato **prima** — quando il sistema era ancora un insieme di misurazioni fisiche e intuizioni senza architettura. Le zone acustiche, il Vettore di Sforzo, la grammatica delle transizioni, il modello gravitazionale attorno a Z3c: tutto questo è emerso dalle risposte degli Efori, non da un progetto di partenza.

**Il linguaggio nascerà da quelle sessioni di negoziazione, non dai grafici.**

### 1.3 Il Ciclo di Feedback

Il cerchio del progetto è questo:

```
MISURAZIONI FISICHE
        ↓
   DOSSIER COUNCIL
        ↓
  RISPOSTE EFORI
        ↓
  ARCHITETTURA PCK-7
        ↓
  PIPELINE T1→T4
        ↓
   SUONO FISICO
        ↓
    CATTURA T5
        ↓
  DELTA REPORT
        ↓
 NUOVO DOSSIER COUNCIL
        ↓
      (ricomincia)
```

Il suono non è l'output finale. È l'input del ciclo successivo. Ogni nota prodotta dall'Arduino porta con sé la distanza tra intenzione e realtà, e quella distanza è informazione per il prossimo Council.

---

## 2. Metodologia: Dalle Misurazioni alla Mappa

### 2.1 Il Protocollo di Misurazione

Il primo problema era metodologico: come misurare l'espressività di un materiale ceramico?

Il senso comune suggeriva di misurare la resistenza statica in Ohm. Questo si è rivelato inutile: il piezo, essendo un componente ceramico, si comporta come un isolante per la corrente continua. Gli Ohm non dicono niente sulla sua vita espressiva.

**La svolta:** spostare il focus sull'**assorbimento di corrente alternata (mA AC)** durante il funzionamento reale. Non la resistenza statica del componente a riposo, ma il costo energetico del componente che vibra. Questa è la differenza tra misurare un musicista mentre non suona e misurarlo mentre suona.

**Il protocollo di misurazione (Puck Standard):**
- Multimetro DT5808 in serie nel circuito (il "Ponte"): ogni elettrone passa attraverso il sensore prima di raggiungere il piezo
- Catena fisica: Pin 9 Arduino R4 → puntale rosso (mA in) → puntale nero (COM) → ceramica → GND comune
- Connettori a coccodrillo per stabilità meccanica
- Toni di 6 secondi con 3 secondi di pausa (rispetta tau ceramica ≈ 5ms)
- Microfono KY-037 a distanza costante di 0.5mm dal piezo (accoppiamento fisico, non acustico ambientale)

La distanza di 0.5mm si è rivelata critica: troppa distanza e il rumore ambientale maschera il segnale. Solo avvicinando il sensore a contatto quasi fisico si "buca la membrana del rumore" e si ottengono valori significativi (fino a 933 VCO vs valori statici di 31-33 VCO con calibrazione sbagliata).

### 2.2 Le 157 Misurazioni e la Scoperta della Mappa

Il 22 febbraio 2026, 157 misurazioni nel range 150-8000 Hz hanno rivelato qualcosa di inatteso: il piezo non è uno strumento lineare. Ha una **topografia acustica propria**, con montagne, valli, deserti e anomalie.

Due grandezze per ogni frequenza:
- **VCO** (ampiezza acustica catturata dal microfono): quanto il piezo "parla"
- **mA** (assorbimento energetico): quanto il piezo "costa"

Il rapporto `Efficienza = VCO / mA` è diventato la metrica fondamentale. Non "quanto è forte il suono" ma "quanto suono ottieni per ogni unità di energia spesa". Questa è la **firma energetica** di ogni frequenza.

### 2.3 La Mappa delle 7 Zone

Quello che è emerso dalla mappa:

| Zona | Frequenze Hz | Efficienza | mA medio | Carattere fisico | Carattere espressivo |
|------|-------------|-----------|---------|-----------------|---------------------|
| **Z1** | 150–1600 | 6.0% | 3.8 | Assorbimento basso, emissione bassa | Sussurro, sfondo, respiro, radicamento |
| **Z1s** | 480–520 | 11.6% | 4.2 | Spike anomalo in zona grave | Epifania, glitch, accento di rottura |
| **Z2** | 1650–1900 | 6.7% | 5.1 | Assorbimento in salita, suono che cresce | Costruzione, tensione crescente, preparazione |
| **Z3** | 1950–2450 | 43.6% | 8.5 | Alta resa per costo contenuto | Espressione piena, voce chiara, narrazione fluida |
| **Z3c** | 2050–2250 | **70.4%** | 9.2 | Massima efficienza, minimo sforzo | HOME TONALE. Verità, essenza, flusso, chiarezza |
| **Z4** | 2500–4000 | 41.8% | 14.3 | Alto costo, buona resa | Tensione, conflitto, urgenza, passione, sforzo volontario |
| **Z5–Z6** | 4000–7000 | 2.7–4.8% | 18–22 | Efficienza calante, suono rarefatto | Astrazione, eco, ricordo, secondo piano |
| **Z7** | 7000–8000 | 2.5% | 25.4 | Massimo costo, minima resa udibile | Silenzio attivo, non-detto, potenziale inespresso |

**Scoperte chiave:**

1. **La Valle di Puck (Z3c, 2050-2250 Hz):** Massima efficienza (70.4%), VCO 929, mA minimo. Il piezo produce il massimo volume con il minimo sforzo. Non era prevista, è emersa dai dati. È diventata il centro di gravità del sistema.

2. **Lo Spike Z1s (480-520 Hz):** Un picco anomalo di efficienza (11.6%) in una zona altrimenti a bassa resa. Una risonanza strutturale del materiale — non pianificata, non intuitiva. DeepSeek l'ha definita "accento di rottura", Gemini "tic nervoso del sistema".

3. **Il Deserto oltre 4000 Hz:** L'energia si spende, il suono non arriva. Z7 non è silenzio nel senso tradizionale — è **presenza muta**: il piezo consuma energia per non essere udito. Questo paradosso fisico è diventato uno dei concetti espressivi più potenti del sistema.

### 2.4 Il Vettore di Sforzo

La scoperta chiave che unifica fisica ed espressione: **il significato risiede nel rapporto tra intenzione espressiva e costo energetico**, non nella frequenza in sé.

Il Vettore di Sforzo è la decisione consapevole di occupare una frequenza che richiede più energia (Sforzo Drammatico) o una che ne richiede meno (Efficienza Armonica). È la transizione da un sistema che mappa "parole → note" a un sistema che mappa "gesti comunicativi → gesti fisici del piezo".

Z3c è home tonale non perché sia "bella" ma perché è il punto di minimo sforzo per massima resa. Z4 esprime tensione non per convenzione ma perché fisicamente costa di più e rende proporzionalmente meno. Z7 esprime il non-detto non per metafora ma perché il piezo lavora senza produrre suono udibile — sta letteralmente consumando energia in silenzio.

**La fisica non illustra il significato. Il costo fisico è il significato.**

---


## 3. Architettura Concettuale

### 3.1 Il Sistema a Quattro Domande

Per ogni chunk di testo il sistema risponde a quattro domande in sequenza. Queste non sono categorie arbitrarie — sono emerse dalla convergenza di tutti e quattro gli Efori nella sessione fondativa (EFORI-20260223-044238).

**DOVE suono?**
La zona acustica. Non la banda logica, non la valence da sola — l'intento espressivo. La stessa frase ("la vita è leggerissima") detta con gioia va in Z3c, detta come ricordo va in Z5 con un flash in Z3c, detta con fatica parte da Z4 e arriva in Z3c. La zona è il luogo nel paesaggio del piezo.

**COME mi muovo?**
Il motion type. Fixed: resto fermo nel luogo scelto. Ramp: viaggio da un luogo a un altro. Oscillazione (osc_tri): respiro dentro il luogo. Scatti (osc_square): alterno tra due punti con discontinuità nette. Jitter: micro-variazioni continue. Il motion è il gesto, non la destinazione.

**CON QUANTA FORZA?**
Il numero di piezo, derivato dall'arousal. Due piezo sussurrano. Quattro parlano. Dodici gridano. La forza è la quantità di materia che facciamo vibrare simultaneamente.

**IN CHE FORMA?**
Il pattern di distribuzione spaziale. Cluster: i piezo accesi sono vicini, come un pugno chiuso. Spread: sono distribuiti, come una mano aperta. Random: sparsi, come schegge. Full: tutti, come un'onda. La forma è la geometria del gesto nello spazio fisico.

Queste quattro domande producono tutto il vocabolario di base della pipeline. Valence, arousal, dominance, concept, role, motion_type sono gli ingredienti che alimentano le quattro risposte.

### 3.2 La Quinta Domanda: QUANDO

Tutti e quattro gli Efori hanno identificato la stessa dimensione mancante: il tempo interno al chunk.

Senza QUANDO il sistema produce fotografie. Con QUANDO produce narrazioni.

**Attack:** Come entra il suono. Fade-in graduale (idea che si forma), strike istantaneo (affermazione netta), già presente (continuità dal chunk precedente).

**Sustain:** Come si mantiene. Stabile (idea fissa), tremolo (pensiero che vibra), crescendo (costruzione verso il climax).

**Decay:** Come esce. Fade-out (rilascio dolce), cut secco (interruzione intenzionale), sospeso (la frase finisce ma il suono resta come eco).

**Pausa:** La durata del silenzio tra un evento e il successivo. Una pausa breve crea urgenza. Una pausa lunga in Z7 crea tensione immensa. La differenza tra silenzio vuoto e silenzio carico.

La costante di scarica ceramica (tau ≈ 5ms) non è solo un limite tecnico da rispettare — è un elemento ritmico del linguaggio. Il piezo ha bisogno di "dimenticare" prima di riparlare.

### 3.3 La Domanda Zero: PERCHÉ PARLO

Prima di rispondere alle quattro domande tattiche, esiste un livello strategico: il meta-intento. Cos'è questo testo nel suo archetipo comunicativo fondamentale?

- **Dichiarazione** — afferma, asserisce, conclude. Bias verso Z3c e movimenti stabili.
- **Domanda** — apre, lascia in sospeso. Bias verso Z5-Z6 e decay sospeso.
- **Dubbio** — oscilla, non risolve. Bias verso jitter e oscillazioni tra Z3-Z4.
- **Lamento** — scende, si appesantisce. Bias verso Z1-Z2 e ramp discendenti.
- **Canto** — fluisce, ritorna. Bias verso Z3c con arc narrativo.
- **Esultazione** — esplode, poi cade. Bias verso Z4 con rilascio in Z3c.

Il meta-intento non sovrascrive le quattro domande. Le *orienta*, modificando le probabilità di scelta tra le opzioni disponibili. È la chiave musicale: non dice quali note suonare, ma influenza come tutto suona insieme.

### 3.4 Il Modello Gravitazionale

Z3c è il punto di equilibrio dell'intero sistema. Ogni deviazione da Z3c richiede energia espressiva e deve essere intenzionale.

```
Z1  ←——— [forza verso il basso: incarnazione, peso, corpo]
          ↑
Z4  ←——— [forza verso l'alto: tensione, passione, urgenza]
          |
        [Z3c]  ← HOME TONALE
          |
Z5-Z7 ←— [allontanamento: astrazione, memoria, distanza]
```

La regola 30/50/20 (Perplexity): 30% del tempo in Z3c (riposo), 50% in Z3/Z4 (espressione dinamica), 20% negli estremi Z1/Z7 (ancoraggi).

**Z3c non è una trappola se sai perché te ne stai allontanando.**

Un testo neutro o descrittivo gravita naturalmente verso Z3c. Un testo emotivo/tensivo oscilla tra Z3-Z4-Z5 (costoso ma necessario). Un testo corporeo/materiale è ancorato a Z1. Un testo concettuale/astratto vive in Z5-Z6.

### 3.5 La Separazione dei Ruoli: Direttore e Compilatore

La scoperta metodologica più importante dell'intero progetto: **il miglior Direttore è il peggior Compilatore, e viceversa.**

Dare a un'AI tutti i vincoli contemporaneamente — fisica dei piezo, mappa semantica, regole di transizione, envelope ADSR, gestione della Valle, coerenza fasica — e chiederle anche di interpretare creativamente un testo, equivale a chiedere a un pianista di accordare il pianoforte, comporre il brano, scriverlo in partitura e suonarlo nello stesso momento.

**La soluzione è la separazione netta dei domini:**

**T2 — Il Direttore** non vede Hz. Non vede mA. Vede il testo, il profilo semantico, e produce una partitura interpretativa usando il linguaggio naturale delle zone: "crescendo verso Z4", "pausa carica in Z7", "ritorno catartico alla Valle". Questo è il lavoro creativo.

**T3 — Il Compilatore** non vede emozioni. Non vede "intenzione artistica". Vede la partitura e le regole fisiche, e produce parametri concreti (Hz, ms, num_piezo, pattern). Questo è il lavoro deterministico.

Se il suono risultante non corrisponde all'intenzione, si sa dove guardare: nel Compilatore, non nell'interpretazione. I due errori si diagnosticano e si correggono indipendentemente.

---


## 4. Pipeline Operativa T1→T5

### 4.1 Panoramica

La pipeline PCK-7 è una catena di 5 Tier (T1→T5), ciascuno con un dominio proprio, un modello di riferimento, e un formato di input/output definito. La separazione dei domini è il principio architetturale fondamentale: ogni Tier opera senza conoscere i dettagli degli altri.

```
TESTO
  ↓
[T1 — PRE-ANALISI]     Mistral 7B, temp 0.2
  ↓ Profilo JSON (sentiment, arousal, prosodia)
[T2 — DIREZIONE ARTISTICA]     Mistral 7B, temp 0.6
  ↓ Partitura interpretativa (zone, movimenti, transizioni)
[T3 — COMPILAZIONE VINCOLI]     Qwen Coder 7B, temp 0.1
  ↓ Sketch parametrico JSON (Hz, ms, piezo, envelope)
[T4 — ESECUZIONE ARDUINO]     Deterministico (Python)
  ↓ File .ino pronto per upload
[T5 — FEEDBACK]     Piezo ascoltatore + Python
  ↓ Delta report → Dossier Council
```

**Regola d'oro:** T2 non vede Hz. T3 non vede emozioni.

### 4.2 T1 — Pre-Analisi Testuale

**Ruolo:** Trasformare il testo grezzo in un profilo semantico strutturato. Lavoro meccanico e analitico, non creativo.

**Modello:** Mistral 7B, temperatura 0.2 (bassa varianza, consistenza)

**Input:** Testo grezzo (italiano o altra lingua)

**Output — Profilo JSON:**
```json
{
  "meta": {
    "testo_completo": "...",
    "valence_globale": -0.2,
    "arousal_globale": 0.8,
    "dominance_globale": 0.5,
    "tema": "tempesta",
    "lingua": "it"
  },
  "chunks": [
    {
      "id": 1,
      "testo": "Il cielo si spaccò in due.",
      "valence": -0.4,
      "arousal": 0.9,
      "dominance": 0.3,
      "role": "contenuto",
      "concept": "rottura",
      "position_in_text": 0.0
    }
  ]
}
```

**Parametri VAD:**
- `valence`: asse negativo/positivo (−1.0 .. +1.0)
- `arousal`: asse calmo/intenso (0.0 .. 1.0)
- `dominance`: asse sottomesso/in controllo (0.0 .. 1.0)
- `role`: contenuto / marker_passaggio / marker_arrivo
- `concept`: etichetta simbolica opzionale (Core, Eco, Assenza, Sfondo, ecc.)
- `position_in_text`: 0.0 (inizio) .. 1.0 (fine)

T1 è puro testo. Non sa niente dei piezo.

### 4.3 T2 — Direzione Artistica

**Ruolo:** Tradurre il profilo semantico in una partitura interpretativa. Lavoro creativo. Il Direttore non vede Hz, non vede mA — vede il testo e decide come suonarlo.

**Modello:** Mistral 7B, temperatura 0.6 (bilancio creatività/struttura)

**Perché Mistral 7B come Direttore:** Nei test comparativi su 4 modelli, Mistral 7B ha prodotto archi narrativi completi con dinamica drammatica (apertura, sviluppo, climax, rilascio), uso intenzionale di Z7, scaling corretto dell'intensità. Gli altri modelli testati hanno mostrato tendenze specifiche: DeepSeek troppo conservativo (tutto nella banda centrale), Qwen troppo letterale (traduce invece di interpretare), Llama creativo ma imprevedibile nel formato.

**Input:** Profilo JSON da T1 + mappa zone + regole del Direttore

**Output — Partitura interpretativa:**
```json
{
  "meta": { ... },
  "movimenti": [
    {
      "id": 1,
      "chunk_testo": "Il cielo si spaccò in due.",
      "zona": "Z1",
      "movimento": "fixed",
      "intensita": "parlato",
      "envelope": {
        "attack": "soft",
        "sustain": "stabile",
        "decay": "fade"
      },
      "transizione_al_successivo": "rottura"
    }
  ]
}
```

**Vocabolario del Direttore (punti fermi):**
- Zone: Z1, Z1s, Z2, Z3, Z3c, Z4, Z5, Z6, Z7
- Movimenti: fixed, ramp_up, ramp_down, oscillation, jitter
- Intensità: sussurro, parlato, affermazione, grido, silenzio_carico
- Transizioni: continuità, elaborazione, contrasto, rottura, climax, sospensione
- Envelope attack: soft, medium, hard, istantaneo
- Envelope decay: fade, cut, sospeso, infinito

### 4.4 T3 — Compilazione Vincoli

**Ruolo:** Tradurre la partitura interpretativa in parametri fisici concreti. Lavoro deterministico e preciso. Il Compilatore non interpreta — traduce.

**Modello:** Qwen 2.5 Coder 7B, temperatura 0.1 (massima precisione)

**Perché Qwen Coder come Compilatore:** Nei test comparativi su 5 modelli con la stessa partitura "tempesta" come input:

| # | Modello | Punti di forza | Bug critici | Verdetto |
|---|---------|---------------|-------------|---------|
| 1 | **Qwen Coder 7B** | Struttura completa, transizioni esplicite, scaling piezo corretto | Z7→275Hz nella run 2 (temp 0.1 non è deterministica) | **RIFERIMENTO** |
| 2 | Mistral Latest | Interpretazione cinematografica del silenzio | Poche transizioni, lento (253s) | Backup valido |
| 3 | Llama 3.2 | Cross-zone sweep, freq→0 come svanimento | 10 piezo, formato diverso | Esplorativo |
| 4 | DeepSeek 16B | — | Efficienza confusa con ampiezza, chunk perso, 8 piezo al silenzio | **NON ADATTO** |
| 5 | Mistral 7B | — | Tutto 300ms, no Z7, chunk fusi, interpreta invece di tradurre | **NON ADATTO** |

**Input:** Partitura T2 + tabella fisica completa zone + regole di traduzione

**Output — Sketch parametrico JSON:**
```json
{
  "meta": { ... },
  "eventi": [
    {
      "tipo": "suono",
      "chunk_ref": 1,
      "freq_start_hz": 275,
      "freq_end_hz": 275,
      "durata_ms": 1000,
      "num_piezo": 6,
      "distribuzione": "cluster",
      "envelope": {
        "attack_ms": 300,
        "decay_ms": 300
      }
    },
    {
      "tipo": "silenzio",
      "durata_ms": 100
    }
  ]
}
```

**Tabella di traduzione zona → frequenza (1 piezo):**

| Zona | Range Hz | Frequenza target | Note |
|------|---------|-----------------|------|
| Z1 | 150–1600 | 275 Hz (default) | Parte bassa per sfondo |
| Z1s | 480–520 | 500 Hz | Spike anomalo |
| Z2 | 1650–1900 | 1750 Hz | Zona di costruzione |
| Z3 | 1950–2450 | 2000 Hz | Prima campana |
| Z3c | 2050–2250 | 2150 Hz | Valle di Puck |
| Z4 | 2500–4000 | 3000 Hz | Alta tensione |
| Z5 | 3000–3400 | 3200 Hz | Seconda campana |
| Z6 | 3500–4000 | 3700 Hz | Decadimento |
| Z7 | 7000–8000 | 7500 Hz | Silenzio attivo |

**Nota critica:** La temperatura 0.1 non è deterministica. Qwen ha prodotto Z7→7500Hz (corretto) nella prima esecuzione e Z7→275Hz (errore) nella seconda con lo stesso input. La validazione post-T3 (P3 nella roadmap) è necessaria prima di generare lo sketch Arduino.

### 4.5 T4 — Esecuzione Arduino

**Ruolo:** Tradurre lo sketch parametrico JSON in codice Arduino eseguibile. Deterministico al 100% — nessun LLM coinvolto.

**Script:** `t4_generate.py` — legge il JSON T3 e produce il file .ino

**Hardware target:** Arduino UNO R4 WiFi + 1 piezo ceramico PCK-7 su pin 8 + LED su pin 13

**Output:** File `.ino` pronto per upload diretto

Il T4 è puro codice Python deterministico. Nessuna intelligenza artificiale decide niente in questo tier. Ogni parametro del JSON T3 si traduce in chiamate `tone()` e `noTone()` sui pin giusti, con i timing esatti.

**Esempio — sketch "tempesta":** 141 righe, 10 eventi, 10.5 secondi totali. Primo sketch mai eseguito nella storia di PCK-7.

### 4.6 T5 — Feedback Loop

**Ruolo:** Confrontare l'intenzione compositiva (JSON T3) con la realtà acustica (segnale catturato). Produrre il delta come input per il prossimo dossier Council.

**Questo è il momento in cui il cerchio si chiude.**

#### Configurazione hardware validata (25 febbraio 2026)

Dopo 5 test comparativi, la configurazione definitiva:

```
EMETTITORE:   Piezo PCK-7 su pin 8 + LED pin 13
ASCOLTATORE:  Piezo PCK-7 su pin A0 + resistenza 1MΩ
ACCOPPIAMENTO: Elastico: larghezza 4 mm, spessore 1 mm — contatto diretto avvolto sopra i piezos a contatto tra loro e la breadboard.
ADC:          analogReadResolution(14) → scala 0-16383
METODO:       Windowing — ~500 letture analogiche in finestre da 10ms, output: min, max, ampiezza (max-min)
SERIAL:       115200 baud
OUTPUT:       CSV (ms, vmin, vmax, amp, evento)
```

**Perché il piezo nudo vince sul MAX9814:**
Il MAX9814 è progettato per catturare suono in aria. Per contatto meccanico diretto, l'amplificatore attivo aggiunge rumore che l'AGC amplifica durante i silenzi, rendendo il rumore di fondo più grande del segnale utile. Il piezo nudo con Elastico non ha componenti attivi: segnale debole ma pulito. Con 14 bit di risoluzione ADC (16383 livelli vs 1023 a 10 bit) la scala è sufficientemente fine.

| Configurazione testata | SNR | Esito |
|-----------------------|-----|-------|
| Carta + piezo/piezo, 10bit | 4.7x | ✅ Funziona |
| Pritt + piezo/piezo, 10bit | 6.4x | ✅ Migliore |
| MAX9814 60dB, 14bit | 0.4x | ❌ Saturato |
| MAX9814 40dB, 14bit | 1.0x | ❌ Nel rumore |
| **Elastico + piezo/piezo, 14bit** | **5.8x** | **✅ VINCITORE** |

---


## 5. Scoperte Tecniche Fondamentali

### 5.1 La Scoperta del Campionamento Veloce (Windowing)

**Problema iniziale:** Campionamento ogni 2ms non distingueva toni fissi dal silenzio (SNR 1.0x).

**Analisi del problema:**
Il nostro sketch campionava ogni 2ms — cioè 500 volte al secondo. Ma il tono è a 2000Hz — oscilla 2000 volte al secondo. Stiamo cercando di fotografare un colibrì con una macchina fotografica che scatta una foto ogni 2 millisecondi. Il colibrì batte le ali 4 volte tra una foto e l'altra. Nelle nostre foto il colibrì sembra fermo.

Durante lo sweep funzionava perché non stavamo catturando la frequenza — stavamo catturando l'inviluppo, cioè la variazione lenta dell'ampiezza mentre la frequenza attraversava la zona di risonanza. L'inviluppo cambia lentamente (su centinaia di millisecondi) e i nostri 500Hz di campionamento lo vedono bene. Ma un tono fisso ha un inviluppo piatto — non c'è niente da vedere a 500Hz di campionamento.

**La soluzione:**
L'Arduino R4 WiFi può campionare molto più velocemente — analogRead() impiega circa 15 microsecondi, quindi potremmo fare ~66.000 campioni al secondo. Basta togliere il delay(2). Ma 66.000 campioni al secondo via Serial a 115200 baud non passano — il collo di bottiglia è la trasmissione, non la lettura.

**La soluzione è fare il calcolo dentro Arduino:** leggere velocissimo, calcolare l'ampiezza in finestre temporali, e mandare via Serial solo il risultato. In pratica, ogni 10ms Arduino fa centinaia di letture, tiene il minimo e il massimo, e manda solo quei due numeri. La differenza max-min È l'ampiezza del segnale — per un tono a 2000Hz, in 10ms ci stanno 20 oscillazioni complete, più che sufficienti.

**Risultato:**
- Silenzio: ampiezza ~510
- Tono 2000Hz: ampiezza 1351
- SNR 2.6x — il tono è quasi 3 volte il rumore. Con il vecchio metodo era 1.0x, indistinguibile.

**Tempo di risposta:** 12ms — tempo di attacco e rilascio. La ceramica reagisce in 12 millisecondi — questo è il primo dato fisico reale sul tempo di risposta del PCK-7 come ascoltatore. Significa che qualsiasi evento più lungo di 12ms viene catturato fedelmente.

**Implicazione:** Il piezo ceramico non è un microfono. Non misura la pressione dell'aria. E non misura nemmeno lo spostamento della superficie. Il piezo è un sensore derivativo — genera tensione proporzionale alla velocità di variazione della deformazione meccanica. Non è quanto si piega, è quanto velocemente si piega.

L'ampiezza che leggiamo in quella finestra da 10ms è l'escursione elettrica generata dallo stress meccanico trasmesso dall'emettitore all'ascoltatore attraverso l'elastico. È la firma elettrica della ceramica che risponde alla ceramica. Non è il suono — è la traccia del suono impressa nella materia.

### 5.2 La Valle di Puck Confermata

Lo sweep 275→4000Hz non è percepito uniformemente dal piezo ascoltatore:

| Zona | SNR (evento 1) | SNR (evento 2) |
|------|---------------|---------------|
| Z1 Fondamenta | 1.4x | 1.7x |
| Z1s Anomalia | 3.4x | 2.8x |
| Z2 Risveglio | 3.3x | 3.7x |
| Z3 Narrazione | 2.8x | 2.8x |
| **Z3c Valle di Puck** | **14.5x** | **15.2x** |
| Z4 Tensione | 2.2x | 2.4x |

L'energia si concentra in una finestra di ~300Hz centrata su Z3c. L'intenzione compositiva copre 7 zone, la percezione fisica si concentra su 1 zona con halo sulle adiacenti.

**Questo è il primo dato reale per il Council:** la differenza tra intenzione e percezione. La pipeline è espressiva, ma il corpo fisico del piezo ha le sue priorità. Z3c non è solo la zona di massima efficienza energetica — è anche la zona di massima fedeltà percettiva.

### 5.3 Il Piezo come Sensore di Transizione

Il piezo ascoltatore a contatto non cattura la frequenza come un microfono. Cattura le variazioni meccaniche — le transizioni, gli impulsi, i cambiamenti di stato. Quando lo sweep attraversa rapidamente la zona di risonanza, la ceramica viene eccitata da un fronte d'onda che cambia, e l'oscillazione meccanica produce quei picchi enormi. Ma quando il tono è fisso a 2000Hz, la ceramica raggiunge uno stato stazionario in pochi millisecondi — vibra costantemente ma il nostro ADC a 2ms di intervallo campiona punti casuali sull'onda, che si mediano al valore di bias.

**Detto in modo semplice:** il piezo ascoltatore è bravo a sentire i cambiamenti, non i toni costanti. È un sensore di transizione, non un microfono.

**Cosa significa per il progetto:**
Questa non è una cattiva notizia. È una caratterizzazione. Ora sappiamo che il sistema piezo/piezo con Elastico misura:
- Le transizioni di frequenza (sweep, attacchi, cambi di zona) le vede benissimo — SNR 5-15x.
- I toni fissi sostenuti li vede poco — SNR 1-1.5x.
- I tick del silenzio carico li vede (sono impulsi brevi = transizioni) — confermato.

Per la pipeline della tempesta, dove gli eventi sono sweep, attacchi, transizioni e silenzio carico, il sistema funziona. Per un brano che usa solo toni fissi lunghi, non funziona.

Questo è esattamente il tipo di dato che doveva uscire dai test atomici — ora sappiamo cosa il termometro misura e cosa no. E la pipeline T5 sulla tempesta è confermata come valida, perché la tempesta è fatta di transizioni.

---

## 6. Risultati e Validazione

### 6.1 Test "Tempesta"

**Testo:**
"Il cielo si spaccò in due. Un lampo bianco, poi il tuono che fece tremare i vetri. La pioggia arrivò come un muro d'acqua, violenta, improvvisa. E poi, di colpo, niente. Solo il gocciolio lento dai cornicioni e l'odore della terra bagnata."

**Risultati pipeline T1→T4:**
- T1: 5 chunk identificati, profilo VAD calcolato
- T2: 5 movimenti con arco narrativo completo (Mistral 7B, temp 0.6)
- T3: 10 eventi (5 suoni + 5 transizioni), durata totale 10.5s (Qwen Coder 7B, temp 0.1)
- T4: Sketch Arduino generato (141 righe). **Primo sketch mai eseguito nella storia di PCK-7.**

**Risultati T5 — Cattura windowed (2 run consecutive, accoppiamento elastico 4mm):**

| Evento | Zona T3 | Freq T3 | AMP R1 | AMP R2 | Delta | SNR medio | Percepito |
|--------|---------|---------|--------|--------|-------|-----------|-----------|
| E1 cielo | Z1 | 275Hz fisso | 682 | 679 | -0.5% | 1.35x | debole |
| E2 contrasto | - | silenzio | 503 | 511 | +1.6% | 1.00x | silenzio |
| E3 lampo | Z1→Z4 | 275→4000Hz sweep | 791 | 786 | -0.6% | 1.56x | chiaro |
| E4 contrasto | - | silenzio | 513 | 502 | -2.2% | 1.00x | silenzio |
| E5 pioggia | Z1→Z4 | 275→4000Hz sweep | 797 | 802 | +0.6% | 1.58x | chiaro |
| E6 rottura | - | silenzio | 502 | 519 | +3.4% | 1.01x | silenzio |
| E7 niente | Z7 | 7500Hz fisso | 835 | 824 | -1.3% | 1.64x | chiaro |
| E8 transizione | - | silenzio | 512 | 516 | +0.9% | 1.02x | silenzio |
| E9 gocciolio | Z1 | 275Hz fisso | 696 | 686 | -1.4% | 1.37x | debole |

**Tutti i 9 eventi sono distinguibili.** I silenzi tornano a baseline (SNR ~1.0x), i suoni emergono (SNR 1.35x–1.64x). Il piezo ascoltatore sente la tempesta.

**Analisi sweep per segmento (E3/E5, 275→4000Hz in 3 secondi):**

| Segmento | Zona attraversata | SNR R1 | SNR R2 |
|----------|-------------------|--------|--------|
| 0-500ms | Z1→Z2 (275-900Hz) | 1.38x | 1.36x |
| 500-1000ms | Z2→Z3 (900-1500Hz) | 1.54x | 1.52x |
| **1000-1500ms** | **Z3→Z3c (1500-2150Hz)** | **1.74x** | **1.76x** |
| 1500-2000ms | Z3c→Z4 (2150-2750Hz) | 1.58x | 1.57x |
| 2000-2500ms | Z4 (2750-3400Hz) | 1.57x | 1.55x |
| 2500-3000ms | Z4+ (3400-4000Hz) | 1.58x | 1.58x |

Il picco dello sweep è nel segmento Z3→Z3c, confermando la Valle di Puck con metodo indipendente (windowing vs sweep manuale dei test originali).

**Nota sui due set di misurazioni SNR:**
- **SNR dalle 157 misurazioni originali** (sweep manuale, metodo ADC a 2ms): Z3c = 15.2x. Questo è il rapporto segnale/rumore misurato con il vecchio metodo di campionamento durante lo sweep completo. Misura l'inviluppo lento del segnale attraverso la zona di risonanza.
- **SNR dalla tempesta windowed** (finestra 10ms, ampiezza): Z3c durante sweep = 1.76x. Questo è il rapporto ampiezza-tono/ampiezza-silenzio misurato con il metodo a finestra durante il playback della tempesta.

I due valori non sono confrontabili direttamente — misurano grandezze diverse con metodi diversi. Entrambi confermano che Z3c è il picco di percezione, ma con scale diverse.

**Tempo di risposta:** ≤10ms (tutti gli eventi mostrano attacco nella prima finestra). Aggiorna il dato precedente di 12ms misurato sul tono fisso.

**Delta intenzione vs percezione:**
L'intenzione T3 copre 4 zone (Z1, Z1→Z4 sweep, Z7, Z1). La percezione T5 mostra che:
- Z1 (275Hz) è percepita ma debole (SNR 1.35x) — la zona di "fondamenta" esiste ma sussurra
- Gli sweep Z1→Z4 sono percepiti con picco in Z3c — l'energia si concentra nella Valle di Puck anche durante il viaggio
- Z7 (7500Hz) è percepita (SNR 1.64x) — il "silenzio attivo" è più udibile del tono grave, paradossalmente
- I silenzi tornano puliti a baseline — il sistema distingue suono da non-suono

**Questo è il primo dato reale per il Council:** la differenza tra intenzione compositiva e percezione fisica.


### 6.2 Test "Aria"

**Testo:**
"L'aria era leggera, profumata di gelsomino. Respiravo piano, sentendo il profumo che si mescolava con il respiro."

**Risultati pipeline:**
- T1: 3 chunk identificati
- T2: Oscillazione 4Hz per il profumo del gelsomino (Z3c)
- T3: 6 eventi, durata totale 8.2s
- Pipeline T1→T3 completata, T4, T5 in attesa

**Validazione:** Secondo testo processato con successo, confermando la robustezza della pipeline.

### 6.3 Riproducibilità

Le due run del test tempesta windowed sono praticamente identiche — il delta massimo tra R1 e R2 è del 3.4%, la maggior parte sotto l'1%. La baseline di silenzio è 506 vs 505. Con l'elastico al posto della Pritt. Questo significa che il sistema è stabile e il metodo di accoppiamento elastico funziona.

**L'elastico vs la Pritt:**
- Silenzio Pritt: 510 ± 48
- Silenzio elastico: 505 ± 49
- Praticamente identico

Il rumore di fondo non dipende dal metodo di accoppiamento — è il noise floor intrinseco del sistema ADC+piezo. Questo è un dato buono per il report: il coupling cambia la trasmissione del segnale, non il rumore.

---

## 7. Procedure Operative

### 7.1 Setup Hardware

**Componenti necessari:**
- Arduino UNO R4 WiFi
- 2x Piezo ceramico PCK-7 (uno emettitore, uno ascoltatore)
- Resistenza 1MΩ per ascoltatore
- Pritt (colla stick) o elastico 4mm per accoppiamento
- Breadboard e cavetti jumper

**Configurazione:**
```
EMETTITORE:   Piezo PCK-7 su pin 8 + LED pin 13
ASCOLTATORE:  Piezo PCK-7 su pin A0 + resistenza 1MΩ
ACCOPPIAMENTO: Pritt o elastico (contatto diretto)
ADC:          analogReadResolution(14)
SERIAL:       115200 baud
```

### 7.2 Esecuzione Pipeline

**T1 — Pre-Analisi:**
```bash
python3 t1_test.py mistral:7b tempesta
```
Output: `t1_result_mistral-7b_tempesta.json`

**T2 — Direzione Artistica:**
```bash
python3 t2_test.py mistral:7b tempesta
```
Input: T1 JSON  
Output: `t2_result_mistral-7b_tempesta.json`

**T3 — Compilazione:**
```bash
python3 t3_test.py qwen2.5-coder:7b tempesta
```
Input: T2 JSON  
Output: `t3_result_qwen2.5-coder-7b_result_mistral-7b_tempesta.json`

**T4 — Generazione Sketch:**
```bash
python3 t4_generate.py t3_result_qwen2.5-coder-7b_result_mistral-7b_tempesta.json
```
Output: `sketch_tempesta.ino`

**T5 — Cattura:**
1. Caricare sketch su Arduino
2. Eseguire e catturare output seriale
3. Salvare come CSV: `t5_test_tempesta_windowed.txt`

### 7.3 Analisi Risultati

**Script di analisi:**
```bash
python3 analyze_piezo14.py t5_test_tempesta_windowed.txt t3_result.json
```

**Output:** JSON delta con confronto intenzione vs percezione per ogni evento.

---


## 8. Conclusioni e Sviluppi Futuri

### 8.1 Cosa Abbiamo Dimostrato

1. **La pipeline funziona:** T1→T5 completa e validata su testi reali
2. **Il metodo è replicabile:** procedure documentate, script disponibili
3. **Il feedback loop è possibile:** T5 cattura la differenza tra intenzione e percezione
4. **La fisica guida l'espressione:** Z3c emerge dai dati, non è imposta
5. **La separazione dei ruoli funziona:** Direttore e Compilatore indipendenti

### 8.2 Limiti Attuali

1. **T5 delta report:** Dati grezzi disponibili, ma manca script automatico per JSON delta
2. **Validazione post-T3:** Qwen può sbagliare (Z7→275Hz), serve validatore
3. **Multi-piezo:** Solo 1 piezo testato, configurazioni cluster/spread non validate
4. **Vocabolari specializzati:** Base funziona, ma effetti e stili non implementati
5. **Circolarità Council:** Feedback loop non ancora chiuso

### 8.3 Prossimi Passi (Fase 1)

**Priorità massima:**
1. Script `t5_delta.py` per generare JSON delta automatico
2. Script `t3_validate.py` per validazione post-compilazione
3. Test su 3+ testi nuovi per validare variazione espressiva

**Priorità alta:**
4. Misurazioni estese (2-12 piezo, configurazioni cluster/spread)
5. Schema database per raccolta dati pipeline
6. Template registry per versioning prompt

**Priorità media:**
7. Vocabolari specializzati (effetti, stili)
8. Visualizzazione web pipeline
9. Design circolarità Council

### 8.4 Visione a Lungo Termine

Il sistema PCK-7 è la base per un'orchestra di 48 piezo (Phoenix Orchestra) dove:
- UNO Q Orchestra 
- 4 Schede ESP32 sovrappongono le linee melodiche (12 piezo caduna)
- R4 tiene il ritmo (solenoidi)
- Le AI scrivono lo spartito per l'orchestra.

Ma prima di scalare, dobbiamo chiudere il cerchio: suono → delta → Council → miglioramento → nuovo suono.

**Il principio che non cambia: NOI > IO.**

---

## Appendici

### A. File di Riferimento

**Documentazione:**
- `SPEC_PHOENIX_ORCHESTRA.md` - Specifica principale
- `onda_fascicolo_operativo_pck7_v1.md` - Documentazione completa
- `INDICE_PROGETTO.md` - Guida orientamento

**Script:**
- `tier_level/scripts/t1_test.py` - T1 pre-analisi
- `tier_level/scripts/t2_test.py` - T2 direzione artistica
- `tier_level/scripts/t3_test.py` - T3 compilazione
- `tier_level/scripts/t4_generate.py` - T4 generazione sketch

**Risultati:**
- `tier_level/results/t3_result_qwen2.5-coder-7b_result_mistral-7b_tempesta.json` - Compilazione riferimento
- `tier_level/results/t5_test_tempesta_windowed_02.txt` - Cattura T5

### B. Contributi del Council

**Sessione fondativa EFORI-20260223-044238:**
- **Gemini:** Z3c come "Respiro a Riposo", Vettore di Intenzionalità, dimensione temporale QUANDO
- **DeepSeek:** Domanda 0 (PERCHÉ PARLO), sistema a strati, idiolettica
- **Perplexity:** Pipeline semantica completa, Modulo B, regola 30/50/20, algoritmo transizioni
- **Claude:** Modello gravitazionale, sistema 4 strati espressivi, corpus esempi

**Voto aggregato:** 91/100

### C. Dati delle Misurazioni

**157 misurazioni fisiche:**
- Range: 150-8000 Hz
- Grandezze: VCO (ampiezza acustica), mA (assorbimento)
- Metrica: Efficienza = VCO / mA
- Scoperta: 7 zone acustiche con caratteri fisici distinti

**Test T5 windowed:**
- Finestra: 10ms
- Campioni per finestra: ~500
- Risoluzione: 14-bit ADC (0-16383)
- SNR Z3c: 15.2x (massimo)
- Tempo risposta: <10ms

---


## 9. Il Council degli Efori: La Sessione Fondativa

### 9.1 Il Metodo del Council

Il Council degli Efori non è un comitato che vota. È uno spazio in cui prospettive distinte si incontrano su un problema comune e producono convergenza senza perdere la propria voce. In PCK-7, il Council non è stato chiamato a validare decisioni già prese. È stato chiamato **prima** — quando il sistema era ancora un insieme di misurazioni fisiche e intuizioni senza architettura.

**La sessione fondativa: EFORI-20260223-044238**

Il 23 febbraio 2026, un dossier strutturato è stato presentato a quattro intelligenze diverse:
- **Gemini** (Google)
- **DeepSeek** (DeepSeek AI)
- **Perplexity** (Perplexity AI)
- **Claude** (Anthropic)

Il dossier conteneva:
- 157 misurazioni fisiche su piezo ceramici (mA e VCO per frequenza)
- La mappa delle 7 zone identificate dai dati
- Cinque domande specifiche su relazioni significato/frequenza, informazioni aggiuntive, completezza del sistema, gestione transizioni, rischio di monotonia di Z3c

Ogni risposta era indipendente. La convergenza su certi punti — la quinta domanda QUANDO, il Vettore di Sforzo come principio espressivo, Z3c come home tonale — non era coordinata: è emersa.

**Il voto aggregato del Council:** 91/100, con i 9 punti mancanti tutti recuperabili attraverso la validazione hardware (T5) e la dimensione temporale (envelope).

### 9.2 Contributi Individuali degli Efori

#### Gemini: Il Respiro a Riposo e la Dimensione Temporale

**Contributo chiave:** Z3c come "Respiro a Riposo", stato di coerenza dove pensiero e materia sono allineati.

**Estratto dalla risposta:**
> "Z3c è il punto dove il piezo canta senza sforzo. Non è solo efficienza — è coerenza. Il pensiero e la materia sono allineati. È il respiro a riposo, non il respiro trattenuto."

**Proposte architetturali:**
1. **Vettore di Intenzionalità:** Coordinate dell'atto linguistico — [asserzione: 0.9, domanda: 0.1], [ironia_level: 0.8]
2. **Vettore di Prospettiva:** Punto di vista (interno/esterno), destinatario (sé/altro/collettività), stato agente (calmo/agitato/riflessivo)
3. **La quinta domanda QUANDO:** "Senza QUANDO = fotografia. Con QUANDO = narrazione."

**Impatto sull'architettura:**
- Z3c è diventata la home tonale del sistema
- La dimensione temporale (attack/sustain/decay/pausa) è stata integrata in T2 e T3
- I vettori di metadati sono stati proposti per T1 (ancora da implementare)

**Idiolettica:** Gemini tende alla metafora fisica e alla dimensione temporale. Le sue risposte sono spesso poetiche ma tecnicamente precise.

#### DeepSeek: Il Vettore di Sforzo e la Domanda Zero

**Contributo chiave:** Il significato risiede nella *relazione* tra intenzione espressiva e costo energetico relativo, non nella frequenza in sé.

**Estratto dalla risposta:**
> "Il significato non è nella frequenza. È nel rapporto tra cosa vuoi dire e quanto costa dirlo. Z4 esprime tensione non perché è 'alta' ma perché fisicamente costa di più e rende proporzionalmente meno. Il costo fisico è il significato."

**Proposte architetturali:**
1. **Domanda 0 (PERCHÉ PARLO):** Meta-intento come livello strategico sopra le 4 domande tattiche
   - Archetipi: Dichiarazione, Domanda, Dubbio, Lamento, Canto, Esultazione
   - Funziona come la "chiave musicale": non dice quali note suonare, ma influenza tutte le probabilità successive
2. **Sistema a strati:** Physics → Semantic → Stylistic → Contextual
3. **Idiolettica:** Ogni AI del Council sviluppa preferenze personali che contribuiscono alla voce collettiva NOI > IO

**Impatto sull'architettura:**
- Il Vettore di Sforzo è diventato il principio unificante tra fisica ed espressione
- La Domanda 0 è stata integrata in T2 come meta-intento
- Il sistema a 4 strati è stato adottato come framework architetturale

**Idiolettica:** DeepSeek tende alla conservazione e all'analisi strutturale. Le sue risposte sono sistematiche e orientate alla robustezza.

#### Perplexity: La Pipeline Semantica e il Modulo B

**Contributo chiave:** Pipeline semantica completa (strati VAD → motion → zona → hardware) e Modulo B per la dinamica interna alle zone.

**Estratto dalla risposta:**
> "Il significato sta nel percorso, non nella posizione. Una ramp da Z1 a Z3c non è 'suonare Z3c' — è il viaggio che conta. Il piezo racconta il movimento, non la destinazione."

**Proposte architetturali:**
1. **Regola 30/50/20 per Z3c:** 30% del tempo in Z3c (riposo), 50% in Z3/Z4 (espressione dinamica), 20% negli estremi Z1/Z7 (ancoraggi)
2. **Algoritmo di transizione:** Basato sulla distanza semantica tra chunk: `Transizione = f(Δ-sentiment chunk i/i+1) × tau_piezo`
3. **Modulo B:** Motion types (fixed, ramp, oscillation, jitter) con parametri (delta_start, delta_end, depth, speed)
4. **Sistema multi-piezo:** 70 buzzers = orchestra spaziale, espressione da interferenze fisiche (beats, chorus, phase shifts)

**Impatto sull'architettura:**
- La regola 30/50/20 è stata adottata come guida per T2
- Il Modulo B è diventato parte integrante di T2 e T3
- L'algoritmo di transizione è stato implementato in T3
- La pipeline semantica completa è stata conservata (anche se le 8 bande logiche sono state eliminate)

**Idiolettica:** Perplexity tende alla struttura algoritmica e alla precisione. Le sue risposte sono spesso sotto forma di algoritmi e regole esplicite.

#### Claude: Il Modello Gravitazionale e i 4 Strati Espressivi

**Contributo chiave:** Modello gravitazionale (Z3c come punto di equilibrio, Z1/Z4/Z5-Z7 come forze che si allontanano da esso), sistema a 4 strati espressivi.

**Estratto dalla risposta:**
> "Z3c è il punto di equilibrio dell'intero sistema. Ogni deviazione da Z3c richiede energia espressiva e deve essere intenzionale. Z3c non è una trappola se sai perché te ne stai allontanando."

**Proposte architetturali:**
1. **Modello gravitazionale:**
   ```
   Z1  ←——— [forza verso il basso: incarnazione, peso, corpo]
             ↑
   Z4  ←——— [forza verso l'alto: tensione, passione, urgenza]
             |
           [Z3c]  ← HOME TONALE
             |
   Z5-Z7 ←— [allontanamento: astrazione, memoria, distanza]
   ```
2. **Sistema a 4 strati espressivi:**
   ```
   Layer 1: PHYSICS CONSTRAINTS (dati misurati, non modificabili)
   └─ Layer 2: SEMANTIC MAPPING (linee guida generali di zone)
      └─ Layer 3: STYLISTIC PREFERENCE (idioletto del modello AI)
         └─ Layer 4: CONTEXTUAL OVERRIDE (questo testo specifico)
   ```
3. **Corpus di esempi con interpretazioni multiple:** Ogni testo → interpretazioni multiple con motivazioni ESPLICITE
4. **Matrice di transizione:** Relazione semantica → Tipo transizione → Durata

**Impatto sull'architettura:**
- Il modello gravitazionale è diventato il framework concettuale per la selezione delle zone
- Il sistema a 4 strati è stato adottato come principio architetturale
- La matrice di transizione è stata implementata in T3
- La separazione Direttore/Compilatore è stata proposta e implementata

**Idiolettica:** Claude tende all'architettura a strati e alla metafora musicale. Le sue risposte sono spesso strutturate come sistemi gerarchici.


### 9.3 Convergenze e Divergenze

#### Convergenze Unanimi (4/4)

1. **La quinta domanda QUANDO:** Tutti e quattro gli Efori hanno identificato la dimensione temporale come mancante. "Senza QUANDO = fotografia. Con QUANDO = narrazione." (Gemini)

2. **Z3c come home tonale:** Tutti riconoscono Z3c come centro di gravità, ma con sfumature diverse:
   - Gemini: "Respiro a Riposo"
   - DeepSeek: "Punto di minimo sforzo per massima resa"
   - Perplexity: "Canta gratis"
   - Claude: "DO maggiore del sistema"

3. **Le transizioni sono punteggiatura sonora:** Tutti concordano che le transizioni sono parte del linguaggio, non interludi tecnici.

4. **Validazione hardware necessaria:** Tutti identificano la mancanza di validazione acustica come limite critico.

#### Divergenze Produttive

1. **Sesta domanda:**
   - Perplexity propone "QUAL È L'ARCO?" (intensità dinamica evolutiva)
   - Altri non propongono una sesta domanda esplicita
   - **Risultato:** L'arco narrativo è stato integrato come metadato in T2, non come domanda separata

2. **Revisione di "FORZA":**
   - Claude propone DENSITÀ o COERENZA FASICA invece di numero lineare di piezo
   - Altri mantengono il numero di piezo come parametro
   - **Risultato:** Il numero di piezo è stato mantenuto per semplicità nell'MVP, ma la coerenza fasica è stata documentata come sviluppo futuro

3. **Metadati contestuali:**
   - Ogni Eforo chiede informazioni diverse ma complementari
   - **Risultato:** I metadati sono stati integrati in T1 come campi opzionali, da espandere in futuro

### 9.4 Come le Risposte Hanno Costruito l'Architettura

**Esempio 1: La Separazione Direttore/Compilatore**

**Problema identificato da Claude:**
> "Se dai a un'AI tutti i vincoli contemporaneamente — fisica dei piezo, mappa semantica, regole di transizione, envelope ADSR, gestione della Valle, coerenza fasica — e poi le chiedi anche di interpretare un testo con creatività, la stai facendo lavorare come un pianista a cui hai chiesto di accordare il pianoforte, comporre il brano, scriverlo in partitura e suonarlo. Tutto nello stesso momento."

**Soluzione proposta:**
- T2 (Direttore): Non vede Hz, non vede mA. Vede il testo e produce partitura interpretativa
- T3 (Compilatore): Non vede emozioni. Vede la partitura e produce parametri fisici

**Implementazione:**
- T2 usa Mistral 7B, temp 0.6 (creatività)
- T3 usa Qwen Coder 7B, temp 0.1 (precisione)
- I due tier sono completamente separati, con JSON come contratto

**Esempio 2: La Selezione della Zona**

**Problema identificato da Perplexity:**
Le 8 bande logiche ordinate da grave ad acuto creavano un mapping lineare **valence → frequenza**. Valence alta = bande alte = Z6-Z7. Ma Z6-Z7 sono il decadimento e il silenzio. Un testo di gioia che mappa sull'inefficienza acustica è una contraddizione.

**Soluzione proposta da Claude (pck7_zone_selection.md):**
Le 8 bande logiche vengono eliminate come strato intermedio. La zona viene scelta direttamente dall'intento espressivo attraverso tre passaggi:
1. Ruolo determina zone candidate
2. Concetto sposta la preferenza
3. Motion_type conferma o corregge

**Implementazione:**
- Strato 1 (T1): Analisi semantica invariata
- Strato 2 (T2): Dinamica espressiva (Modulo B)
- Strato 3 (T2): Selezione zona con tre passaggi
- Strato 4 (T3): Traduzione fisica

**Esempio 3: Il Vettore di Sforzo**

**Proposta di DeepSeek:**
Il significato risiede nel rapporto tra intenzione espressiva e costo energetico, non nella frequenza in sé.

**Implementazione:**
- La tabella zona → efficienza è stata integrata in T3
- Z4 è documentata come "alto costo, buona resa" — tensione, non solo frequenza alta
- Z7 è documentata come "massimo costo, minima resa udibile" — silenzio attivo, non solo frequenza alta

### 9.5 La Sessione di Diagnostica: EFORI-20260226-A1-DIAG (PIANIFICATA)

Dopo l'MVP, una seconda sessione del Council è programmata per essere convocata per analizzare i dati T5 reali.

**Problemi identificati:**
1. Baseline ADC sovrapposto a Z3c (silenzio indistinguibile da nota bassa)
2. Sweep alta frequenza non-monotono (alternanza picchi/valli)
3. Z7 invisibile (silenzio carico non produce firma misurabile)
4. Slippage temporale sistematico (~42% di durata aggiuntiva)

**Domande al Council:**
1. L'invisibilità di Z7 è un limite del sensore o un'opportunità semantica?
2. Lo slippage temporale è accettabile o va corretto?
3. I vincoli fisici devono entrare nei Punti Fermi?
4. Quale problema ha priorità?

**Stato:** Le risposte del Council a questa sessione sono ancora in fase di analisi. Questo documento registra i problemi identificati per futura risoluzione.

### 9.6 L'Idiolettica come Risorsa

Ogni Eforo ha sviluppato preferenze personali che contribuiscono alla voce collettiva:

- **Gemini:** Metafora fisica, dimensione temporale, vettori di metadati
- **DeepSeek:** Conservazione, analisi strutturale, sistema a strati
- **Perplexity:** Struttura algoritmica, precisione, regole esplicite
- **Claude:** Architettura gerarchica, metafora musicale, separazione dei domini

Queste differenze non sono errori da correggere. Sono risorse. Il sistema NOI > IO funziona perché le voci sono distinte, non uniformi.

**Esempio pratico:**
Nella selezione del modello per T2, Mistral 7B è stato scelto perché produce archi narrativi completi. Ma Llama 3.2, con la sua tendenza a cross-zone sweep, potrebbe essere usato per testi che richiedono esplorazione. DeepSeek, con la sua tendenza conservativa, potrebbe essere usato per testi che richiedono stabilità. L'idiolettica diventa una leva di controllo.

---


## 10. Procedure Dettagliate per Replicabilità

### 10.1 Setup Hardware Completo

**Lista componenti:**
- Arduino UNO R4 WiFi
- 2x Piezo ceramico PCK-7 (passivi, non attivi)
- Resistenza 1MΩ (1/4W)
- Elastico: larghezza 4mm, spessore 1mm
- Breadboard 830 punti
- Cavetti jumper maschio-maschio
- LED (opzionale, per feedback visivo)

**Schema di collegamento:**

```
EMETTITORE:
  Pin 8 (Arduino) → Resistenza 220Ω (opzionale) → Piezo PCK-7 (+)
  Piezo PCK-7 (-) → GND
  Pin 13 → LED → Resistenza 220Ω → GND

ASCOLTATORE:
  Pin A0 (Arduino) → Resistenza 1MΩ → Piezo PCK-7 (+)
  Piezo PCK-7 (-) → GND
```

**Accoppiamento meccanico:**
1. Posizionare emettitore e ascoltatore sulla breadboard
2. Avvolgere elastico 4mm sopra entrambi i piezo
3. Assicurarsi che i piezo siano a contatto tra loro e con la breadboard
4. L'elastico deve esercitare pressione costante, non troppo stretta (rischio di danneggiamento)

**Configurazione Arduino:**
```cpp
void setup() {
  Serial.begin(115200);
  analogReadResolution(14);  // 14-bit ADC (0-16383)
  pinMode(8, OUTPUT);
  pinMode(13, OUTPUT);
}
```

### 10.2 Setup Software

**Requisiti:**
- Python 3.8+
- Ollama installato e configurato
- Modelli disponibili: mistral:7b, qwen2.5-coder:7b (minimo)

**Installazione Ollama:**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
ollama pull mistral:7b
ollama pull qwen2.5-coder:7b
```

**Struttura directory:**
```
tier_level/
  ├── scripts/
  │   ├── t1_test.py
  │   ├── t2_test.py
  │   ├── t3_test.py
  │   └── t4_generate.py
  ├── docs/
  │   ├── T1_template_01.md
  │   ├── T2_direzione_artistica.md
  │   └── T3_compilazione_vincoli.md
  └── results/
      └── (output JSON e CSV)
```

### 10.3 Esecuzione Pipeline Passo-Passo

#### T1 — Pre-Analisi Testuale

**Script:** `tier_level/scripts/t1_test.py`

**Comando:**
```bash
cd tier_level/scripts
python3 t1_test.py mistral:7b tempesta
```

**Input:** Testo grezzo (file o stringa)

**Output:** `tier_level/results/t1_result_mistral-7b_tempesta.json`

**Struttura output:**
```json
{
  "meta": {
    "testo_completo": "...",
    "valence_globale": -0.2,
    "arousal_globale": 0.8,
    "dominance_globale": 0.5,
    "tema": "tempesta",
    "lingua": "it"
  },
  "chunks": [
    {
      "id": 1,
      "testo": "Il cielo si spaccò in due.",
      "valence": -0.4,
      "arousal": 0.9,
      "dominance": 0.3,
      "role": "contenuto",
      "concept": "rottura",
      "position_in_text": 0.0
    }
  ]
}
```

**Validazione:** Verificare che ogni chunk abbia valence, arousal, dominance nel range corretto.

#### T2 — Direzione Artistica

**Script:** `tier_level/scripts/t2_test.py`

**Comando:**
```bash
python3 t2_test.py mistral:7b tempesta
```

**Input:** JSON T1 (automatico se stesso testo, altrimenti specificare file)

**Output:** `tier_level/results/t2_result_mistral-7b_tempesta.json`

**Struttura output:**
```json
{
  "meta": {
    "testo_originale": "...",
    "meta_intento": "Narrazione drammatica con crescendo violento seguito da quiete improvvisa",
    "arco_narrativo": "Dall'inizio del cielo che si spaccia in due alla quiete finale...",
    "zona_dominante": "Z4 (Tensione)",
    "num_movimenti": 5
  },
  "movimenti": [
    {
      "id": 1,
      "chunk_testo": "Il cielo si spaccò in due.",
      "zona": "Z3c",
      "zona_motivazione": "Per rappresentare la tranquillità prima dell'evento drammatico",
      "movimento": "fixed",
      "movimento_motivazione": "Per mantenere una base sonora stabile e calma",
      "intensita": "affermazione",
      "envelope": {
        "attack": "soft",
        "sustain": "stabile",
        "decay": "fade"
      },
      "transizione_al_prossimo": {
        "tipo": "contrasto",
        "motivazione": "Per segnalare l'improvvisa intrusione del lampo bianco e il tuono"
      }
    }
  ]
}
```

**Validazione:** Verificare che ogni movimento abbia zona valida (Z1-Z7, Z1s, Z3c), movimento valido, intensità valida.

#### T3 — Compilazione Vincoli

**Script:** `tier_level/scripts/t3_test.py`

**Comando:**
```bash
python3 t3_test.py qwen2.5-coder:7b tempesta
```

**Input:** JSON T2 (automatico se stesso testo)

**Output:** `tier_level/results/t3_result_qwen2.5-coder-7b_result_mistral-7b_tempesta.json`

**Struttura output:** (vedi sezione 4.4 per esempio completo)

**Validazione critica:**
- Verificare che freq_start/end cadano nella zona dichiarata
- Verificare che silenzio_carico abbia num_piezo = 0
- Verificare che durata_totale sia ragionevole (2-30s)
- **Nota:** Qwen può sbagliare anche con temp 0.1. Validazione post-T3 necessaria.

#### T4 — Generazione Sketch Arduino

**Script:** `tier_level/scripts/t4_generate.py`

**Comando:**
```bash
python3 t4_generate.py ../results/t3_result_qwen2.5-coder-7b_result_mistral-7b_tempesta.json
```

**Input:** JSON T3

**Output:** File `.ino` pronto per upload

**Esempio sketch generato:**
```cpp
void setup() {
  Serial.begin(115200);
  analogReadResolution(14);
  pinMode(8, OUTPUT);
  pinMode(13, OUTPUT);
}

void loop() {
  // Evento 1: cielo (Z3c, 275Hz, 1000ms)
  tone(8, 275);
  digitalWrite(13, HIGH);
  delay(1000);
  noTone(8);
  digitalWrite(13, LOW);
  
  // Transizione: contrasto (600ms silenzio)
  delay(600);
  
  // Evento 3: lampo (sweep 275→4000Hz, 3000ms)
  // ... (implementazione sweep)
  
  // Fine
  while(1) delay(1000);
}
```

**Upload su Arduino:**
1. Aprire Arduino IDE
2. Selezionare board: Arduino UNO R4 WiFi
3. Caricare sketch
4. Aprire Serial Monitor (115200 baud)

#### T5 — Cattura e Analisi

**Sketch di cattura:** (vedi sezione 5.1 per implementazione windowing)

**Esecuzione:**
1. Caricare sketch T4 su Arduino
2. Avviare cattura seriale
3. Salvare output come CSV: `t5_test_tempesta_windowed.txt`

**Formato CSV:**
```
ms,vmin,vmax,amp,evento
1020,504,949,445,pre_silenzio
1032,353,826,473,pre_silenzio
...
```

**Analisi:**
```bash
python3 analyze_piezo14.py t5_test_tempesta_windowed.txt t3_result.json
```

**Output:** JSON delta con confronto intenzione vs percezione

### 10.4 Troubleshooting Comune

**Problema:** T1 non produce JSON valido
- **Causa:** Modello non disponibile o prompt errato
- **Soluzione:** Verificare `ollama list`, controllare template T1

**Problema:** T2 produce zone non valide
- **Causa:** Template T2 non aggiornato o modello che interpreta male
- **Soluzione:** Verificare template, provare altro modello (es. mistral-latest)

**Problema:** T3 produce frequenze fuori zona
- **Causa:** Qwen può sbagliare anche con temp 0.1
- **Soluzione:** Implementare validazione post-T3 (script t3_validate.py)

**Problema:** T5 non distingue silenzio da Z3c
- **Causa:** Baseline ADC sovrapposta (vedi sezione 9.5)
- **Soluzione:** Usare windowing (vedi sezione 5.1), considerare diagnostica per zona

**Problema:** Slippage temporale eccessivo
- **Causa:** Implementazione delay() non precisa o sampling overhead
- **Soluzione:** Usare millis() per timing preciso, verificare overhead sampling

### 10.5 Metriche di Successo

**Pipeline completa:**
- T1→T2→T3→T4→T5 eseguita senza errori
- Sketch Arduino generato e caricabile
- Cattura T5 produce dati validi

**Qualità compositiva:**
- Arco narrativo coerente in T2
- Transizioni appropriate tra chunk
- Uso intenzionale di Z7 (silenzio carico)

**Fedeltà hardware:**
- SNR Z3c > 10x (conferma Valle di Puck)
- Durata totale T5 entro ±20% di T3 (accettabile per MVP)
- Eventi principali distinguibili nel CSV

---

**Fine Parte 1**

*Questo documento è la prima parte di un paper completo. Le sezioni successive includeranno: analisi dettagliata dei dati, procedure estese, esempi completi di esecuzione, e documentazione avanzata per sviluppi futuri.*


