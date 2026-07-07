# djdeckard.com — Go-Live Status & Handoff

**Last updated:** 2026-07-06 — ✅ **RESOLVED / LIVE.**
**Status:** djdeckard.com serves the Netlify site over HTTPS with a valid Let's
Encrypt cert. www → apex redirect works. No forward to adjsjourney.com. M365 email intact.

Verified 2026-07-06:
- A `@` → 75.2.60.5 (only apex A). `www` → apex, both 200 from Netlify.
- Cert: `issuer=Let's Encrypt, subject=CN=djdeckard.com`.
- HTTP-01 challenge path returns Netlify 404 (no GoDaddy interception).
- Apex title served: "DJ Deckard — Breakbeat, Funk & House DJ · San Francisco".
- If a browser still shows a forward to adjsjourney.com, it's a **cached 301**
  from the old GoDaddy forward — clear site data / use incognito. Server-side is clean.

---
_Historical (the block that got resolved) below._

**Status (2026-07-03):** ⏳ Blocked on SSL cert — root cause is a GoDaddy domain entanglement to undo when back.

---

## Goal
Point **djdeckard.com** (GoDaddy-registered) at the **Netlify** site
(`djdeckard-site.netlify.app`, repo `github.com/kah1970/djdeckard-site`)
**while keeping Microsoft 365 email on the domain intact.**

Decision (locked): **Keep GoDaddy DNS** — do NOT switch nameservers to Netlify.
We only change the apex **A record**. Email lives in the other DNS records and
must not be touched.

---

## What's DONE ✅
- Site is live on Netlify: `https://djdeckard-site.netlify.app` (7 pages, working).
- GoDaddy **A record** `@` → **75.2.60.5** (Netlify's external-DNS IP), TTL 600s.
  Verified propagated at both `8.8.8.8` and `1.1.1.1`.
- GoDaddy **Website Builder** placeholder site was **unpublished** — that had been
  locking/reverting the A record. Lock is gone; A record now holds.
- **Email verified intact** — do not touch these:
  - MX → `djdeckard-com.mail.protection.outlook.com`
  - SPF TXT → `v=spf1 include:secureserver.net -all`
  - autodiscover CNAME → `autodiscover.outlook.com`
  - (plus M365 verification TXT, email/lyncdiscover/msoid/sip CNAMEs, SIP SRV records)
- **NS records** `ns01`/`ns02.domaincontrol.com` — GoDaddy's own nameservers.
  Correct, required, locked ("can't edit/delete"). **Leave alone.**
- Netlify DNS verification for djdeckard.com **passed** (green checkmark).
- Over **HTTP** (port 80) Netlify serves the real site (200) for `djdeckard.com`.

## What's BLOCKED ⛔
- **SSL cert not provisioned.** Netlify still serves its generic `*.netlify.app`
  cert for djdeckard.com, so HTTPS fails validation → browser shows a **blank
  white page**. The Let's Encrypt cert for `djdeckard.com` never issued.
- Diagnostic (re-run to confirm):
  ```
  echo | openssl s_client -connect 75.2.60.5:443 -servername djdeckard.com 2>/dev/null \
    | openssl x509 -noout -issuer
  # BLOCKED  = CN=DigiCert Global G2 ... (the *.netlify.app default)
  # FIXED    = issuer mentions Let's Encrypt / subject CN=djdeckard.com
  ```

---

## ⚠️ ROOT-CAUSE TO FIX FIRST (the GoDaddy mess)
Keith **accidentally "joined" the GoDaddy A DJ's Journey (adjsjourney) and
DJDeckard products/sites.** When GoDaddy prompted, it looked like "manage both
sites from one dashboard" but it actually set up a **domain forwarding**.
Keith **deleted the forward**, but the entanglement likely left djdeckard.com in
a state where GoDaddy is still asserting control (forwarding/parking) over the
domain, which is why Netlify can't complete Let's Encrypt provisioning.

**This is almost certainly why the cert won't issue** — Let's Encrypt does an
HTTP-01 challenge to `http://djdeckard.com/.well-known/...`, and if GoDaddy
forwarding/parking intercepts that request, the challenge fails.

### Fix steps when back (in order)
1. **GoDaddy → djdeckard.com → Forwarding:** confirm there is **NO domain
   forwarding** and **no domain-connection/parking** still active. Remove any
   residual forward or "connected site" tie between adjsjourney and djdeckard.
2. **GoDaddy → djdeckard.com → DNS:** confirm the **A `@` record = 75.2.60.5**
   is still the ONLY apex A record (no GoDaddy forwarding A records like
   `Parked`/`WebsiteBuilder`/`15.197.x`/`3.33.x` sneaking back). Delete any that reappear.
3. **Verify the HTTP-01 path is clean** (must return Netlify, not a GoDaddy redirect):
   ```
   curl -sI --resolve djdeckard.com:80:75.2.60.5 http://djdeckard.com/.well-known/acme-challenge/test
   # want: HTTP 404 from Netlify (server: Netlify).  BAD: 301/302 to a GoDaddy/park URL.
   ```
4. **Netlify → Domain management → HTTPS/SSL:** click **"Verify DNS
   configuration"**, then let Let's Encrypt auto-provision (or click
   **"Provision certificate"** — NOT "Provide your own certificate").
5. **Confirm live:** re-run the openssl diagnostic above → should show a
   `djdeckard.com` Let's Encrypt cert. Then `https://djdeckard.com` loads the
   real site with a padlock (hard-refresh ⌘⇧R to clear the blank-page cache).

### Do NOT
- Do NOT switch nameservers to Netlify (would break M365 email).
- Do NOT delete/edit the MX, SPF/TXT, email CNAMEs, SIP SRV, or the two NS records.
- Do NOT click "Provide your own certificate" in Netlify.

---

## Quick reference
- Netlify site: `djdeckard-site.netlify.app` · repo `github.com/kah1970/djdeckard-site`
- Netlify external-DNS apex IP: **75.2.60.5**
- Registrar/DNS: **GoDaddy** (keeping GoDaddy DNS) · Email: **Microsoft 365**
- Force-check past local DNS cache:
  ```
  curl -sk -o /dev/null -w "%{http_code}\n" --resolve djdeckard.com:443:75.2.60.5 https://djdeckard.com/
  ```
