title: "Nucleo: claude_prolog_scanner_v1"
layout: default
section: "OB-Tools"
# http://127.0.0.1:4000//log-puck-blog/ob-tools/nucleo/claude_prolog_scanner_v1/
---

<div class="landing-page">
	<section class="landing-content">
		<h1 class="landing-title">claude_prolog_scanner_v1</h1>
		<p>Timeline ultimi esperimenti registrati</p>

		<table>
			<thead>
				<tr>
					<th>ID</th>
					<th>Tier</th>
					<th>Tempo (ms)</th>
				</tr>
			</thead>
			<tbody id="nucleo-runs-table">
				<!-- riempito via JS -->
			</tbody>
		</table>
	</section>
</div>

<script>
	async function loadNucleoRuns() {
		try {
			const res = await fetch('{{ "/assets/data/stats.json" | relative_url }}');
			const data = await res.json();

			const nucleoId = 'claude_prolog_scanner_v1';
			const runs = (data.recent && data.recent[nucleoId]) || [];

			const tbody = document.getElementById('nucleo-runs-table');
			tbody.innerHTML = runs.map(run => `
				<tr>
					<td>${run.id}</td>
					<td>${run.tier_reached}</td>
					<td>${run.time_ms}</td>
				</tr>
			`).join('');
		} catch (e) {
			console.error('Errore caricando stats.json per nucleo', e);
		}
	}

	document.addEventListener('DOMContentLoaded', loadNucleoRuns);
</script>
