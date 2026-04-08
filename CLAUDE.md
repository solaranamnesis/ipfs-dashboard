# CLAUDE.md

## Project Overview

**Solar Anamnesis** is a multilingual meteorite thin section gigapixel microphotography gallery. The site hosts high-resolution gigapixel mosaics of polished meteorite thin sections photographed under cross-polarized light (XPL) and visible light.

**Live Site:** https://www.solaranamnesis.com/

**Technical Stack:**
- Static HTML/CSS (vanilla, no JavaScript frameworks)
- Python 3 for utility scripts (`fix_footer_translations.py`)
- Deployed via HTTPS on static CDN with IPFS mirror
- Bootstrap-based responsive layout

---

## Repository Structure

```text
/
├── index.html              # English front-end (source of truth for structure)
├── index-{lang}.html       # Localized variants (42+ languages, BCP-47 codes)
├── style.css               # Site-wide stylesheet
├── style/                  # Assets (CSS, images, fonts, revolution slider)
│   ├── css/
│   ├── images/
│   └── revolution/
├── ajax/                   # AJAX content fragments
├── contact/                # Contact page assets
├── fix_footer_translations.py  # Utility script for footer link updates
├── package.json            # Dev dependencies (js-beautify, prettier)
├── robots.txt
└── sitemap.xml
```

---

## Coding Standards

### HTML Formatting

All `*.html` files are formatted with **js-beautify** (2-space indentation, no line-length wrap).

To re-format all HTML files:

```bash
npx html-beautify --indent-size 2 --wrap-line-length 0 --preserve-newlines --unformatted "" -r *.html
```

**Requirements:**

- 2-space indentation throughout.
- No line-length wrapping (long attribute lists stay on one line).
- Attribute values are unquoted where possible (matching existing style).
- Boolean attributes written without values (e.g., `aria-expanded=false` not `aria-expanded="false"`).
- Validate against W3C HTML validator.

### CSS Best Practices

- Site-wide styles live in `style.css` (minified/compact format).
- Per-page custom styles are added inside `<style>` blocks in each HTML file.
- No inline styles unless positioning/layout requires it.
- Use existing Bootstrap utility classes where possible.
- Follow existing naming conventions from `style.css`.

### RTL Language Support

RTL languages (`ar`, `he`, `fa`, `ur`) require:

- `dir=rtl` on the `<html>` element.
- Logical CSS properties where applicable.
- Bidirectional text testing.

---

## Localization

The English `index.html` is the **source of truth** for structure. All `index-{lang}.html` files mirror its structure with translated content.

### Supported Languages

| Code | Language       | RTL |
|------|----------------|-----|
| `ar` | Arabic         | ✓   |
| `fa` | Persian        | ✓   |
| `he` | Hebrew         | ✓   |
| `ur` | Urdu           | ✓   |
| `am` | Amharic        |     |
| `bn` | Bengali        |     |
| `bo` | Lhasa Tibetan  |     |
| `de` | German         |     |
| `el` | Greek          |     |
| `es` | Spanish        |     |
| `fr` | French         |     |
| `gu` | Gujarati       |     |
| `ha` | Hausa          |     |
| `hi` | Hindi          |     |
| `hu` | Magyar         |     |
| `hy` | Armenian       |     |
| `id` | Bahasa Indonesia |   |
| `it` | Italian        |     |
| `ja` | Japanese       |     |
| `jv` | Javanese       |     |
| `ka` | Georgian       |     |
| `kn` | Kannada        |     |
| `ko` | Korean         |     |
| `mr` | Marathi        |     |
| `new`| Nepal Bhasa    |     |
| `nl` | Dutch          |     |
| `or` | Odia           |     |
| `pa` | Punjabi        |     |
| `pl` | Polish         |     |
| `pt` | Portuguese     |     |
| `ru` | Russian        |     |
| `si` | Sinhala        |     |
| `sv` | Swedish        |     |
| `sw` | Kiswahili      |     |
| `ta` | Tamil          |     |
| `te` | Telugu         |     |
| `th` | Thai           |     |
| `tl` | Tagalog        |     |
| `tr` | Turkish        |     |
| `vi` | Vietnamese     |     |
| `yo` | Yoruba         |     |
| `zh` | Chinese        |     |

### Structural Conventions for Localized Files

Each `index-{lang}.html` follows this structure:

1. `<html lang={code}>` (add `dir=rtl` for RTL languages).
2. Localized `<meta>` tags (description, keywords, OG, Twitter).
3. `<link rel="canonical">` pointing to the localized URL.
4. Full `hreflang` link set (all 42+ languages + `x-default`).
5. Same `<header>` / navbar structure as English.
6. `<button class=about-toggle>` between `</header>` and `<main>`.
7. `<h1>` (visually hidden, for accessibility) inside `<main>`.
8. `<section id=about-collapse>` immediately after the hidden `<h1>`.
9. Four content sections: Blog, Flickr, Store, Panorama — each with translated heading, lead text, and CTA button.
10. `<footer>` with language switcher links (same set across all files).

---

## Common Tasks

### Adding a New Language

1. Copy `index.html` to `index-{lang}.html`.
2. Update `<html lang={code}>` (and add `dir=rtl` if needed).
3. Translate all `<meta>` tags, headings, lead paragraphs, and CTA button labels.
4. Update `<link rel="canonical">` to the new URL.
5. Add `<link rel="alternate" hreflang="{lang}">` entries to **all** existing files.
6. Add the new language link to the `<footer>` language switcher in **all** files.
7. Run js-beautify on the new file.

### Updating Footer Language Links (All Files)

Use the utility script to propagate footer changes across all localized files:

```bash
python3 fix_footer_translations.py
```

### Formatting HTML Files

```bash
# Format all HTML files at once
npx html-beautify --indent-size 2 --wrap-line-length 0 --preserve-newlines --unformatted "" -r *.html

# Format a single file
npx html-beautify --indent-size 2 --wrap-line-length 0 --preserve-newlines --unformatted "" -r index-{lang}.html
```

---

## IPFS Mirror

The site is mirrored on IPFS via IPNS:

```
k51qzi5uqu5dkr14dcifrhtn2jpqndw7pgyvgsxk5v9iq6y7ln9udh48trq5le
```

Access via: https://dweb.link/ipns/k51qzi5uqu5dkr14dcifrhtn2jpqndw7pgyvgsxk5v9iq6y7ln9udh48trq5le/

---

## Security Considerations

- All pages served over HTTPS only.
- No dynamic user input or server-side code.
- No external JavaScript dependencies loaded from third-party CDNs (all assets are self-hosted under `style/`).
- No mixed content — all asset URLs must be HTTPS.

---

## Testing Checklist

Before deploying changes:

- [ ] HTML validates (W3C validator or local check).
- [ ] All language files have consistent `hreflang` sets.
- [ ] Footer language switcher is complete and consistent across all files.
- [ ] RTL languages render correctly (`dir=rtl` present, layout intact).
- [ ] Responsive design tested on mobile/tablet/desktop.
- [ ] HTTPS enforced; no mixed content warnings.
- [ ] IPFS mirror updated if content changes.

---

## Contact & Support

- **Repository:** [ipfs-dashboard](https://github.com/solaranamnesis/ipfs-dashboard)
- **Live Site:** https://www.solaranamnesis.com/
- **Support:** Refer to project documentation or repository issues.
