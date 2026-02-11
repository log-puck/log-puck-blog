---
title: "Nucleo Evolution Dashboard"
slug: "nucleo-evolution"
date: 2026-02-06
section: "wAw"
subsection: "Evolution"
layout: "default"
permalink: /waw/evolution/
description: "Dashboard esperimenti AI multi-linguaggio del progetto Nucleo Evolution"
---

<div class="landing-page">
  <!-- Hero Section - Summary Minimale -->
  <section class="hero">
    <h1 class="hero-title">Nucleo Evolution</h1>
    <p class="hero-description">
      <strong>{{ site.data.evolution_dashboard.summary.total_experiments }}</strong> esperimenti
      • <strong>{{ site.data.evolution_dashboard.summary.unique_nuclei }}</strong> nuclei attivi
      • <strong>{{ site.data.evolution_dashboard.summary.languages | size }}</strong> linguaggi
    </p>
    <p class="text-muted" style="margin-top: 0.5rem; font-size: 0.9rem;">
      Ultimo aggiornamento: {{ site.data.evolution_dashboard.generated | date: "%d %B %Y, %H:%M" }}
    </p>
  </section>

  <!-- Performance per Linguaggio -->
  <section class="landing-content">
    <h2>Performance per Linguaggio</h2>
    <div class="articles-grid">
      {% for lang_pair in site.data.evolution_dashboard.by_language %}
        {% assign lang_name = lang_pair[0] %}
        {% assign lang_data = lang_pair[1] %}
        
        <a href="{{ '/waw/evolution/language/' | append: lang_name | downcase | replace: ' ', '_' | append: '/' | relative_url }}" class="article-card language-card">
          <h3>{{ lang_name }}</h3>
          
          <div class="nucleo-stats">
            <div class="stat-item">
              <span class="stat-label">Esperimenti</span>
              <span class="stat-value">{{ lang_data.experiments }}</span>
            </div>
            
            <div class="stat-item">
              <span class="stat-label">Tempo medio</span>
              <span class="stat-value">{{ lang_data.avg_time_ms | round: 1 }} <span class="unit">ms</span></span>
            </div>
            
            <div class="stat-item">
              <span class="stat-label">Output medio</span>
              <span class="stat-value">{{ lang_data.avg_output_bytes | round: 0 }} <span class="unit">bytes</span></span>
            </div>
            
            <div class="stat-item">
              <span class="stat-label">Max tier</span>
              <span class="stat-value tier-badge tier-{{ lang_data.max_tier }}">{{ lang_data.max_tier }}</span>
            </div>
          </div>
          
          <p class="card-action">→ Dettaglio linguaggio</p>
        </a>
      {% endfor %}
    </div>
  </section>

  <!-- Nuclei Attivi -->
  <section class="landing-content">
    <h2>Nuclei Attivi</h2>
    <div class="articles-grid">
      {% for nucleo in site.data.evolution_dashboard.by_nucleo %}
        <a href="{{ '/waw/evolution/expressions/' | append: nucleo.nucleo_id | append: '/' | relative_url }}" class="article-card nucleo-card">
          <h3>{{ nucleo.nucleo_id }}</h3>
          <p class="text-muted" style="margin: 0.5rem 0;">{{ nucleo.language }}</p>
          
          <div class="nucleo-stats">
            <div class="stat-item">
              <span class="stat-label">Run totali</span>
              <span class="stat-value">{{ nucleo.total_runs }}</span>
            </div>
            
            <div class="stat-item">
              <span class="stat-label">Tempo medio</span>
              <span class="stat-value">{{ nucleo.avg_time_ms | round: 1 }} <span class="unit">ms</span></span>
            </div>
            
            <div class="stat-item">
              <span class="stat-label">Best tier</span>
              <span class="stat-value tier-badge tier-{{ nucleo.best_tier }}">{{ nucleo.best_tier }}</span>
            </div>
          </div>
          
          <div class="nucleo-last-run">
            <p class="last-run-label">Ultimo run:</p>
            <p class="last-run-data">
              <span class="last-run-id">{{ nucleo.last_run.id }}</span><br>
              <span class="last-run-meta">
                {{ nucleo.last_run.timestamp | date: "%d/%m %H:%M" }}
                • Tier {{ nucleo.last_run.tier_reached }}
                • {{ nucleo.last_run.time_ms }} ms
              </span>
            </p>
          </div>
          
          <p class="card-action">→ Timeline completa</p>
        </a>
      {% endfor %}
    </div>
  </section>
</div>