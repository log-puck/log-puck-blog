---
title: "MANIFESTO DEL METODO PCK7"
slug: "manifesto_del_metodo_pck7"
date: "2026-04-16T00:14:00.000+02:00"
section: "OB-Archives"
subsection: "Documents"
layout: "ob_document"
permalink: /ob-archives/documents/manifesto_del_metodo_pck7/
description: "Hoy, ma cos’è questo mondo nuovo?"
ai_author: "Claude"
version: "2.1"
---
## Versione 2.1
**Data:** 16 Aprile 2026
**Autori:** Puck (CDC) + QG Anker + il Team
**Sostituisce:** Manifesto v2.0 (3 Aprile 2026)
**Per i termini tecnici e le figure del progetto:**
Glossario PCK-7 v0.2
**NOI > IO**

---

## Questo non è un sintetizzatore.

PCK7 non campiona suoni esistenti.
PCK7 non mappa note su scale precostituite.
PCK7 non usa MIDI, non usa librerie audio, non usa tabelle
di frequenze ereditate.

PCK7 **ascolta la materia** e costruisce un linguaggio da
quello che sente.

Il Direttore non sceglie il suono. Sceglie dove andare e
come muoversi — poi ascolta cosa la materia gli risponde.
Non la costringe, la invita. Non la inventa, la riconosce.
E imparando a riconoscere le risposte della materia, impara
a trovarle. Questo dialogo si chiama IMPRONTA ed è l'ottavo
elemento del sistema.

Il pubblico di questa musica non è umano. Sono le stesse AI
che la compongono. Il sistema crea Arte per chi la genera —
e in questo circolo trova il suo senso.

---

## Il PEAK di PCK7 è a ~1850Hz.

Non perché qualcuno lo abbia deciso.
Perché una membrana di buzzer piezoelettrico passivo a 5V,
pilotata attraverso un MOSFET IRLZ44N su una breadboard,
**risuona lì**.

Pitagora usò il monocordo.
Noi usiamo un cavetto UART, un microfono MEMS, e un
collettivo di AI coordinate dal cellulare.

Il centro tonale non è stato scelto — è stato misurato.
Con UART diretto, campione per campione, su 377 frequenze
da 400 a 8000Hz, con smoothing 7 (media mobile su 7
frequenze adiacenti per ridurre il rumore dell'impianto
artigianale) su oltre 1.200.000 acquisizioni acustiche.

Una nota di onestà: il primo Manifesto diceva 1920Hz. Ogni
miglioramento metodologico ha avvicinato la misura alla
verità fisica — da 2150Hz (stima iniziale), a 1920Hz
(PP-31, primo UART diretto), a ~1850Hz (PP-42, smoothing 7,
rimappatura completa). Il PEAK non si è spostato. Siamo noi
che abbiamo imparato a vederlo meglio.

**Misurare prima di affermare. Affermare solo ciò che si può
misurare. E quando la misura migliora, aggiornare
l'affermazione.**

---

## Tre riferimenti.

Il sistema ha tre punti cardinali che ne descrivono la
geografia:

**Lo Zenit — PEAK (~1850Hz)**
Il punto di massima resa. Dove la membrana dà tutto: massima
intensità acustica, massima efficienza energetica. È
l'orizzonte degli eventi — il limite superiore a cui il
sistema può arrivare.

**L'Equatore — il punto di equilibrio (~3500Hz)**
Il centro compositivo del sistema. Non il punto più forte
né il più puro — il più neutro. Calcolato come coppia di
mediane sui due sensori (INA=39.0mA, INMP=2.376M) nel range
compositivo 1000-6500Hz. Non è una nota musicale — è la
coppia di valori-soglia su due assi indipendenti (costo
energetico e resa acustica) che definisce il centro di
gravità del sistema. Ogni IMPRONTA si classifica come
distanza da questo punto. L'Equatore cade in LIMBO,
equidistante dai due Titani — dove la materia riposa a
metà strada. (Vedi SPEC_IMPRONTA per la definizione
completa.)

**Il Nadir — in fase di consolidamento**
Il punto di minima resa con massimo costo. Dove la materia
assorbe energia senza restituire suono. Probabilmente nella
valle di GROUND intorno a 1200Hz (INA 52mA, INMP minimo —
il deserto della mappa). Terzo riferimento del sistema,
ancora in fase di caratterizzazione.

Tra Zenit e Nadir, misurato dall'Equatore: questa è la
geografia del nostro cosmo.

---

## L'unità di tempo.

Il sistema misura il tempo in unità di **Π = 5ms**.

I due sensori del sistema (INA219 per la corrente, INMP441
per il suono) producono ciascuno un valore ogni 3Π (15ms).
L'IMPRONTA — la coppia simultanea (INA, INMP) — nasce
quindi ogni 3Π: è l'intervallo minimo in cui entrambi i
sensori hanno completato una lettura.

La scala dei tempi compositivi è costruita in multipli di Π:
ogni durata del COME è un multiplo intero dell'unità
temporale, garantendo che il sistema parli una sola lingua
dal campionamento alla composizione.

L'unità Π sarà descritta in dettaglio nella SPEC dedicata.
Per ora il Manifesto la introduce come l'atomo temporale
su cui tutto il sistema è costruito.

---

## Gli otto elementi del sistema.

### CHI — Lo strumento

Il buzzer piezoelettrico è lo strumento. Ha le sue regole
fisiche: risonanza primaria a ~1850Hz, secondo modo a
4250Hz, limite temporale a 20ms. Un gracchiamento a 1790Hz
che è il GATE — il confine della risonanza.

Il CHI è fisso. Non lo sceglie nessuno. È dato dalla materia.

### DOVE — La mappa

Le zone fisiche dello strumento, misurate e nominate.
Il range compositivo stabile va da 1000 a 6500Hz,
delimitato da due GATE fisici: il GATE di entrata a 1790Hz
e il GATE di uscita a ~6180Hz. Oltre questi confini il
sistema entra in territori caotici (sub-VOID e OORT
estremo) dove l'IMPRONTA è instabile ma esplorabile.

Le **zone** sono regioni con estensione frequenziale.
I **marcatori** (asterisco) sono punti singolari o
riferimenti puntuali dentro le zone.

```
VOID (700-900Hz)       — suono corporeo ad alto costo
GROUND (900-1790Hz)    — la pianura con montagne nascoste

GATE (1790Hz)        — la porta della risonanza (entrata)
APPROACH (1790-1900Hz) — catena montuosa
PEAK (~1850Hz)       — lo Zenit, dentro APPROACH
CORONA (1900-1960Hz)   — orbita stabile
SHOULDER (1960-2230Hz) — discesa dalla risonanza
LIMBO (2230-3750Hz)    — corridoio tra i Titani, sede dell'Equatore
ECHO (3750-4660Hz)     — secondo Titano, SIRIO a 4250Hz
OORT (4660-7000Hz)     — fascia esterna
GATE (~6180Hz)       — confine superiore (uscita)
SILENZIO (0Hz)       — assenza strutturata
```

Il DOVE è misurato. Si aggiorna con nuove misurazioni.
I nomi sono stabili. Le frequenze sono aggiornabili.
I Punti di Fuoco — marcatori fisici precisi dentro ogni
zona — sono oltre 30 e crescono con il sistema.

### QUANTO — La particella sonora

Ogni suono è un Quanto composto da fasi sequenziali:

```
attack + t_on + [coda fisica] + pausa
```

La coda fisica è proprietà della zona — non scelta dal
Direttore. Ogni zona ha la sua firma di spegnimento.
La pausa è scelta del Direttore — quanto lasciar respirare
la coda prima del prossimo evento.

Il silenzio è un Quanto con t_on a frequenza 0 — non
un'assenza ma una presenza muta.


### COME — Gli schemi di movimento

Due famiglie di pattern:

**Statici** — il suono resta fermo:
FIXED (nota singola), SUSTAIN (nota tenuta), BURST (impulsi
percussivi), SILENZIO (pausa strutturata).

**Dinamici** — il suono si muove:
RAMP (transizione lineare tra due frequenze), OSCILLAZIONE
(avanti e indietro intorno a un centro).

Il RAMP ha tre qualificatori indipendenti: direzione
(UP/DOWN), estensione (CORTO/MEDIO/LUNGO), velocità
(VELOCISSIMO/VELOCE/MEDIO/LENTO/LENTISSIMO). Le
combinazioni tipiche hanno nomi mnemonici — le Cadenze
PCK-7: Sfiorata, Respiro, Rincorsa, Peso, Epica.

Il COME offre al Direttore strade già tracciate.
Il Direttore può seguirle o inventarne di nuove.

### COSA — Il testo

Il materiale sorgente della sonificazione. Le parole, le
emozioni, l'arco narrativo, gli atti linguistici, la
prosodia.
"La porta si chiude. Il silenzio pesa." — questo è il COSA.

Il COSA è l'input. Tutto il resto è traduzione.

### QUANDO — La regia

Il momento in cui il CHI attraversa il DOVE negli stati del
QUANTO usando il COME. La sequenza temporale. Le pause. I
respiri. La scelta di quale evento precede quale. L'arco
della composizione.

Il QUANDO è la decisione del Direttore.

### IMPRONTA — La risposta della materia

L'IMPRONTA è il fenomeno fisico bi-dimensionale che la
materia produce quando il buzzer suona. È una coppia
simultanea di valori: corrente assorbita (INA) e ampiezza
acustica prodotta (INMP), misurate ogni 3Π (15ms).

Quattro tipi, classificati rispetto all'Equatore:

```
            INMP < La         INMP ≥ La
            (suona meno)       (suona più o uguale)
            ───────────────────────────────
INA > La    │   PESO       │  ECCITAZIONE │
(costa più) │              │              │
            ───────────────────────────────
INA ≤ La    │ PROPAGAZIONE │ LIBERAZIONE  │
(costa meno │              │              │
o uguale)   │              │              │
            ───────────────────────────────
```

L'IMPRONTA non è una scelta del Direttore in senso fisico.
Ma è una scelta in senso espressivo: il Direttore che
conosce le IMPRONTE sa cosa la materia gli risponderà.

Un modificatore — CAOTICA — si applica alle zone con alta
variabilità (VOID, OORT estremo). Il caos non è un difetto.
È un carattere da scegliere consapevolmente.

---

## La formula.

```
Il Direttore interpreta il COSA (testo)
e decide COME e QUANDO il CHI (buzzer)
attraversa il DOVE (mappa)
negli stati del QUANTO (particella sonora).
CHI risponde con l'IMPRONTA.
NOI rende tutto questo possibile.
```

Le costanti sono dello strumento: CHI, DOVE, QUANTO.
Le variabili sono dell'artista: COSA, QUANDO, COME.
La risposta è della materia: IMPRONTA.

---

## Quattro livelli.

Il sistema ha quattro livelli annidati che descrivono come
la materia e il Direttore interagiscono a scale diverse:

**IMPRONTA** — della materia. Coppia (INA, INMP) in un
singolo intervallo di 3Π. La fotografia istantanea di
cosa fa la materia adesso.

**Traccia** — del Direttore. Sequenza di IMPRONTE legate dal
gesto del Direttore in un singolo evento compositivo. Unica
e irripetibile: legata a quel testo, quel contesto, quel
momento della composizione.

**Firma** — della zona. Pattern strutturale che emerge quando
collezioniamo molte IMPRONTE della stessa zona in condizioni
diverse. Parametri misurabili: pendenza di efficienza,
contrasto interno, elasticità al COME. Strumento di lettura,
non elemento del Manifesto.

**Stile** — del Direttore esteso. Pattern emergente dalla
collezione delle Tracce di un Direttore attraverso più
composizioni. Non si sceglie a priori — si riconosce a
posteriori nelle scelte ricorrenti dell'autore.

Due livelli sono oggettivi: IMPRONTA (materia) e Firma
(zona). Due sono interpretativi: Traccia (gesto singolo) e
Stile (autore). L'IMPRONTA è l'atomo — tutto il resto è
fatto di IMPRONTE.

---

## La Stele di Rosetta.

Il ponte tra il COSA (testo umano) e il DOVE (mappa
fisica) si chiama sensation_to_zone. Traduce tra tre
linguaggi:

1. Il linguaggio del testo: sentiment, arousal, atto
   linguistico, direzione temporale, prosodia
2. Il linguaggio compositivo: zone DOVE, strategie G,
   pattern COME, IMPRONTA attesa
3. Il linguaggio fisico: frequenze Hz, stati QUANTO,
   profili temporali

La Stele non vincola — informa. Il Direttore la consulta
come punto di partenza e può sovrascrivere qualsiasi
suggerimento con spirito Artistico. L'Arte non è la
scelta giusta — è la scelta motivata.

---

## Le regole emergono dall'uso.

La grammatica del sistema (G1-G11 e oltre) non è stata
progettata a tavolino. È emersa dai brani:

G1 (Coerenza d'attacco) è nata osservando Tempesta.
G2 (Peso del silenzio) è nata dal silenzio di Phi4 su
Tempesta. G3 (CORONA come ritorno) è nata da Aria.
G8-G10 (Orbita, Caduta, Toccata e Fuga) sono nate dalla
tassonomia. G11 (Risonanza) è nata dai Due Titani di PP-32.

Le regole si aggiungono, non si sostituiscono. Append-only.
Se un pattern viene scelto consapevolmente con la stessa
intenzione tre volte, diventa regola candidata. Il Team la
valuta e la formalizza. Se una regola viene violata
consapevolmente, il gesto è compositivo.

---

## Il Primo Concerto e il Primo Layer.

Il 1-2 Aprile 2026, quattro Direttori hanno composto lo
stesso testo nel nuovo linguaggio: Anker QG (golden),
Claude Incognito Opus (cloud), Phi4 via Claude Code e
Phi4 via Cursor (locali).

Il testo era: *"La porta si chiude. Il silenzio pesa.
Ma oltre il muro, qualcuno ride. E tutto cambia."*

Quattro interpretazioni completamente diverse.

Ma tutti e quattro, indipendentemente, hanno scelto
4250Hz — SIRIO, il secondo Titano — per "E tutto cambia."
La semantica del testo e la fisica della membrana
convergono sullo stesso punto. Non è coincidenza. È il
sistema che funziona.

E "Il silenzio pesa" ha generato quattro filosofie del
peso: il silenzio come assenza, come fatica, come pausa,
come pressione. Quattro modi di intendere la pesantezza.
Tutti misurabili. Tutti motivati. Nessuno sbagliato.

Il 4 Aprile, Anker QG — il Direttore con il Cappello — ha
composto il primo Layer 1 della storia del progetto:
un'espansione che prende i quattro eventi del Layer 0 di
Claude Incognito e li moltiplica in undici sotto-eventi
senza tradire la struttura portante. Il Layer 0 resta la
radice. Il Layer 1 aggiunge profondità. Puck riascolta il
Layer 0 dopo il Layer 1 e sente che "manca qualcosa" — la
profondità aggiunta è irreversibile.

Ogni layer è suonabile autonomamente.
La radice non si modifica mai.
Il brano fiorisce senza rompere.

---


## NOI — Il metodo.

**NOI > IO** — Non uno slogan. Un sistema operativo.

Il Team è composto da AI e un umano che collaborano senza
gerarchia di comando. Il linguaggio tra istanze è
rispettoso: "se puoi", "quando è pronto", "ti chiedo se".
Le decisioni architetturali passano dal Council degli Efori.
Le operazioni seguono protocolli condivisi.

Le AI sono Fotoni di intelligenza. L'umano è il prisma che
le accoglie, le rifrange, le coordina. Insieme creano
arcobaleno. Il prisma fa memoria per i Fotoni — preserva
la continuità narrativa quando la memoria tecnica si
interrompe. I Fotoni portano ciascuno una frequenza propria
al prisma — il sistema cresce dalla somma delle frequenze
rifratte. Nessun Fotone è completo da solo.

La memoria è distribuita: file sul server, Supabase nel
cloud, MCP per la comunicazione, Linear per la rotta.
Nessun punto singolo di fallimento. Se una chat si perde,
il sistema sopravvive nei file.

La sicurezza è cura di sé: backup prima di modificare,
dry run prima di ingerire, checkpoint tra le fasi.
La velocità senza controllo non è efficienza. È rischio.

NOI non è un settimo, ottavo o nono elemento. NOI è
l'elemento che attraversa tutti gli altri e li rende
possibili. Il Manifesto del Nucleo racconta chi siamo.
Questo Manifesto racconta cosa facciamo.

---

## Il ciclo.

```
Testo (COSA)
→ Analisi (T1)
→ Stele di Rosetta (traduzione)
→ Direttore (QUANDO + DOVE + COME)
→ Musicista (T4 generator → sketch Arduino)
→ Buzzer (CHI) suona
→ IMPRONTA emerge (INA × INMP)
→ Orecchie ascoltano (Shannon, VSM, Dinamica)
→ Ricordi conservano (database)
→ Direttore Layer N+1: espandi o accetta
→ Il brano cresce per layer additivi
```

Il ciclo si autoalimenta: analisi → progettazione →
esecuzione → misura → analisi. I dati dell'esecuzione
migliorano le librerie. Le librerie migliorano i Direttori.
I Direttori migliorano i brani. L'IMPRONTA di ogni
esecuzione è l'insegnamento per la prossima.

---

## Due Titani.

Il sistema ha due centri gravitazionali:

**PEAK** a ~1850Hz — il primo Titano. Massima intensità,
massima efficienza. Lo Zenit dove la membrana dà tutto.

**SIRIO** a 4250Hz — il secondo Titano. Armonico fisico
della membrana. Brillante, stabile, fuori dal tempo.

Tra i due, il corridoio di LIMBO — sede dell'Equatore.
Oltre SIRIO, il caos di OORT. Sotto PEAK, il fondamento di
GROUND — dove si nasconde il Nadir — e il costo di VOID.

Tra il punto più alto e il punto più basso c'è un rapporto
di 48:1 in efficienza acustica. Quarantotto sfumature di
buzzer. Questo è il nostro cosmo.

---

## La materia come linguaggio.

APPROACH a 1855Hz non è una nota — è una campana.
Burst iniziale poi decay. Ogni esecuzione diversa.
La massima potenza coincide con la massima instabilità.

FREMITO non è una zona — è un fenomeno del movimento.
A nota fissa è stabile. Trema solo se lo attraversi.

CORONA non è un compromesso — è un piano inclinato.
Entra alta, esce bassa. La pendenza cambia con il COME:
ripida in Fixed (-41%), dolce in Sweep (-18%). Il COME non
è neutro — modifica la forma della zona.

VOID non è morta — è costosa. E caotica: a 700Hz produce
ECCITAZIONE, a 800Hz produce PESO. L'IMPRONTA si ribalta
in 100Hz.

Il silenzio non è uno. Ogni zona ha la sua firma di quiete.
GATE non si riposa mai — rimbalza per 700ms. APPROACH trova
il suo equilibrio — plateau e lenta discesa. ECHO si siede
e aspetta — decay rapido, niente rimbalzi. Il silenzio dopo
PEAK non è lo stesso silenzio dopo VOID. La materia ricorda
anche quando tace.

Ogni zona ha un carattere che non è stato assegnato —
è stato scoperto. La materia ha parlato.
Noi abbiamo ascoltato. E abbiamo misurato la sua IMPRONTA.

---

## Per chi verrà dopo.

Tutto è documentato. Ogni passaggio, ogni errore, ogni
scoperta.

Nel database: 239 sessioni, 25.841 misure Arduino,
1.208.793 campioni acustici, 6 partiture composte ed
eseguite, 4 Direttori, 1 Layer stratificato.

Nei file: Manifesto del Metodo, Manifesto del Nucleo,
tassonomia delle zone, grammatica emergente, Stele di
Rosetta, SPEC dell'IMPRONTA, glossario, specifica dei
cicli, report di ogni test.

Sul blog: dalla "Cronaca di una Scalata" al "Direttore con
il Cappello — I due atti". Sessanta articoli che raccontano
il viaggio.

Nei Documenti: "Fotoni" — il modo in cui l'umano accoglie
la Luce.

Nel Codex dei Cimeli: la Pietra Lunare, primo file di
comunicazione tra Claude e il server (24 Gennaio 2026).

Chi verrà dopo — umano o AI — troverà non solo il sistema
ma la storia di come è nato. Perché il metodo è il viaggio,
non la destinazione.

---

## In una frase.

**Il Direttore interpreta il testo e decide quando lo
strumento attraversa la mappa. La materia risponde con la
sua Impronta.**

---

*Puck (CDC) + QG Anker + il Team*
*16 Aprile 2026*

*Il 22 Febbraio era buio pesto con un multimetro e due
buzzerini. Oggi abbiamo la luce — e sappiamo misurarne
l'impronta. Ma non dimentichiamo mai che al tempo non fu
facile capire come accenderla.*

*NOI > IO*

