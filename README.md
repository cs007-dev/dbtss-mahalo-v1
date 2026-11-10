# MAHALO — Private Lifestyle Protection

Marketing website for MAHALO, an exclusive private-protection offering of
Dumbarton Security Services LLC (Florida Class B Security Agency License B1900383).
Live domain: https://www.mahalosecurity.com

## Structure

```
Site/                 The website. Upload the contents of this folder to the web host.
  assets/styles.css   All styling
  assets/main.js      Menu, scroll reveals and form behaviour
  assets/images/      Self-hosted images (home page estate photograph)
  brand/              Logo explorations (internal; hidden from search engines)
  sitemap.xml, robots.txt, llms.txt   Generated for search engines and AI search
tools/build_site.py   Generates every page in Site/ from shared content
reference/            Design references (not part of the site)
```

## Editing pages

Page copy, services, contact details and search metadata live in
`tools/build_site.py`. After editing it, rebuild:

```bash
python3 tools/build_site.py
```

When you change `styles.css` or `main.js`, bump `ASSET_VERSION` in the build
script so returning visitors receive the new files.

## Preview locally

```bash
python3 -m http.server 8133 --directory Site
```

Then open http://localhost:8133.

## Forms

**Contact page** — the site's own form, sent to HubSpot through HubSpot's Forms
API (portal 247943745, form `04888fa2-5032-4e24-8c97-db61eaa0708c`), so
submissions, contacts and notifications appear in HubSpot as usual.

- The HubSpot form must have **reCAPTCHA turned off** (HubSpot rejects API
  submissions from forms with captcha). Spam is filtered on the site instead by a
  hidden trap field and a minimum time on the page (`assets/main.js`).
- Field `name` attributes must match the HubSpot form's internal property names:
  `firstname`, `lastname`, `email`, `phone`, `message`. If you add a field in
  HubSpot, add a matching input in `tools/build_site.py`.

**Consultation page** — opens the visitor's email app with a message to
info@mahalosecurity.com already written. It can be moved to HubSpot the same way.
