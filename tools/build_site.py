#!/usr/bin/env python3
"""Build the MAHALO website.

Generates every page in Site/ from the shared header, footer and content below,
plus sitemap.xml, robots.txt and llms.txt. Edit content here, then run:

    python3 tools/build_site.py

Styles live in Site/assets/styles.css and behaviour in Site/assets/main.js.
"""
import datetime
import html
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "Site")

SITE = "https://www.mahalosecurity.com"
TODAY = datetime.date.today().isoformat()
ASSET_VERSION = "17"  # bump when styles.css or main.js change so browsers fetch the new files

PHONE_DISPLAY = "727-400-6259"
PHONE_TEL = "+17274006259"
EMAIL = "info@mahalosecurity.com"
WEBSITE_DISPLAY = "www.mahalosecurity.com"

# HubSpot forms that receive the site's submissions (sent by assets/main.js)
HUBSPOT_PORTAL = "247943745"
HUBSPOT_CONTACT_FORM = "04888fa2-5032-4e24-8c97-db61eaa0708c"
HUBSPOT_CONSULTATION_FORM = "c8c878c2-7aea-4b94-8a8f-585ebe8103b0"

OPERATOR = "Dumbarton Security Services LLC"
LICENSE = "Florida Class B Security Agency License B1900383"
LICENSE_NO = "B1900383"
TAGLINE = "Some choose a lifestyle. Others protect it."
HERO_IMAGE = "assets/images/mahalo-estate-sunset-v2.webp"
SHARE_IMAGE = "assets/images/mahalo-estate-sunset-share.jpg"  # 1200x630 JPG for link previews


# Photography: Unsplash photos (free for commercial use under the Unsplash
# License), downloaded once and served from Site/assets/images. Each entry is
# key: (Unsplash photo id, descriptive file name).
PHOTOS = {
    "villa_pool": ("1613490493576-7fde63acd811", "luxury-residence-pool"),
    "villa_dusk": ("1600585154340-be6161a56a0c", "private-residence-dusk"),
    "jet": ("1474302770737-173ee21bab63", "private-jet-runway-sunset"),
    "wing": ("1436491865332-7a61a109cc05", "private-jet-wing-above-clouds"),
    "resort_pool": ("1566073771259-6a8506099945", "luxury-resort-pool-palms"),
    "resort_twilight": ("1542314831-068cd1dbfeeb", "luxury-resort-pool-twilight"),
    "tropical_resort": ("1520250497591-112f2f40a3f4", "tropical-resort-pool"),
    "yacht": ("1567899378494-47b22a2ae96a", "superyacht-at-anchor"),
    "superyacht": ("1569263979104-865ab7cd8d13", "superyacht-cruising-coast"),
    "celebration": ("1519167758481-83f550bb49b3", "private-celebration-ballroom"),
    "dinner": ("1414235077428-338989a2e8c0", "private-dinner-table"),
    "coast": ("1505852679233-d9fd70aff56d", "pacific-coast-cliffs"),
    "aerial": ("1506929562872-bb421503ef21", "boats-turquoise-water-aerial"),
}
IMG = {key: key for key in PHOTOS}  # services and pages refer to photos by key
PHOTO_DIR = os.path.join(OUT, "assets", "images")
_photos_used = set()


def photo(key, w):
    """Local path of a photo at width w; the file is downloaded at the end of the build if missing."""
    _photos_used.add((key, w))
    return f"assets/images/{PHOTOS[key][1]}-{w}.jpg"


def hero_photo(key):
    """src/srcset for a full-width photo: phones load the 1200px file, large screens the 2400px."""
    small, large = photo(key, 1200), photo(key, 2400)
    return f'src="{large}" srcset="{small} 1200w, {large} 2400w" sizes="100vw"'


def compress_photo(path):
    """Recompress large photos with macOS sips; detail loss is invisible behind the site's photo overlays."""
    import shutil
    import subprocess
    if shutil.which("sips") and os.path.getsize(path) > 250_000:
        subprocess.run(["sips", "-s", "format", "jpeg", "-s", "formatOptions", "low", path, "--out", path],
                       check=True, capture_output=True)


def download_photos():
    import urllib.request
    fetched = 0
    for key, w in sorted(_photos_used):
        pid, name = PHOTOS[key]
        dest = os.path.join(PHOTO_DIR, f"{name}-{w}.jpg")
        if os.path.exists(dest):
            continue
        quality = 70 if w >= 2000 else 76
        url = f"https://images.unsplash.com/photo-{pid}?fm=jpg&w={w}&q={quality}"
        with urllib.request.urlopen(url, timeout=60) as res, open(dest, "wb") as f:
            f.write(res.read())
        compress_photo(dest)
        fetched += 1
    return fetched

# ---------------------------------------------------------------- services
SERVICES = [
    {
        "slug": "estate-protection.html",
        "key": "estate",
        "name": "The Private Estate",
        "label": "Residence",
        "short": "Private estate, residential and family protection.",
        "title": "Private Estate & Luxury Residential Protection",
        "description": "Discreet estate security, luxury residential protection and family protection from MAHALO, designed around your home, your household and the way you live.",
        "tile": IMG["villa_dusk"], "tile_alt": "A private residence glowing at dusk beneath a great oak",
        "hero": IMG["villa_pool"], "hero_alt": "A luxury residence with a pool, framed by palms",
        "lede": "Private estate, residential and family protection, so home remains the one place where you never have to think about security.",
        "h2": "Your sanctuary, <em>quietly kept.</em>",
        "paras": [
            "A great home is more than an address. It is where children grow up, where guests are welcomed and where private life is lived. MAHALO protects primary residences, seasonal homes and waterfront estates with a presence that feels like part of the household: attentive, courteous and unobtrusive.",
            "Every program begins with an understanding of how your home actually works: the rhythm of the day, the staff who keep it running, the arrivals and departures, and the moments when you want no one around at all. Protection is then designed to fit that life, rather than reshape it.",
        ],
        "included": [
            "Private estate and residential protection programs",
            "Family and child protection",
            "Estate assessments and privacy reviews",
            "Coordination with household staff and estate managers",
            "Gate, guest and vendor arrival protocols",
            "Seasonal openings, closings and oversight while you are away",
        ],
        "moments": [
            ("Arrivals", "Guests, deliveries and staff are welcomed graciously, and every arrival is expected."),
            ("Family time", "Children play, swim and explore while protection stays in the background."),
            ("Time away", "When the house is closed for the season, it is still looked after as if you were home."),
        ],
    },
    {
        "slug": "executive-protection.html",
        "key": "executive",
        "name": "The Executive Life",
        "label": "Personal",
        "short": "Executive protection and personal security.",
        "title": "Executive Protection & Personal Security",
        "description": "Executive protection and personal security for chief executives, principals and their families: discreet, polished and designed around a demanding schedule.",
        "tile": IMG["jet"], "tile_alt": "A private jet on the tarmac at sunset",
        "hero": IMG["jet"], "hero_alt": "A private jet waiting on the runway at sunset",
        "lede": "Executive protection and personal security, delivered with the discretion your position requires.",
        "h2": "For the leader, <em>wherever they lead.</em>",
        "paras": [
            "The demands on today's executives do not end at the office door. Board meetings, investor dinners, public appearances and family commitments each carry their own exposure. MAHALO provides close, considered protection that lets principals focus entirely on the people and decisions in front of them.",
            "Our professionals are selected for judgment and composure as much as capability. They move easily between the boardroom, the hotel lobby and the family table: present when needed, invisible when not.",
        ],
        "included": [
            "Executive and close personal protection",
            "Secure ground transportation coordination",
            "Advance planning for offices, venues and hotels",
            "Support for board meetings, shareholder events and roadshows",
            "Protection that extends to spouses and family",
            "Awareness of public profile and personal privacy",
        ],
        "moments": [
            ("The commute", "Routes, timings and arrivals are handled before you step outside."),
            ("The meeting", "Conversations stay in the room, and the room stays private."),
            ("The evening", "Dinner with clients or family, without a second thought about who is watching."),
        ],
    },
    {
        "slug": "luxury-hospitality-security.html",
        "key": "hospitality",
        "name": "The World of Hospitality",
        "label": "Hospitality",
        "short": "Luxury hotels, resorts, private clubs and residential communities.",
        "title": "Luxury Hotel, Resort & Private Club Protection",
        "description": "Hospitality-minded protection for luxury hotels, resorts, private clubs and residential communities, safeguarding distinguished guests, members and residents.",
        "tile": IMG["resort_pool"], "tile_alt": "A luxury resort pool surrounded by palms",
        "hero": IMG["resort_twilight"], "hero_alt": "A luxury resort and pool lit at twilight",
        "lede": "Luxury hotels, resorts, private clubs and residential communities, protected with the same grace your guests expect from everything else.",
        "h2": "Protection that speaks <em>the language of service.</em>",
        "paras": [
            "In the finest hospitality settings, security should never feel like security. It should feel like one more expression of care. MAHALO partners with luxury hotels, resorts, private clubs and residential communities to protect distinguished guests, members and residents in a manner consistent with the property's own standard of service.",
            "Our professionals are introduced to your culture, your guests and your expectations before they ever take their place. The result is a presence that is calm, courteous and fully aligned with your brand.",
        ],
        "included": [
            "Protection for distinguished guests, members and residents",
            "Discreet arrival, departure and suite protection",
            "Support for high-profile stays and private events",
            "Programs for private clubs and residential communities",
            "Coordination with management, concierge and guest services",
            "Hospitality-minded protection professionals",
        ],
        "moments": [
            ("The arrival", "Distinguished guests are welcomed quietly, with privacy assured from the first moment."),
            ("The stay", "Residents and members enjoy the property exactly as it was meant to be enjoyed."),
            ("The occasion", "Galas, weddings and member events unfold without interruption."),
        ],
    },
    {
        "slug": "yacht-aviation-travel-security.html",
        "key": "journey",
        "name": "The Private Journey",
        "label": "Travel",
        "short": "Yacht, maritime, private aviation and travel security coordination.",
        "title": "Yacht, Private Aviation & Travel Security",
        "description": "Yacht and maritime protection, private aviation and luxury travel security coordination, so every journey at sea or in the air feels effortless.",
        "tile": IMG["yacht"], "tile_alt": "A superyacht at anchor in turquoise water",
        "hero": IMG["superyacht"], "hero_alt": "A superyacht cruising along the coast",
        "lede": "Yacht, maritime, private aviation and travel security coordination, from wheels-up to the last evening at anchor.",
        "h2": "Open horizons, <em>unhurried journeys.</em>",
        "paras": [
            "Travel is where life opens up, and where it can feel most exposed. MAHALO coordinates protection across private aviation, yachts and luxury destinations, so that every leg of the journey feels as considered as the destination itself.",
            "We work alongside your flight department, captain and crew, hotels and local partners, quietly handling the details that make an itinerary effortless and leaving you free to enjoy the view.",
        ],
        "included": [
            "Travel security planning and itinerary coordination",
            "Private aviation and FBO arrival coordination",
            "Yacht and maritime protection, at anchor and in port",
            "Tender, shore excursion and marina escort",
            "Hotel, villa and destination advance planning",
            "Coordination with captains, crews and flight departments",
        ],
        "moments": [
            ("Wheels up", "Cars, terminals and arrivals are coordinated before you leave home."),
            ("At anchor", "Guests come aboard by tender while the evening is quietly looked after."),
            ("Ashore", "Dinners, excursions and shopping, enjoyed without hesitation."),
        ],
    },
    {
        "slug": "private-event-security.html",
        "key": "entertaining",
        "name": "The Art of Entertaining",
        "label": "Occasions",
        "short": "Private events, VIP protection and exclusive gatherings.",
        "title": "Private Event Security & VIP Protection",
        "description": "Discreet private event security and VIP protection for celebrations, galas, private dinners and exclusive gatherings, so hosts and guests simply enjoy.",
        "tile": IMG["celebration"], "tile_alt": "A candlelit table set for a private celebration",
        "hero": IMG["dinner"], "hero_alt": "A private dinner table set for guests",
        "lede": "Private events, VIP protection and exclusive gatherings, so the only thing your guests remember is the evening itself.",
        "h2": "Gatherings that stay <em>beautifully private.</em>",
        "paras": [
            "Whether an intimate dinner at home, a milestone celebration, a charity gala or a confidential gathering of business leaders, entertaining well depends on ease. MAHALO protects the host, the guests and the privacy of the occasion, while staying entirely in keeping with its atmosphere.",
            "We plan alongside your event team, venue and household from the earliest stages, so that guest arrivals, VIP movements and the flow of the evening are considered long before the first guest arrives.",
        ],
        "included": [
            "Private event and celebration protection",
            "VIP and distinguished guest protection",
            "Guest list and arrival coordination",
            "Venue and residence planning",
            "Event teams attired to suit the occasion",
            "Discretion around privacy and photography",
        ],
        "moments": [
            ("Before", "Venues, guest lists and arrivals are quietly prepared."),
            ("During", "Hosts welcome their guests with complete peace of mind."),
            ("After", "Every guest departs safely, and the evening stays private."),
        ],
    },
]
SERVICE_BY_SLUG = {s["slug"]: s for s in SERVICES}

FAQ = [
    ("What is private lifestyle protection?",
     "Private lifestyle protection is personal security designed around the way you live: your home, your family, your work, your travel and your occasions. Rather than simply placing guards at a door, MAHALO designs discreet, hospitality-minded protection that lets you live fully, with confidence."),
    ("Who does MAHALO serve?",
     "MAHALO serves affluent individuals and families, executives, estate owners and luxury hospitality clients, including hotels, resorts, private clubs and residential communities."),
    ("What services does MAHALO offer?",
     "MAHALO offers five lifestyle services: The Private Estate (private estate, residential and family protection), The Executive Life (executive protection and personal security), The World of Hospitality (luxury hotels, resorts, private clubs and residential communities), The Private Journey (yacht, maritime, private aviation and travel security coordination) and The Art of Entertaining (private events, VIP protection and exclusive gatherings)."),
    ("Is MAHALO licensed?",
     f"MAHALO is an exclusive private-protection offering of {OPERATOR}, which holds {LICENSE}."),
    ("How does an engagement begin?",
     f"Every engagement begins with a private, confidential conversation. Call {PHONE_DISPLAY} or email {EMAIL}, or request a consultation through this website."),
]

NAV = [("index.html", "Home"), ("about.html", "About Us"), ("services.html", "Services")]

ICON_PHONE = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" aria-hidden="true"><path d="M5 3h3.5l1.7 4.3-2.2 1.4a11 11 0 0 0 7.3 7.3l1.4-2.2L21 15.5V19a2 2 0 0 1-2 2A16 16 0 0 1 3 5a2 2 0 0 1 2-2z"/></svg>'
ICON_MAIL = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="1"/><path d="M3.5 6l8.5 7 8.5-7"/></svg>'
ICON_WEB = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.5 2.6 3.8 5.6 3.8 9s-1.3 6.4-3.8 9c-2.5-2.6-3.8-5.6-3.8-9S9.5 5.6 12 3z"/></svg>'


def esc(s):
    return html.escape(s, quote=True)


def page_url(fname):
    """Public address of a page. Netlify serves about.html at /about, so canonical
    URLs, the sitemap and structured data use the clean form; internal links keep
    .html so the local preview works."""
    if fname == "index.html":
        return SITE + "/"
    return f"{SITE}/{fname[:-5] if fname.endswith('.html') else fname}"


# ---------------------------------------------------------------- structured data
ORG_ID = SITE + "/#mahalo"
OPERATOR_ID = SITE + "/#operator"


def org_schema():
    return {
        "@context": "https://schema.org",
        "@type": "ProfessionalService",
        "@id": ORG_ID,
        "name": "MAHALO",
        "alternateName": "MAHALO Private Lifestyle Protection",
        "slogan": TAGLINE,
        "description": "MAHALO provides private lifestyle protection for affluent individuals and families, executives, estate owners and luxury hospitality clients: private estate and family protection, executive protection, luxury hospitality protection, yacht and private aviation travel security, and private event and VIP protection.",
        "url": SITE + "/",
        "image": f"{SITE}/{SHARE_IMAGE}",
        "telephone": "+1-727-400-6259",
        "email": EMAIL,
        "knowsAbout": [
            "Private lifestyle protection", "Executive protection", "Personal security",
            "Estate security", "Luxury residential protection", "Family protection",
            "Yacht and maritime security", "Private aviation security", "Travel security",
            "Private event security", "VIP protection", "Luxury hospitality security",
        ],
        "parentOrganization": {
            "@type": "Organization",
            "@id": OPERATOR_ID,
            "name": OPERATOR,
            "hasCredential": {
                "@type": "EducationalOccupationalCredential",
                "credentialCategory": "license",
                "name": "Florida Class B Security Agency License",
                "identifier": LICENSE_NO,
                "recognizedBy": {
                    "@type": "GovernmentOrganization",
                    "name": "Florida Department of Agriculture and Consumer Services, Division of Licensing",
                },
            },
        },
        "hasOfferCatalog": {
            "@type": "OfferCatalog",
            "name": "MAHALO private lifestyle protection services",
            "itemListElement": [
                {"@type": "Offer", "itemOffered": {"@type": "Service", "name": s["name"], "description": s["short"], "url": page_url(s["slug"])}}
                for s in SERVICES
            ],
        },
    }


def breadcrumb_schema(trail):
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": name, "item": page_url(f)}
            for i, (f, name) in enumerate(trail)
        ],
    }


def service_schema(s):
    return {
        "@context": "https://schema.org",
        "@type": "Service",
        "name": s["name"],
        "serviceType": s["title"],
        "description": s["description"],
        "url": page_url(s["slug"]),
        "image": f"{SITE}/{photo(s['hero'], 1200)}",
        "provider": {"@id": ORG_ID},
        "audience": {"@type": "Audience", "audienceType": "Affluent individuals and families, executives, estate owners and luxury hospitality clients"},
    }


def faq_schema():
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in FAQ
        ],
    }


# ---------------------------------------------------------------- shared chrome
def head(fname, title, description, schemas=(), image=None, noindex=False, preload=None):
    full_title = title if "MAHALO" in title else f"{title} | MAHALO"
    og_image = image or f"{SITE}/{SHARE_IMAGE}"
    robots = "noindex, follow" if noindex else "index, follow, max-image-preview:large, max-snippet:-1"
    ld = "".join(
        f'\n<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>' for s in schemas
    )
    pre = f'\n<link rel="preload" as="image" href="{preload}">' if preload else ""
    canonical = "" if noindex else f'\n<link rel="canonical" href="{page_url(fname)}">'
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(full_title)}</title>
<meta name="description" content="{esc(description)}">
<meta name="robots" content="{robots}">{canonical}
<meta name="theme-color" content="#121816">
<meta property="og:type" content="website">
<meta property="og:site_name" content="MAHALO Private Lifestyle Protection">
<meta property="og:title" content="{esc(full_title)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:url" content="{page_url(fname)}">
<meta property="og:image" content="{og_image}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(full_title)}">
<meta name="twitter:description" content="{esc(description)}">
<meta name="twitter:image" content="{og_image}">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bodoni+Moda:ital,opsz,wght@0,6..96,400..600;1,6..96,400..600&family=Jost:wght@300..600&display=swap">
<link rel="stylesheet" href="assets/styles.css?v={ASSET_VERSION}">{pre}{ld}
</head>
"""


BRAND = """<a class="brand" href="index.html" aria-label="MAHALO, Private Lifestyle Protection, home">
      <!-- Brand wordmark. Replace with the final MAHALO logo artwork when approved. -->
      <span class="brand-word"><strong>MAHALO</strong><small>Private Lifestyle Protection</small></span>
    </a>"""


def header(active):
    cur = ' aria-current="page"'
    links = "\n".join(
        '          <li><a href="%s"%s>%s</a></li>' % (h, cur if h == active else "", t) for h, t in NAV
    )
    ccur = cur if active == "contact.html" else ""
    return f"""<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header">
  <div class="wrap header-inner">
    {BRAND}
    <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="primary-nav" aria-label="Open menu"><span></span><span></span></button>
    <nav class="primary-nav" id="primary-nav" aria-label="Primary">
      <ul class="nav-links">
{links}
      </ul>
      <div class="nav-ctas">
        <a class="nav-contact" href="contact.html"{ccur}>Contact</a>
        <a class="btn" href="consultation.html">Request a Private Consultation</a>
      </div>
    </nav>
  </div>
</header>
"""


def footer():
    services = "\n".join(f'          <li><a href="{s["slug"]}">{s["name"]}</a></li>' for s in SERVICES)
    return f"""<footer class="site-footer">
  <div class="wrap">
    <div class="footer-top">
      <div class="footer-brand">
        {BRAND}
        <p class="footer-tagline">{TAGLINE}</p>
        <p class="footer-statement">Timeless elegance · Discreet protection · Peace of mind</p>
      </div>
      <div class="footer-col">
        <h4>Explore</h4>
        <ul>
          <li><a href="index.html">Home</a></li>
          <li><a href="about.html">About Us</a></li>
          <li><a href="services.html">Services</a></li>
          <li><a href="contact.html">Contact</a></li>
          <li><a href="consultation.html">Private Consultation</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h4>Services</h4>
        <ul>
{services}
        </ul>
      </div>
      <div class="footer-col">
        <h4>Private Line</h4>
        <ul>
          <li><a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a></li>
          <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
          <li><a href="{SITE}/">{WEBSITE_DISPLAY}</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <p class="license">MAHALO is an exclusive private-protection offering of <strong>{OPERATOR}</strong><br>{LICENSE}</p>
      <span>&copy; <span id="year">{TODAY[:4]}</span> MAHALO. All engagements held in strict confidence. <a href="privacy.html">Privacy Policy</a></span>
    </div>
  </div>
</footer>
<script src="assets/main.js?v={ASSET_VERSION}"></script>
</body>
</html>
"""


def page(fname, title, description, active, body, hero=True, **head_kw):
    doc = head(fname, title, description, **head_kw)
    doc += '<body class="%s">\n' % ("has-hero" if hero else "")
    doc += header(active) + body + footer()
    with open(os.path.join(OUT, fname), "w", encoding="utf-8") as f:
        f.write(doc)


def cta_band(photo_key="aerial", heading="A private conversation <em>begins here.</em>"):
    return f"""<section class="cta-band" aria-labelledby="cta-title">
  <img {hero_photo(photo_key)} alt="" loading="lazy" decoding="async">
  <div class="wrap">
    <span class="eyebrow">Private inquiries</span>
    <h2 id="cta-title">{heading}</h2>
    <p class="lede">Every engagement starts with a confidential conversation, held on your schedule and in complete confidence.</p>
    <div class="cta-actions">
      <a class="btn btn--brass" href="consultation.html">Request a Private Consultation <span class="arrow" aria-hidden="true">→</span></a>
      <a class="btn btn--ghost-light" href="tel:{PHONE_TEL}">Call {PHONE_DISPLAY}</a>
    </div>
  </div>
</section>
"""


def experience_tile(s, with_text=True, lazy=True):
    loading = ' loading="lazy"' if lazy else ""
    text = f'<p>{s["short"]}</p><span class="more">Discover</span>' if with_text else ""
    return f"""<a class="experience reveal" href="{s['slug']}">
        <img src="{photo(s['tile'], 900)}" alt="{esc(s['tile_alt'])}"{loading} decoding="async">
        <div class="experience-body"><span>{s['label']}</span><h3>{s['name']}</h3>{text}</div>
      </a>"""


def faq_html():
    items = "\n".join(
        f"      <details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in FAQ
    )
    return f'<div class="faq reveal">\n{items}\n    </div>'


# ================================================================ HOME
tiles = "\n      ".join(experience_tile(s) for s in SERVICES)
home = f"""<main id="main">
<section class="hero hero--home">
  <div class="hero-media"><img src="{HERO_IMAGE}" alt="A waterfront estate at sunset, its lit terraces and palms reflected in the water beside a yacht at its private dock" fetchpriority="high"></div>
  <div class="wrap hero-content">
    <div>
      <h1 class="rise hero-tagline">Some choose a lifestyle. <span class="tagline-2">Others protect it.</span></h1>
      <p class="hero-sub rise rise-2">Private Lifestyle Protection</p>
      <div class="hero-actions rise rise-3">
        <a class="btn btn--brass" href="#experience">Explore the MAHALO Experience <span class="arrow" aria-hidden="true">→</span></a>
        <a class="btn btn--ghost-light" href="consultation.html">Request a Private Consultation</a>
      </div>
    </div>
    <aside class="hero-aside rise rise-4">
      <strong>Dockside, 7:40 pm.</strong>
      Guests arriving by tender, the gate list confirmed, the evening unfolding exactly as planned. You simply enjoy the sunset.
    </aside>
  </div>
</section>

<section class="section" id="experience">
  <div class="wrap">
    <div class="meaning">
      <div class="reveal">
        <p class="pronounce">Ma·ha·lo</p>
        <p class="pronounce-meta"><i>/mə-ˈhä-lō/</i> &nbsp;·&nbsp; Hawaiian &nbsp;·&nbsp; gratitude, respect, hospitality, trust</p>
      </div>
      <div class="reveal">
        <span class="eyebrow">The MAHALO experience</span>
        <h2 class="meaning-statement" style="margin-top:1.5rem">For those who value the privilege of <em>living well.</em> We are not in the business of security guards. We offer the confidence of knowing that professional protection is thoughtfully provided, with the grace of the world’s finest hospitality.</h2>
      </div>
    </div>
    <div class="pillars reveal">
      <div class="pillar"><h3>Gratitude</h3><p>We never take access for granted. Being invited into your life is a privilege we earn every day.</p></div>
      <div class="pillar"><h3>Respect</h3><p>Your time, your privacy and your family’s routines come first. Protection adapts to you, never the other way around.</p></div>
      <div class="pillar"><h3>Hospitality</h3><p>Anticipatory, gracious and quietly present: protection delivered in the language of five-star service.</p></div>
      <div class="pillar"><h3>Trust</h3><p>Discretion is absolute. Every engagement is held in strict confidence.</p></div>
    </div>
  </div>
</section>

<section class="section section--sand" aria-labelledby="services-title">
  <div class="wrap">
    <div class="section-head reveal">
      <div>
        <span class="eyebrow">Five private experiences</span>
        <h2 id="services-title">Protection, composed around <em>the life you lead.</em></h2>
      </div>
      <p class="lede">From the estate to the open sea, the boardroom to the celebration, each MAHALO experience is designed around the way you already live.</p>
    </div>
    <div class="experiences">
      {tiles}
    </div>
  </div>
</section>

<section class="section section--dark">
  <div class="wrap reframe">
    <p class="reframe-label reveal">What we are not</p>
    <p class="reframe-old reveal">“We provide security guards.”</p>
    <p class="reframe-new reveal">We offer the privilege of <em>living well,</em> with the confidence that protection is thoughtfully provided.</p>
    <div class="reframe-foot reveal">
      <p class="lede">We create environments where extraordinary people can work, travel, invest and live without distraction.</p>
      <a class="btn btn--ghost-light" href="about.html">About MAHALO <span class="arrow" aria-hidden="true">→</span></a>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap split">
    <figure class="split-media reveal" style="margin:0">
      <img src="{photo('superyacht', 1400)}" alt="A superyacht cruising along a sunlit coast" loading="lazy" decoding="async">
      <figcaption>The Private Journey</figcaption>
    </figure>
    <div class="split-body reveal">
      <span class="eyebrow">Invisible by design</span>
      <h2>The finest protection is the kind <em>you barely notice.</em></h2>
      <p class="lede">Our professionals blend into the rhythm of your day, as comfortable at a gala as they are on a dock or in a hangar. Guests see a gracious team. You see a day that simply works.</p>
      <p class="lede">Behind the calm sits careful planning: advance work, coordination with your staff and partners, and contingencies considered long before you arrive.</p>
      <a class="text-link" href="services.html">Explore our services <span aria-hidden="true">→</span></a>
    </div>
  </div>
</section>

<section class="section section--basalt">
  <div class="wrap">
    <div class="section-head reveal">
      <div>
        <span class="eyebrow">The MAHALO engagement</span>
        <h2>Four steps to <em>unhurried</em> confidence.</h2>
      </div>
      <p class="lede">A deliberate process, shaped around your calendar and conducted in complete confidence.</p>
    </div>
    <ol class="process reveal">
      <li><h3>Private conversation</h3><p>A confidential conversation, in person or by phone, to understand the life you lead and the way you like to live it.</p></li>
      <li><h3>Discreet assessment</h3><p>We review your residences, travel, occasions and public profile, quietly and without disrupting your household.</p></li>
      <li><h3>Bespoke design</h3><p>A protection program tailored to you, integrated with your staff, your family office and your partners.</p></li>
      <li><h3>Seamless presence</h3><p>A dedicated lead oversees every detail and refines the program as your plans and profile evolve.</p></li>
    </ol>
    <div class="statement-strip reveal" style="margin-top:clamp(3.5rem,7vw,6rem)">
      <p>Timeless elegance. Discreet protection. Unparalleled peace of mind.</p>
      <small>An exclusive private-protection offering of {OPERATOR} · {LICENSE}</small>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head reveal">
      <div>
        <span class="eyebrow">Who we serve</span>
        <h2>For lives that are <em>anything but ordinary.</em></h2>
      </div>
      <p class="lede">Our clients share a need for privacy and a preference for discretion. Beyond that, every engagement is entirely their own.</p>
    </div>
    <div class="served reveal">
      <div><h3>Individuals &amp; families</h3><p>Affluent households who want their children to grow up with freedom, not fear.</p></div>
      <div><h3>Executives</h3><p>Chief executives, board members and principals, at home, at work and on the road.</p></div>
      <div><h3>Estate owners</h3><p>Owners of private estates, waterfront residences and seasonal homes.</p></div>
      <div><h3>Luxury hospitality</h3><p>Hotels, resorts, private clubs and residential communities and the distinguished guests they welcome.</p></div>
    </div>
  </div>
</section>

{cta_band()}
</main>
"""
page("index.html", "MAHALO | Private Lifestyle Protection & Estate Security",
     "Discreet private protection for affluent families, executives, estate owners and luxury hospitality: estate, executive, travel and private event security.",
     "index.html", home, schemas=[org_schema()], preload=HERO_IMAGE)

# ================================================================ ABOUT
about = f"""<main id="main">
<section class="hero hero--page">
  <div class="hero-media"><img {hero_photo('coast')} alt="Green cliffs meeting a turquoise Pacific ocean" fetchpriority="high"></div>
  <div class="wrap hero-content">
    <div>
      <span class="eyebrow rise">About MAHALO</span>
      <h1 class="rise rise-2">The privilege of living well, <em>thoughtfully protected.</em></h1>
      <p class="lede rise rise-3">Created for those who carry the most responsibility, and deserve to move through the world with the most ease.</p>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap split">
    <div class="split-body reveal">
      <span class="eyebrow">Our story</span>
      <h2>A private offering, <em>by invitation of trust.</em></h2>
      <p class="lede">MAHALO is an exclusive private-protection offering of {OPERATOR}, created for individuals and families, executives, estate owners and luxury hospitality clients who expect protection to be delivered with the polish of the world’s finest hotels.</p>
      <p class="lede">Rather than a security service, MAHALO is a way of living: estates that remain sanctuaries, journeys that unfold effortlessly and occasions that stay beautifully private. Protection is always present, and never the point.</p>
    </div>
    <figure class="split-media reveal" style="margin:0">
      <img src="{photo('resort_twilight', 1400)}" alt="A luxury resort and pool lit at twilight" loading="lazy" decoding="async">
      <figcaption>Hospitality is the standard</figcaption>
    </figure>
  </div>
</section>

<section class="section section--dark">
  <div class="wrap">
    <div class="meaning">
      <div class="reveal">
        <p class="pronounce">Mahalo</p>
        <p class="pronounce-meta" style="color:rgba(242,241,237,.65)"><i style="color:var(--salt)">/mə-ˈhä-lō/</i> &nbsp;·&nbsp; gratitude, respect, hospitality, trust</p>
      </div>
      <div class="reveal">
        <span class="eyebrow">Why the name</span>
        <p class="meaning-statement" style="margin-top:1.5rem">In Hawaiian, <em style="color:var(--brass-soft)">mahalo</em> is more than thank you. It carries a sense of admiration, respect and mutual obligation. It is how we see every relationship: a privilege extended to us, and one we honor through the way we work.</p>
      </div>
    </div>
  </div>
</section>

<section class="section section--sand">
  <div class="wrap">
    <div class="section-head reveal">
      <div>
        <span class="eyebrow">Our standards</span>
        <h2>The standards behind <em>the calm.</em></h2>
      </div>
    </div>
    <div class="pillars reveal" style="margin-top:0">
      <div class="pillar"><h3>Selected, not staffed</h3><p>Our professionals are chosen for judgment, composure and polish as much as for capability.</p></div>
      <div class="pillar"><h3>Fluent in service</h3><p>Etiquette, discretion and genuine hospitality sit alongside protective skill.</p></div>
      <div class="pillar"><h3>One point of contact</h3><p>A dedicated lead knows your household, your preferences and your people.</p></div>
      <div class="pillar"><h3>Licensed &amp; accountable</h3><p>Every MAHALO engagement is provided by a licensed Florida security agency.</p></div>
    </div>
    <p class="disclosure-note reveal">MAHALO services are provided by <strong>{OPERATOR}</strong>, {LICENSE}.</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head reveal">
      <div>
        <span class="eyebrow">Five private experiences</span>
        <h2>Explore <em>the MAHALO experience.</em></h2>
      </div>
    </div>
    <div class="experiences">
      {tiles}
    </div>
  </div>
</section>

{cta_band(IMG['wing'])}
</main>
"""
page("about.html", "About MAHALO: Private Lifestyle Protection",
     f"MAHALO is an exclusive private-protection offering of {OPERATOR}: discreet, hospitality-minded protection for families and executives.",
     "about.html", about,
     schemas=[org_schema(), breadcrumb_schema([("index.html", "Home"), ("about.html", "About Us")])])

# ================================================================ SERVICES OVERVIEW
rows = []
for s in SERVICES:
    bullets = "".join(f"<li>{i}</li>" for i in s["included"][:3])
    rows.append(f"""    <article class="service reveal" id="{s['key']}">
      <div class="service-media"><img src="{photo(s['tile'], 1400)}" alt="{esc(s['tile_alt'])}" loading="lazy" decoding="async"></div>
      <div>
        <span class="service-tag">{s['short']}</span>
        <h2><a href="{s['slug']}" style="text-decoration:none">{s['name']}</a></h2>
        <p>{s['paras'][0]}</p>
        <ul>{bullets}</ul>
        <a class="text-link more-link" href="{s['slug']}">Discover {s['name']} <span aria-hidden="true">→</span></a>
      </div>
    </article>""")
index_links = "".join(f'<li><a href="#{s["key"]}">{s["name"]}</a></li>' for s in SERVICES)
services_page = f"""<main id="main">
<section class="hero hero--page">
  <div class="hero-media"><img {hero_photo('aerial')} alt="An aerial view of boats moored in clear turquoise water" fetchpriority="high"></div>
  <div class="wrap hero-content">
    <div>
      <span class="eyebrow rise">Services</span>
      <h1 class="rise rise-2">Five private experiences, <em>one standard of care.</em></h1>
      <p class="lede rise rise-3">Every MAHALO program is bespoke. These five lifestyle services are brought together around each client, their family and the way they live.</p>
      <ul class="service-index rise rise-4">{index_links}</ul>
    </div>
  </div>
</section>

<section class="section" style="padding-top:clamp(2rem,4vw,3rem)">
  <div class="wrap">
{chr(10).join(rows)}
  </div>
</section>

<section class="section section--sand" aria-labelledby="faq-title">
  <div class="wrap">
    <div class="section-head reveal">
      <div>
        <span class="eyebrow">Questions</span>
        <h2 id="faq-title">Private lifestyle protection, <em>explained.</em></h2>
      </div>
    </div>
    {faq_html()}
  </div>
</section>

{cta_band(IMG['tropical_resort'])}
</main>
"""
page("services.html", "Estate, Executive & VIP Protection Services",
     "Five private protection services: estate and family, executive, luxury hospitality, yacht and aviation travel, and private event and VIP protection.",
     "services.html", services_page,
     schemas=[org_schema(), breadcrumb_schema([("index.html", "Home"), ("services.html", "Services")]), faq_schema()])

# ================================================================ SERVICE DETAIL PAGES
for s in SERVICES:
    paras = "\n".join(f'      <p class="lede">{p}</p>' for p in s["paras"])
    included = "".join(f"<li>{i}</li>" for i in s["included"])
    moments = "\n".join(f"      <div><h3>{t}</h3><p>{d}</p></div>" for t, d in s["moments"])
    related = "\n      ".join(experience_tile(o, with_text=False) for o in SERVICES if o is not s)
    body = f"""<main id="main">
<section class="hero hero--page">
  <div class="hero-media"><img {hero_photo(s['hero'])} alt="{esc(s['hero_alt'])}" fetchpriority="high"></div>
  <div class="wrap hero-content">
    <div>
      <ol class="crumbs rise"><li><a href="index.html">Home</a></li><li><a href="services.html">Services</a></li><li aria-current="page">{s['name']}</li></ol>
      <h1 class="rise rise-2">{s['name']}</h1>
      <p class="lede rise rise-3">{s['lede']}</p>
      <div class="hero-actions rise rise-4">
        <a class="btn btn--brass" href="consultation.html?service={s['key']}">Request a Private Consultation <span class="arrow" aria-hidden="true">→</span></a>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap detail-grid">
    <div class="detail-copy reveal">
      <span class="eyebrow">{s['title']}</span>
      <h2>{s['h2']}</h2>
{paras}
    </div>
    <aside class="included reveal">
      <h3>What is included</h3>
      <ul>{included}</ul>
      <a class="btn" href="consultation.html?service={s['key']}">Begin a Private Conversation <span class="arrow" aria-hidden="true">→</span></a>
    </aside>
  </div>
</section>

<section class="section section--dark section--tight">
  <div class="wrap">
    <div class="section-head reveal" style="margin-bottom:2rem">
      <div><span class="eyebrow">How it feels</span><h2>Protection you <em>experience as ease.</em></h2></div>
    </div>
    <div class="moments reveal">
{moments}
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head reveal">
      <div><span class="eyebrow">Also from MAHALO</span><h2>Explore other <em>private experiences.</em></h2></div>
      <p class="lede">Every MAHALO program can bring several experiences together around you and your family.</p>
    </div>
    <div class="related">
      {related}
    </div>
  </div>
</section>

{cta_band(s['tile'])}
</main>
"""
    page(s["slug"], f"{s['title']} | MAHALO", s["description"], "services.html", body,
         image=f"{SITE}/{photo(s['hero'], 1200)}",
         schemas=[service_schema(s), breadcrumb_schema([("index.html", "Home"), ("services.html", "Services"), (s["slug"], s["name"])])])

# ================================================================ CONSULTATION
interest_chips = "\n".join(
    f'            <label class="chip"><input type="checkbox" name="areas_of_interest" id="int-{s["key"]}" value="{s["name"]}"><span>{s["name"]}</span></label>'
    for s in SERVICES
)
consult = f"""<main id="main" style="padding-top:calc(var(--header-h) + env(safe-area-inset-top, 0px))">
<section class="section">
  <div class="wrap form-layout">
    <div class="form-aside">
      <span class="eyebrow">Private consultation</span>
      <h1 style="font-size:var(--t-2xl);margin-block:1.25rem 1.5rem">Tell us a little. <em>We’ll take it from there.</em></h1>
      <p class="lede">Share only what you are comfortable with. A member of the MAHALO team will reach out personally to arrange a confidential conversation.</p>
      <dl>
        <div><dt>Private line</dt><dd><a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a></dd></div>
        <div><dt>Email</dt><dd><a href="mailto:{EMAIL}">{EMAIL}</a></dd></div>
      </dl>
      <p class="note">Your request is held in strict confidence and shared only with the MAHALO team.</p>
    </div>

    <div class="form">
      <!-- Submissions go to HubSpot form {HUBSPOT_CONSULTATION_FORM} (portal {HUBSPOT_PORTAL}). Field names and option values match HubSpot's internal values. -->
      <form id="consult-form" data-hubspot-portal="{HUBSPOT_PORTAL}" data-hubspot-form="{HUBSPOT_CONSULTATION_FORM}" data-success="consult-success" novalidate>
        <div class="form-grid">
          <div class="field"><label for="c-first">First name</label><input id="c-first" name="firstname" autocomplete="given-name" required></div>
          <div class="field"><label for="c-last">Last name</label><input id="c-last" name="lastname" autocomplete="family-name" required></div>
          <div class="field"><label for="c-email">Email</label><input id="c-email" name="email" type="email" autocomplete="email" required></div>
          <div class="field"><label for="c-phone">Phone <span class="optional">(optional)</span></label><input id="c-phone" name="phone" type="tel" autocomplete="tel"></div>
          <div class="field"><label for="c-org">Organization <span class="optional">(optional)</span></label><input id="c-org" name="company" autocomplete="organization"></div>
          <div class="field"><label for="c-for">Consultation is for</label>
            <select id="c-for" name="consultation_is_for" required>
              <option value="">Select one</option>
              <option>Myself</option>
              <option>My family</option>
              <option>An executive or principal I represent</option>
              <option>An estate or residence</option>
              <option>A hotel, resort, club or community</option>
              <option>An event or gathering</option>
            </select>
          </div>
          <div class="field field--full"><label for="c-contact">Preferred contact</label>
            <select id="c-contact" name="preferred_contact_method">
              <option value="phone">Phone call</option>
              <option value="email">Email</option>
              <option value="in_person">In-person meeting</option>
            </select>
          </div>
          <fieldset class="field field--full">
            <legend>Areas of interest <span class="optional">(select any)</span></legend>
            <div class="chips">
{interest_chips}
            </div>
          </fieldset>
          <div class="field field--full"><label for="c-msg">Anything you’d like us to know <span class="optional">(optional)</span></label><textarea id="c-msg" name="message" placeholder="Residences, upcoming travel or occasions, as much or as little as you like."></textarea></div>
          <div class="field hp-field" aria-hidden="true"><label for="c-hp">Leave blank</label><input id="c-hp" name="mh_hp" type="text" tabindex="-1" autocomplete="off" data-1p-ignore data-lpignore="true" data-bwignore data-form-type="other"></div>
        </div>
        <p class="form-error" role="alert" hidden>We couldn’t send your request just now. Please try again, or email <a href="mailto:{EMAIL}">{EMAIL}</a> or call <a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a>.</p>
        <div class="form-foot">
          <small>We’ll store and process this information to respond to your request. You may opt out at any time. See our <a href="privacy.html">Privacy Policy</a>.</small>
          <button class="btn" type="submit"><span class="btn-label" data-default="Request Consultation">Request Consultation</span> <span class="arrow" aria-hidden="true">→</span></button>
        </div>
      </form>
      <div class="form-success" id="consult-success" tabindex="-1" hidden>
        <span class="eyebrow">MAHALO</span>
        <h2 style="margin-top:1.25rem;font-size:var(--t-2xl)">Thank you. <em>Your request is with us.</em></h2>
        <p>A member of the MAHALO team will contact you personally, in the way you prefer, to arrange a confidential conversation. For anything urgent, please call <a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a>.</p>
      </div>
    </div>
  </div>
</section>
</main>
"""
page("consultation.html", "Request a Private Consultation | MAHALO",
     f"Request a confidential consultation about estate, executive, hospitality, travel or event protection. Call {PHONE_DISPLAY} or email {EMAIL}.",
     "", consult, hero=False,
     schemas=[breadcrumb_schema([("index.html", "Home"), ("consultation.html", "Private Consultation")])])

# ================================================================ CONTACT
contact = f"""<main id="main">
<section class="hero hero--page">
  <div class="hero-media"><img src="{HERO_IMAGE}" alt="A waterfront estate and its docked yacht at sunset, reflected in calm water" fetchpriority="high"></div>
  <div class="wrap hero-content">
    <div>
      <span class="eyebrow rise">Contact</span>
      <h1 class="h-caps rise rise-2">A private conversation begins here.</h1>
      <p class="lede rise rise-3">For inquiries, consultations or to learn more about the MAHALO experience, please reach out.</p>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap form-layout">
    <div class="form-aside">
      <span class="eyebrow">Connect with MAHALO</span>
      <h2>We look forward to <em>hearing from you.</em></h2>
      <div class="contact-lines">
        <a class="contact-line" href="tel:{PHONE_TEL}"><span class="ico">{ICON_PHONE}</span><span><small>Telephone</small><strong>{PHONE_DISPLAY}</strong></span></a>
        <a class="contact-line" href="mailto:{EMAIL}"><span class="ico">{ICON_MAIL}</span><span><small>Email</small><strong>{EMAIL}</strong></span></a>
        <a class="contact-line" href="{SITE}/"><span class="ico">{ICON_WEB}</span><span><small>Website</small><strong>{WEBSITE_DISPLAY}</strong></span></a>
      </div>
      <p class="note">Looking to begin an engagement? A <a href="consultation.html">private consultation request</a> helps us prepare for our first conversation.</p>
    </div>
    <div class="form">
      <!-- Submissions go to HubSpot form {HUBSPOT_CONTACT_FORM} (portal {HUBSPOT_PORTAL}) via HubSpot's Forms API; see assets/main.js. -->
      <form id="contact-form" data-hubspot-portal="{HUBSPOT_PORTAL}" data-hubspot-form="{HUBSPOT_CONTACT_FORM}" data-success="contact-success" novalidate>
        <div class="form-grid">
          <div class="field"><label for="k-first">First name</label><input id="k-first" name="firstname" autocomplete="given-name" required></div>
          <div class="field"><label for="k-last">Last name</label><input id="k-last" name="lastname" autocomplete="family-name" required></div>
          <div class="field"><label for="k-email">Email</label><input id="k-email" name="email" type="email" autocomplete="email" required></div>
          <div class="field"><label for="k-phone">Phone <span class="optional">(optional)</span></label><input id="k-phone" name="phone" type="tel" autocomplete="tel"></div>
          <div class="field field--full"><label for="k-msg">Message <span class="optional">(optional)</span></label><textarea id="k-msg" name="message"></textarea></div>
          <div class="field hp-field" aria-hidden="true"><label for="k-hp">Leave blank</label><input id="k-hp" name="mh_hp" type="text" tabindex="-1" autocomplete="off" data-1p-ignore data-lpignore="true" data-bwignore data-form-type="other"></div>
        </div>
        <p class="form-error" role="alert" hidden>We couldn’t send your message just now. Please try again, or email <a href="mailto:{EMAIL}">{EMAIL}</a> or call <a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a>.</p>
        <div class="form-foot">
          <small>We’ll store and process this information to respond to your inquiry. You may opt out at any time. See our <a href="privacy.html">Privacy Policy</a>.</small>
          <button class="btn" type="submit"><span class="btn-label" data-default="Send Message">Send Message</span> <span class="arrow" aria-hidden="true">→</span></button>
        </div>
      </form>
      <div class="form-success" id="contact-success" tabindex="-1" hidden>
        <span class="eyebrow">MAHALO</span>
        <h2 style="margin-top:1.25rem;font-size:var(--t-2xl)">Thank you. <em>Your message is with us.</em></h2>
        <p>A member of the MAHALO team will be in touch personally. For anything urgent, please call <a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a>.</p>
      </div>
    </div>
  </div>
</section>

<section class="section section--basalt section--tight">
  <div class="wrap">
    <div class="statement-strip" style="border:0;padding-block:0">
      <p>Timeless elegance. Discreet protection. Unparalleled peace of mind.</p>
      <small>An exclusive private-protection offering of {OPERATOR} · {LICENSE}</small>
    </div>
  </div>
</section>
</main>
"""
page("contact.html", "Contact MAHALO: A Private Conversation Begins Here",
     f"Contact MAHALO Private Lifestyle Protection. Call {PHONE_DISPLAY}, email {EMAIL} or request a confidential consultation.",
     "contact.html", contact,
     schemas=[org_schema(), breadcrumb_schema([("index.html", "Home"), ("contact.html", "Contact")])])

# ================================================================ PRIVACY
# Plain-language draft describing what this site actually does. Have counsel
# review before launch, and update it whenever forms, hosting or tracking change.
PRIVACY_UPDATED = "November 9, 2026"
privacy = f"""<main id="main" style="padding-top:calc(var(--header-h) + env(safe-area-inset-top, 0px))">
<section class="section">
  <div class="wrap">
    <article class="prose">
      <span class="eyebrow">Privacy</span>
      <h1>Privacy Policy</h1>
      <p class="updated">Last updated {PRIVACY_UPDATED}</p>

      <p>Discretion is the foundation of everything we do, and it extends to how we handle your information. This policy explains what information the MAHALO website collects, how we use it and the choices you have.</p>

      <h2>Who we are</h2>
      <p>MAHALO is an exclusive private-protection offering of {OPERATOR} (“MAHALO”, “we”, “us”), {LICENSE}. This policy applies to {WEBSITE_DISPLAY} and to inquiries made through it.</p>

      <h2>Information you provide</h2>
      <p>When you use our contact or consultation forms, you may share your first and last name, email address, telephone number, organization, the type of consultation you are interested in, your preferred method of contact, the services you are interested in and any message you choose to include. You may also share information with us when you call or email us.</p>
      <p>Please share only what you are comfortable with. Detailed information about your residences, travel or security arrangements is best discussed in a private conversation rather than through the website.</p>

      <h2>Information collected automatically</h2>
      <p>Like most websites, the servers that host this site keep standard technical logs, such as your IP address, browser type, the pages you visit and the time of your visit, which are used to operate and secure the site. The site loads its typefaces from Google Fonts, so your browser connects to Google’s servers when pages load.</p>
      <p>This website does not use advertising cookies or analytics tracking. If that changes, we will update this policy.</p>

      <h2>How we use your information</h2>
      <ul>
        <li>To respond to your inquiry and arrange a confidential consultation</li>
        <li>To plan, provide and manage the services you request</li>
        <li>To send occasional communications related to your inquiry or our services, which you may opt out of at any time</li>
        <li>To operate, secure and improve this website</li>
        <li>To meet our legal, licensing and regulatory obligations</li>
      </ul>

      <h2>How we share information</h2>
      <p>We do not sell or rent your personal information. We share it only as needed with:</p>
      <ul>
        <li>The MAHALO and {OPERATOR} team members who handle your inquiry or engagement</li>
        <li>Service providers who support our operations, such as HubSpot, which stores and manages the inquiries submitted through our forms, and the companies that host this website and our email, each under their own privacy and security obligations</li>
        <li>Authorities or other parties when required by law, or when necessary to protect the safety, rights or property of our clients, our team or others</li>
      </ul>

      <h2>How long we keep information</h2>
      <p>We keep your information for as long as needed to respond to you, to provide our services and to meet our legal and licensing obligations, and then delete it or keep it in a form that no longer identifies you.</p>

      <h2>How we protect information</h2>
      <p>We use reasonable administrative, technical and physical safeguards to protect your information and limit access to those who need it. No method of transmission or storage is completely secure, so we cannot guarantee absolute security.</p>

      <h2>Your choices</h2>
      <p>You may ask us to tell you what personal information we hold about you, to correct or delete it, or to stop sending you communications, by emailing <a href="mailto:{EMAIL}">{EMAIL}</a> or calling <a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a>. We may need to verify your identity before acting on a request, and we may keep certain information where the law requires it.</p>

      <h2>Children</h2>
      <p>This website is intended for adults. We do not knowingly collect personal information online from children under 13. If you believe a child has provided us with information, please contact us and we will delete it.</p>

      <h2>Other websites</h2>
      <p>Links to other websites are provided for convenience. Their privacy practices are their own, and we encourage you to review their policies.</p>

      <h2>Changes to this policy</h2>
      <p>We may update this policy from time to time. The date at the top of this page shows when it was last revised.</p>

      <h2>Contact us</h2>
      <p>{OPERATOR}, operating MAHALO<br>
        Telephone: <a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a><br>
        Email: <a href="mailto:{EMAIL}">{EMAIL}</a></p>
    </article>
  </div>
</section>
</main>
"""
page("privacy.html", "Privacy Policy | MAHALO",
     f"How MAHALO, an offering of {OPERATOR}, collects, uses and protects information shared through this website.",
     "", privacy, hero=False,
     schemas=[breadcrumb_schema([("index.html", "Home"), ("privacy.html", "Privacy Policy")])])

# ================================================================ 404
not_found = f"""<main id="main" style="padding-top:calc(var(--header-h) + env(safe-area-inset-top, 0px))">
<section class="section">
  <div class="wrap" style="max-width:52rem">
    <span class="eyebrow">Page not found</span>
    <h1 style="font-size:var(--t-3xl);margin-block:1.25rem 1.5rem">This page has <em>moved on.</em></h1>
    <p class="lede">The page you were looking for isn’t here. Let us take you somewhere better.</p>
    <div class="hero-actions" style="margin-top:2.5rem">
      <a class="btn" href="index.html">Return Home</a>
      <a class="btn btn--ghost" href="services.html">Explore Services</a>
    </div>
  </div>
</section>
</main>
"""
page("404.html", "Page Not Found | MAHALO", "The page you were looking for could not be found.", "", not_found, hero=False, noindex=True)

# ================================================================ sitemap, robots, llms.txt
INDEXED = ["index.html", "about.html", "services.html"] + [s["slug"] for s in SERVICES] + ["consultation.html", "contact.html", "privacy.html"]
PRIORITY = {"index.html": "1.0", "services.html": "0.9", "about.html": "0.7", "consultation.html": "0.7", "contact.html": "0.7", "privacy.html": "0.3"}
urls = "\n".join(
    f"  <url><loc>{page_url(f)}</loc><lastmod>{TODAY}</lastmod><priority>{PRIORITY.get(f, '0.8')}</priority></url>"
    for f in INDEXED
)
with open(os.path.join(OUT, "sitemap.xml"), "w", encoding="utf-8") as f:
    f.write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}\n</urlset>\n')

AI_AND_SEARCH_BOTS = ["Googlebot", "Bingbot", "Applebot", "Applebot-Extended", "Google-Extended", "OAI-SearchBot",
                      "ChatGPT-User", "GPTBot", "PerplexityBot", "Perplexity-User", "ClaudeBot", "Claude-SearchBot",
                      "Claude-User", "DuckAssistBot"]
with open(os.path.join(OUT, "robots.txt"), "w", encoding="utf-8") as f:
    f.write("# MAHALO: welcome to search engines and AI search assistants\n")
    f.write("User-agent: *\n")
    for bot in AI_AND_SEARCH_BOTS:
        f.write(f"User-agent: {bot}\n")
    f.write("Allow: /\n\n")
    f.write(f"Sitemap: {SITE}/sitemap.xml\n")

llms = [
    "# MAHALO: Private Lifestyle Protection",
    "",
    f"> {TAGLINE} MAHALO provides discreet, hospitality-minded private protection for affluent individuals and families, executives, estate owners and luxury hospitality clients. MAHALO is an exclusive private-protection offering of {OPERATOR} ({LICENSE}).",
    "",
    f"Contact: {PHONE_DISPLAY} · {EMAIL} · {SITE}/",
    "",
    "## Services",
    "",
]
llms += [f"- [{s['name']}]({page_url(s['slug'])}): {s['short']} {s['description']}" for s in SERVICES]
llms += ["", "## Pages", "",
         f"- [Home]({page_url('index.html')}): Overview of MAHALO private lifestyle protection",
         f"- [About MAHALO]({page_url('about.html')}): Philosophy, standards and licensing",
         f"- [Services]({page_url('services.html')}): All five services and frequently asked questions",
         f"- [Private consultation]({page_url('consultation.html')}): Request a confidential consultation",
         f"- [Contact]({page_url('contact.html')}): Telephone, email and website",
         "", "## Frequently asked questions", ""]
llms += [f"- **{q}** {a}" for q, a in FAQ]
with open(os.path.join(OUT, "llms.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(llms) + "\n")

fetched = download_photos()
credits = ["# Image sources", "",
           "Photographs from Unsplash (https://unsplash.com/license): free for commercial use, no attribution required.",
           "Generated by tools/build_site.py.", ""]
credits += [f"- assets/images/{name}-*.jpg: https://images.unsplash.com/photo-{pid}" for pid, name in sorted(PHOTOS.values(), key=lambda p: p[1])]
credits += [f"- {HERO_IMAGE}, {SHARE_IMAGE}: MAHALO's own generated estate image"]
with open(os.path.join(ROOT, "IMAGE-SOURCES.md"), "w", encoding="utf-8") as f:
    f.write("\n".join(credits) + "\n")

print("Built", len(INDEXED) + 1, "pages, sitemap.xml, robots.txt and llms.txt;", fetched, "photos downloaded")
