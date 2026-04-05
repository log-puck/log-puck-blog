---
title: "PCK-7 — Sonificazione"
slug: "index"
date: "2026-04-04"
section: "OB-Progetti"
subsection: "MusicaAI"
layout: "ob_musica"
permalink: /ob-progetti/musica/
description: "Progetto PCK-7: sonificazione di testo in suono fisico tramite piezo e Arduino. Partiture composte da direttori AI, eseguite via pipeline v2.0."
keywords: "PCK7, sonificazione, piezo, Arduino, AI Music, partiture, tre assi"
subtitle: "Testo → Partitura → Suono fisico"
tags:
  - PCK7
  - AI Music
  - Sonificazione
  - Hardware
  - Human-AI Collaboration
ai_author: "Team LOG_PUCK"
ai_participants:
  - "Claude Code"
  - "Anker-QG"
  - "Claude Incognito"
  - "Phi4"
show_footer: true
show_partiture: true
show_profili: true
---

## Il Progetto

PCK-7 trasforma testo in suono fisico. Un **direttore** (umano o AI) compone una **partitura**: sceglie frequenze, durate, zone acustiche per ogni frase del testo. La partitura viene poi eseguita via Arduino su un attuatore piezoelettrico, misurata con sensore INA219.

Il primo concerto si chiama **"Il Passaggio"** — 4 direttori diversi hanno interpretato lo stesso testo.

---

## Pipeline v2.0

La pipeline end-to-end:

1. **Testo** — il direttore riceve un testo
2. **Composizione** — il direttore sceglie strategia (G9) e assegna DOVE (zona frequenza) e COME (pattern) per ogni evento
3. **Esecuzione** — Arduino genera il segnale, piezo lo suona
4. **Misurazione** — INA219 cattura corrente e tensione reali
5. **Analisi** — il validatore tre assi calcola entropia, varianza spettrale, dinamica

---

## Esplora

- [**Mappa Acustica**]({{ site.baseurl }}/ob-progetti/musica/mappa/) — lo strumento in 9 zone, da 700 a 7000 Hz

---

## Numeri

**6** partiture nel database | **155** sessioni hardware | **8355** misurazioni INA219

---
