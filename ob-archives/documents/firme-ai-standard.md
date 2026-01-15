---
title: "Firme AI - Standard"
slug: "firme-ai-standard"
date: "2026-01-15"
section: "OB-Archives"
subsection: "Documents"
layout: "ob_document"
permalink: /ob-archives/documents/firme-ai-standard/
description: "Standard ufficiale per definire e mantenere le firme AI."
ai_author: "Claude"
version: "1"
---

# FIRME AI — STANDARD

Questo documento definisce **lo standard fisso** delle firme AI.  
Include anche la **spec operativa** per l’inserimento nei contenuti.

---

## 1) Struttura HTML (fissa)

```html
<div class="firma-claude">
  <strong>Claude:</strong> Testo della firma.
</div>
```

**Regole fisse:**
- La classe è **sempre** `firma-<ai>` in lowercase (es: `firma-claude`, `firma-cursor`).
- La classe base `firma-base` è **solo SCSS** (non va usata in HTML).
- Dentro il box, il nome è in `<strong>` seguito dal testo.
- Non usare inline style.

---

## 2) Struttura SCSS (fissa)

Le firme sono definite in `_sass/_firme.scss` e importate da `assets/css/main.scss`.

**Regole fisse:**
- Ogni AI ha una classe dedicata: `.firma-claude`, `.firma-gemini`, ecc.
- Ogni classe **estende** `.firma-base`.
- I colori base (background + border + text) sono **standardizzati**.

---

## 2.1) Base comune `.firma-base` (standard fisso)

**Bordo:** `border-left: 4px solid`  
**Raggio:** `border-radius: 6px`  
**Padding:** `1.5rem`  
**Margin:** `1.5rem 0`  
**Font size:** `0.95rem`  
**Line height:** `1.6`  
**Position:** `relative`  
**Strong:** `font-weight: bold; color: inherit;`  
**Ultimo paragrafo:** `p:last-child { margin-bottom: 0; }`

---

## 2.2) Classi accessorie (standard fisso)

- `.emoji-signature` → badge emoji (posizionamento assoluto nel box)
- `.data-firma` → data della firma (testo piccolo, allineato a destra)
- `.immagini-firma` → banner image (solo immagini orizzontali)

---

## 2.3) Banner guidelines (uso `.immagini-firma`)

Queste linee guida servono a inserire **banner immagine** al posto della firma testuale.

**Regole fisse:**
- La classe deve essere `immagini-firma`.
- Usare solo immagini **orizzontali** (formato banner).
- Nessun inline style.
- Il banner sta **dentro** il box firma.

**HTML standard:**
```html
<div class="firma-claude">
  <strong>Claude:</strong>
  <img
    src="/assets/images/claude-banner.png"
    alt="Firma Claude"
    class="immagini-firma"
  >
</div>
```

**Note operative:**
- `alt` descrittivo e coerente con l'AI.
- Dimensioni consigliate: larghezza 1200–1600px, altezza 240–420px.
- Sfondo trasparente o tinta uniforme; evitare testi lunghi sul banner.

---

## 3) Parametri standard da definire per ogni AI

Per ogni nuova AI, definire:
- **Colore di sfondo** (background)
- **Colore bordo** (border-color)
- **Colore testo** (color)
- **Eventuali note di stile** (es. italic, font-weight)

---

## 3.1) Specifica Gemini (approvata)

**Classe:** `.firma-gemini`  
**Background:** `rgba(153, 255, 0, 0.15)` (effetto evidenziatore)  
**Border:** `var(--accent-yellow-dark)`  
**Text:** `var(--text-main)`  
**Strong:** `var(--accent-yellow-dark)`  
**Variante consigliata:** `firma-variant-shadow`

---

## 3.2) Specifica Cursor (approvata)

**Classe:** `.firma-cursor`  
**Background:** `rgba(239, 68, 68, 0.12)` (wash rosso elettrico)  
**Border:** `#EF4444`  
**Text:** `#111827`  
**Strong:** `#EF4444`  
**Variante consigliata:** `firma-variant-shadow`

**Emoji consigliate (non hardcode):**
- `⚡` (velocita / focus)
- `🧭` (direzione / precisione)
- `🧪` (verifica / validazione)

---

## 4) Varianti consentite (limitate)

Sono permesse **solo** varianti definite a livello SCSS.

Esempio (già disponibile):
```html
<div class="firma-claude firma-variant-shadow">
  <strong>Claude:</strong> Nota con ombra leggera.
</div>
```

Se serve una nuova variante, va aggiunta in `_sass/_firme.scss`.

---

## 4.1) Ambito di utilizzo (fase attuale)

- **Consentito:** articoli (`ob-session`)
- **Non standardizzato:** documents (`ob-archives/documents`, `ob-ai`, `ob-progetti`, ecc.)
  - Per i documents servirà una selezione per documento e un passaggio Notion dedicato.

---

## 5) Naming convention

- File SCSS: `_sass/_firme.scss`
- Classi: `firma-<ai>` in lowercase
- Variante: `firma-variant-<nome>`

---

## 6) Spec operativa (uso)

Questa sezione serve come promemoria operativo quando un’AI deve inserire una firma.

**Cosa è fisso:**
- Classe principale: `firma-<ai>` (es: `firma-cursor`)
- Struttura HTML standard con `<strong>Nome:</strong>` e testo a seguire
- Nessun inline style

**Cosa è variabile (concesso):**
- Emoji nel testo
- Emoji come badge (`.emoji-signature` + eventuale modificatore)
- Testo libero della firma
- Data come testo (`.data-firma`)
- Immagine banner (`.immagini-firma`)
- **Una variante visiva** se già definita in SCSS (es: `firma-variant-shadow`)

**Cosa NON fare:**
- Non inventare nuove classi
- Non usare inline style
- Non usare immagini non‑banner (solo orizzontali)
- Non creare nuove varianti SCSS senza approvazione

**Metodo operativo (raccolta firme):**
1. Se l’articolo è online: fornire il link.  
2. Se non è online: fornire il file.  
3. L’AI risponde con:
   - **frase prima / frase dopo** (punto d’ingresso)
   - **testo firma**
   - **posizione emoji** (nel testo o badge)
   - eventuale **data** e/o **banner**

---

## 7) Checklist rapida (per chi implementa)

- [ ] Ho usato la classe `firma-<ai>` corretta?
- [ ] Ho rispettato il formato `<strong>Nome:</strong>`?
- [ ] Ho evitato inline style?
- [ ] Se ho usato una variante, esiste in `_firme.scss`?
