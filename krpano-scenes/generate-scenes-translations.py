#!/usr/bin/env python3
"""Generate per-language scenes-{lang}.xml files for krpano i18n.

For each supported language, produces a copy of scenes.xml with:
  - "NWA" kept as-is; the full localized "Northwest Africa" phrase is
    appended after the title with an em-dash separator:
        "NWA 032 (Lunar)" -> "NWA 032 (Lunar) \u2014 \u5317\u897f\u30a2\u30d5\u30ea\u30ab"
  - "(Lunar)" translated to the local word for Lunar/Moon.
  - "Martian" in titles (e.g. "Martian Breccia") translated.

Usage:
    python3 generate-scenes-translations.py

Generates scenes-{lang}.xml in both SurfacePhotos/ and ThinSections/.
English uses the original scenes.xml (no scenes-en.xml generated).
"""

import os
import re

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SUBDIRS = ["SurfacePhotos", "ThinSections"]

# ============================================================================
# Northwest Africa translations — appended to titles containing "NWA"
# ============================================================================
NWA = {
    "en": "Northwest Africa",
    "es": "Noroeste de \u00c1frica",
    "de": "Nordwestafrika",
    "fr": "Afrique du Nord-Ouest",
    "ja": "\u5317\u897f\u30a2\u30d5\u30ea\u30ab",
    "it": "Nordovest dell\u2019Africa",
    "ru": "\u0421\u0435\u0432\u0435\u0440\u043e-\u0417\u0430\u043f\u0430\u0434\u043d\u0430\u044f \u0410\u0444\u0440\u0438\u043a\u0430",
    "zh": "\u897f\u5317\u975e",
    "he": "\u05de\u05e2\u05e8\u05d1 \u05d0\u05e4\u05e8\u05d9\u05e7\u05d4 \u05d4\u05e6\u05e4\u05d5\u05e0\u05d9\u05ea",
    "th": "\u0e41\u0e2d\u0e1f\u0e23\u0e34\u0e01\u0e32\u0e15\u0e30\u0e27\u0e31\u0e19\u0e15\u0e01\u0e40\u0e09\u0e35\u0e22\u0e07\u0e40\u0e2b\u0e19\u0e37\u0e2d",
    "vi": "T\u00e2y B\u1eafc Phi",
    "ar": "\u0634\u0645\u0627\u0644 \u063a\u0631\u0628 \u0623\u0641\u0631\u064a\u0642\u064a\u0627",
    "hi": "\u0909\u0924\u094d\u0924\u0930-\u092a\u0936\u094d\u091a\u093f\u092e \u0905\u092b\u094d\u0930\u0940\u0915\u093e",
    "el": "\u0392\u03bf\u03c1\u03b5\u03b9\u03bf\u03b4\u03c5\u03c4\u03b9\u03ba\u03ae \u0391\u03c6\u03c1\u03b9\u03ba\u03ae",
    "ko": "\ubd81\uc11c \uc544\ud504\ub9ac\uce74",
    "pt": "Noroeste da \u00c1frica",
    "bn": "\u0989\u09a4\u09cd\u09a4\u09b0-\u09aa\u09b6\u09cd\u099a\u09bf\u09ae \u0986\u09ab\u09cd\u09b0\u09bf\u0995\u09be",
    "pa": "\u0a09\u0a71\u0a24\u0a30-\u0a2a\u0a71\u0a1b\u0a2e\u0a40 \u0a05\u0a2b\u0a3c\u0a30\u0a40\u0a15\u0a3e",
    "fa": "\u0634\u0645\u0627\u0644 \u063a\u0631\u0628\u06cc \u0622\u0641\u0631\u06cc\u0642\u0627",
    "sw": "Magharibi Mwa Afrika",
    "id": "Barat Laut Afrika",
    "pl": "Afryka P\u00f3\u0142nocno-Zachodnia",
    "nl": "Noordwest-Afrika",
    "sv": "Nordv\u00e4stra Afrika",
    "tr": "Kuzeybat\u0131 Afrika",
    "hu": "\u00c9szaknyugat-Afrika",
    "new": "\u0909\u0924\u094d\u0924\u0930-\u092a\u0936\u094d\u091a\u093f\u092e \u0905\u092b\u094d\u0930\u093f\u0915\u093e",
    "bo": "\u0f64\u0f62\u0f0b\u0f53\u0f74\u0f56\u0f0b\u0f68\u0f0b\u0f67\u0fa5\u0f72\u0f0b\u0f62\u0f72\u0f0b\u0f40\u0f0b",
    "si": "\u0d8b\u0dad\u0dd4\u0dbb\u0dd4-\u0db6\u0da7\u0dc4\u0dd2\u0dbb \u0d85\u0db4\u0dca\u200d\u0dbb\u0dd2\u0d9a\u0dcf\u0dc0",
    "ta": "\u0bb5\u0b9f\u0bae\u0bc7\u0bb1\u0bcd\u0b95\u0bc1 \u0b86\u0baa\u0bcd\u0baa\u0bbf\u0bb0\u0bbf\u0b95\u0bcd\u0b95\u0bbe",
    "or": "\u0b09\u0b24\u0b4d\u0b24\u0b30-\u0b2a\u0b36\u0b4d\u0b1a\u0b3f\u0b2e \u0b06\u0b2b\u0b4d\u0b30\u0b3f\u0b15\u0b3e",
    "hy": "\u0540\u0575\u0578\u0582\u057d\u056b\u057d\u0561\u0580\u0565\u057e\u0574\u057f\u0575\u0561\u0576 \u0531\u0586\u0580\u056b\u056f\u0561",
    "tl": "Hilagang Kanlurang Aprika",
    "ka": "\u10e9\u10e0\u10d3\u10d8\u10da\u10dd\u10d4\u10d7-\u10d3\u10d0\u10e1\u10d0\u10d5\u10da\u10d4\u10d7\u10d8 \u10d0\u10e4\u10e0\u10d8\u10d9\u10d0",
    "kn": "\u0c89\u0ca4\u0ccd\u0ca4\u0cb0-\u0caa\u0cb6\u0ccd\u0c9a\u0cbf\u0cae \u0c86\u0cab\u0ccd\u0cb0\u0cbf\u0c95\u0cbe",
    "am": "\u1230\u121c\u1295 \u121d\u12d5\u122b\u1265 \u12a0\u134d\u122a\u12ab",
    "yo": "\u00ccw\u1ecd\u0300-O\u00f2r\u00f9n \u00c0r\u00edw\u00e1 \u00c1fr\u00edk\u00e0",
    "gu": "\u0a89\u0aa4\u0acd\u0aa4\u0ab0-\u0aaa\u0ab6\u0acd\u0a9a\u0abf\u0aae \u0a86\u0aab\u0acd\u0ab0\u0abf\u0a95\u0abe",
    "ha": "Arewa Masu Yammacin Afirka",
    "jv": "Afrika Lor-Kulon",
    "ur": "\u0634\u0645\u0627\u0644 \u0645\u063a\u0631\u0628\u06cc \u0627\u0641\u0631\u06cc\u0642\u06c1",
    "te": "\u0c09\u0c24\u0c4d\u0c24\u0c30-\u0c2a\u0c36\u0c4d\u0c1a\u0c3f\u0c2e \u0c06\u0c2b\u0c4d\u0c30\u0c3f\u0c15\u0c3e",
    "mr": "\u0909\u0924\u094d\u0924\u0930-\u092a\u0936\u094d\u091a\u093f\u092e \u0906\u092b\u094d\u0930\u093f\u0915\u093e",
    "la": "Africa Septentrionalis Occidentalis",
    "eu": "Ipar-mendebaldeko Afrika",
    "fi": "Luoteis-Afrikka",
    "mn": "\u0425\u043e\u0439\u0434 \u0431\u0430\u0440\u0443\u0443\u043d \u0410\u0444\u0440\u0438\u043a",
    "tt": "\u0422\u04e9\u043d\u044c\u044f\u043a-\u0411\u0430\u0442\u044b\u0448 \u0410\u0444\u0440\u0438\u043a\u0430",
    "kk": "\u0421\u043e\u043b\u0442\u04af\u0441\u0442\u0456\u043a-\u0411\u0430\u0442\u044b\u0441 \u0410\u0444\u0440\u0438\u043a\u0430",
    "ky": "\u0422\u04af\u043d\u0434\u04af\u043a-\u0411\u0430\u0442\u044b\u0448 \u0410\u0444\u0440\u0438\u043a\u0430",
    "cs": "Severoz\u00e1padn\u00ed Afrika",
    "uk": "\u041f\u0456\u0432\u043d\u0456\u0447\u043d\u043e-\u0417\u0430\u0445\u0456\u0434\u043d\u0430 \u0410\u0444\u0440\u0438\u043a\u0430",
    "ro": "Africa de Nord-Vest",
    "ku": "Bakur-Rojavay\u00ea Afr\u00eekay\u00ea",
    "ml": "\u0d35\u0d1f\u0d15\u0d4d\u0d15\u0d4d-\u0d2a\u0d1f\u0d3f\u0d1e\u0d4d\u0d1e\u0d3e\u0d31\u0d4d \u0d06\u0d2b\u0d4d\u0d30\u0d3f\u0d15\u0d4d\u0d15",
    "sr": "\u0421\u0435\u0432\u0435\u0440\u043e\u0437\u0430\u043f\u0430\u0434\u043d\u0430 \u0410\u0444\u0440\u0438\u043a\u0430",
    "bs": "Sjeverozapadna Afrika",
    "hr": "Sjeverozapadna Afrika",
    "ps": "\u0634\u0645\u0627\u0644 \u0644\u0648\u06cc\u062f\u06cc\u0681\u0647 \u0627\u0641\u0631\u064a\u0642\u0627",
    "ig": "\u1eccdi\u0323da Anyanw\u1ee5 Afr\u1ecbka",
    "af": "Noordwes-Afrika",
    "ca": "Nord-oest d\u2019\u00c0frica",
    "bg": "\u0421\u0435\u0432\u0435\u0440\u043e\u0437\u0430\u043f\u0430\u0434\u043d\u0430 \u0410\u0444\u0440\u0438\u043a\u0430",
    "my": "\u1021\u1014\u1031\u102c\u1000\u1039\u1019\u103c\u1031\u102c\u1000\u1039\u1021\u102c\u1016\u101b\u102d\u1000",
    "so": "Waqooyi Galbeed ee Afrika",
    "zu": "Ntshonalanga-Emazantsi Afrika",
    "ht": "N\u00f2dw\u00e8s Lafrik",
    "da": "Nordvestafrika",
    "no": "Nordvest-Afrika",
    "az": "\u015eimal-q\u0259rbi Afrika",
    "mg": "Afrika Atsinanana-andrefana",
    "qu": "Antikuna \u00d1awpaqman",
    "lb": "Nordwestafrika",
    "ga": "Thiar Thuaidh na hAfraice",
    "cy": "Gogledd-orllewin Affrica",
    "eo": "Nordokcidenta Afriko",
    "ia": "Africa Nord-Occidental",
}

# ============================================================================
# "Lunar" translations (Moon-related adjective/noun)
# ============================================================================
LUNAR = {
    "en": "Lunar",
    "es": "Lunar",
    "de": "Mond",
    "fr": "Lunaire",
    "ja": "\u6708",
    "it": "Lunare",
    "ru": "\u041b\u0443\u043d\u043d\u044b\u0439",
    "zh": "\u6708\u7403",
    "he": "\u05d9\u05e8\u05d7\u05d9",
    "th": "\u0e14\u0e27\u0e07\u0e08\u0e31\u0e19\u0e17\u0e23\u0e4c",
    "vi": "M\u1eb7t Tr\u0103ng",
    "ar": "\u0642\u0645\u0631\u064a",
    "hi": "\u091a\u0902\u0926\u094d\u0930",
    "el": "\u03a3\u03b5\u03bb\u03b7\u03bd\u03b9\u03b1\u03ba\u03cc\u03c2",
    "ko": "\ub2ec",
    "pt": "Lunar",
    "bn": "\u099a\u09be\u09a8\u09cd\u09a6\u09cd\u09b0",
    "pa": "\u0a1a\u0a70\u0a26\u0a30",
    "fa": "\u0642\u0645\u0631\u06cc",
    "sw": "Mwezi",
    "id": "Bulan",
    "pl": "Lunar",
    "nl": "Maan",
    "sv": "Lunar",
    "tr": "Ay",
    "hu": "Hold",
    "new": "\u091a\u0928\u094d\u0926\u094d\u0930",
    "bo": "\u0f5f\u0fb3\u0f0b\u0f56",
    "si": "\u0da0\u0db1\u0dca\u0daf\u0dca\u200d\u0dbb",
    "ta": "\u0ba8\u0bbf\u0bb2\u0bbe",
    "or": "\u0b1a\u0b28\u0b4d\u0b26\u0b4d\u0b30",
    "hy": "\u053c\u0578\u0582\u057d\u0576\u0561\u0575\u056b\u0576",
    "tl": "Buwan",
    "ka": "\u10db\u10d7\u10d5\u10d0\u10e0\u10d4",
    "kn": "\u0c9a\u0c82\u0ca6\u0ccd\u0cb0",
    "am": "\u1328\u1228\u1243",
    "yo": "O\u1e63upa",
    "gu": "\u0a9a\u0a82\u0aa6\u0acd\u0ab0",
    "ha": "Wata",
    "jv": "Bulan",
    "ur": "\u0642\u0645\u0631\u06cc",
    "te": "\u0c1a\u0c02\u0c26\u0c4d\u0c30",
    "mr": "\u091a\u0902\u0926\u094d\u0930",
    "la": "Lunaris",
    "eu": "Ilargi",
    "fi": "Kuu",
    "mn": "\u0421\u0430\u0440",
    "tt": "\u0410\u0439",
    "kk": "\u0410\u0439",
    "ky": "\u0410\u0439",
    "cs": "Lun\u00e1rn\u00ed",
    "uk": "\u041c\u0456\u0441\u044f\u0447\u043d\u0438\u0439",
    "ro": "Lunar",
    "ku": "Heyv",
    "ml": "\u0d1a\u0d28\u0d4d\u0d26\u0d4d\u0d30",
    "sr": "\u041b\u0443\u043d\u0430\u0440\u043d\u0438",
    "bs": "Lunarni",
    "hr": "Lunarni",
    "ps": "\u0633\u067e\u0648\u0696\u0645\u06cc\u0632",
    "ig": "\u1ecc\u1e45wa",
    "af": "Maan",
    "ca": "Lunar",
    "bg": "\u041b\u0443\u043d\u0435\u043d",
    "my": "\u101c",
    "so": "Dayax",
    "zu": "Inyanga",
    "ht": "Lalin",
    "da": "Lunar",
    "no": "Lunar",
    "az": "Ay",
    "mg": "Volana",
    "qu": "Killa",
    "lb": "Lunar",
    "ga": "Geala\u00ed",
    "cy": "Lleuad",
    "eo": "Luna",
}

# ============================================================================
# "Martian" translations (Mars-related adjective)
# ============================================================================
MARTIAN = {
    "en": "Martian",
    "es": "Marciano",
    "de": "Mars",
    "fr": "Martien",
    "ja": "\u706b\u661f",
    "it": "Marziano",
    "ru": "\u041c\u0430\u0440\u0441\u0438\u0430\u043d\u0441\u043a\u0438\u0439",
    "zh": "\u706b\u661f",
    "he": "\u05de\u05d0\u05d3\u05d9\u05de\u05d9",
    "th": "\u0e14\u0e32\u0e27\u0e2d\u0e31\u0e07\u0e04\u0e32\u0e23",
    "vi": "Sao H\u1ecfa",
    "ar": "\u0645\u0631\u064a\u062e\u064a",
    "hi": "\u092e\u0902\u0917\u0932",
    "el": "\u0391\u03c1\u03b5\u03b9\u03b1\u03bd\u03cc\u03c2",
    "ko": "\ud654\uc131",
    "pt": "Marciano",
    "bn": "\u09ae\u0999\u09cd\u0997\u09b2",
    "pa": "\u0a2e\u0a70\u0a17\u0a32",
    "fa": "\u0645\u0631\u06cc\u062e\u06cc",
    "sw": "Mirihi",
    "id": "Mars",
    "pl": "Marsja\u0144ski",
    "nl": "Mars",
    "sv": "Mars",
    "tr": "Mars",
    "hu": "Mars",
    "new": "\u092e\u0902\u0917\u0932",
    "bo": "\u0f58\u0f72\u0f42\u0f0b\u0f51\u0f58\u0f62",
    "si": "\u0d85\u0d9f\u0dc4\u0dbb\u0dd4",
    "ta": "\u0b9a\u0bc6\u0bb5\u0bcd\u0bb5\u0bbe\u0baf\u0bcd",
    "or": "\u0b2e\u0b19\u0b4d\u0b17\u0b33",
    "hy": "\u0544\u0561\u0580\u057d\u0575\u0561\u0576",
    "tl": "Marte",
    "ka": "\u10db\u10d0\u10e0\u10e1\u10d8",
    "kn": "\u0cae\u0c82\u0c97\u0cb3",
    "am": "\u121b\u122d\u1235",
    "yo": "M\u00e1\u00e0s\u00ec",
    "gu": "\u0aae\u0a82\u0a97\u0ab3",
    "ha": "Maras",
    "jv": "Mars",
    "ur": "\u0645\u0631\u06cc\u062e\u06cc",
    "te": "\u0c05\u0c02\u0c17\u0c3e\u0c30\u0c15",
    "mr": "\u092e\u0902\u0917\u0933",
    "la": "Martianus",
    "eu": "Marte",
    "fi": "Mars",
    "mn": "\u0410\u043d\u0433\u0430\u0440\u0430\u0433",
    "tt": "\u041c\u0430\u0440\u0441",
    "kk": "\u041c\u0430\u0440\u0441",
    "ky": "\u041c\u0430\u0440\u0441",
    "cs": "Mars",
    "uk": "\u041c\u0430\u0440\u0441\u0456\u0430\u043d\u0441\u044c\u043a\u0438\u0439",
    "ro": "Mar\u021bian",
    "ku": "Mars",
    "ml": "\u0d1a\u0d4a\u0d35\u0d4d\u0d35",
    "sr": "\u041c\u0430\u0440\u0441\u043e\u0432\u0441\u043a\u0438",
    "bs": "Marsovski",
    "hr": "Marsovski",
    "ps": "\u0645\u0631\u06cc\u062e",
    "ig": "Mars",
    "af": "Mars",
    "ca": "Marci\u00e0",
    "bg": "\u041c\u0430\u0440\u0441\u0438\u0430\u043d\u0441\u043a\u0438",
    "my": "\u1021\u1004\u1039\u1562\u102b",
    "so": "Mars",
    "zu": "uMars",
    "ht": "Mars",
    "da": "Mars",
    "no": "Mars",
    "az": "Mars",
    "mg": "Mars",
    "qu": "Mars",
    "lb": "Mars",
    "ga": "M\u00e1irt",
    "cy": "Mawrth",
    "eo": "Marsa",
}


def translate_title(title, lang):
    """Apply translations to a single scene title string."""
    if lang == "en":
        return title

    result = title

    # Translate "(Lunar)" -> "({lunar_word})"
    lunar = LUNAR.get(lang, "Lunar")
    result = result.replace("(Lunar)", f"({lunar})")

    # Translate "Martian" -> "{martian_word}" (handles "Martian Breccia")
    martian = MARTIAN.get(lang, "Martian")
    result = result.replace("Martian", martian)

    # For titles containing "NWA", append the localized phrase
    if "NWA" in result:
        nwa_phrase = NWA.get(lang, "Northwest Africa")
        result = f"{result} \u2014 {nwa_phrase}"

    return result


def process_scenes_file(input_path, output_path, lang):
    """Read scenes.xml, translate titles, write scenes-{lang}.xml."""
    with open(input_path, "r", encoding="utf-8") as f:
        content = f.read()

    def replace_title(match):
        original_title = match.group(1)
        translated = translate_title(original_title, lang)
        # Escape XML special characters in the translated title
        translated = translated.replace("&", "&amp;")
        return f'title="{translated}"'

    translated_content = re.sub(r'title="([^"]*)"', replace_title, content)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(translated_content)


def main():
    languages = sorted(NWA.keys())

    for subdir in SUBDIRS:
        input_path = os.path.join(SCRIPT_DIR, subdir, "scenes.xml")
        if not os.path.exists(input_path):
            print(f"WARNING: {input_path} not found, skipping")
            continue

        count = 0
        for lang in languages:
            if lang == "en":
                continue  # English uses the original scenes.xml
            output_path = os.path.join(SCRIPT_DIR, subdir, f"scenes-{lang}.xml")
            process_scenes_file(input_path, output_path, lang)
            count += 1

        print(f"{subdir}: generated {count} scenes-{{lang}}.xml files")

    print(f"\nDone! {len(languages) - 1} languages processed per directory.")


if __name__ == "__main__":
    main()
