#!/usr/bin/env python3
"""Generate per-language scenes-{lang}.xml files for krpano i18n.

For each supported language, produces a copy of scenes.xml with:
  - "NWA" kept as-is, with the full localized "Northwest Africa" phrase
    appended to every title that contains "NWA":
        "NWA 032 (Lunar)" -> "NWA 032 (Lunar) — 北西アフリカ"
  - "(Lunar)" translated to the local word for Lunar/Moon.
  - "Martian" in titles (e.g. "Martian Breccia") translated.

Usage:
    python3 generate-scenes-translations.py

Generates scenes-{lang}.xml in both SurfacePhotos/ and ThinSections/.
"""

import os
import re

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------------------
# Translation dictionaries
# ---------------------------------------------------------------------------

# fmt: off

# "Northwest Africa" — appended after titles containing "NWA"
NWA_TRANSLATIONS = {
    "en": "Northwest Africa",
    "es": "Noroeste de África",
    "de": "Nordwestafrika",
    "fr": "Afrique du Nord-Ouest",
    "ja": "北西アフリカ",
    "it": "Nordovest dell\u2019Africa",
    "ru": "Северо-Западная Африка",
    "zh": "西北非",
    "he": "מערב אפריקה הצפונית",
    "th": "แอฟริกาตะวันตกเฉียงเหนือ",
    "vi": "Tây Bắc Phi",
    "ar": "شمال غرب أفريقيا",
    "hi": "उत्तर-पश्चिम अफ्रीका",
    "el": "Βορειοδυτική Αφρική",
    "ko": "북서 아프리카",
    "pt": "Noroeste da África",
    "bn": "উত্তর-পশ্চিম আফ্রিকা",
    "pa": "ਉੱਤਰ-ਪੱਛਮੀ ਅਫ਼ਰੀਕਾ",
    "fa": "شمال غربی آفریقا",
    "sw": "Magharibi Mwa Afrika",
    "id": "Barat Laut Afrika",
    "pl": "Afryka Północno-Zachodnia",
    "nl": "Noordwest-Afrika",
    "sv": "Nordvästra Afrika",
    "tr": "Kuzeybatı Afrika",
    "hu": "Északnyugat-Afrika",
    "new": "उत्तर-पश्चिम अफ्रिका",
    "bo": "ཤར་ནུབ་ཨ་ཧྥི་རི་ཀ་",
    "si": "උතුරු-බටහිර අප්\u200dරිකාව",
    "ta": "வடமேற்கு ஆப்பிரிக்கா",
    "or": "ଉତ୍ତର-ପଶ୍ଚିମ ଆଫ୍ରିକା",
    "hy": "Հյուսիసարdelays. let me think again",
}

# fmt: on
