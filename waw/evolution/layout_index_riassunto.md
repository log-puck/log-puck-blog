# Layout Index Nucleo – Riassunto

## Scopo

La pagina index raccoglie e visualizza in vetrina:
- Le statistiche aggregate per ogni linguaggio (card linguaggi)
- Gli ultimi esperimenti per ogni nucleo (card nuclei)

## Dati visualizzati

**Per ogni linguaggio:**
- Nome linguaggio
- Numero esperimenti
- Tempo medio (ms)
- Output medio (bytes)
- Max tier raggiunto

**Per ogni nucleo:**
- Nome nucleo
- Ultimo ID esperimento
- Tier e tempo dell’ultimo esperimento

## Struttura

- Titolo e descrizione
- Sezione “Linguaggi” con cards (una per linguaggio)
- Sezione “Esperimenti” con cards (una per nucleo)
- Ogni card nucleo linka alla pagina dettaglio nucleo

## Template Markdown (esempio)

```markdown
---
title: "Tools Nucleo Dashboard"
layout: default
section: ob-tools
languages:
  - name: Python
    experiments: 12
    avg_time_ms: 1100.5
    avg_output_bytes: 2048
    max_tier: 5
  # ...
nuclei:
  - nucleo_id: claude_prolog_scanner_v1
    url: /waw/evolution/claude_prolog_scanner_v1/
    last_id: 103
    last_tier: 5
    last_time_ms: 800
  # ...
---
```

## Dati richiesti

- Array `languages` con i dati aggregati per ogni linguaggio
- Array `nuclei` con i dati di sintesi per ogni nucleo

**Generazione**

- La pagina può essere generata tramite script che converte i dati JSON in Markdown usando il template.
