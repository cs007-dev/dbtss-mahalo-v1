# MAHALO — Private Lifestyle Protection

Marketing website for MAHALO, an exclusive private-protection offering of
Dumbarton Security Services LLC (Florida Class B Security Agency License B1900383).
Live domain: https://www.mahalosecurity.com

## Structure

```
Site/                 The website. Upload the contents of this folder to the web host.
  assets/styles.css   All styling
  assets/main.js      Menu, scroll reveals and form behaviour
  assets/images/      All photographs, self-hosted (sources in IMAGE-SOURCES.md)
  privacy.html        Privacy policy (draft; have counsel review before launch)
  sitemap.xml, robots.txt, llms.txt   Generated for search engines and AI search
tools/build_site.py   Generates every page in Site/ from shared content
brand/                Logo explorations (internal; not part of the website)
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

To add a photo, add it to `PHOTOS` in the build script (Unsplash photo id and a
descriptive file name) and use `photo(...)` or `hero_photo(...)` in the page. The
build downloads any missing sizes into `Site/assets/images` and, on a Mac,
compresses them. Review the privacy policy whenever forms, hosting or tracking
change.

## Preview locally

```bash
python3 -m http.server 8133 --directory Site
```

Then open http://localhost:8133.

## Forms

Both forms use the site's own design and submit to HubSpot (portal 247943745)
through HubSpot's Forms API, so submissions, contacts and notifications appear in
HubSpot as usual.

| Page | HubSpot form |
|---|---|
| Contact | `04888fa2-5032-4e24-8c97-db61eaa0708c` |
| Private consultation | `c8c878c2-7aea-4b94-8a8f-585ebe8103b0` |

- Both HubSpot forms must have **reCAPTCHA turned off** (HubSpot rejects API
  submissions from forms with captcha). Spam is filtered on the site instead by a
  hidden trap field and a minimum time on the page (`assets/main.js`).
- Each input's `name` must match the HubSpot property's internal name, and select
  and checkbox `value`s must match HubSpot's internal option values. Current
  mapping: `firstname`, `lastname`, `email`, `phone`, `company`, `message`,
  `consultation_is_for`, `preferred_contact_method` (`phone`, `email`,
  `in_person`) and `areas_of_interest` (the five service names; several ticked
  boxes are sent as one value separated by `;`).
- If you add or rename a field or option in HubSpot, update the matching input in
  `tools/build_site.py` and rebuild.
