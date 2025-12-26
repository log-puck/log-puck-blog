source "https://rubygems.org"

group :jekyll_plugins do
  gem "github-pages", "~> 231"
end

# Optional: allow local `jekyll build`
gem "jekyll", "~> 4.3"

# Plugins essenziali
group :jekyll_plugins do
  gem "jekyll-feed", "~> 0.12"
  gem "jekyll-seo-tag", "~> 2.8"
end

# FIX: Evita sass-embedded che esplode su Ruby 3.1.4
# Forza jekyll-sass-converter vecchio che usa sassc
gem "jekyll-sass-converter", "~> 2.2"

# Dipendenze esplicite per evitare conflitti
gem "webrick", "~> 1.8"
