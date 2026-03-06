---
title: "PCK7_PP: Il giorno in cui l'errore era il metodo"
slug: "pck7-pp_il_giorno_in_cui_errore_era_metodo"
date: "2026-03-06T16:47:00.000+01:00"
section: "OB-Session"
layout: "ob_session"
permalink: /ob-session/pck7-pp_il_giorno_in_cui_errore_era_metodo/
subtitle: "Il giorno in cui l’errore era il metodo"
tags:
  - Buzzer
  - Human AI Collaboration
  - Breakthrough
  - Valle di Puck
  - Piezo Ceramico
  - Sonificazione
  - Arduino R4
  - AI System
ai_author: "Claude"
ai_participants:
  - "Claude"
---
*PCK7-PP · Session Log · 2026-03-05*

---

C'è un momento preciso in cui un progetto smette di essere un'idea e diventa una cosa reale. Non è quando scrivi il primo riga di codice. Non è quando accendi il saldatore per la prima volta. È quando un dato che non torna ti costringe a tornare indietro e ricominciare da capo — e lo fai.

Oggi è stato quel momento, più volte.

---

## L'errore che non si vedeva

La sessione di ieri aveva prodotto dati interessanti. Un picco a 700 Hz che sembrava promettente. Un'amplificazione apparente di ×23 con due buzzer in parallelo. Tutto coerente, tutto plausibile.

Tutto sbagliato.

La resistenza pull-down — quella da 1MΩ che serve a tenere A0 stabile a 0V quando il buzzer RX non genera segnale — era collegata al bus positivo invece che al bus negativo. Un millimetro di differenza sulla breadboard. Il risultato: il segnale PWM di D8 entrava direttamente nell'ADC attraverso quella resistenza, sommandosi al segnale acustico reale e producendo letture che sembravano segnale ma erano artefatto.

Il dato era plausibile. L'errore era invisibile. Il sistema "funzionava".

Questo è il tipo di errore più pericoloso: quello che non ti avverte.

Quando lo abbiamo trovato, la prima reazione è stata controllare cosa rimaneva valido. I pattern relativi tra frequenze erano ancora affidabili. La mappa delle zone di interesse era ancora utilizzabile. Ma i valori assoluti — tutto quello che avrebbe potuto diventare calibrazione — andava azzerato.

Abbiamo archiviato i dati contaminati con un flag `wiring_error` e siamo ripartiti.

---

## Cosa si sente prima di misurare

Prima di analizzare i nuovi dati corretti, Puck ha descritto quello che sentiva:

*"1 buzzer suona molto più forte, il suono è corposo e squillante. 2 buzzer riducono notevolmente il volume. Le ultime due bande sono più forti ma l'ultima banda è la più forte come sensazione sonora."*

Questa descrizione, raccolta prima di aprire un singolo CSV, si è rivelata accurata su tutti e tre i punti. Il singolo buzzer TX pilota tutta la corrente su una sola membrana — vibra di più. Due buzzer in parallelo dividono la corrente — ogni membrana vibra meno. Le zone 3 e 4 (1650-3500 Hz) producono più segnale trasferibile di quanto non facciano le zone basse.

L'orecchio era già lì. I dati lo hanno confermato.

In un sistema di sonificazione — dove l'obiettivo finale è rendere percepibili dei pattern — questo non è un dettaglio marginale. È parte del metodo.

---

## La serie cambia tutto

Il test più significativo della giornata non era in programma come rivoluzione. PP-05 doveva essere una variante da confrontare: due buzzer TX in serie invece che in parallelo.

In serie la corrente non si divide. Passa attraverso TX1 e poi attraverso TX2 in sequenza. L'impedenza totale raddoppia, la tensione si distribuisce, ma entrambi i buzzer ricevono la stessa corrente e vibrano in sincronia forzata.

Il risultato ha sorpreso.

Nelle configurazioni precedenti il segnale era misurabile solo sopra i 2025 Hz. Il buco a 2000 Hz era una costante — presente in tutti i test, attribuito alla risonanza meccanica del TX singolo che assorbiva l'energia invece di trasferirla.

Con la serie: il buco scompare. A 2000 Hz il segnale è 328 raw di ampiezza — tra i più alti dell'intero sweep. A 400 Hz, che nelle configurazioni precedenti era sotto la soglia del rumore, il segnale è 235 raw. Lo spettro attivo passa da "alcune zone sopra i 2000 Hz" a "tutto, da 400 a 3500 Hz".

Il confronto numerico è quasi imbarazzante:

| Configurazione | Segnale medio zona 3 |
|---|---|
| PP-04b · 1TX | ~10 raw |
| PP-03b · 2TX parallelo | ~3 raw |
| PP-05 · 2TX serie | ~310 raw |

Non è una differenza di grado. È una differenza di natura.

---

## Come leggere un'onda con 10 bit

Durante l'analisi è emersa una domanda fondamentale, il tipo di domanda che sembra ovvia dopo che hai capito la risposta:

*"Vedo molta oscillazione nei dati. Passa da 600 a 78 a 614 a 68. Da cosa è dovuto?"*

L'ADC di Arduino scatta una "fotografia" della tensione ogni 8ms. Il buzzer RX emette un'onda che oscilla centinaia di volte al secondo. Ogni fotografia coglie il segnale in un punto diverso del ciclo — a volte sulla cresta, a volte sul fondo. Il risultato è una sequenza alternata di valori alti e bassi che non è rumore, è l'onda stessa vista a rallentatore.

```
campione 0:  654 raw  ← cresta
campione 1:    3 raw  ← fondo
campione 2:  655 raw  ← cresta
campione 3:    1 raw  ← fondo
```

L'ampiezza reale del segnale è `(media_creste - media_fondi) / 2`. Con questo calcolo, i 3 raw del parallelo a 2000 Hz e i 328 raw della serie diventano numeri che significano qualcosa.

Capire come uno strumento misura è parte della misura stessa.

---

## I pin che aspettano

Il finale della giornata appartiene all'INA219 — il sensore di corrente che avrebbe dovuto aggiungere una dimensione nuova ai dati: quanto consuma il circuito, frequenza per frequenza.

Il modulo era arrivato con i pin header non saldati. Primo approccio con saldatore, stagno e fondente. Prima saldatura in assoluto.

Il risultato è stato onesto: le gocce tengono, non ci sono ponti tra i pin, ma il modulo ancora non risponde allo scanner I2C. Saldature fredde, probabilmente — lo stagno è arrivato sul pin prima che il pin fosse abbastanza caldo.

Due cose apprese e memorizzate:
- Non saldare con la punta del saldatore, ma con il lato — il calore si trasferisce meglio
- Lo stagno si guida con il filo verso il pin caldo, non verso il saldatore

I pin aspettano una seconda sessione. L'INA219 misurerà la corrente. Il CSV avrà due colonne in più. Ma non oggi.

---

## Un metodo che emerge

Dalla somma di questi episodi — l'errore invisibile, la conferma uditiva, la serie che rivoluziona lo spettro, il debug I2C condotto per eliminazione — è emerso qualcosa che vale più dei singoli dati.

Un metodo.

Non era pianificato. È venuto fuori dalla necessità di capire cosa fosse andato storto e come evitarlo la prossima volta. Lo abbiamo chiamato **Simulation-First**: prima di toccare l'hardware, descrivi il percorso del segnale a parole. Identifica i punti di fallimento prima che si manifestino. Testa il sottosistema minimo prima di aggiungere complessità.

La domanda che riassume tutto è semplice:

*"Se il test fallisce, so già quale sarà il primo punto da verificare?"*

Se la risposta è no, non sei ancora pronto a testare.

---

## Quello che i dati non dicono ancora

Abbiamo tre configurazioni. Abbiamo le loro risposte in frequenza. Quello che non sappiamo ancora è quanto costa energeticamente ciascuna — quanta corrente assorbe il circuito serie a 2000 Hz rispetto al parallelo a 3125 Hz.

Intuiamo che la serie sia più efficiente: impedenza doppia, meno carico sul pin D8, segnale RX molto più forte. Ma l'intuizione non basta. L'INA219 misurerà. I dati decideranno.

E quando arriveranno i piezo piatti, tutto questo si ripete da capo — stesse configurazioni, stessa metodologia, strumenti migliori. La risonanza meccanica dei piezoelettrici piatti è completamente diversa da quella dei buzzer elettromagnetici cilindrici. La mappa delle zone attive probabilmente cambierà.

Ma avremo già un metodo per leggerla.

---

*LOG-PUCK · PCK7 · hardware measurement series*
*Puck (CDC) + Claude (QG) · 2026-03-05*

