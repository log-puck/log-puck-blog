---
title: "Tools Nucleo Dashboard"
layout: default
section: ob-tools
# Generato automaticamente da script Notion/Supabase → Markdown
---

<div class="landing-page">
  <section class="hero">
    <h1 class="hero-title">Nucleo Tools</h1>
    <p class="hero-description">Esperimenti AI performance tracking</p>
  </section>

  <!-- Language summaries -->
  <section class="landing-content">
    <h2>Linguaggi</h2>
    <div class="articles-grid">
      {% for lang in languages %}
      <article class="article-card card">
        <h3>{{ lang.name }}</h3>
        <p>{{ lang.experiments }} esperimenti</p>
        <p>{{ lang.avg_time_ms | round: 1 }} ms • {{ lang.avg_output_bytes | round: 1 }} bytes</p>
        <p>Max tier: {{ lang.max_tier }}</p>
      </article>
      {% endfor %}
    </div>
  </section>

  <!-- Tool cards -->
  <section class="landing-content">
    <h2>Esperimenti</h2>
    <div class="articles-grid">
      {% for nucleo in nuclei %}
      <a href="{{ nucleo.url }}" class="article-card card" style="display:block; text-decoration:none; color:inherit;">
        <h3>{{ nucleo.nucleo_id }}</h3>
        <p>Ultimo ID: {{ nucleo.last_id }}</p>
        <p>Tier: {{ nucleo.last_tier }} • {{ nucleo.last_time_ms }} ms</p>
        <p style="margin-top:8px; font-weight:bold;">→ Apri dettaglio nucleo</p>
      </a>
      {% endfor %}
    </div>
  </section>
</div>
