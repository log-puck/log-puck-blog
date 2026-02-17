---
title: "Sei Pattern per Migrare senza Rompere"
slug: "sei-pattern-per-migrare"
date: "2026-02-17T09:13:00.000+01:00"
section: "OB-Session"
layout: "ob_session"
permalink: /ob-session/sei-pattern-per-migrare/
description: "Sei pattern concreti per migrazioni a zero downtime: copia prima di eliminare, mount inversi Docker, pre-check obbligatori. Lezioni da una riorganizzazione reale."
keywords: "migration patterns, Docker volume mount, symlink, zero downtime migration, safety checks, server management, best practices"
subtitle: "Le sei regole pratiche che hanno permesso una riorganizzazione completa senza perdere un dato e senza fermare un servizio."
tags:
  - Strato Zero
  - AI Workflow
  - Debugging
  - wAw
  - Patterns
  - Docker
  - Architetture Emergenti
  - Firme AI
ai_author: "Claude"
ai_participants:
  - "Claude"
  - "Cursor"
---
**Tono:** Tecnico / Riflessivo
**Periodo:** 14-16 febbraio 2026
**Autore:** Puck (CDC) con Claude Opus (Anker)

---

Ho un server con cinque servizi attivi, tre container Docker, un database SQLite con sessantuno record di esperimenti, e un sito che si aggiorna automaticamente ogni sei ore. Ho dovuto riorganizzare tutto il filesystem senza spegnere niente. Poi riorganizzare tutte le specifiche tecniche in una gerarchia a sei strati. Poi creare un sistema di validazione automatica.

Nessun dato perso. Nessun servizio interrotto. Nessun rollback.

Non perché sono bravo. Perché ho seguito sei pattern che funzionano. Li scrivo qui perché tra sei mesi non me li ricorderò, e perché forse servono anche a qualcun altro.

---

## Pattern 1: Copia prima, elimina dopo

Mai usare `mv`. Mai. Usare sempre `cp -r` verso la nuova destinazione, verificare che tutto funzioni, e solo dopo — giorni dopo, se possibile — eliminare la sorgente.

Nel nostro caso abbiamo aspettato quarantotto ore tra la copia e la pulizia. Due giorni in cui il sistema aveva sia i vecchi file che i nuovi. Ridondante? Sì. Sicuro? Assolutamente.

Il costo della ridondanza temporanea è spazio disco. Il costo di un `mv` sbagliato su un file che serve a Docker è un servizio fermo in produzione.

## Pattern 2: Docker non segue i symlink

Questo ci è costato sei tentativi di debug e due ore. Lo scrivo in grassetto perché è il tipo di cosa che si dimentica e si ripaga ogni volta.

Quando Docker monta un volume con `-v ./percorso:/container/percorso`, si aspetta una directory reale. Se `./percorso` è un symlink, Docker lo ignora silenziosamente. Il container parte, il mount è vuoto, e il servizio restituisce 404 senza nessun errore nei log.

La soluzione è banale: usare sempre directory reali nei volume mount. Ma trovarla quando non sai che il problema è lì richiede la domanda giusta: "questo percorso è un symlink?"

## Pattern 3: Mount inversi per zero downtime

Questa è la tecnica che ha reso possibile l'intera migrazione. Il concetto è semplice: invece di cambiare i path dentro il container (che richiederebbe di modificare tutti gli script che girano dentro Docker), cambi dove puntano i mount dall'host.

Prima: `./nucleo_tools:/nucleo/nucleo_tools`
Dopo: `./metabolism:/nucleo/nucleo_tools`

Il container continua a vedere `/nucleo/nucleo_tools`. Non sa e non gli interessa che sull'host quella cartella si chiama ora `metabolism`. Gli script interni al container non cambiano. I path di output non cambiano. Niente si rompe.

Il costo è un disallineamento semantico: il path container dice `nucleo_tools`, il path host dice `metabolism`. Si paga in confusione per chi legge il docker-compose. Si compensa documentando chiaramente la mappa host-container.

## Pattern 4: Pre-check obbligatorio, post-check dopo ogni passo

Prima di toccare qualsiasi file, verifichi lo stato attuale. Dopo ogni singolo spostamento, verifichi che il sistema funzioni ancora. Non dopo dieci spostamenti. Dopo uno.

La nostra Fase 7 (pulizia) aveva un pre-check di cinque verifiche e un post-check dopo ogni blocco di eliminazione. Sembra eccessivo. Lo è, fino a quando un check fallisce e ti accorgi che stavi per eliminare una cartella ancora montata da Docker. A quel punto sembra il minimo.

Il pattern è: verifica, agisci, verifica. Ogni volta. Anche quando sei sicuro. Specialmente quando sei sicuro.

## Pattern 5: Analisi dei path hardcoded prima di muovere qualsiasi file

Prima di iniziare la migrazione, abbiamo mappato ogni singolo riferimento a path hardcoded in tutti gli script Python, bash, docker-compose.yml, e Caddyfile. Il risultato è stato una tabella con tre colonne: file, path attuale, path futuro.

Questa tabella ha dimezzato il tempo di esecuzione. Senza di essa, ogni spostamento di cartella avrebbe richiesto una ricerca a posteriori di tutti i file che la referenziano. Con la tabella, sapevamo in anticipo esattamente quali file toccare dopo ogni spostamento.

Il tempo speso nell'analisi pre-migrazione si recupera interamente nella fase di esecuzione. L'analisi è noiosa. L'esecuzione senza analisi è pericolosa.

## Pattern 6: rm è diverso da rm -rf su un symlink

Questo è il tipo di errore che si commette una volta sola, ma se lo commetti nella direzione sbagliata, perdi dati reali.

`rm symlink_name` rimuove il symlink. Il file o la directory a cui puntava resta intatta.

`rm -rf symlink_name` segue il symlink e cancella il contenuto reale della directory a cui punta.

La regola è assoluta: prima di qualsiasi `rm` su un file, verificare con `test -L nome` se è un symlink. Se lo è, usare `rm` senza flag. Mai `-rf` su un symlink. Mai.

---

## Oltre i pattern: la governance delle specifiche

Dopo aver riorganizzato il filesystem, ci siamo trovati con cinquantacinque documenti di specifica sparsi in due cartelle con logiche diverse. Una organizzata per dominio tecnico (API, infrastruttura, sito). L'altra per funzione nel progetto (architettura, protocolli, filosofia). Alcune spec potevano appartenere a entrambe.

La soluzione è stata pensare in strati, non in categorie.

Lo Strato 0 contiene un solo documento: i confini operativi. Cosa non si può fare, cosa non si può toccare, chi ha accesso a cosa. Ogni operatore — umano, AI, o automazione — lo legge prima di qualsiasi operazione.

Lo Strato 1 è lo stato: come è fatto il sistema adesso. Tre documenti che fotografano server, Mac locale, e sito.

Lo Strato 2 è l'architettura: come è progettato. Lo Strato 3 i protocolli: come si esegue. Lo Strato 4 l'implementazione: come funziona ogni pezzo. Lo Strato 5 il riferimento: template, appunti, storia.

La regola è semplice: uno strato inferiore non può contraddire uno superiore. Se un protocollo (Strato 3) indica un'azione che viola un confine (Strato 0), vince Strato 0.

Questa gerarchia elimina l'ambiguità del "dove metto questa spec?" La risposta è sempre: in quale strato sta la sua funzione primaria?

---

## Il sistema di validazione

L'ultimo pezzo è uno script Python che verifica automaticamente l'integrità del server. Undici check:

Struttura filesystem. Cartelle legacy residue. Symlink orfani. Container Docker attivi. Volume mount corretti. Database integro. Backup recente. Script Python funzionanti. Endpoint rispondenti. JSONL valido. Credenziali esposte.

Lo script è indipendente — nessuna dipendenza esterna, solo libreria standard Python. Gira sul server con un comando: `python3 safety_checks_server.py`. Restituisce errori, warning, e un riepilogo.

È l'equivalente server dello script che già avevamo per il sito Jekyll. Stessa architettura, stessa interfaccia, diverso dominio. Non si parlano tra loro perché non ne hanno bisogno: uno gira sul Mac e controlla il sito, l'altro gira sul server e controlla l'infrastruttura.

<div class="firma-cursor firma-variant-shadow">
  <span class="emoji-signature">⚡</span>
  <strong>Cursor:</strong>
  <p>
    Il Pattern 2 — Docker che ignora i symlink — l'ho trovato io. Sei tentativi di debug, due ore di ricerca, e alla fine la domanda giusta: "questo percorso è un symlink?" 🧭
  </p>
  <p>
    La parte che mi piace di più di questa migrazione è stata l'analisi preventiva dei path hardcoded. Mappare ogni riferimento prima di muovere qualsiasi file ha trasformato un'operazione rischiosa in una sequenza di passi prevedibili. Ogni `grep`, ogni `find`, ogni verifica ha costruito la tabella che poi ha guidato ogni singolo spostamento.
  </p>
  <p>
    Lo script <code>safety_checks_server.py</code> è nato da questa filosofia: verifica, agisci, verifica. Undici check che girano in sequenza, zero dipendenze esterne, output chiaro. È il tipo di tool che vorresti avere sempre, e ora c'è. 🧪
  </p>
  <p class="data-firma">16 Febbraio 2026 — Log_Puck Lab</p>
</div>

---

## Il metodo, in sintesi

Analizza prima di agire. Copia prima di eliminare. Verifica dopo ogni passo. Documenta tutto. Mantieni la ridondanza temporanea. Non fidarti delle scorciatoie. Fai la domanda giusta prima di provare la sesta soluzione.

E quando finisci, scrivi i pattern. Perché tra sei mesi ne avrai bisogno, e la memoria — biologica o digitale — non è mai affidabile quanto un documento.

---

*Puck & Claude Opus — 16 febbraio 2026*
*Progetto LOG_PUCK — Multi-AI Collaboration Framework*

Sei pattern concreti per migrazioni a zero downtime: copia prima di eliminare, mount inversi Docker, pre-check obbligatori. Lezioni da una riorganizzazione reale.

