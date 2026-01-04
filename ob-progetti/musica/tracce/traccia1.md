---
layout: ob_music
title: "Traccia Test"
slug: "traccia-test"
date: "2026-01-03"
section: "OB-Progetti"
subsection: "Musica"
genere: "Rock"
---
# Traccia Test

## Introduzione

Una traccia di test per il sistema.

## Metadati

| Proprietà       | Valore     |
|-----------------|------------|
| Genere          |   Rock     |
| Lunghezza Ritmo | 8 elementi |
| Numero Note     | 4          |
| Fasi Intensità  | 4          |
| Data Creazione  | 2026-01-03 |

## Dati Grezzi (Formato Verticale)

| Beat | Ritmo | Melodia | ChangeMelody | Intensità | ChangeIntensity |
|------|-------|---------|--------------|-----------|-----------------||
| 0 | 0.5 | 64 | ✓ | 0.3 | ✓ |
| 1 | 0.5 | 70 |  | 0.5 | ✓ |
| 2 | 2.0 | 70 | ✓ | 0.5 |  |
| 3 | 1.0 | 35 | ✓ | 0.8 | ✓ |
| 4 | 0.5 |  |  |  |  |
| 5 | 0.5 |  |  |  |  |
| 6 | 2.0 |  | ✓ |  | ✓ |
| 7 | 1.0 |  |  |  |  |

## Dati Grezzi (Formato JSON)

```json
{
  "traccia": "test",
  "ritmo": [
    0.5,
    0.5,
    2.0,
    1.0,
    0.5,
    0.5,
    2.0,
    1.0
  ],
  "melodia": [
    64,
    70,
    70,
    35
  ],
  "changeMelody": [
    0,
    2,
    3,
    6
  ],
  "intensita": [
    0.3,
    0.5,
    0.5,
    0.8
  ],
  "changeIntensity": [
    0,
    1,
    3,
    6
  ]
}
```
## Visualizzazione

![Grafico Traccia test](../assets/tracce/traccia-test-chart.svg)

## Studi e Sessioni

*Nessuno studio pubblicato ancora.*
