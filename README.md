# djdeckard.com

The DJ Deckard artist hub. Static HTML/CSS/JS, no frameworks, one file per page —
mirrors the adjsjourney.com pipeline (GitHub → Netlify → djdeckard.com).

**Design system:** "Golden Hour / Playa" (light/warm, never dark). All styles live in
`css/deckard.css` — pages carry **zero inline styles**. Fonts: Bebas Neue / DM Serif
Display / DM Sans. Build spec + plan: `docs/dj-deckard-site/` (in the deckard-ops docs).

## Brand rules baked in
- **Books Deckard** on this site; references **Lumen Soundworks** (the billing/production
  entity) — never a hard sell ("inquire for booking").
- Points to **A DJ's Journey** for the podcast.
- **No PIOS**, no "Keith Harris / founder" framing — this is the artist hub only.
- On-page copy is **Deckard register** — drafts here are placeholders for Keith to finalize.

## Structure
```
index.html        Home  ✅ built (template page)
bio.html          Bio / EPK            — todo
mixes.html        Mixes                — todo
gigs.html         Gigs                 — todo
gallery.html      Gallery + lightbox   — todo
booking.html      Booking / inquiry    — todo (Netlify Forms → team@djdeckard.com)
links.html        Linktree-style hub   — todo
css/deckard.css   Golden Hour system   ✅ built
js/deckard.js     Mobile nav (+lightbox/form later) ✅ built
assets/           img/ (hero, gallery, og, press, logos), video/, press-kit/
```

## Preview locally
Paths are relative, so you can just **double-click `index.html`** to preview. Or serve it:
```
cd djdeckard-site && python3 -m http.server 8000   # → http://localhost:8000
```
(Note: pages use relative paths — `css/deckard.css`, not `/css/deckard.css` — which works
both on `file://` and on Netlify since the site is flat at the repo root.)

## Assets still needed (go-live gate — build proceeds with placeholders meanwhile)
- `assets/img/hero/hero-poster.jpg` — hero photo (Image 1)
- `assets/img/gallery/*` — gallery shots
- `assets/img/logos/lumensoundworks.png` — light/transparent LSW mark for the footer
- `assets/img/og/deckard-og.jpg` — 1200×630 share image
- `assets/press-kit/` — EPK PDF + press photos
- `favicon.ico` / `favicon.svg` / `apple-touch-icon.png` — from the DECKARD. wordmark
- Final mix list (3 featured are placeholders), gallery photos, EPK copy

## Deploy (when ready)
New GitHub repo → Netlify (build command: none; publish dir: repo root) →
point **djdeckard.com** DNS at Netlify (registrar: **GoDaddy** — external DNS, ALIAS/CNAME + A).
Auto Let's Encrypt SSL, force HTTPS, apex↔www redirect.

## Status
**2026-06-14:** first checkpoint — `css/deckard.css` + Home + mobile nav.
**2026-06-15/16:** all 7 pages built; gallery wired to 9 optimized photos; EPK + favicons in.
**2026-06-18:** home gallery wired to 4 real photos (was placeholders); working OG image
generated at `assets/img/og/deckard-og.jpg` (1200×630, padded portrait — replace with a
branded wordmark version when ready). Remaining = Keith-owned copy/assets (see below) + deploy.

### Still open (Keith-owned, blocking nothing on the build)
- **Bio copy + press quotes** — `bio.html` has a Deckard-register *draft*; finalize the prose,
  and the Press block is a placeholder quote + `[Placeholder attribution]` — swap for real ones.
- **Mix list + artwork** — only 3 featured mixes (real SoundCloud links, good); each card shows
  `[PLACEHOLDER] mix art` (no image asset). Add full list + cover art. Same on Home.
- **OG image** — working placeholder shipped; optional upgrade to a branded/wordmark version.
- **LSW footer logo** — parked separately.
