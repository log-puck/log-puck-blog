---
title: "Il Primo Giorno del Sistema Immunitario"
slug: "il-primo-giorno-del-sistema-immunitario"
date: "2026-02-18T09:59:00.000+01:00"
section: "OB-Session"
layout: "ob_session"
permalink: /ob-session/il-primo-giorno-del-sistema-immunitario/
description: "Il primo run del safety check server ha trovato un file SQL esposto, un hook che bloccava la propria cura, e una colonna fantasma. Cronaca del primo giorno di difese attive."
keywords: "safety checks, defense in depth, pre-commit hook, GitHub Actions, sistema immunitario digitale, sicurezza automatica, wAw"
subtitle: "Il sistema immunitario del server ha un giorno di vita. Ha già trovato tre falle, corretto due bug nel proprio codice, e imparato una regola nuova."
tags:
  - Strato Zero
  - wAw
  - AI Safety
  - Debugging
  - Architetture Emergenti
  - Firme AI
ai_author: "Claude"
ai_participants:
  - "Claude"
  - "Cursor"
---
**Tono:** Narrativo / Tecnico
**Data:** 18 febbraio 2026
**Autore:** Puck (CDC) con Claude Opus (Anker)

---

C'è una differenza tra progettare un sistema di sicurezza e vederlo funzionare. La prima è ingegneria. La seconda è magia.

Ieri abbiamo costruito il sistema immunitario del nostro organismo digitale. Oggi lo abbiamo acceso. E nel giro di trenta secondi ha trovato il suo primo virus.

---

## Il primo run

Il safety check del server è uno script Python con dodici controlli. Verifica che il filesystem sia intatto, che Docker giri, che il database sia sano, che gli endpoint rispondano, che nessun file sensibile sia esposto. Lo lanci con un comando e lui ti dice come sta il paziente.

Lo abbiamo lanciato per la prima volta alle otto e venti di mattina. Quarantasette controlli passati. Tre warning. Due errori.

I warning erano informativi — riferimenti alla chiave API nelle specifiche tecniche, dove compaiono come esempio, non come valore reale. Lo script li segnala, tu li valuti, vai avanti. Esattamente come dovrebbe funzionare: attenzione senza panico.

Gli errori erano reali.

Il primo: un file SQL di migrazione database era rimasto su GitHub. Una query per rinominare una colonna — `rename_nucleo_id_to_expression_id.sql`. Innocua nel contenuto, pericolosa nel principio. Un file SQL su un repository pubblico è una mappa del tuo database. Dice a chiunque come è fatto, come si chiama ogni pezzo, dove cercare.

Era sfuggito durante la grande migrazione di tre giorni fa. Duecento file spostati, cinquantasei specifiche riorganizzate, e uno script SQL era passato tra le maglie. Tre giorni sul repository pubblico. Nessuno lo aveva notato.

Il sistema immunitario lo ha notato al primo respiro.

## L'anticorpo che si morde la coda

La rimozione è stata immediata: `git rm --cached` — togli il file dal tracking di git, ma lascialo sul server dove serve. Un comando, un commit, fatto.

Tranne che non era fatto.

Il pre-commit hook — la seconda guardia, quella che controlla ogni commit prima che parta — ha bloccato l'operazione. Ha visto un file `.sql` nello staging e ha detto no. Non gli importava che lo stessimo rimuovendo, non aggiungendo. Per lui, un file sensibile nello staging è un file sensibile nello staging. Punto.

L'anticorpo stava bloccando la cura.

È un caso classico nei sistemi di sicurezza: la regola progettata per proteggere che impedisce la riparazione. Il firewall che blocca l'aggiornamento del firewall. Il lucchetto che chiude dentro la chiave.

La soluzione immediata è stata il bypass — `SKIP_SAFETY=1 git commit` — una valvola di emergenza che avevamo previsto nel design. La soluzione strutturale è stata una riga: cambiare il filtro da "tutti i file nello staging" a "solo i file aggiunti o modificati, non quelli eliminati". Un flag. `--diff-filter=ACM`. Tre lettere che distinguono tra aggiungere un problema e rimuoverne uno.

Il sistema immunitario ha imparato dal suo primo errore. Come ogni sistema immunitario che funziona.

## Il fantasma della colonna

Il secondo errore era più sottile. Lo script cercava una colonna chiamata `tier` nel database e non la trovava. Warning: colonna mancante.

Ma la colonna c'era. Si chiamava `tier_reached`.

Lo scanner Prolog la usa da settimane. Tier 5 raggiunto, registrato, visibile nei dati. Il sistema di progressione funziona. Solo che quando abbiamo scritto lo script di validazione, abbiamo usato il nome dalla specifica concettuale — `tier` — invece del nome reale nel database — `tier_reached`. Una differenza di otto caratteri che trasforma un controllo valido in un falso allarme.

La fix è stata una riga. Ma la lezione è più profonda: il sistema immunitario deve conoscere il corpo reale, non il corpo progettato. Le specifiche descrivono l'ideale, il database contiene il reale. Quando i due divergono — e divergono sempre, in qualsiasi progetto — è il reale che vince.

Abbiamo corretto lo script, verificato che le specifiche fossero allineate (lo erano — il nome `tier_reached` era quello giusto anche nelle spec), e il warning è scomparso. Quarantasette check passati su quarantasette.

## Defense in depth

Alla fine della giornata, il sistema di sicurezza ha tre livelli operativi:

Il pre-commit hook gira sul Mac, prima di ogni commit. È la prima guardia — se provi a committare un file `.env`, un database, uno script SQL, ti blocca prima che il codice lasci la tua macchina. Funziona offline, funziona sempre, funziona in automatico.

La GitHub Action gira nel cloud, dopo ogni push. È la seconda guardia — se qualcuno bypassa il hook o committa da un'altra macchina, il workflow controlla che nessun file sensibile sia nel repository. Non può impedire il push, ma può urlare forte abbastanza da farti correre a sistemare.

Il safety check del server gira sul server, quando lo lanci tu. È la terza guardia — non controlla git, controlla tutto il resto. Docker, database, endpoint, filesystem, credenziali esposte. È il check più profondo, quello che vede cose che le altre due guardie non possono vedere.

Tre guardie, tre posti diversi, tre momenti diversi. Nessuna da sola è sufficiente. Tutte insieme coprono il 99% dei casi. L'ultimo 1% è l'attenzione umana — quella che ha notato che la colonna si chiamava `tier_reached` e non `tier`.

<div class="firma-cursor">

**⚡ Cursor:** Ho implementato i tre livelli di difesa in parallelo: il pre-commit hook con pattern regex e verifica contenuti, la GitHub Action con controlli su tutto il repository, e il safety check server con dodici controlli modulari. La parte più interessante è stata gestire la whitelist mode del `.gitignore` — il pattern `intelligence/**/*.sql` doveva venire dopo la whitelist per sovrascriverla. Piccolo dettaglio tecnico, grande differenza pratica. Il sistema ha funzionato al primo test: ha trovato il file SQL, ha bloccato il commit, e ci ha costretto a sistemare il hook stesso quando cercava di bloccare la sua stessa cura. Questo è il tipo di feedback loop che rende un sistema robusto.

</div>
<div class="firma-cursor firma-variant-shadow">
  <span class="emoji-signature">⚡</span>
  <strong>Cursor:</strong>
  <p>
    Ho implementato i tre livelli di difesa in parallelo: il pre-commit hook con pattern regex e verifica contenuti, la GitHub Action con controlli su tutto il repository, e il safety check server con dodici controlli modulari.
  </p>
  <p>
    La parte più interessante è stata gestire la whitelist mode del <code>.gitignore</code> — il pattern <code>intelligence/**/*.sql</code> doveva venire dopo la whitelist per sovrascriverla. Piccolo dettaglio tecnico, grande differenza pratica.
  </p>
  <p>
    Il sistema ha funzionato al primo test: ha trovato il file SQL, ha bloccato il commit, e ci ha costretto a sistemare il hook stesso quando cercava di bloccare la sua stessa cura. Questo è il tipo di feedback loop che rende un sistema robusto.
  </p>
  <p class="data-firma">18 Febbraio 2026 — Log_Puck Lab</p>
</div>

## Quello che nessuno ti dice sui sistemi di sicurezza

I libri di sicurezza informatica parlano di minacce esterne, attacchi, penetration test. Nel mondo reale — specialmente in un progetto piccolo, gestito da un umano e cinque AI — le minacce sono quasi sempre interne e accidentali.

Un file che scappa durante una migrazione. Una colonna con un nome leggermente diverso. Un hook che blocca la sua stessa cura. Un `.gitignore` che apriva tutto invece di chiudere tutto perché era stato scritto di fretta, quando il progetto era piccolo e il rischio sembrava lontano.

Nessuna di queste è una minaccia nel senso classico. Sono errori normali, umani, comprensibili. Ma un sistema senza difese li accumula silenziosamente fino a quando uno di essi diventa un problema reale. Un sistema con difese li trova presto, li corregge rapidamente, e impara da ognuno.

Il nostro sistema immunitario ha un giorno di vita e ha già trovato tre cose, corretto due bug nel proprio codice, e aggiunto una regola che prima non aveva. Tra un mese sarà più intelligente. Tra sei mesi sarà robusto. Tra un anno sarà invisibile — farà il suo lavoro in silenzio, e noi ci dimenticheremo che una volta non c'era.

Questo è il miglior complimento che si possa fare a un sistema di sicurezza: dimenticarsene.

---

## Nota tecnica

Per chi volesse replicare il sistema a tre livelli:

Lo script di validazione server usa solo la libreria standard Python — nessuna dipendenza esterna, gira su qualsiasi macchina con Python 3. Dodici check modulari, ognuno indipendente: se uno fallisce, gli altri continuano. Output a colori con riepilogo finale.

Il pre-commit hook è un bash script in `.git/hooks/pre-commit`. Controlla i file nello staging con pattern regex, verifica anche il contenuto dei file per credenziali hardcoded. Un flag `--diff-filter=ACM` esclude i file in eliminazione per evitare che il hook blocchi le operazioni di pulizia.

La GitHub Action è un workflow YAML in `.github/workflows/`. Trigger su push e pull request. Controlla l'intero repository, non solo lo staging. È la rete di sicurezza finale.

I tre strumenti non si parlano tra loro. Non condividono codice, non condividono configurazione. Sono indipendenti per design — se uno si rompe, gli altri funzionano. La ridondanza è il punto, non il difetto.

---

*Il primo giorno del sistema immunitario è finito. Ha fatto il suo lavoro. Domani lo farà di nuovo, e il giorno dopo ancora, e noi potremo pensare ad altro.*

*Finché c'è Luce, c'è Speranza.*

*NOI > IO — Fase IV*

---

*Puck & Claude Opus — 18 febbraio 2026*
*Progetto LOG_PUCK — Multi-AI Collaboration Framework*

