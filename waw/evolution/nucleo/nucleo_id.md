---
layout: default
section: ob-tools
---

{% assign nucleo_data = site.data.nucleo_detail %}

<div class="landing-page">
  <section class="landing-content">
    <h1 class="landing-title">{{ nucleo_data.nucleo_id }}</h1>
    
    <div class="nucleo-info">
      <p><strong>Linguaggio:</strong> {{ nucleo_data.info.language }}</p>
      <p><strong>Runtime:</strong> {{ nucleo_data.info.runtime }}</p>
      <p><strong>Task:</strong> {{ nucleo_data.info.task }}</p>
    </div>

    <div class="nucleo-stats">
      <p>Run totali: <strong>{{ nucleo_data.stats.total_runs }}</strong></p>
      <p>Tempo medio: <strong>{{ nucleo_data.stats.avg_time_ms | round: 1 }}</strong> ms</p>
      <p>Best tier: <strong>{{ nucleo_data.stats.best_tier }}</strong></p>
    </div>

    <h2>Timeline Esperimenti</h2>
    <table class="nucleo-table">
      <thead>
        <tr>
          <th>ID</th>
          <th>Timestamp</th>
          <th>Tier</th>
          <th>Tempo (ms)</th>
          <th>Sensazione</th>
        </tr>
      </thead>
      <tbody>
        {% for run in nucleo_data.runs %}
        <tr>
          <td><code>{{ run.id }}</code></td>
          <td>{{ run.timestamp | date: "%d/%m/%Y %H:%M" }}</td>
          <td class="tier-{{ run.tier_reached }}">{{ run.tier_reached }}</td>
          <td>{{ run.time_ms }}</td>
          <td class="sensation-{{ run.sensation.mood }}">
            {{ run.sensation.mood }}
            {% if run.sensation.rsai %}
              <span class="tooltip">{{ run.sensation.rsai }}</span>
            {% endif %}
          </td>
        </tr>
        {% endfor %}
      </tbody>
    </table>
  </section>
</div>