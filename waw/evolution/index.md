---
title: "Nucleo Evolution Dashboard"
layout: default
section: ob-tools
---

<div class="landing-page">
  <section class="hero">
    <h1 class="hero-title">Nucleo Evolution</h1>
    <p class="hero-description">
      {{ site.data.nucleo_dashboard.summary.total_experiments }} esperimenti 
      • {{ site.data.nucleo_dashboard.summary.unique_nuclei }} nuclei attivi
    </p>
    <p class="text-muted">
      Ultimo aggiornamento: {{ site.data.nucleo_dashboard.generated | date: "%d %B %Y, %H:%M" }}
    </p>
  </section>

  <!-- Statistiche per Linguaggio -->
  <section class="landing-content">
    <h2>Performance per Linguaggio</h2>
    <div class="articles-grid">
      {% for lang_pair in site.data.nucleo_dashboard.by_language %}
        {% assign lang_name = lang_pair[0] %}
        {% assign lang_data = lang_pair[1] %}
        <article class="article-card card">
          <h3>{{ lang_name }}</h3>
          <div class="card-stats">
            <p><strong>{{ lang_data.experiments }}</strong> esperimenti</p>
            <p>Tempo medio: <strong>{{ lang_data.avg_time_ms | round: 1 }}</strong> ms</p>
            <p>Output medio: <strong>{{ lang_data.avg_output_bytes | round: 0 }}</strong> bytes</p>
            <p>Max tier: <strong>{{ lang_data.max_tier }}</strong></p>
          </div>
        </article>
      {% endfor %}
    </div>
  </section>

  <!-- Nuclei Attivi -->
  <section class="landing-content">
    <h2>Nuclei Attivi</h2>
    <div class="articles-grid">
      {% for nucleo in site.data.nucleo_dashboard.by_nucleo %}
        <a href="/evolution/nucleo/{{ nucleo.nucleo_id }}/" class="article-card card">
          <h3>{{ nucleo.nucleo_id }}</h3>
          <p class="text-muted">{{ nucleo.language }}</p>
          <div class="card-stats">
            <p><strong>{{ nucleo.total_runs }}</strong> run totali</p>
            <p>Ultimo: {{ nucleo.last_run.timestamp | date: "%d/%m %H:%M" }}</p>
            <p>Tier <strong>{{ nucleo.last_run.tier_reached }}</strong> • {{ nucleo.last_run.time_ms }} ms</p>
          </div>
          <p class="card-action">→ Dettaglio timeline</p>
        </a>
      {% endfor %}
    </div>
  </section>
</div>