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
      {% assign nuclei = "nucleo_claude_01,nucleo_gemini_01,nucleo_deepseek_01" | split: "," %}
      
      {% for nucleus_id in nuclei %}
        {% assign nucleus_data = site.data.nucleus_overview[nucleus_id] %}
        
        <a href="{{ '/ob-ai/' | append: nucleus_id | append: '/' | relative_url }}" class="article-card nucleus-card">
          {% if nucleus_data %}
            <h3>{{ nucleus_data.display_name }}</h3>
            <p class="text-muted" style="margin: 0.5rem 0;">{{ nucleus_data.model }}</p>
            
            <div class="nucleus-stats">
              <div class="stat-item">
                <span class="stat-label">Experiments</span>
                <span class="stat-value">{{ nucleus_data.stats.total_experiments | default: 0 }}</span>
              </div>
              
              <div class="stat-item">
                <span class="stat-label">Expressions</span>
                <span class="stat-value">{{ nucleus_data.expressions | size }}</span>
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
          {% else %}
            <!-- Fallback se JSON non esiste ancora -->
            <h3>{{ nucleus_id | replace: "nucleo_", "" | replace: "_01", "" | capitalize }}</h3>
            <p class="text-muted" style="margin: 0.5rem 0;">In attesa dati...</p>
            
            <div class="nucleus-stats">
              <div class="stat-item">
                <span class="stat-label">Status</span>
                <span class="stat-value" style="color: #999;">Pending</span>
              </div>
            </div>
          {% endif %}
          
          <p class="card-action">→ Nucleus profile</p>
        </a>
      {% endfor %}
    </div>
  </section>
</div>