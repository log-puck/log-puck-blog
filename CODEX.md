# Codex — Repo Guardrails (log-puck-blog)

Obiettivo: mantenere build verde su GitHub Pages (Jekyll).

Quando ti chiedo "check repo":
1) Verifica file minimi: _config.yml, index.md, _layouts/default.html, Gemfile
2) Verifica baseurl/url e che i link usino {{ site.baseurl }}
3) Controlla che non ci siano plugin non supportati da GitHub Pages
4) Se trovi problemi, proponi patch in formato unified diff (git apply)
5) Output: (a) problemi trovati, (b) fix consigliato, (c) patch

Comandi locali attesi:
- bundle install
- bundle exec jekyll serve
  
## Styling rules
- No inline styles in HTML.
- Keep CSS in /assets/css/ (or SCSS in /assets/scss/ compiled to CSS).
- Prefer small, reviewable diffs.
