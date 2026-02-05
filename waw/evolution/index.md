---
title: "Tools Nucleo Dashboard"
layout: "default"  # o default se oblanding non esiste
section: "ob-tools"
# http://127.0.0.1:4000/log-puck-blog/ob-tools/tools-nucleo/
# /ob-tools/nucleo/<nucleo_id>/
---

<div class="landing-page">
  <section class="hero">
    <h1 class="hero-title">Nucleo Tools</h1>
    <p class="hero-description">Esperimenti AI performance tracking</p>
  </section>

  <!-- Language summaries -->
  <section class="landing-content">
    <h2>Linguaggi</h2>
    <div id="language-grid" class="articles-grid"></div>
  </section>

  <!-- Tool cards -->
  <section class="landing-content">
    <h2>Esperimenti</h2>
    <div id="tools-grid" class="articles-grid"></div>
  </section>
</div>

<script>
  async function loadStats() {
    const res = await fetch('{{ "/assets/data/stats.json" | relative_url }}');
    const data = await res.json();

    // 1) Lingue
    const langGrid = document.getElementById('language-grid');
    langGrid.innerHTML = Object.entries(data.by_language).map(([name, v]) => `
      <article class="article-card card">
        <h3>${name}</h3>
        <p>${v.experiments} esperimenti</p>
        <p>${v.avg_time_ms.toFixed(1)} ms • ${v.avg_output_bytes.toFixed(1)} bytes</p>
        <p>Max tier: ${v.max_tier}</p>
      </article>
    `).join('');

    // 2) Esperimenti per nucleo_id
    const toolsGrid = document.getElementById('tools-grid');
    toolsGrid.innerHTML = Object.entries(data.recent).map(([nucleoId, runs]) => {
      const last = runs[0];
      const detailUrl = '{{ "/ob-tools/nucleo/" | relative_url }}' + nucleoId + '/';

      return `
        <a href="${detailUrl}" class="article-card card" style="display:block; text-decoration:none; color:inherit;">
          <h3>${nucleoId}</h3>
          <p>Ultimo ID: ${last.id}</p>
          <p>Tier: ${last.tier_reached} • ${last.time_ms} ms</p>
          <p style="margin-top:8px; font-weight:bold;">→ Apri dettaglio nucleo</p>
        </a>
      `;
    }).join('');
  }

  document.addEventListener('DOMContentLoaded', loadStats);
</script>


<script>
  loadRealData();
  // Metriche colorate
  function tierColor(tier) {
    return tier >= 5 ? 'var(--accent-yellow)' : tier >= 3 ? '#ffa500' : '#ff6b6b';
  }
  // Nelle cards:
  style="border-left: 4px solid ${tierColor(t.tierreached)}"
</script>
