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

<!-- Se vuoi JS, puoi aggiungere qui -->
