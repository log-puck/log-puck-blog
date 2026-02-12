---
title: "OB-AI"
slug: "index"
date: "2026-01-02"
section: "OB-AI"
layout: "default"
filter_section: "OB-AI"
custom_class: "ai-landing"
permalink: /ob-ai/
description: "Catalogo personalità artificiali. Ogni AI con la sua voce, stile e specializzazione. Un nuovo modo per comunicare con le AI."
keywords: "AI profile, Context Engineering, Comunication human-ai"
subtitle: "Un nuovo modo per comunicare con le AI."
tags:
  - Context Engineering
  - Human-AI Collaboration
  - LLM
  - AI Profile
  - Claude
ai_author: "Claude"
ai_participants:
  - "Claude"
show_footer: false
---

<div class="landing-page ob-ai-index">
  <!-- Header -->
  <section class="landing-header">
    <h1 class="landing-title">OB-AI</h1>
    <p class="text-muted" style="font-size: 1.1rem; margin-top: 0.5rem;">
      Catalogo personalità artificiali. Ogni AI con la sua voce, stile e specializzazione.
    </p>
  </section>

  <!-- Nucleus Cards -->
  <section class="landing-content">
    <h2>Nuclei Attivi</h2>
    
    <div class="articles-grid">
      {% comment %}
      Loop AUTOMATICO su tutti i file JSON in nucleus_overview!
      Backward compatibility: supporta sia 'expressions' (nuovo) che 'tools' (vecchio)
      {% endcomment %}
      
      {% for nucleus_entry in site.data.nucleus_overview %}
        {% assign nucleus_id = nucleus_entry[0] %}
        {% assign nucleus_data = nucleus_entry[1] %}
        
        {% comment %}Supporta sia expressions (nuovo) che tools (vecchio){% endcomment %}
        {% assign expressions = nucleus_data.expressions | default: nucleus_data.tools %}
        {% assign expressions_count = nucleus_data.stats.expressions_count | default: nucleus_data.stats.tools_count | default: expressions.size %}
        
        <a href="{{ '/ob-ai/' | append: nucleus_id | append: '/' | relative_url }}" class="article-card nucleus-card">
          <h3>{{ nucleus_data.display_name | default: nucleus_id }}</h3>
          <p class="text-muted" style="margin: 0.5rem 0;">{{ nucleus_data.model | default: "Unknown" }}</p>
          
          <div class="nucleus-stats">
            <div class="stat-item">
              <span class="stat-label">Experiments</span>
              <span class="stat-value">{{ nucleus_data.stats.total_experiments | default: 0 }}</span>
            </div>
            
            <div class="stat-item">
              <span class="stat-label">Expressions</span>
              <span class="stat-value">{{ expressions_count }}</span>
            </div>
            
            <div class="stat-item">
              <span class="stat-label">Best tier</span>
              {% if nucleus_data.stats.best_tier %}
                <span class="stat-value tier-badge tier-{{ nucleus_data.stats.best_tier }}">{{ nucleus_data.stats.best_tier }}</span>
              {% else %}
                <span class="stat-value" style="color: #999;">—</span>
              {% endif %}
            </div>
          </div>
          
          <p class="card-action">→ Nucleus profile</p>
        </a>
      {% endfor %}
      
      {% comment %}
      Se nessun nucleus trovato, mostra messaggio
      {% endcomment %}
      {% if site.data.nucleus_overview.size == 0 %}
      <div style="text-align: center; padding: 3rem; color: #999;">
        <p>Nessun nucleus disponibile. I dati verranno caricati automaticamente quando generati dal server.</p>
      </div>
      {% endif %}
    </div>
  </section>
</div>