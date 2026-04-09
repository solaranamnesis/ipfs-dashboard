#!/usr/bin/env python3
"""
Helper script to add a new language to the solaranamnesis.com site.

Usage:
    python3 add_new_language.py <lang_code>

Example:
    python3 add_new_language.py af   # Afrikaans

What this script does:
  1. Copies index-sr.html (or a chosen template file) as index-<lang>.html
     and reminds you to translate all strings.
  2. Adds hreflang="<lang>" to ALL existing index-*.html files.
  3. Adds a footer link for the new language to ALL existing index-*.html files.
  4. Updates fix_footer_translations.py LANG_ORDER to include the new lang.
  5. Prints a checklist of remaining manual steps.

The only manual work remaining after running this script:
  - Translate all text in the new index-<lang>.html file.
  - Add the correct translation to fix_footer_translations.py.
  - Update sitemap.xml and robots.txt if needed.
  - Test the page in a browser.
"""

import re
import os
import sys
import shutil

WORKDIR = os.path.dirname(os.path.abspath(__file__))

HREFLANG_PLACEHOLDER = '  <link rel="alternate" hreflang="x-default" href="https://www.solaranamnesis.com/">'
TEMPLATE_FILE = 'index-sr.html'   # best starting template for Latin-script Slavic


def get_href(lang):
    return 'index.html' if lang == 'en' else f'index-{lang}.html'


def get_all_hreflangs(exclude_new_lang=None):
    """Return list of (lang, href) for all existing lang files."""
    pairs = [('en', 'https://www.solaranamnesis.com/')]
    for fn in sorted(os.listdir(WORKDIR)):
        m = re.match(r'^index-(.+)\.html$', fn)
        if m:
            lang = m.group(1)
            if lang != exclude_new_lang:
                pairs.append((lang, f'https://www.solaranamnesis.com/{fn}'))
    return pairs


def add_hreflang_to_file(fpath, new_lang):
    """Add hreflang for new_lang to an existing HTML file."""
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    if f'hreflang="{new_lang}"' in content:
        return False  # already present
    new_link = f'  <link rel="alternate" hreflang="{new_lang}" href="https://www.solaranamnesis.com/index-{new_lang}.html">\n'
    content = content.replace(HREFLANG_PLACEHOLDER,
                               new_link + HREFLANG_PLACEHOLDER)
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(content)
    return True


def add_footer_link_to_file(fpath, new_lang, display_name, is_self=False):
    """Append new language link after the last language in the footer."""
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    href = '#' if is_self else f'index-{new_lang}.html'
    new_link = f'&nbsp;|&nbsp; <a href={href}>{display_name}</a>'

    # Strategy: find the last </a> before </p> in the footer paragraph
    # The footer paragraph contains all the language links
    pattern = r'((?:<a href=[^>]+>[^<]+</a>&nbsp;\|&nbsp; )*<a href=[^>]+>[^<]+</a>)(</p>)'

    if '<footer' not in content:
        return False

    footer_start = content.index('<footer')
    body = content[:footer_start]
    footer = content[footer_start:]

    new_footer = re.sub(
        r'(<a href=(?:index-[a-z]{2,3}(?:-[a-z]+)?\.html|#)>[^<]+</a>)(</p>)',
        rf'\1{new_link}\2',
        footer,
        count=1
    )
    if new_footer == footer:
        return False

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(body + new_footer)
    return True


def update_lang_order(new_lang, after_lang=None):
    """Add new_lang to LANG_ORDER in fix_footer_translations.py."""
    script_path = os.path.join(WORKDIR, 'fix_footer_translations.py')
    with open(script_path, 'r', encoding='utf-8') as f:
        content = f.read()

    if f"'{new_lang}'" in content:
        print(f"  fix_footer_translations.py already has '{new_lang}'")
        return

    if after_lang and f"'{after_lang}'" in content:
        content = content.replace(f"'{after_lang}'", f"'{after_lang}', '{new_lang}'", 1)
    else:
        # Append before closing bracket of LANG_ORDER
        content = re.sub(r"('(?:cs|ro|ku|[a-z]+)')\s*\n\]",
                         rf"\1, '{new_lang}'\n]", content)

    with open(script_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"  Updated LANG_ORDER in fix_footer_translations.py")


def create_new_lang_file(new_lang, template=TEMPLATE_FILE):
    """Copy template and update lang attribute, canonical, og:url, hreflang self-link."""
    src = os.path.join(WORKDIR, template)
    dst = os.path.join(WORKDIR, f'index-{new_lang}.html')
    if os.path.exists(dst):
        print(f"  {dst} already exists — skipping copy")
        return False

    with open(src, 'r', encoding='utf-8') as f:
        content = f.read()

    # Detect template's lang code
    m = re.search(r'<html lang=([a-z\-]+)', content)
    tmpl_lang = m.group(1) if m else 'sr'

    # Update lang attribute
    content = re.sub(r'<html lang=[a-z\-]+>', f'<html lang={new_lang}>', content)

    # Update canonical and og:url
    content = content.replace(
        f'href="https://www.solaranamnesis.com/index-{tmpl_lang}.html"',
        f'href="https://www.solaranamnesis.com/index-{new_lang}.html"'
    )
    content = content.replace(
        f'content="https://www.solaranamnesis.com/index-{tmpl_lang}.html"',
        f'content="https://www.solaranamnesis.com/index-{new_lang}.html"'
    )

    # Update JSON-LD url
    content = content.replace(
        f'"url": "https://www.solaranamnesis.com/index-{tmpl_lang}.html"',
        f'"url": "https://www.solaranamnesis.com/index-{new_lang}.html"'
    )
    content = content.replace(f'"inLanguage": "{tmpl_lang}"', f'"inLanguage": "{new_lang}"')

    # Update nav self-link
    content = content.replace(
        f'href=index-{tmpl_lang}.html>',
        f'href=index-{new_lang}.html>'
    )

    # Add hreflang for self before x-default
    self_hreflang = f'  <link rel="alternate" hreflang="{new_lang}" href="https://www.solaranamnesis.com/index-{new_lang}.html">\n'
    if f'hreflang="{new_lang}"' not in content:
        content = content.replace(HREFLANG_PLACEHOLDER, self_hreflang + HREFLANG_PLACEHOLDER)

    # Update footer self-link from template's lang to new lang self-link
    # Change `href=index-{tmpl_lang}.html>TEXT</a>` -> `href=#>TEXT</a>` in footer
    if '<footer' in content:
        footer_start = content.index('<footer')
        footer = content[footer_start:]
        # The self-link in footer references the template lang - change to #
        footer = re.sub(
            rf'href=index-{re.escape(tmpl_lang)}\.html>([^<]+</a>)',
            r'href=#>\1',
            footer
        )
        content = content[:footer_start] + footer

    with open(dst, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"  Created {dst} (based on {template})")
    print(f"  *** YOU MUST NOW TRANSLATE ALL TEXT IN {dst} ***")
    return True


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ('-h', '--help'):
        print("Usage: python3 add_new_language.py <lang_code> [display_name] [after_lang]")
        print("  lang_code:    BCP-47 language code, e.g. 'af', 'sq', 'bs'")
        print("  display_name: Native name for footer, e.g. 'Afrikaans'. Defaults to lang_code.")
        print("  after_lang:   Insert after this lang in LANG_ORDER, e.g. 'sr'")
        print()
        print("Example:")
        print("  python3 add_new_language.py af Afrikaans")
        sys.exit(0)

    new_lang = sys.argv[1].lower()
    # Validate lang code looks like a real BCP-47 code
    if not re.match(r'^[a-z]{2,3}(-[A-Za-z0-9]+)*$', new_lang):
        print(f"Error: '{new_lang}' does not look like a valid BCP-47 language code.")
        print("Examples: 'af', 'zh', 'sr-Latn', 'zh-Hant'")
        sys.exit(1)
    display_name = sys.argv[2] if len(sys.argv) > 2 else new_lang.title()
    after_lang = sys.argv[3] if len(sys.argv) > 3 else None

    print(f"\n=== Adding language: {new_lang} ({display_name}) ===\n")

    # 1. Create new language file from template
    print("Step 1: Creating new language file from template...")
    create_new_lang_file(new_lang)

    # 2. Update all existing files with hreflang + footer link
    print("\nStep 2: Updating all existing HTML files...")
    updated_hreflang = 0
    updated_footer = 0
    for fname in sorted(os.listdir(WORKDIR)):
        if not fname.endswith('.html'):
            continue
        fpath = os.path.join(WORKDIR, fname)
        is_self = (fname == f'index-{new_lang}.html')
        if add_hreflang_to_file(fpath, new_lang):
            updated_hreflang += 1
        if add_footer_link_to_file(fpath, new_lang, display_name, is_self=is_self):
            updated_footer += 1

    print(f"  Added hreflang to {updated_hreflang} files")
    print(f"  Added footer link to {updated_footer} files")

    # 3. Update LANG_ORDER in fix_footer_translations.py
    print("\nStep 3: Updating fix_footer_translations.py LANG_ORDER...")
    update_lang_order(new_lang, after_lang)

    # 4. Print checklist
    print(f"""
=== Checklist for completing '{new_lang}' language addition ===

  [x] Created index-{new_lang}.html from template
  [x] Added hreflang=\"{new_lang}\" to all HTML files
  [x] Added footer link '{display_name}' to all HTML files
  [x] Updated LANG_ORDER in fix_footer_translations.py

  [ ] TRANSLATE: Translate all text in index-{new_lang}.html
      - <html lang=...> attribute (verify correct BCP-47 code)
      - <meta name=description>, <meta name=keywords>
      - <title>, og:title, og:description, twitter:title, twitter:description
      - Navbar: page title, menu items, dropdown labels
      - About section: heading and paragraphs
      - Section headings and lead text for Blog, Flickr, Store, Panorama
      - Footer: copyright line, logo alt text
      - Footer language links: translate names of other languages

  [ ] Add translation entry to fix_footer_translations.py
      (follow the pattern of existing locales like 'sr', 'de', 'fr')

  [ ] If RTL language: add dir=rtl to <html> element

  [ ] Format with: npx html-beautify --indent-size 2 --wrap-line-length 0 \\
                   --preserve-newlines --unformatted "" -r index-{new_lang}.html

  [ ] Update sitemap.xml with new URL

  [ ] Validate HTML (W3C validator)

  [ ] Test in browser on desktop and mobile
""")


if __name__ == '__main__':
    main()
