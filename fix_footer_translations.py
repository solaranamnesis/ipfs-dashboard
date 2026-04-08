#!/usr/bin/env python3
"""Fix footer language link translations in all index-*.html files."""

import re
import os

WORKDIR = os.path.dirname(os.path.abspath(__file__))

LANG_ORDER = [
    'en', 'es', 'de', 'fr', 'ja', 'it', 'ru', 'zh', 'he', 'th', 'vi', 'ar',
    'hi', 'el', 'ko', 'pt', 'bn', 'pa', 'fa', 'sw', 'id', 'pl', 'nl', 'sv',
    'tr', 'hu', 'new', 'bo', 'si', 'or', 'ta', 'hy', 'tl', 'ka', 'am', 'kn',
    'yo', 'gu', 'ha', 'jv', 'ur', 'te', 'mr', 'la', 'eu', 'fi', 'mn', 'tt'
]

def get_href(lang):
    return 'index.html' if lang == 'en' else f'index-{lang}.html'


def extract_native_scripts():
    """Extract native self-link text from each language file."""
    ns = {}
    for lang in LANG_ORDER:
        fn = os.path.join(WORKDIR, get_href(lang))
        if not os.path.exists(fn):
            continue
        with open(fn, 'r', encoding='utf-8') as f:
            content = f.read()
        for line in content.split('\n'):
            if 'href=#>' in line and ('href=index-mr' in line or 'href=index-te' in line or 'href=index-es' in line):
                pairs = re.findall(r'href=([^>]+)>([^<]+)</a>', line)
                for href, text in pairs:
                    if '#' in href:
                        m = re.search(r'\((.+?)\)\s*$', text)
                        ns[lang] = m.group(1) if m else text
                        break
                if lang in ns:
                    break
    return ns


def build_translations(ns):
    """Build complete translation table for all locales.

    Each entry: translations[locale][target_lang] = display_text
    Only entries that currently appear as English (and need replacing) are listed.
    For the 9 fully-English files, all 43 entries are provided.
    For partial files, only the needed entries are provided.
    """

    # Helper: format with native script in parens if non-Latin
    def wp(word, lang):
        """word + ' (' + native_script + ')'"""
        return f'{word} ({ns[lang]})'

    t = {}

    # =========== FULL REPLACEMENTS (all entries currently English) ===========

    t['mr'] = {
        'en': 'इंग्रजी',
        'es': 'स्पॅनिश',
        'de': 'जर्मन',
        'fr': 'फ्रेंच',
        'ja': f'जपानी ({ns["ja"]})',
        'it': 'इटालियन',
        'ru': f'रशियन ({ns["ru"]})',
        'zh': f'चिनी ({ns["zh"]})',
        'he': f'हिब्रू ({ns["he"]})',
        'th': f'थाई ({ns["th"]})',
        'vi': f'व्हिएतनामी ({ns["vi"]})',
        'ar': f'अरबी ({ns["ar"]})',
        'hi': f'हिंदी ({ns["hi"]})',
        'el': f'ग्रीक ({ns["el"]})',
        'ko': f'कोरियन ({ns["ko"]})',
        'pt': 'पोर्तुगीज',
        'bn': f'बंगाली ({ns["bn"]})',
        'pa': f'पंजाबी ({ns["pa"]})',
        'fa': f'फारसी ({ns["fa"]})',
        'sw': 'स्वाहिली',
        'id': 'इंडोनेशियन',
        'pl': 'पोलिश',
        'nl': 'डच',
        'sv': 'स्वीडिश',
        'tr': f'तुर्की ({ns["tr"]})',
        'hu': 'हंगेरियन',
        'new': f'नेवारी ({ns["new"]})',
        'bo': f'ल्हासा तिबेटी ({ns["bo"]})',
        'si': f'सिंहली ({ns["si"]})',
        'or': f'ओडिया ({ns["or"]})',
        'ta': f'तमिळ ({ns["ta"]})',
        'hy': f'आर्मेनियन ({ns["hy"]})',
        'tl': 'तागालोग',
        'ka': f'जॉर्जियन ({ns["ka"]})',
        'am': f'अम्हारिक ({ns["am"]})',
        'kn': f'कन्नड ({ns["kn"]})',
        'yo': 'योरुबा',
        'gu': f'गुजराती ({ns["gu"]})',
        'ha': 'हौसा',
        'jv': 'जावानीस',
        'ur': f'उर्दू ({ns["ur"]})',
        'te': f'तेलुगू ({ns["te"]})',
        'mr': 'मराठी',
        'la': 'लॅटिन',
        'eu': 'बास्क',
        'fi': 'फिन्निश',
        'mn': 'मंगोलियन (Latin)',
        'tt': f'तातार ({ns["tt"]})',
    }

    t['gu'] = {
        'en': 'અંગ્રેજી',
        'es': 'સ્પેનિશ',
        'de': 'જર્મન',
        'fr': 'ફ્રેંચ',
        'ja': f'જાપાની ({ns["ja"]})',
        'it': 'ઇટાલિયન',
        'ru': f'રશિયન ({ns["ru"]})',
        'zh': f'ચીની ({ns["zh"]})',
        'he': f'હિબ્રુ ({ns["he"]})',
        'th': f'થાઈ ({ns["th"]})',
        'vi': f'વિયેતનામી ({ns["vi"]})',
        'ar': f'અરબી ({ns["ar"]})',
        'hi': f'હિન્દી ({ns["hi"]})',
        'el': f'ગ્રીક ({ns["el"]})',
        'ko': f'કોરિયન ({ns["ko"]})',
        'pt': 'પોર્ટુગીઝ',
        'bn': f'બાંગ્લા ({ns["bn"]})',
        'pa': f'પંજાબી ({ns["pa"]})',
        'fa': f'ફારસી ({ns["fa"]})',
        'sw': 'સ્વાહિલી',
        'id': 'ઇન્ડોનેશિયન',
        'pl': 'પોલિશ',
        'nl': 'ડચ',
        'sv': 'સ્વીડિશ',
        'tr': f'તુર્કી ({ns["tr"]})',
        'hu': 'હંગેરિયન',
        'new': f'નેપાળ ભાષા ({ns["new"]})',
        'bo': f'લ્હાસા તિબેટી ({ns["bo"]})',
        'si': f'સિંહળ ({ns["si"]})',
        'or': f'ઓડિયા ({ns["or"]})',
        'ta': f'તમિળ ({ns["ta"]})',
        'hy': f'આર્મેનિયન ({ns["hy"]})',
        'tl': 'ટાગાલોગ',
        'ka': f'જ્યોર્જિયન ({ns["ka"]})',
        'am': f'અમ્હારિક ({ns["am"]})',
        'kn': f'કન્નડ ({ns["kn"]})',
        'yo': 'યોરુબા',
        'gu': 'ગુજરાતી',
        'ha': 'હૌસા',
        'jv': 'જાવાનીઝ',
        'ur': f'ઉર્દૂ ({ns["ur"]})',
        'te': f'તેલુગુ ({ns["te"]})',
        'mr': f'મરાઠી ({ns["mr"]})',
        'la': 'લૅટિન',
        'eu': 'Euskara',
        'fi': 'ફિનિश',
        'mn': 'મોંગોલિયન (Latin)',
        'tt': f'તતાર ({ns["tt"]})',
    }

    t['ha'] = {
        'en': 'Turanci',
        'es': 'Sipeniyanci',
        'de': 'Jamusanci',
        'fr': 'Faransanci',
        'ja': f'Japananci ({ns["ja"]})',
        'it': 'Italiyanci',
        'ru': f'Rashanci ({ns["ru"]})',
        'zh': f'Sinanci ({ns["zh"]})',
        'he': f'Ibrananci ({ns["he"]})',
        'th': f'Taiiyanci ({ns["th"]})',
        'vi': f'Bietnamusanci ({ns["vi"]})',
        'ar': f'Larabci ({ns["ar"]})',
        'hi': f'Hindiyanci ({ns["hi"]})',
        'el': f'Girikanci ({ns["el"]})',
        'ko': f'Koreyanci ({ns["ko"]})',
        'pt': 'Fotigalanci',
        'bn': f'Bangalanci ({ns["bn"]})',
        'pa': f'Punjabanci ({ns["pa"]})',
        'fa': f'Farisanci ({ns["fa"]})',
        'sw': 'Kiswahili',
        'id': 'Indonesiyanci',
        'pl': 'Polandiyanci',
        'nl': 'Hollandanci',
        'sv': 'Suwidanci',
        'tr': f'Turkanci ({ns["tr"]})',
        'hu': 'Bangaranci',
        'new': f'Nepal Bhasa ({ns["new"]})',
        'bo': f'Tibetanci ({ns["bo"]})',
        'si': f'Sinhalanci ({ns["si"]})',
        'or': f'Odiyanci ({ns["or"]})',
        'ta': f'Tamilanci ({ns["ta"]})',
        'hy': f'Armeniyanci ({ns["hy"]})',
        'tl': 'Tagalog',
        'ka': f'Jojiyanci ({ns["ka"]})',
        'am': f'Amharanci ({ns["am"]})',
        'kn': f'Kannadanci ({ns["kn"]})',
        'yo': 'Yarbanci',
        'gu': f'Gujaratanci ({ns["gu"]})',
        'ha': 'Hausa',
        'jv': 'Jawanci',
        'ur': f'Urdiyanci ({ns["ur"]})',
        'te': f'Telugunci ({ns["te"]})',
        'mr': f'Marathanci ({ns["mr"]})',
        'la': 'Latinci',
        'eu': 'Euskara',
        'fi': 'Faransancin Finnish',
        'mn': 'Mongoliyanci (Latin)',
        'tt': f'Tataranci ({ns["tt"]})',
    }

    t['ka'] = {
        'en': 'ინგლისური',
        'es': 'ესპანური',
        'de': 'გერმანული',
        'fr': 'ფრანგული',
        'ja': f'იაპონური ({ns["ja"]})',
        'it': 'იტალიური',
        'ru': f'რუსული ({ns["ru"]})',
        'zh': f'ჩინური ({ns["zh"]})',
        'he': f'ებრაული ({ns["he"]})',
        'th': f'ტაილანდური ({ns["th"]})',
        'vi': f'ვიეტნამური ({ns["vi"]})',
        'ar': f'არაბული ({ns["ar"]})',
        'hi': f'ჰინდი ({ns["hi"]})',
        'el': f'ბერძნული ({ns["el"]})',
        'ko': f'კორეული ({ns["ko"]})',
        'pt': 'პორტუგალიური',
        'bn': f'ბენგალური ({ns["bn"]})',
        'pa': f'პენჯაბური ({ns["pa"]})',
        'fa': f'სპარსული ({ns["fa"]})',
        'sw': 'სუაჰილი',
        'id': 'ინდონეზიური',
        'pl': 'პოლონური',
        'nl': 'ნიდერლანდური',
        'sv': 'შვედური',
        'tr': f'თურქული ({ns["tr"]})',
        'hu': 'უნგრული',
        'new': f'ნეპალ ბჰასა ({ns["new"]})',
        'bo': f'ლხასა ტიბეტური ({ns["bo"]})',
        'si': f'სინჰალური ({ns["si"]})',
        'or': f'ორია ({ns["or"]})',
        'ta': f'თამილური ({ns["ta"]})',
        'hy': f'სომხური ({ns["hy"]})',
        'tl': 'ტაგალოგი',
        'ka': 'ქართული',
        'am': f'ამჰარული ({ns["am"]})',
        'kn': f'კანადური ({ns["kn"]})',
        'yo': 'იორუბა',
        'gu': f'გუჯარათული ({ns["gu"]})',
        'ha': 'ჰაუსა',
        'jv': 'ჯავური',
        'ur': f'ურდუ ({ns["ur"]})',
        'te': f'თელუგუ ({ns["te"]})',
        'mr': f'მარათი ({ns["mr"]})',
        'la': 'ლათინური',
        'eu': 'ბასკური',
        'fi': 'ფინური',
        'mn': 'მონღოლური (Latin)',
        'tt': f'თათარული ({ns["tt"]})',
    }

    t['am'] = {
        'en': 'እንግሊዝኛ',
        'es': 'ስፓኒሽ',
        'de': 'ጀርመንኛ',
        'fr': 'ፈረንሳይኛ',
        'ja': f'ጃፓንኛ ({ns["ja"]})',
        'it': 'ኢጣሊያኛ',
        'ru': f'ሩሲያኛ ({ns["ru"]})',
        'zh': f'ቻይንኛ ({ns["zh"]})',
        'he': f'ዕብራይስጥ ({ns["he"]})',
        'th': f'ታይኛ ({ns["th"]})',
        'vi': f'ቬትናምኛ ({ns["vi"]})',
        'ar': f'አረብኛ ({ns["ar"]})',
        'hi': f'ሒንዲ ({ns["hi"]})',
        'el': f'ግሪክኛ ({ns["el"]})',
        'ko': f'ኮርያኛ ({ns["ko"]})',
        'pt': 'ፖርቱጋልኛ',
        'bn': f'ቤንጋሊኛ ({ns["bn"]})',
        'pa': f'ፑንጃቢኛ ({ns["pa"]})',
        'fa': f'ፋርሲኛ ({ns["fa"]})',
        'sw': 'ኪስዋሒሊ',
        'id': 'ኢንዶኔዥያኛ',
        'pl': 'ፖሊሽ',
        'nl': 'ደች',
        'sv': 'ስዊድንኛ',
        'tr': f'ቱርክኛ ({ns["tr"]})',
        'hu': 'ሃንጋሪኛ',
        'new': f'ነፓል ብሃሳ ({ns["new"]})',
        'bo': f'ቲቤትኛ ({ns["bo"]})',
        'si': f'ሲንሃላ ({ns["si"]})',
        'or': f'ኦዲያ ({ns["or"]})',
        'ta': f'ታሚልኛ ({ns["ta"]})',
        'hy': f'አርሜንያኛ ({ns["hy"]})',
        'tl': 'ታጋሎግ',
        'ka': f'ጆርጂያኛ ({ns["ka"]})',
        'am': 'አማርኛ',
        'kn': f'ካናዳኛ ({ns["kn"]})',
        'yo': 'ዮሩባ',
        'gu': f'ጉጅራቲኛ ({ns["gu"]})',
        'ha': 'ሃውሳ',
        'jv': 'ጃቫንኛ',
        'ur': f'ኡርዱ ({ns["ur"]})',
        'te': f'ቴሉጉ ({ns["te"]})',
        'mr': f'ማራቲ ({ns["mr"]})',
        'la': 'ላቲን',
        'eu': 'Euskara',
        'fi': 'ፊኒሽ',
        'mn': 'ሞንጎሊያኛ (Latin)',
        'tt': f'ታታርኛ ({ns["tt"]})',
    }

    t['kn'] = {
        'en': 'ಇಂಗ್ಲಿಷ್',
        'es': 'ಸ್ಪ್ಯಾನಿಷ್',
        'de': 'ಜರ್ಮನ್',
        'fr': 'ಫ್ರೆಂಚ್',
        'ja': f'ಜಾಪನೀಸ್ ({ns["ja"]})',
        'it': 'ಇಟಾಲಿಯನ್',
        'ru': f'ರಷ್ಯನ್ ({ns["ru"]})',
        'zh': f'ಚೀನೀ ({ns["zh"]})',
        'he': f'ಹೀಬ್ರೂ ({ns["he"]})',
        'th': f'ಥಾಯ್ ({ns["th"]})',
        'vi': f'ವಿಯೆಟ್ನಾಮೀಸ್ ({ns["vi"]})',
        'ar': f'ಅರಬಿಕ್ ({ns["ar"]})',
        'hi': f'ಹಿಂದಿ ({ns["hi"]})',
        'el': f'ಗ್ರೀಕ್ ({ns["el"]})',
        'ko': f'ಕೊರಿಯನ್ ({ns["ko"]})',
        'pt': 'ಪೋರ್ಚುಗೀಸ್',
        'bn': f'ಬೆಂಗಾಲಿ ({ns["bn"]})',
        'pa': f'ಪಂಜಾಬಿ ({ns["pa"]})',
        'fa': f'ಪರ್ಷಿಯನ್ ({ns["fa"]})',
        'sw': 'ಕಿಸ್ವಾಹಿಲಿ',
        'id': 'ಇಂಡೋನೇಷಿಯನ್',
        'pl': 'ಪೋಲಿಷ್',
        'nl': 'ಡಚ್',
        'sv': 'ಸ್ವೀಡಿಷ್',
        'tr': f'ತುರ್ಕಿ ({ns["tr"]})',
        'hu': 'ಹಂಗೇರಿಯನ್',
        'new': f'ನೇಪಾಳ ಭಾಷಾ ({ns["new"]})',
        'bo': f'ಲ್ಹಾಸಾ ಟಿಬೆಟಿಯನ್ ({ns["bo"]})',
        'si': f'ಸಿಂಹಳ ({ns["si"]})',
        'or': f'ಒಡಿಯಾ ({ns["or"]})',
        'ta': f'ತಮಿಳು ({ns["ta"]})',
        'hy': f'ಅರ್ಮೇನಿಯನ್ ({ns["hy"]})',
        'tl': 'ತಾಗಲೋಗ್',
        'ka': f'ಜಾರ್ಜಿಯನ್ ({ns["ka"]})',
        'am': f'ಅಮ್ಹಾರಿಕ್ ({ns["am"]})',
        'kn': 'ಕನ್ನಡ',
        'yo': 'ಯೊರುಬಾ',
        'gu': f'ಗುಜರಾತಿ ({ns["gu"]})',
        'ha': 'ಹೌಸಾ',
        'jv': 'ಜಾವಾನೀಸ್',
        'ur': f'ಉರ್ದು ({ns["ur"]})',
        'te': f'ತೆಲುಗು ({ns["te"]})',
        'mr': f'ಮರಾಠಿ ({ns["mr"]})',
        'la': 'ಲ್ಯಾಟಿನ್',
        'eu': 'ಬಾಸ್ಕ್',
        'fi': 'ಫಿನ್ನಿಶ್',
        'mn': 'ಮಂಗೋಲಿಯನ್ (Latin)',
        'tt': f'ತಾತರ್ ({ns["tt"]})',
    }

    t['te'] = {
        'en': 'ఇంగ్లీష్',
        'es': 'స్పానిష్',
        'de': 'జర్మన్',
        'fr': 'ఫ్రెంచ్',
        'ja': f'జపనీస్ ({ns["ja"]})',
        'it': 'ఇటాలియన్',
        'ru': f'రష్యన్ ({ns["ru"]})',
        'zh': f'చైనీస్ ({ns["zh"]})',
        'he': f'హీబ్రూ ({ns["he"]})',
        'th': f'థాయ్ ({ns["th"]})',
        'vi': f'వియత్నామీస్ ({ns["vi"]})',
        'ar': f'అరబిక్ ({ns["ar"]})',
        'hi': f'హిందీ ({ns["hi"]})',
        'el': f'గ్రీక్ ({ns["el"]})',
        'ko': f'కొరియన్ ({ns["ko"]})',
        'pt': 'పోర్చుగీస్',
        'bn': f'బెంగాలీ ({ns["bn"]})',
        'pa': f'పంజాబీ ({ns["pa"]})',
        'fa': f'పర్షియన్ ({ns["fa"]})',
        'sw': 'స్వాహిలి',
        'id': 'ఇండోనేషియన్',
        'pl': 'పోలిష్',
        'nl': 'డచ్',
        'sv': 'స్వీడిష్',
        'tr': f'టర్కిష్ ({ns["tr"]})',
        'hu': 'హంగేరియన్',
        'new': f'నేపాల్ భాష ({ns["new"]})',
        'bo': f'ల్హాసా టిబెటన్ ({ns["bo"]})',
        'si': f'సిన్హళ ({ns["si"]})',
        'or': f'ఒడియా ({ns["or"]})',
        'ta': f'తమిళ్ ({ns["ta"]})',
        'hy': f'అర్మేనియన్ ({ns["hy"]})',
        'tl': 'తగలాగ్',
        'ka': f'జార్జియన్ ({ns["ka"]})',
        'am': f'అమ్హారిక్ ({ns["am"]})',
        'kn': f'కన్నడ ({ns["kn"]})',
        'yo': 'యోరుబా',
        'gu': f'గుజరాతీ ({ns["gu"]})',
        'ha': 'హౌసా',
        'jv': 'జావానీస్',
        'ur': f'ఉర్దూ ({ns["ur"]})',
        'te': 'తెలుగు',
        'mr': f'మరాఠీ ({ns["mr"]})',
        'la': 'లాటిన్',
        'eu': 'Euskara',
        'fi': 'ఫిన్నిష్',
        'mn': 'మంగోలియన్ (Latin)',
        'tt': f'తాటర్ ({ns["tt"]})',
    }

    t['tl'] = {
        'en': 'Ingles',
        'es': 'Espanyol',
        'de': 'Aleman',
        'fr': 'Pranses',
        'ja': f'Hapon ({ns["ja"]})',
        'it': 'Italyano',
        'ru': f'Ruso ({ns["ru"]})',
        'zh': f'Intsik ({ns["zh"]})',
        'he': f'Hebreo ({ns["he"]})',
        'th': f'Thai ({ns["th"]})',
        'vi': f'Biyetnames ({ns["vi"]})',
        'ar': f'Arabe ({ns["ar"]})',
        'hi': f'Hindi ({ns["hi"]})',
        'el': f'Griyego ({ns["el"]})',
        'ko': f'Koreano ({ns["ko"]})',
        'pt': 'Portuges',
        'bn': f'Bengali ({ns["bn"]})',
        'pa': f'Punjabi ({ns["pa"]})',
        'fa': f'Persyano ({ns["fa"]})',
        'sw': 'Kiswahili',
        'id': 'Indonesyano',
        'pl': 'Polako',
        'nl': 'Olandes',
        'sv': 'Suweko',
        'tr': f'Turko ({ns["tr"]})',
        'hu': 'Hungaro',
        'new': f'Nepal Bhasa ({ns["new"]})',
        'bo': f'Tibetano ({ns["bo"]})',
        'si': f'Sinhala ({ns["si"]})',
        'or': f'Odia ({ns["or"]})',
        'ta': f'Tamil ({ns["ta"]})',
        'hy': f'Armenyo ({ns["hy"]})',
        'tl': 'Tagalog',
        'ka': f'Heorxiano ({ns["ka"]})',
        'am': f'Amharic ({ns["am"]})',
        'kn': f'Kannada ({ns["kn"]})',
        'yo': 'Yoruba',
        'gu': f'Gujarati ({ns["gu"]})',
        'ha': 'Hausa',
        'jv': 'Jawa',
        'ur': f'Urdu ({ns["ur"]})',
        'te': f'Telugu ({ns["te"]})',
        'mr': f'Marathi ({ns["mr"]})',
        'la': 'Latin',
        'eu': 'Euskara',
        'fi': 'Finlandes',
        'mn': 'Mongolian (Latin)',
        'tt': f'Tatar ({ns["tt"]})',
    }

    t['yo'] = {
        'en': 'Èdè Gẹ̀ẹ́sì',
        'es': 'Èdè Sípáánì',
        'de': 'Èdè Jámánì',
        'fr': 'Èdè Fárándì',
        'ja': f'Èdè Japánì ({ns["ja"]})',
        'it': 'Èdè Ítálì',
        'ru': f'Èdè Rọ́ṣíà ({ns["ru"]})',
        'zh': f'Èdè Ṣáínà ({ns["zh"]})',
        'he': f'Èdè Hébérù ({ns["he"]})',
        'th': f'Èdè Tailandi ({ns["th"]})',
        'vi': f'Èdè Vietnamu ({ns["vi"]})',
        'ar': f'Èdè Lárúbáwá ({ns["ar"]})',
        'hi': f'Èdè Hindì ({ns["hi"]})',
        'el': f'Èdè Giriisi ({ns["el"]})',
        'ko': f'Èdè Kòrìà ({ns["ko"]})',
        'pt': 'Èdè Potogí',
        'bn': f'Èdè Bengalì ({ns["bn"]})',
        'pa': f'Èdè Punjabi ({ns["pa"]})',
        'fa': f'Èdè Páṣíà ({ns["fa"]})',
        'sw': 'Kiswahili',
        'id': 'Èdè Indonéṣíà',
        'pl': 'Èdè Polandi',
        'nl': 'Èdè Dọ́ọ̀tísì',
        'sv': 'Èdè Swídíìsì',
        'tr': f'Èdè Tọọ̀kì ({ns["tr"]})',
        'hu': 'Èdè Hangárì',
        'new': f'Nepal Bhasa ({ns["new"]})',
        'bo': f'Èdè Tibetì ({ns["bo"]})',
        'si': f'Èdè Sinhala ({ns["si"]})',
        'or': f'Èdè Odiya ({ns["or"]})',
        'ta': f'Èdè Tamili ({ns["ta"]})',
        'hy': f'Èdè Araméníà ({ns["hy"]})',
        'tl': 'Tagalog',
        'ka': f'Èdè Jọọ̀jíà ({ns["ka"]})',
        'am': f'Èdè Amhariki ({ns["am"]})',
        'kn': f'Èdè Kannadà ({ns["kn"]})',
        'yo': 'Yorùbá',
        'gu': f'Èdè Gujarati ({ns["gu"]})',
        'ha': 'Èdè Hausa',
        'jv': 'Èdè Javanese',
        'ur': f'Èdè Urdù ({ns["ur"]})',
        'te': f'Èdè Telugu ({ns["te"]})',
        'mr': f'Èdè Marathi ({ns["mr"]})',
        'la': 'Èdè Látìnì',
        'eu': 'Euskara',
        'fi': 'Èdè Finnish',
        'mn': 'Mongólíà (Latin)',
        'tt': f'Tatar ({ns["tt"]})',
    }


    t['la'] = {
        'en': 'Anglice',
        'es': 'Hispanice',
        'de': 'Germanice',
        'fr': 'Gallice',
        'ja': f'Iaponice ({ns["ja"]})',
        'it': 'Italice',
        'ru': f'Russice ({ns["ru"]})',
        'zh': f'Sinice ({ns["zh"]})',
        'he': f'Hebraice ({ns["he"]})',
        'th': f'Thaice ({ns["th"]})',
        'vi': f'Vietnamice ({ns["vi"]})',
        'ar': f'Arabice ({ns["ar"]})',
        'hi': f'Hindice ({ns["hi"]})',
        'el': f'Graece ({ns["el"]})',
        'ko': f'Coreance ({ns["ko"]})',
        'pt': 'Lusitanice',
        'bn': f'Bengalice ({ns["bn"]})',
        'pa': f'Panjabiice ({ns["pa"]})',
        'fa': f'Persice ({ns["fa"]})',
        'sw': 'Kiswahili',
        'id': 'Indonesice',
        'pl': 'Polonice',
        'nl': 'Batavice',
        'sv': 'Suecice',
        'tr': f'Turcice ({ns["tr"]})',
        'hu': 'Hungarice',
        'new': f'Nepal Bhasa ({ns["new"]})',
        'bo': f'Tibetice ({ns["bo"]})',
        'si': f'Singhalice ({ns["si"]})',
        'or': f'Odice ({ns["or"]})',
        'ta': f'Tamilice ({ns["ta"]})',
        'hy': f'Armenice ({ns["hy"]})',
        'tl': 'Tagalice',
        'ka': f'Georgice ({ns["ka"]})',
        'am': f'Amharice ({ns["am"]})',
        'kn': f'Kannadice ({ns["kn"]})',
        'yo': 'Yorubice',
        'gu': f'Gujaratice ({ns["gu"]})',
        'ha': 'Hausaice',
        'jv': 'Iavanice',
        'ur': f'Urduice ({ns["ur"]})',
        'te': f'Teluguce ({ns["te"]})',
        'mr': f'Marathice ({ns["mr"]})',
        'la': 'Latina',
        'eu': 'Euskara',
        'fi': 'Finnice',
        'mn': 'Mongolica (Latina)',
        'tt': f'Lingua Tatarica ({ns["tt"]})',
    }

    # Finnish (fi) - full translations of all language names in Finnish
    t['fi'] = {
        'en': 'Englanti',
        'es': 'Espanja',
        'de': 'Saksa',
        'fr': 'Ranska',
        'ja': f'Japani ({ns["ja"]})',
        'it': 'Italia',
        'ru': f'Venäjä ({ns["ru"]})',
        'zh': f'Kiina ({ns["zh"]})',
        'he': f'Heprea ({ns["he"]})',
        'th': f'Thai ({ns["th"]})',
        'vi': f'Vietnam ({ns["vi"]})',
        'ar': f'Arabia ({ns["ar"]})',
        'hi': f'Hindi ({ns["hi"]})',
        'el': f'Kreikka ({ns["el"]})',
        'ko': f'Korea ({ns["ko"]})',
        'pt': 'Portugali',
        'bn': f'Bengali ({ns["bn"]})',
        'pa': f'Punjabi ({ns["pa"]})',
        'fa': f'Persia ({ns["fa"]})',
        'sw': 'Kiswahili',
        'id': 'Indonesia',
        'pl': 'Puola',
        'nl': 'Hollanti',
        'sv': 'Ruotsi',
        'tr': f'Turkki ({ns["tr"]})',
        'hu': 'Unkari',
        'new': f'Nepal Bhasa ({ns["new"]})',
        'bo': f'Tiibetin kieli ({ns["bo"]})',
        'si': f'Sinhala ({ns["si"]})',
        'or': f'Odia ({ns["or"]})',
        'ta': f'Tamili ({ns["ta"]})',
        'hy': f'Armenia ({ns["hy"]})',
        'tl': 'Tagalog',
        'ka': f'Georgia ({ns["ka"]})',
        'am': f'Amhara ({ns["am"]})',
        'kn': f'Kannada ({ns["kn"]})',
        'yo': 'Joruba',
        'gu': f'Gujarati ({ns["gu"]})',
        'ha': 'Hausa',
        'jv': 'Jaava',
        'ur': f'Urdu ({ns["ur"]})',
        'te': f'Telugu ({ns["te"]})',
        'mr': f'Marathi ({ns["mr"]})',
        'la': 'Latina',
        'eu': 'Euskara',
        'fi': 'Suomi',
        'mn': 'Mongoli (Latin)',
        'tt': f'Tataari ({ns["tt"]})',
    }

    # =========== PARTIAL REPLACEMENTS ===========

    # Arabic (ar) - yo, gu, ha, jv, ur, te, mr
    t['ar'] = {
        'yo': 'يوروبا',
        'gu': f'الغوجاراتية ({ns["gu"]})',
        'ha': 'الهوسا',
        'jv': 'الجاوية',
        'ur': f'الأردية ({ns["ur"]})',
        'te': f'التيلوغوية ({ns["te"]})',
        'mr': f'الماراثية ({ns["mr"]})',
        'la': 'اللاتينية',
        'eu': 'Euskara',
        'fi': 'الفنلندية',
        'mn': 'المنغولية (Latin)',
        'tt': f'التترية ({ns["tt"]})',
    }

    # Bengali (bn)
    t['bn'] = {
        'yo': 'ইয়োরুবা',
        'gu': f'গুজরাটি ({ns["gu"]})',
        'ha': 'হাউসা',
        'jv': 'জাভানিজ',
        'ur': f'উর্দু ({ns["ur"]})',
        'te': f'তেলুগু ({ns["te"]})',
        'mr': f'মারাঠি ({ns["mr"]})',
        'la': 'লাটিন',
        'eu': 'Euskara',
        'fi': 'ফিনিশ',
        'mn': 'মঙ্গোলীয় (Latin)',
        'tt': f'তাতার ({ns["tt"]})',
    }

    # Greek (el)
    t['el'] = {
        'yo': 'Γιορούμπα',
        'gu': f'Γκουτζαράτι ({ns["gu"]})',
        'ha': 'Χάουσα',
        'jv': 'Ιαβανικά',
        'ur': f'Ουρντού ({ns["ur"]})',
        'te': f'Τελούγκου ({ns["te"]})',
        'mr': f'Μαράθι ({ns["mr"]})',
        'la': 'Λατινικά',
        'eu': 'Euskara',
        'fi': 'Φινλανδικά',
        'mn': 'Μογγολική (Latin)',
        'tt': f'Ταταρικά ({ns["tt"]})',
    }

    # Persian (fa)
    t['fa'] = {
        'yo': 'یوروبایی',
        'gu': f'گجراتی ({ns["gu"]})',
        'ha': 'هوسایی',
        'jv': 'جاوایی',
        'ur': f'اردو ({ns["ur"]})',
        'te': f'تلوگویی ({ns["te"]})',
        'mr': f'مراتی ({ns["mr"]})',
        'la': 'لاتین',
        'eu': 'Euskara',
        'fi': 'فنلاندی',
        'mn': 'مغولی (Latin)',
        'tt': f'تاتاری ({ns["tt"]})',
    }

    # Hebrew (he)
    t['he'] = {
        'yo': 'יורובה',
        'gu': f'גוג\'ראטית ({ns["gu"]})',
        'ha': 'האוסה',
        'jv': 'ג\'אווה',
        'ur': f'אורדו ({ns["ur"]})',
        'te': f'טלוגו ({ns["te"]})',
        'mr': f'מראתית ({ns["mr"]})',
        'la': 'לטינית',
        'eu': 'Euskara',
        'fi': 'פינית',
        'mn': 'מונגולית (Latin)',
        'tt': f'טטרית ({ns["tt"]})',
    }

    # Hindi (hi)
    t['hi'] = {
        'yo': 'योरूबा',
        'gu': f'गुजराती ({ns["gu"]})',
        'ha': 'हौसा',
        'jv': 'जावानी',
        'ur': f'उर्दू ({ns["ur"]})',
        'te': f'तेलुगु ({ns["te"]})',
        'mr': f'मराठी ({ns["mr"]})',
        'la': 'लैटिन',
        'eu': 'Euskara',
        'fi': 'फ़िनिश',
        'mn': 'मंगोलियाई (Latin)',
        'tt': f'तातार ({ns["tt"]})',
    }

    # Japanese (ja)
    t['ja'] = {
        'yo': 'ヨルバ語',
        'gu': f'グジャラート語 ({ns["gu"]})',
        'ha': 'ハウサ語',
        'jv': 'ジャワ語',
        'ur': f'ウルドゥー語 ({ns["ur"]})',
        'te': f'テルグ語 ({ns["te"]})',
        'mr': f'マラーティー語 ({ns["mr"]})',
        'la': 'ラテン語',
        'eu': 'バスク語',
        'fi': 'フィンランド語',
        'mn': 'モンゴル語 (Latin)',
        'tt': f'タタール語 ({ns["tt"]})',
    }

    # Korean (ko)
    t['ko'] = {
        'yo': '요루바어',
        'gu': f'구자라트어 ({ns["gu"]})',
        'ha': '하우사어',
        'jv': '자바어',
        'ur': f'우르두어 ({ns["ur"]})',
        'te': f'텔루구어 ({ns["te"]})',
        'mr': f'마라티어 ({ns["mr"]})',
        'la': '라틴어',
        'eu': '바스크어',
        'fi': '핀란드어',
        'mn': '몽골어 (Latin)',
        'tt': f'타타르어 ({ns["tt"]})',
    }

    # Dutch (nl) - also fix en and pl
    t['nl'] = {
        'en': 'Engels',
        'pl': 'Pools',
        'yo': 'Yoruba',
        'gu': f'Gujarati ({ns["gu"]})',
        'ha': 'Hausa',
        'jv': 'Javaans',
        'ur': f'Urdu ({ns["ur"]})',
        'te': f'Telugu ({ns["te"]})',
        'mr': f'Marathi ({ns["mr"]})',
        'la': 'Latijn',
        'eu': 'Baskisch',
        'fi': 'Fins',
        'mn': 'Mongools (Latin)',
        'tt': f'Tataars ({ns["tt"]})',
    }

    # Odia (or)
    t['or'] = {
        'yo': 'ଯୋରୁବା',
        'gu': f'ଗୁଜ\u0b30ାଟି ({ns["gu"]})',
        'ha': 'ହୌସା',
        'jv': 'ଜାଭାନୀଜ',
        'ur': f'ଉର\u0b4d\u0b26\u0b41 ({ns["ur"]})',
        'te': f'ତେଲୁଗୁ ({ns["te"]})',
        'mr': f'ମ\u0b30ାଠି ({ns["mr"]})',
        'la': 'ଲାଟିନ',
        'eu': 'Euskara',
        'fi': 'ଫିନ୍ନିଶ',
        'mn': 'ମଙ୍ଗୋଲୀୟ (Latin)',
        'tt': f'ତାଟାର ({ns["tt"]})',
    }

    # Punjabi (pa)
    t['pa'] = {
        'yo': 'ਯੋਰੂਬਾ',
        'gu': f'ਗੁਜਰਾਤੀ ({ns["gu"]})',
        'ha': 'ਹੌਸਾ',
        'jv': 'ਜਾਵਾਨੀ',
        'ur': f'ਉਰਦੂ ({ns["ur"]})',
        'te': f'ਤੇਲਗੂ ({ns["te"]})',
        'mr': f'ਮਰਾਠੀ ({ns["mr"]})',
        'la': 'ਲੈਟਿਨ',
        'eu': 'Euskara',
        'fi': 'ਫਿਨਿਸ਼',
        'mn': 'ਮੰਗੋਲੀਅਨ (Latin)',
        'tt': f'ਤਾਤਾਰੀ ({ns["tt"]})',
    }

    # Russian (ru)
    t['ru'] = {
        'yo': 'Йоруба',
        'gu': f'Гуджарати ({ns["gu"]})',
        'ha': 'Хауса',
        'jv': 'Яванский',
        'ur': f'Урду ({ns["ur"]})',
        'te': f'Телугу ({ns["te"]})',
        'mr': f'Маратхи ({ns["mr"]})',
        'la': 'Латинский',
        'eu': 'Баскский',
        'fi': 'Финский',
        'mn': 'Монгольский (Latin)',
        'tt': f'Татарский ({ns["tt"]})',
    }

    # Sinhala (si)
    t['si'] = {
        'yo': 'යොරුබා',
        'gu': f'ගුජරාති ({ns["gu"]})',
        'ha': 'හවුසා',
        'jv': 'ජාවානීස්',
        'ur': f'උර්දු ({ns["ur"]})',
        'te': f'තෙලිඟු ({ns["te"]})',
        'mr': f'මරාති ({ns["mr"]})',
        'la': 'ලතින්',
        'eu': 'Euskara',
        'fi': 'ෆින්නිෂ්',
        'mn': 'මොංගෝලියානු (Latin)',
        'tt': f'ටාටාර් ({ns["tt"]})',
    }

    # Tamil (ta)
    t['ta'] = {
        'yo': 'யோரூபா',
        'gu': f'குஜராத்தி ({ns["gu"]})',
        'ha': 'ஹவுசா',
        'jv': 'ஜாவானீஸ்',
        'ur': f'உருது ({ns["ur"]})',
        'te': f'தெலுங்கு ({ns["te"]})',
        'mr': f'மராத்தி ({ns["mr"]})',
        'la': 'லத்தீன்',
        'eu': 'Euskara',
        'fi': 'பின்னிஷ்',
        'mn': 'மங்கோலியன் (Latin)',
        'tt': f'தாதர் ({ns["tt"]})',
    }

    # Thai (th)
    t['th'] = {
        'yo': 'ยอรูบา',
        'gu': f'คุชราต ({ns["gu"]})',
        'ha': 'เฮาซา',
        'jv': 'ชวา',
        'ur': f'อูรดู ({ns["ur"]})',
        'te': f'เตลูกู ({ns["te"]})',
        'mr': f'มราฐี ({ns["mr"]})',
        'la': 'ภาษาละติน',
        'eu': 'Euskara',
        'fi': 'ฟินแลนด์',
        'mn': 'ภาษามองโกเลีย (Latin)',
        'tt': f'ภาษาตาตาร์ ({ns["tt"]})',
    }

    # Vietnamese (vi)
    t['vi'] = {
        'yo': 'Tiếng Yoruba',
        'gu': f'Tiếng Gujarati ({ns["gu"]})',
        'ha': 'Tiếng Hausa',
        'jv': 'Tiếng Java',
        'ur': f'Tiếng Urdu ({ns["ur"]})',
        'te': f'Tiếng Telugu ({ns["te"]})',
        'mr': f'Tiếng Marathi ({ns["mr"]})',
        'la': 'Tiếng La-tinh',
        'eu': 'Tiếng Basque',
        'fi': 'Tiếng Phần Lan',
        'mn': 'Tiếng Mông Cổ (Latin)',
        'tt': f'Tiếng Tatar ({ns["tt"]})',
    }

    # Chinese (zh)
    t['zh'] = {
        'yo': '约鲁巴语',
        'gu': f'古吉拉特语 ({ns["gu"]})',
        'ha': '豪萨语',
        'jv': '爪哇语',
        'ur': f'乌尔都语 ({ns["ur"]})',
        'te': f'泰卢固语 ({ns["te"]})',
        'mr': f'马拉地语 ({ns["mr"]})',
        'la': '拉丁语',
        'eu': '巴斯克语',
        'fi': '芬兰语',
        'mn': '蒙古语 (Latin)',
        'tt': f'鞑靼语 ({ns["tt"]})',
    }

    # Urdu (ur) - only te and mr
    t['ur'] = {
        'te': f'تیلگو ({ns["te"]})',
        'mr': f'مراٹھی ({ns["mr"]})',
        'la': f'لاطینی',
        'eu': 'Euskara',
        'fi': 'فنلش',
        'mn': 'منگولی (Latin)',
        'tt': f'تاتاری ({ns["tt"]})',
    }

    # Armenian (hy) - tl, ka, am, kn, yo, gu, ha, jv, ur, te, mr
    # Armenian Unicode constants
    t['hy'] = {
        'tl': '\u0539\u0561\u0563\u0561\u056c\u0578\u0563\u0565\u0580\u0565\u0576',  # Թagalogérén
        'ka': f'\u054e\u0580\u0561\u057d\u057f\u0565\u0580\u0565\u0576 ({ns["ka"]})',  # Vrastérén
        'am': f'\u0531\u0574\u0570\u0561\u0580\u0565\u0580\u0565\u0576 ({ns["am"]})',  # Amharérén
        'kn': f'\u053f\u0561\u0576\u0576\u0561\u0564\u0565\u0580\u0565\u0576 ({ns["kn"]})',  # Kannadérén
        'yo': 'Yoruba',
        'gu': f'\u0533\u0578\u0582\u057b\u0561\u057c\u0561\u057f\u0565\u0580\u0565\u0576 ({ns["gu"]})',  # Gudzharatérén
        'ha': 'Hausa',
        'jv': '\u0545\u0561\u057e\u0561\u0576\u0565\u0580\u0565\u0576',  # Yavanerén
        'ur': f'Urdu ({ns["ur"]})',
        'te': f'\u054f\u0565\u056c\u0578\u0582\u0563\u0565\u0580\u0565\u0576 ({ns["te"]})',  # Telugérén
        'mr': f'\u0544\u0561\u0580\u0561\u057f\u0565\u0580\u0565\u0576 ({ns["mr"]})',  # Maratérén
        'la': 'Լատիներեն',
        'eu': 'Euskara',
        'fi': 'Ֆիննական',
        'mn': 'Մոնղոլ (Latin)',
        'tt': f'Թաթարերեն ({ns["tt"]})',
    }

    # German (de)
    t['de'] = {
        'gu': f'Gujaratisch ({ns["gu"]})',
        'jv': 'Javanisch',
        'la': 'Lateinisch',
        'eu': 'Baskisch',
        'fi': 'Finnisch',
        'mn': 'Mongolisch (Latein)',
        'tt': f'Tatarisch ({ns["tt"]})',
    }

    # Spanish (es)
    t['es'] = {
        'gu': f'Gujaratí ({ns["gu"]})',
        'jv': 'Javanés',
        'mr': f'Maratí ({ns["mr"]})',
        'la': 'Latín',
        'eu': 'Euskera',
        'fi': 'Finés',
        'mn': 'Mongol (Latin)',
        'tt': f'Tártaro ({ns["tt"]})',
    }

    # French (fr)
    t['fr'] = {
        'ha': 'Haoussa',
        'jv': 'Javanais',
        'ur': f'Ourdou ({ns["ur"]})',
        'te': f'Télougou ({ns["te"]})',
        'la': 'Latin',
        'eu': 'Basque',
        'fi': 'Finnois',
        'mn': 'Mongol (Latin)',
        'tt': f'Tatar ({ns["tt"]})',
    }

    # Hungarian (hu)
    t['hu'] = {
        'yo': 'Joruba',
        'gu': f'Gudzsaráti ({ns["gu"]})',
        'ha': 'Hausza',
        'jv': 'Jávai',
        'mr': f'Maráthi ({ns["mr"]})',
        'la': 'Latin',
        'eu': 'Baszk',
        'fi': 'Finn',
        'mn': 'Mongol (Latin)',
        'tt': f'Tatár ({ns["tt"]})',
    }

    # Italian (it)
    t['it'] = {
        'jv': 'Giavanése',
        'la': 'Latino',
        'eu': 'Basco',
        'fi': 'Finlandese',
        'mn': 'Mongolo (Latino)',
        'tt': f'Tataro ({ns["tt"]})',
    }

    # Javanese (jv) - minimal changes needed
    t['jv'] = {
        'eu': 'Euskara',
        'fi': 'Finlandia',
        'mn': 'Mongol (Latin)',
        'tt': f'Tatar ({ns["tt"]})',
    }

    # Newari (new) - no reliable translations available for newly missing entries
    t['new'] = {}

    # Tibetan (bo) - no reliable translations available
    t['bo'] = {}

    # Polish (pl)
    t['pl'] = {
        'yo': 'Joruba',
        'gu': f'Gudżarati ({ns["gu"]})',
        'jv': 'Jawajski',
        'la': 'Latin',
        'eu': 'Baskijski',
        'fi': 'Fiński',
        'mn': 'Mongolski (Latin)',
        'tt': f'Tatar ({ns["tt"]})',
    }

    # Portuguese (pt)
    t['pt'] = {
        'jv': 'Javanês',
        'la': 'Latim',
        'eu': 'Basco',
        'fi': 'Finlandês',
        'mn': 'Mongol (Latim)',
        'tt': f'ཐ་ཐར་སྐད་ ({ns["tt"]})',
    }

    # Swedish (sv)
    t['sv'] = {
        'jv': 'Javanesiska',
        'la': 'Latin',
        'eu': 'Euskara',
        'fi': 'Finska',
        'mn': 'Mongoliska (Latin)',
        'tt': f'Tatarski ({ns["tt"]})',
    }

    # Swahili (sw) - Ki- prefix pattern
    t['sw'] = {
        'yo': 'Kiyoruba',
        'gu': f'Kigujarati ({ns["gu"]})',
        'ha': 'Kihausa',
        'jv': 'Kijawa',
        'ur': f'Kiurdu ({ns["ur"]})',
        'te': f'Kitelugu ({ns["te"]})',
        'mr': f'Kimarathi ({ns["mr"]})',
        'la': 'Kilatini',
        'eu': 'Kibaski',
        'fi': 'Kifini',
        'mn': 'Kimongolia (Latin)',
        'tt': f'Tártaro ({ns["tt"]})',
    }

    # Turkish (tr)
    t['tr'] = {
        'gu': f'Gujaratça ({ns["gu"]})',
        'jv': 'Yavanice',
        'ur': f'Urduca ({ns["ur"]})',
        'te': f'Teluguca ({ns["te"]})',
        'la': 'Latince',
        'eu': 'Baskça',
        'fi': 'Fince',
        'mn': 'Moğolca (Latin)',
        'tt': f'Tatarca ({ns["tt"]})',
    }

    # Indonesian (id) - existing entries are acceptable Indonesian forms
    t['id'] = {
        'eu': 'Basque',
        'fi': 'Finlandia',
        'mn': 'Mongol (Latin)',
        'tt': f'Tatar ({ns["tt"]})',
    }

    # Basque (eu)
    t['eu'] = {
        'fi': 'Finlandiera',
        'mn': 'Mongoliera (Latin)',
        'tt': f'Tatariera ({ns["tt"]})',
    }

    # Mongolian Latin (mn) - full translations of all language names in Mongolian Latin
    t['mn'] = {
        'en': 'Angli',
        'es': 'Ispani',
        'de': 'German',
        'fr': 'Frants',
        'ja': f'Yapon ({ns["ja"]})',
        'it': 'Itali',
        'ru': f'Oros ({ns["ru"]})',
        'zh': f'Khyatad ({ns["zh"]})',
        'he': f'Evrei ({ns["he"]})',
        'th': f'Tailand ({ns["th"]})',
        'vi': f'Vyetnam ({ns["vi"]})',
        'ar': f'Arabi ({ns["ar"]})',
        'hi': f'Khindi ({ns["hi"]})',
        'el': f'Grek ({ns["el"]})',
        'ko': f'Solongos ({ns["ko"]})',
        'pt': 'Portugali',
        'bn': f'Bengali ({ns["bn"]})',
        'pa': f'Punjabi ({ns["pa"]})',
        'fa': f'Persi ({ns["fa"]})',
        'sw': 'Kiswahili',
        'id': 'Indonezi',
        'pl': 'Polsh',
        'nl': 'Golland',
        'sv': 'Shved',
        'tr': f'Turk ({ns["tr"]})',
        'hu': 'Ungar',
        'new': f'Nepal Bhasa ({ns["new"]})',
        'bo': f'Lkhasa Tövd ({ns["bo"]})',
        'si': f'Singal ({ns["si"]})',
        'or': f'Odia ({ns["or"]})',
        'ta': f'Tamil ({ns["ta"]})',
        'hy': f'Armeni ({ns["hy"]})',
        'tl': 'Tagalog',
        'ka': f'Gurj ({ns["ka"]})',
        'am': f'Amkhar ({ns["am"]})',
        'kn': f'Kannada ({ns["kn"]})',
        'yo': 'Yoruba',
        'gu': f'Gujarati ({ns["gu"]})',
        'ha': 'Khaus',
        'jv': 'Javanese',
        'ur': f'Urdu ({ns["ur"]})',
        'te': f'Telugu ({ns["te"]})',
        'mr': f'Marati ({ns["mr"]})',
        'la': 'Latin',
        'eu': 'Euskara',
        'fi': 'Suomi',
        'mn': 'Mongol (Latin)',
        'tt': f'Tatar ({ns["tt"]})',
    }


    t['tt'] = {
        'en': 'Инглиз',
        'es': 'Испан',
        'de': 'Немец',
        'fr': 'Француз',
        'ja': f'Япон ({ns["ja"]})',
        'it': 'Итальян',
        'ru': f'Рус ({ns["ru"]})',
        'zh': f'Кытай ({ns["zh"]})',
        'he': f'Гыйбрәй ({ns["he"]})',
        'th': f'Тай ({ns["th"]})',
        'vi': f'Вьетнам ({ns["vi"]})',
        'ar': f'Гарәп ({ns["ar"]})',
        'hi': f'Хинди ({ns["hi"]})',
        'el': f'Грек ({ns["el"]})',
        'ko': f'Корей ({ns["ko"]})',
        'pt': 'Португаль',
        'bn': f'Бенгаль ({ns["bn"]})',
        'pa': f'Панджаби ({ns["pa"]})',
        'fa': f'Фарсы ({ns["fa"]})',
        'sw': 'Суахили',
        'id': 'Индонезиян',
        'pl': 'Поляк',
        'nl': 'Нидерланд',
        'sv': 'Швед',
        'tr': f'Төрек ({ns["tr"]})',
        'hu': 'Мадьяр',
        'new': f'Nepal Bhasa ({ns["new"]})',
        'bo': f'Лхаса Тибет ({ns["bo"]})',
        'si': f'Сингала ({ns["si"]})',
        'or': f'Одия ({ns["or"]})',
        'ta': f'Тамил ({ns["ta"]})',
        'hy': f'Әрмән ({ns["hy"]})',
        'tl': 'Тагалог',
        'ka': f'Грузин ({ns["ka"]})',
        'am': f'Амхар ({ns["am"]})',
        'kn': f'Каннада ({ns["kn"]})',
        'yo': 'Йоруба',
        'gu': f'Гуджарати ({ns["gu"]})',
        'ha': 'Хауса',
        'jv': 'Ява',
        'ur': f'Урду ({ns["ur"]})',
        'te': f'Телугу ({ns["te"]})',
        'mr': f'Маратхи ({ns["mr"]})',
        'la': 'Латин',
        'eu': 'Euskara',
        'fi': 'Suomi',
        'mn': 'Монгол (Latin)',
        'tt': 'Татарча',
    }

    return t


def build_footer_line(locale, translations):
    """Build the complete footer language line for a locale."""
    parts = []
    for lang in LANG_ORDER:
        href = '#' if lang == locale else get_href(lang)
        text = translations.get(lang, '')
        if not text:
            continue
        parts.append(f'<a href={href}>{text}</a>')
    return '&nbsp;|&nbsp; '.join(parts)


def update_footer_line(line, locale, replacements):
    """Update a footer line by replacing English entries with locale translations."""
    def replace_anchor(m):
        href = m.group(1)
        text = m.group(2)
        # Determine lang from href
        if href == '#':
            lang = locale
        elif href == 'index.html':
            lang = 'en'
        else:
            m2 = re.match(r'index-(\w+)\.html', href)
            lang = m2.group(1) if m2 else None
        if lang and lang in replacements:
            return f'<a href={href}>{replacements[lang]}</a>'
        return m.group(0)
    return re.sub(r'<a href=([^>]+)>([^<]+)</a>', replace_anchor, line)


def fix_kn_footer(content, kn_translations):
    """Fix the special case of kn file with split footer."""
    lines = content.split('\n')
    new_lines = []
    i = 0
    while i < len(lines):
        line = lines[i]
        # Find the broken line: has English link + copyright
        if re.search(r'<a href=index\.html>ಇಂಗ್ಲಿಷ್</a>', line) and '©' in line:
            # Extract copyright text
            m = re.search(r'©[^<]+', line)
            copyright_text = m.group(0).strip() if m else '© 2026 ಸೋಲಾರ್ ಅನಾಮ್ನೆಸಿಸ್. ಎಲ್ಲಾ ಹಕ್ಕುಗಳನ್ನು ಕಾಯ್ದಿರಿಸಲಾಗಿದೆ.'
            # Replace with just the copyright paragraph
            indent = re.match(r'\s*', line).group(0)
            new_lines.append(f'{indent}<p>{copyright_text}</p>')
            i += 1
            # Next should be space30 div - keep it
            if i < len(lines) and 'space30' in lines[i]:
                new_lines.append(lines[i])
                i += 1
            # Next line should be the rest of the languages (without English)
            if i < len(lines) and 'href=index-es.html' in lines[i]:
                # Build the complete footer line
                full_footer = build_footer_line('kn', kn_translations)
                new_lines.append(f'{indent}<p>{full_footer}</p>')
                i += 1  # skip the broken partial line
            continue
        new_lines.append(line)
        i += 1
    return '\n'.join(new_lines)


def process_file(locale, replacements, translations_for_full=None):
    """Process a single HTML file."""
    fn = os.path.join(WORKDIR, get_href(locale))
    if not os.path.exists(fn):
        print(f'  SKIP: {fn} not found')
        return

    with open(fn, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    if locale == 'kn':
        content = fix_kn_footer(content, translations_for_full)
    else:
        lines = content.split('\n')
        new_lines = []
        for line in lines:
            if ('href=index.html>' in line and
                    ('href=index-mr' in line or 'href=index-te' in line or
                     ('href=index-es' in line and '&nbsp;|&nbsp;' in line)) and
                    '&nbsp;|&nbsp;' in line):
                line = update_footer_line(line, locale, replacements)
            new_lines.append(line)
        content = '\n'.join(new_lines)

    if content != original:
        with open(fn, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'  Updated: {fn}')
    else:
        print(f'  No changes: {fn}')


def main():
    print('Extracting native scripts...')
    ns = extract_native_scripts()
    print(f'  Got {len(ns)} native scripts')

    print('Building translation table...')
    translations = build_translations(ns)

    # Files needing full replacement
    full_replace_locales = ['am', 'fi', 'gu', 'ha', 'ka', 'kn', 'la', 'mn', 'mr', 'te', 'tl', 'yo']
    # All other locales with partial replacements
    partial_locales = [
        'ar', 'bn', 'el', 'eu', 'fa', 'he', 'hi', 'ja', 'ko', 'nl', 'or', 'pa',
        'ru', 'si', 'ta', 'th', 'vi', 'zh', 'ur', 'hy',
        'de', 'es', 'fr', 'hu', 'id', 'it', 'jv', 'new', 'bo', 'pl', 'pt',
        'sv', 'sw', 'tr', 'tt',
    ]

    print('\nProcessing full-replacement files...')
    for locale in full_replace_locales:
        print(f'  {locale}:')
        if locale in translations:
            process_file(locale, translations[locale], translations[locale])

    print('\nProcessing partial-replacement files...')
    for locale in partial_locales:
        print(f'  {locale}:')
        replacements = translations.get(locale, {})
        if replacements:
            process_file(locale, replacements)
        else:
            print(f'    Skipped (no replacements defined)')

    print('\nDone!')


if __name__ == '__main__':
    main()
