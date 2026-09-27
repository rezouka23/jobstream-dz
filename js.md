# PRD — JobStream DZ Landing Page: UI Fixes & Refactor

| Field | Value |
|---|---|
| Scope | `landing/index.html`, `landing/styles.css`, `landing/script.js`, `landing/assets/` |
| Status | Draft |
| Source | UI review of the landing page (code-based; visual verification pending) |

## 1. Overview

The landing page is a static, trilingual (FR/EN/AR, RTL-aware) site with a hero, a live job feed, three explainer sections (Proof, Method, FAQ) and a closing banner. It has accumulated two stacked CSS layers, duplicated sections and copy, several layout bugs, and developer-facing messaging aimed at a job-seeker audience.

This PRD defines the fixes and refactors needed to make the page correct, focused on one audience, visually coherent, and maintainable.

## 2. Goals

1. Fix functional/layout bugs (sticky headers, hero overlap, invalid markup, empty no-JS render).
2. Address a single primary audience — **job seekers** — with a clear CTA hierarchy.
3. Reduce visual repetition and improve scannability of sections below the hero.
4. Consolidate CSS into one coherent layer driven by design tokens.
5. Modularise JS and reduce page weight.

## 3. Non-goals

- Changing the backend feed API (`/api/feed/latest`) or its payload shape.
- Redesigning the `/cv-match/` app.
- Introducing a build framework (React, Tailwind, bundler) unless separately approved.
- Adding new languages.

## 4. Target audience

- **Primary:** job seekers in Algeria browsing fresh listings and trying CV matching.
- **Secondary:** developers interested in self-hosting — served via footer/GitHub links only, not in main-page copy.

## 5. Success metrics

| Metric | Target |
|---|---|
| Sticky section headers stick on desktop (≥861px) | 100% of sections |
| Hero text/phone overlap at 1180–1450px widths | None |
| HTML validation errors (W3C) | 0 |
| Meaningful content (H1, hero copy) present with JS disabled | Yes |
| `styles.css` line count | ≤ 1,600 (from 2,888) |
| Duplicate media-query blocks per breakpoint | 1 |
| Total image weight | −40% or more (from ~1.08 MB) |
| Lighthouse Accessibility / SEO | ≥ 95 / ≥ 95 |
| Distinct CTAs to `/cv-match/` visible above the fold | ≤ 2 |

## 6. Requirements

Priority: **P0** = must ship first, **P1** = required for release, **P2** = nice to have.

### 6.1 Workstream A — Bug fixes

**A1 (P0) — Restore sticky behaviour**
- Remove `overflow-x: hidden` from `html, body`, `overflow-y: auto` from `html`, and `overflow-y: hidden` from `body` (`styles.css` L21–34).
- Replace with `body { overflow-x: clip; }`.
- *Acceptance:* `.proof-head`, `.live-feed-head`, `.story-head`, `.faq-head` stick while their section scrolls at ≥861px; no horizontal scrollbar appears at any breakpoint.

**A2 (P0) — Eliminate hero copy/visual overlap**
- Replace the absolutely positioned `.hero-visuals` (`width: min(62%, 900px)`) and `.hero-copy` (`width: min(980px, 74%)`) with a two-column CSS grid on `.hero-panel` at ≥1181px; stack at ≤1180px.
- Decorative layers (map, flag, monument) remain absolutely positioned within their column.
- *Acceptance:* no text overlaps the phone mockup at 1181, 1280, 1366, 1440 and 1920px in FR, EN and AR.

**A3 (P0) — Valid list markup**
- Remove `<span class="{proof,story,faq}-progress">` from inside `<ol>`; render the progress rail via `::before` on the list, with the fill driven by a CSS custom property (e.g. `--progress`) set by GSAP.
- *Acceptance:* W3C validator reports 0 errors; scroll-driven progress still animates.

**A4 (P0) — Content renders without JS**
- Pre-populate every `data-i18n` / `data-i18n-html` node in `index.html` with the default FR string.
- `applyLanguage()` continues to overwrite on load/switch.
- *Acceptance:* with JS disabled, H1, hero subtitle, section titles, step text and FAQ are visible in French; no layout shift when JS applies FR.

### 6.2 Workstream B — Content & conversion

**B1 (P1) — Single-audience copy**
- Rewrite for job seekers (all three languages):
  - `feed.subtitle` — remove references to "sheet", "backend", "local preview".
  - `faq.subtitle` — remove "deploying your own instance".
  - `banner.subtitle` — remove "your instance".
  - `feed.fallbackNote` — user-friendly wording (e.g. "Showing recent sample listings").
- *Acceptance:* no user-facing string mentions sheet, backend, instance or deploy.

**B2 (P1) — De-duplicate claims across sections**
- "Every 3 minutes" and "no duplicates" each appear once as a primary claim on the page.
- Proof becomes a stat strip (see C1); Method keeps process steps; FAQ answers questions without restating Proof verbatim.
- *Acceptance:* each claim appears at most once as a heading.

**B3 (P1) — CTA hierarchy and labelling**
- Rename `nav.join` ("Recevoir les offres / Get job alerts / استقبل الوظائف") to a CV-match label, or point it to an actual alerts destination.
- Hero: keep **one primary** ("Explorer les offres" → `#live-feed`) and **one secondary** (CV match). Remove either `.btn-secondary` or `.hero-cv-teaser`.
- *Acceptance:* ≤2 CV-match CTAs above the fold; every CTA label matches its destination.

**B4 (P1) — Navigation labels**
- Remove the "Accueil/Home" link (logo covers it).
- Rename jargon: `nav.proof` → e.g. "Avantages/Benefits", `nav.feed` "Digest" → "Offres/Jobs".
- Final nav: *Offres · Matching CV · Méthode · FAQ*.
- *Acceptance:* nav has ≤5 items, all plain-language, in FR/EN/AR.

**B5 (P1) — Add a footer**
- New `<footer>` after `.bottom-banner` containing: logo, GitHub link, MIT licence, "Self-host JobStream" link (secondary audience), language switcher, contact.
- *Acceptance:* footer renders in all languages, RTL-mirrored for AR, links keyboard-accessible.

### 6.3 Workstream C — Layout & visual design

**C1 (P1) — Proof → stat strip**
- Replace the Proof pipeline with a compact 4-up stat row directly under the hero: *3 min* · *0 duplicates* · *4 sources* · *MIT*, each with a one-line caption.
- 4 columns ≥861px, 2×2 at ≤860px.
- *Acceptance:* section height ≤ 40% of the current Proof section at 1440px.

**C2 (P1) — FAQ → accordion**
- Replace numbered FAQ steps with `<details>/<summary>` items (no numbering, no progress rail).
- *Acceptance:* keyboard toggle works; first item open by default; RTL chevron mirrored.

**C3 (P1) — Hero polish**
- Restore accent colour on `.hero-kicker`.
- Decorative assets: either raise visibility intentionally (map ≥0.4 opacity) or remove flag/monument; set `alt=""` on all three.
- *Acceptance:* design sign-off on hero at desktop and mobile.

**C4 (P1) — Palette consistency**
- `.phone-preview-cta` uses the accent (green) or neutral treatment instead of the blue gradient.

**C5 (P2) — Simplify phone mockup**
- Replace the GSAP modal (`openPhoneModal`, `closePhoneModal`, `setupPhoneModal`, backdrop, tap hint, expand) with a static preview whose CTA scrolls to `#live-feed`.
- *Acceptance:* ~250 lines of JS and associated CSS removed; phone still shows up to 3 live/fallback jobs.

**C6 (P1) — Job card improvements**
- Show publish time once (drop either `.live-job-age` or the footer `publishedLabel`).
- Make the whole card clickable via a stretched link on the title; keep the apply button as the visible affordance.
- Show the results count visibly next to filters (currently `sr-only`).
- Add a search icon inside `.live-feed-search`; render active filters as removable chips; restyle "Clear filters" as a button.
- Mobile carousel: add a position indicator (dots or "1 / N"); remove `scroll-snap-stop: always`.
- *Acceptance:* one timestamp per card; card click opens apply URL in a new tab; count updates live with `aria-live`.

**C7 (P1) — Sticky header**
- Make `.topbar` `position: sticky; top: 0.5rem` with a condensed state (smaller logo, stronger background) after scrolling past the hero.
- Align sticky section-head offsets with the header height via a `--header-h` token.
- *Acceptance:* header never overlaps sticky section heads; mobile menu still opens correctly.

**C8 (P2) — Stronger closing banner**
- Increase `.bottom-banner` min-height (~240px desktop), larger headline, skyline opacity raised.

### 6.4 Workstream D — CSS refactor

**D1 (P0) — Collapse the two CSS layers**
- Merge the "Premium AIDA redesign layer" (L1481+) into base rules so each component is defined once.
- One media-query block per breakpoint (1380, 1180, 860, 620, 520), ordered mobile-last consistently.
- *Acceptance:* no selector defined in more than one non-media block; visual parity with current page (screenshot diff) before C-workstream changes.

**D2 (P0) — Remove dead code**
- Delete selectors with no matching markup: `.how-*`, `.features-*`, `.feature-card`, `.feature-tag`, `.icon-circle`, `.cities-*`, `.city-icon`, `.hero-trust*`, `.hero-mini-proof`, `.step-index`, `body::before/::after`, `@keyframes phone-tap-hint-pulse`, and their RTL overrides.
- Delete unused asset `assets/phone.png`.
- *Acceptance:* no CSS selector without a match in HTML or JS templates (verified via grep/coverage).

**D3 (P1) — Design tokens**
- Add tokens: `--accent-soft`, `--accent-line`, `--accent-text`, `--focus-ring`, `--radius-panel`, `--radius-card`, `--radius-pill`, `--header-h`.
- Replace hard-coded greens (`rgba(126,233,166,…)` ×23, `#7fe5ab`, `#83ebb0`, `#8ef0b8`, `#85eeb4`, `#49db7e`) and radii (24/28/30/42px).
- Single `:focus-visible { outline: var(--focus-ring); }` rule replacing per-component focus styles.
- *Acceptance:* no raw accent colour literals outside `:root`.

**D4 (P1) — Unified pipeline component**
- Replace `.story-*`, `.proof-*`, `.faq-*` class sets with `.pipeline`, `.pipeline-head`, `.pipeline-step`, `.pipeline-step-index`, `.pipeline-step-body` (used by Method; Proof/FAQ move to C1/C2).
- Update `initMotionSystem()` selectors accordingly.

**D5 (P1) — Logical properties for RTL**
- Replace `[dir="rtl"] … text-align: right` and left/right overrides with `text-align: start`, `inset-inline-*`, `margin-inline-*`, `border-inline-*`.
- *Acceptance:* AR layout visually unchanged; `[dir="rtl"]` rule count reduced by ≥50%.

### 6.5 Workstream E — JS refactor & performance

**E1 (P1) — Extract i18n strings**
- Move `STRINGS` (~490 lines) into `landing/i18n/{fr,en,ar}.js` (or JSON loaded before `script.js`).

**E2 (P2) — Split `script.js` into modules**
- `i18n.js`, `feed.js` (fetch, normalise, filter, render), `phone-preview.js`, `motion.js`, `nav.js`, loaded as native ES modules (`type="module"`).
- *Acceptance:* no behaviour change; no file >500 lines.

**E3 (P1) — Asset optimisation**
- `logo.png` (265 KB) → SVG or WebP at 2× display size.
- `map.png`, `flag.png`, `monument.png`, skylines → WebP/AVIF with `<picture>` fallback; add `width`/`height` attributes.
- `loading="lazy"` + `decoding="async"` on below-the-fold images (skylines).
- *Acceptance:* total image weight reduced ≥40%; no CLS from images.

**E4 (P1) — Font loading**
- Request only used weights (audit: likely Outfit 400/600/700/800, Tajawal 400/700).
- *Acceptance:* ≤6 font files requested.

**E5 (P2) — Cache busting**
- Replace manual `?v=20260602-cv-match-nav` with a content-hash or deploy-time version.

**E6 (P1) — Accessibility pass**
- `alt=""` on decorative images (map, flag, monument, skylines).
- Verify `aria-pressed` on language buttons and chips, `aria-current` on nav, `aria-expanded` on dropdown/menu.
- Colour contrast ≥4.5:1 for body text, ≥3:1 for UI components.

## 7. Phasing

| Phase | Items | Outcome |
|---|---|---|
| 1 — Stabilise | A1–A4, D1, D2 | Correct, valid, lean baseline with visual parity |
| 2 — Message | B1–B5 | Single-audience copy, clear CTAs, footer |
| 3 — Restructure | C1–C4, C6, C7, D3–D5 | New section layout on tokenised CSS |
| 4 — Optimise | C5, C8, E1–E6 | Smaller, modular, faster page |

Phase 1 must land before Phase 3 to avoid reworking duplicated CSS.

## 8. QA plan

- **Breakpoints:** 375, 414, 768, 1024, 1180, 1280, 1440, 1920px.
- **Languages:** FR, EN, AR (RTL) at each breakpoint.
- **States:** feed loading, live, fallback, empty, filtered-to-zero; mobile menu open; reduced motion.
- **Browsers:** latest Chrome, Firefox, Safari (desktop + iOS), Chrome Android.
- **Tooling:** W3C validator, Lighthouse, axe; screenshot diff for Phase 1 parity.
- **No-JS check:** disable JS, confirm FR content renders.
- **Existing tests:** run the repo's `tests/` suite to confirm no regressions in any landing-related checks.

## 9. Risks

| Risk | Mitigation |
|---|---|
| CSS merge (D1) causes silent visual regressions | Screenshot diff at all QA breakpoints before/after |
| Removing phone modal (C5) loses an engagement hook | Ship behind review; keep static preview with CTA |
| Pre-rendered FR strings (A4) drift from `STRINGS` | Single source: generate HTML defaults from `fr` dictionary or add a consistency check |
| RTL regressions from logical-property migration (D5) | AR screenshot diff per breakpoint |

## 10. Open questions

1. Should `nav.join` point to a real job-alerts channel (e.g. Telegram/email), or be relabelled as CV match?
2. Keep or drop the decorative flag/monument imagery?
3. Is the phone preview modal a tracked engagement feature that must be retained?
4. Is a build step (for hashing, image pipeline, module bundling) acceptable, or must the page remain zero-build?

