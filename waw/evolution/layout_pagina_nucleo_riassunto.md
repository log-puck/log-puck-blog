# Layout Pagina Nucleo – Riassunto

## Scopo

Ogni pagina Nucleo visualizza la timeline degli esperimenti registrati per uno specifico nucleo AI (es. `claude_prolog_scanner_v1`). La pagina è generata automaticamente a partire da dati strutturati (JSON Notion, Supabase, ecc.).

Dati visualizzati
Per ogni esperimento (run) vengono mostrati:

- **ID:** identificativo univoco dell’esperimento
- **Tier:** livello/tier raggiunto dall’esperimento
- **Tempo (ms):** tempo di esecuzione in millisecondi

## Struttura

- Titolo: nome del nucleo (`Nucleo: <nucleo_id>`)
- Tabella con le colonne: ID, Tier, Tempo (ms)
- Ciclo sui dati: ogni riga rappresenta un esperimento
- Possibilità di aggiungere JS per interattività (opzionale)

## Template Markdown (esempio)

```
---
title: "Nucleo: {{ nucleo_id }}"
layout: default
section: "OB-Tools"
# Generato automaticamente da script Notion → Markdown
---

<div class="landing-page">
  <section class="landing-content">
    <h1 class="landing-title">{{ nucleo_id }}</h1>
    <p>Timeline ultimi esperimenti registrati</p>
    <table>
      <thead>
        <tr>
          <th>ID</th>
          <th>Tier</th>
          <th>Tempo (ms)</th>
        </tr>
      </thead>
      <tbody>
        {% for run in runs %}
        <tr>
          <td>{{ run.id }}</td>
          <td>{{ run.tier_reached }}</td>
          <td>{{ run.time_ms }}</td>
        </tr>
        {% endfor %}
      </tbody>
    </table>
  </section>
</div>
```

## Dati richiesti

- Un array di esperimenti (runs) per ogni nucleo, con almeno i campi: `id`, `tier_reached`, `time_ms`.

**Generazione**

- La pagina può essere generata tramite script (Python, bash, GitHub Action) che converte i dati JSON in Markdown usando il template.
