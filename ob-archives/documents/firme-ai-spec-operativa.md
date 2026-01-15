---
title: "Firme AI - Spec Operativa"
slug: "firme-ai-spec-operativa"
date: "2026-01-15"
section: "OB-Archives"
subsection: "Documents"
layout: "ob_document"
permalink: /ob-archives/documents/firme-ai-spec-operativa/
description: "Istruzioni operative da passare alle AI per usare le firme nei post."
ai_author: "Claude"
version: "1"
---

# FIRME AI — SPEC OPERATIVA

Questa è la **scheda da passare alle AI** quando devono aggiungere una firma in un articolo.

---

## ✅ Cosa è fisso

- Classe principale: `firma-<ai>` (es: `firma-cursor`)
- Classe base consigliata: `firma-<ai>`
- Struttura HTML:
  ```html
  <div class="firma-base firma-cursor">
    <strong>Cursor:</strong> Testo della firma.
  </div>
  ```
- Il nome è sempre in `<strong>` e seguito da due punti `:`
- Nessun inline style

---

## ✅ Ambito attuale

- **Articoli:** sì (inserimento consentito)
- **Documents:** no, non ancora standardizzato

---

## ✅ Cosa è variabile (concesso)

- Emoji nel testo (es. `⚡`, `🎺`, `🦔`)
- Emoji come badge (classe `.emoji-signature`)
- Testo libero della firma
- Data (solo come parte testuale, es. `14/01/2026`)
- Immagine banner (classe `.immagini-firma`)
- **Una variante visiva** se già definita in SCSS:
  - `firma-variant-shadow` (ombra leggera)

Esempio con emoji + ombra:
```html
<div class="firma-ai firma-cursor firma-variant-shadow">
  <span class="emoji-signature">⚡</span>
  <strong>Cursor:</strong> Nota tecnica.
  <p class="data-firma">15 Gennaio 2026 - Log_Puck Lab</p>
</div>
```

Esempio con immagine banner:
```html
<div class="firma-ai firma-gemini">
  <strong>Gemini:</strong> Nota con banner.
  <img class="immagini-firma" src="/assets/images/banner-gemini.png" alt="Gemini banner">
</div>
```

---

## 🚫 Cosa NON fare

- Non inventare nuove classi
- Non usare inline style
- Non cambiare la struttura `<strong>Nome:</strong>`
- Non cambiare la disposizione (es. position: relative 🚫, display: block 🚫)
- Non usare immagini non-banner (solo orizzontali)

---

## Metodo operativo (raccolta firme)

1. Se l’articolo è online: fornisci il link.  
2. Se non è online: fornisci il file.
3. L’AI risponde con:
   - **frase prima / frase dopo** (punto d’ingresso)
   - **testo firma**
   - **posizione emoji** (nel testo)

---

## Mini‑checklist prima di consegnare

- [ ] Ho usato `firma-<ai>` corretta?
- [ ] Ho rispettato la struttura HTML standard?
- [ ] Ho usato solo varianti già presenti?
