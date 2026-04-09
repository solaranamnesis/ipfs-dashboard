#!/usr/bin/env python3
"""Fix footer language link translations in all index-*.html files."""

import re
import os

WORKDIR = os.path.dirname(os.path.abspath(__file__))

LANG_ORDER = [
    'en', 'es', 'de', 'fr', 'ja', 'it', 'ru', 'sr', 'bs', 'hr', 'uk', 'zh', 'he', 'th', 'vi', 'ar',
    'hi', 'el', 'ko', 'pt', 'bn', 'pa', 'fa', 'sw', 'id', 'pl', 'nl', 'sv',
    'tr', 'hu', 'new', 'bo', 'si', 'or', 'ta', 'hy', 'tl', 'ka', 'am', 'kn',
    'yo', 'ig', 'gu', 'ha', 'jv', 'ur', 'ps', 'te', 'mr', 'ml', 'la', 'eu', 'fi', 'mn', 'tt', 'kk', 'ky', 'cs', 'ro', 'ku', 'af', 'ca',
]

def get_href(lang):
    return 'index.html' if lang == 'en' else f'index-{lang}.html'


def extract_native_scripts():
    """Extract native self-link text from each language file.

    Looks for the footer language-switcher line (identified by multiple &nbsp;|&nbsp;
    separators) and extracts the text of the self-link (href=#).
    """
    ns = {}
    for lang in LANG_ORDER:
        fn = os.path.join(WORKDIR, get_href(lang))
        if not os.path.exists(fn):
            continue
        with open(fn, 'r', encoding='utf-8') as f:
            content = f.read()
        for line in content.split('\n'):
            if '&nbsp;|&nbsp;' in line and 'href=#>' in line and line.count('href=') >= 10:
                m = re.search(r'href=#>([^<]+)</a>', line)
                if m:
                    text = m.group(1)
                    paren_m = re.search(r'\((.+?)\)\s*$', text)
                    ns[lang] = paren_m.group(1) if paren_m else text
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
        'uk': 'युक्रेनियन (Українська)',
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
        'ml': 'मलयाळम (മലയാളം)',
        'la': 'लॅटिन',
        'eu': 'बास्क',
        'fi': 'फिन्निश',
        'mn': 'मंगोलियन (Latin)',
        'tt': f'तातार ({ns["tt"]})',
        'kk': f'कझाक ({ns["kk"]})',
    }

    t['ml'] = {
        'en': 'ഇംഗ്ലീഷ്',
        'es': 'സ്പാനിഷ്',
        'de': 'ജർമ്മൻ',
        'fr': 'ഫ്രഞ്ച്',
        'ja': f'ജാപ്പനീസ് ({ns["ja"]})',
        'it': 'ഇറ്റാലിയൻ',
        'ru': f'റഷ്യൻ ({ns["ru"]})',
        'uk': 'Українська',
        'zh': f'ചൈനീസ് ({ns["zh"]})',
        'he': f'ഹീബ്രു ({ns["he"]})',
        'th': f'തായ് ({ns["th"]})',
        'vi': f'വിയറ്റ്നാമീസ് ({ns["vi"]})',
        'ar': f'അറബിക് ({ns["ar"]})',
        'hi': f'ഹിന്ദി ({ns["hi"]})',
        'el': f'ഗ്രീക്ക് ({ns["el"]})',
        'ko': f'കൊറിയൻ ({ns["ko"]})',
        'pt': 'പോർച്ചുഗീസ്',
        'bn': f'ബംഗാളി ({ns["bn"]})',
        'pa': f'പഞ്ചാബി ({ns["pa"]})',
        'fa': f'പേർഷ്യൻ ({ns["fa"]})',
        'sw': 'സ്വാഹിലി',
        'id': 'ഇന്തോനേഷ്യൻ',
        'pl': 'പോളിഷ്',
        'nl': 'ഡച്ച്',
        'sv': 'സ്വീഡിഷ്',
        'tr': f'തുർക്കിഷ് ({ns["tr"]})',
        'hu': 'ഹംഗേറിയൻ',
        'new': f'നെപ്പാൾ ഭാഷ ({ns["new"]})',
        'bo': f'ലാസ തിബറ്റിയൻ ({ns["bo"]})',
        'si': f'സിംഹള ({ns["si"]})',
        'or': f'ഒഡിയ ({ns["or"]})',
        'ta': f'തമിഴ് ({ns["ta"]})',
        'hy': f'അർമേനിയൻ ({ns["hy"]})',
        'tl': 'തഗലോഗ്',
        'ka': f'ജോർജിയൻ ({ns["ka"]})',
        'am': f'അംഹാരിക് ({ns["am"]})',
        'kn': f'കന്നഡ ({ns["kn"]})',
        'yo': 'യോറുബ',
        'gu': f'ഗുജറാത്തി ({ns["gu"]})',
        'ha': 'ഹൗസ',
        'jv': 'ജാവ',
        'ur': f'ഉർദു ({ns["ur"]})',
        'te': f'തെലുഗു ({ns["te"]})',
        'mr': f'മറാഠി ({ns["mr"]})',
        'ml': 'മലയാളം',
        'la': 'Latina',
        'eu': 'Euskara',
        'fi': 'Suomi',
        'mn': 'Mongol (Latin)',
        'tt': f'Татарча ({ns["tt"]})',
        'kk': f'Қазақша ({ns["kk"]})',
    }

    t['gu'] = {
        'en': 'અંગ્રેજી',
        'es': 'સ્પેનિશ',
        'de': 'જર્મન',
        'fr': 'ફ્રેંચ',
        'ja': f'જાપાની ({ns["ja"]})',
        'it': 'ઇટાલિયન',
        'ru': f'રશિયન ({ns["ru"]})',
        'uk': 'યુક્રેનિયન (Українська)',
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
        'ml': 'મlayalam (മlayalamml)',
        'la': 'લૅટિન',
        'eu': 'Euskara',
        'fi': 'ફિનિश',
        'mn': 'મોંગોલિયન (Latin)',
        'tt': f'તતાર ({ns["tt"]})',
        'kk': f'કઝાક ({ns["kk"]})',
    }

    t['ha'] = {
        'en': 'Turanci',
        'es': 'Sipeniyanci',
        'de': 'Jamusanci',
        'fr': 'Faransanci',
        'ja': f'Japananci ({ns["ja"]})',
        'it': 'Italiyanci',
        'ru': f'Rashanci ({ns["ru"]})',
        'uk': 'Yukreiniyanci',
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
        'ml': 'Maleyalam (മlayalamml)',
        'la': 'Latinci',
        'eu': 'Euskara',
        'fi': 'Faransancin Finnish',
        'mn': 'Mongoliyanci (Latin)',
        'tt': f'Tataranci ({ns["tt"]})',
        'kk': f'Kazakanci ({ns["kk"]})',
    }

    t['ka'] = {
        'en': 'ინგლისური',
        'es': 'ესპანური',
        'de': 'გერმანული',
        'fr': 'ფრანგული',
        'ja': f'იაპონური ({ns["ja"]})',
        'it': 'იტალიური',
        'ru': f'რუსული ({ns["ru"]})',
        'uk': 'უკრაინული (Українська)',
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
        'ml': 'მlayalam (മlayalamml)',
        'la': 'ლათინური',
        'eu': 'ბასკური',
        'fi': 'ფინური',
        'mn': 'მონღოლური (Latin)',
        'tt': f'თათარული ({ns["tt"]})',
        'kk': f'ყაზახური ({ns["kk"]})',
    }

    t['am'] = {
        'en': 'እንግሊዝኛ',
        'es': 'ስፓኒሽ',
        'de': 'ጀርመንኛ',
        'fr': 'ፈረንሳይኛ',
        'ja': f'ጃፓንኛ ({ns["ja"]})',
        'it': 'ኢጣሊያኛ',
        'ru': f'ሩሲያኛ ({ns["ru"]})',
        'uk': 'ዩክሬናዊ',
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
        'ml': 'ማላያላምኛ (മlayalamml)',
        'la': 'ላቲን',
        'eu': 'Euskara',
        'fi': 'ፊኒሽ',
        'mn': 'ሞንጎሊያኛ (Latin)',
        'tt': f'ታታርኛ ({ns["tt"]})',
        'kk': f'ካዛክኛ ({ns["kk"]})',
    }

    t['kn'] = {
        'en': 'ಇಂಗ್ಲಿಷ್',
        'es': 'ಸ್ಪ್ಯಾನಿಷ್',
        'de': 'ಜರ್ಮನ್',
        'fr': 'ಫ್ರೆಂಚ್',
        'ja': f'ಜಾಪನೀಸ್ ({ns["ja"]})',
        'it': 'ಇಟಾಲಿಯನ್',
        'ru': f'ರಷ್ಯನ್ ({ns["ru"]})',
        'sr': 'Serbian (Српски)',
        'uk': 'ಉಕ್ರೇನಿಯನ್ (Українська)',
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
        'ml': 'ಮlayalam (മlayalamml)',
        'la': 'ಲ್ಯಾಟಿನ್',
        'eu': 'ಬಾಸ್ಕ್',
        'fi': 'ಫಿನ್ನಿಶ್',
        'mn': 'ಮಂಗೋಲಿಯನ್ (Latin)',
        'tt': f'ತಾತರ್ ({ns["tt"]})',
        'kk': f'ಕಜಾಕ್ ({ns["kk"]})',
    }

    t['te'] = {
        'en': 'ఇంగ్లీష్',
        'es': 'స్పానిష్',
        'de': 'జర్మన్',
        'fr': 'ఫ్రెంచ్',
        'ja': f'జపనీస్ ({ns["ja"]})',
        'it': 'ఇటాలియన్',
        'ru': f'రష్యన్ ({ns["ru"]})',
        'uk': 'ఉక్రేనియన్ (Українська)',
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
        'ml': 'మlayalam (മlayalamml)',
        'la': 'లాటిన్',
        'eu': 'Euskara',
        'fi': 'ఫిన్నిష్',
        'mn': 'మంగోలియన్ (Latin)',
        'tt': f'తాటర్ ({ns["tt"]})',
        'kk': f'కజఖ్ ({ns["kk"]})',
    }

    t['tl'] = {
        'en': 'Ingles',
        'es': 'Espanyol',
        'de': 'Aleman',
        'fr': 'Pranses',
        'ja': f'Hapon ({ns["ja"]})',
        'it': 'Italyano',
        'ru': f'Ruso ({ns["ru"]})',
        'uk': 'Ukranyano',
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
        'ml': 'Malayalam (മlayalamml)',
        'la': 'Latin',
        'eu': 'Euskara',
        'fi': 'Finlandes',
        'mn': 'Mongolian (Latin)',
        'tt': f'Tatar ({ns["tt"]})',
        'kk': f'Kazakh ({ns["kk"]})',
    }

    t['yo'] = {
        'en': 'Èdè Gẹ̀ẹ́sì',
        'es': 'Èdè Sípáánì',
        'de': 'Èdè Jámánì',
        'fr': 'Èdè Fárándì',
        'ja': f'Èdè Japánì ({ns["ja"]})',
        'it': 'Èdè Ítálì',
        'ru': f'Èdè Rọ́ṣíà ({ns["ru"]})',
        'uk': 'Yukirenia',
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
        'ml': f'Èdè Malayalam ({ns["ml"]})',
        'la': 'Èdè Látìnì',
        'eu': 'Euskara',
        'fi': 'Èdè Finnish',
        'mn': 'Mongólíà (Latin)',
        'tt': f'Tatar ({ns["tt"]})',
        'kk': f'Kazakh ({ns["kk"]})',
    }

    t['ig'] = {
        'en': 'Bekee',
        'es': 'Spain',
        'de': 'Jamani',
        'fr': 'France',
        'ja': f'Japan ({ns["ja"]})',
        'it': 'Italy',
        'ru': f'Russia ({ns["ru"]})',
        'sr': 'Srpski',
        'bs': 'Bosanski',
        'hr': 'Hrvatski',
        'uk': f'Ukrenian ({ns["uk"]})',
        'zh': f'China ({ns["zh"]})',
        'he': f'Hebrew ({ns["he"]})',
        'th': f'Thai ({ns["th"]})',
        'vi': f'Vietnam ({ns["vi"]})',
        'ar': f'Arab ({ns["ar"]})',
        'hi': f'Hindi ({ns["hi"]})',
        'el': f'Greece ({ns["el"]})',
        'ko': f'Korea ({ns["ko"]})',
        'pt': 'Portugal',
        'bn': f'Bengali ({ns["bn"]})',
        'pa': f'Punjabi ({ns["pa"]})',
        'fa': f'Persian ({ns["fa"]})',
        'sw': 'Swahili',
        'id': 'Indonesia',
        'pl': 'Poland',
        'nl': 'Netherlands',
        'sv': 'Sweden',
        'tr': f'Turkey ({ns["tr"]})',
        'hu': 'Hungary',
        'new': f'Nepal Bhasa ({ns["new"]})',
        'bo': f'Lhasa Tibetan ({ns["bo"]})',
        'si': f'Sinhala ({ns["si"]})',
        'or': f'Odia ({ns["or"]})',
        'ta': f'Tamil ({ns["ta"]})',
        'hy': f'Armenian ({ns["hy"]})',
        'tl': 'Tagalog',
        'ka': f'Georgia ({ns["ka"]})',
        'am': f'Amharic ({ns["am"]})',
        'kn': f'Kannada ({ns["kn"]})',
        'yo': 'Yoruba',
        'ig': 'Igbo',
        'gu': f'Gujarati ({ns["gu"]})',
        'ha': 'Hausa',
        'jv': 'Java',
        'ur': f'Urdu ({ns["ur"]})',
        'ps': 'پښتو',
        'te': f'Telugu ({ns["te"]})',
        'mr': f'Marathi ({ns["mr"]})',
        'ml': f'Malayalam ({ns["ml"]})',
        'la': 'Latin',
        'eu': 'Euskara',
        'fi': 'Finnish',
        'mn': 'Mongolian (Latin)',
        'tt': f'Tatar ({ns["tt"]})',
        'kk': f'Kazakh ({ns["kk"]})',
        'ky': f'Kyrgyz ({ns["ky"]})',
        'cs': 'Czech',
        'ro': 'Romanian',
        'ku': f'Kurdish ({ns["ku"]})',
    }

    t['la'] = {
        'en': 'Anglice',
        'es': 'Hispanice',
        'de': 'Germanice',
        'fr': 'Gallice',
        'ja': f'Iaponice ({ns["ja"]})',
        'it': 'Italice',
        'ru': f'Russice ({ns["ru"]})',
        'uk': 'Ucrainicus',
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
        'ml': 'Malaialum (മlayalamml)',
        'la': 'Latina',
        'eu': 'Euskara',
        'fi': 'Finnice',
        'mn': 'Mongolica (Latina)',
        'tt': f'Lingua Tatarica ({ns["tt"]})',
        'kk': f'Lingua Kazachica ({ns["kk"]})',
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
        'uk': 'Ukraina',
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
        'ml': 'Malajalam (മlayalamml)',
        'la': 'Latina',
        'eu': 'Euskara',
        'fi': 'Suomi',
        'mn': 'Mongoli (Latin)',
        'tt': f'Tataari ({ns["tt"]})',
        'kk': f'Kazakki ({ns["kk"]})',
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
        'ml': 'الملايالامية (മlayalamml)',
        'la': 'اللاتينية',
        'eu': 'Euskara',
        'fi': 'الفنلندية',
        'mn': 'المنغولية (Latin)',
        'tt': f'التترية ({ns["tt"]})',
        'kk': f'الكازاخية ({ns["kk"]})',
        'uk': 'الأوكرانية (Українська)',
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
        'ml': 'মালায়ালম (മlayalamml)',
        'la': 'লাটিন',
        'eu': 'Euskara',
        'fi': 'ফিনিশ',
        'mn': 'মঙ্গোলীয় (Latin)',
        'tt': f'তাতার ({ns["tt"]})',
        'kk': f'কাজাখ ({ns["kk"]})',
        'uk': 'ইউক্রেনীয় (Українська)',
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
        'ml': 'Μαλαγιαλάμ (മlayalamml)',
        'la': 'Λατινικά',
        'eu': 'Euskara',
        'fi': 'Φινλανδικά',
        'mn': 'Μογγολική (Latin)',
        'tt': f'Ταταρικά ({ns["tt"]})',
        'kk': f'Καζακικά ({ns["kk"]})',
        'uk': 'Ουκρανικά (Українська)',
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
        'ml': 'مالایالامی (മlayalamml)',
        'la': 'لاتین',
        'eu': 'Euskara',
        'fi': 'فنلاندی',
        'mn': 'مغولی (Latin)',
        'tt': f'تاتاری ({ns["tt"]})',
        'kk': f'قزاقی ({ns["kk"]})',
        'uk': 'اوکراینی (Українська)',
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
        'ml': 'מלאיאלם (മlayalamml)',
        'la': 'לטינית',
        'eu': 'Euskara',
        'fi': 'פינית',
        'mn': 'מונגולית (Latin)',
        'tt': f'טטרית ({ns["tt"]})',
        'kk': f'קזחית ({ns["kk"]})',
        'uk': 'אוקראינית (Українська)',
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
        'ml': 'मलयालम (മlayalamml)',
        'la': 'लैटिन',
        'eu': 'Euskara',
        'fi': 'फ़िनिश',
        'mn': 'मंगोलियाई (Latin)',
        'tt': f'तातार ({ns["tt"]})',
        'kk': f'कज़ाख़ ({ns["kk"]})',
        'uk': 'यूक्रेनी (Українська)',
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
        'ml': 'マラヤーラム語 (മlayalamml)',
        'la': 'ラテン語',
        'eu': 'バスク語',
        'fi': 'フィンランド語',
        'mn': 'モンゴル語 (Latin)',
        'tt': f'タタール語 ({ns["tt"]})',
        'kk': f'カザフ語 ({ns["kk"]})',
        'uk': 'ウクライナ語 (Українська)',
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
        'ml': '말라얄람어 (മlayalamml)',
        'la': '라틴어',
        'eu': '바스크어',
        'fi': '핀란드어',
        'mn': '몽골어 (Latin)',
        'tt': f'타타르어 ({ns["tt"]})',
        'kk': f'카자흐어 ({ns["kk"]})',
        'uk': '우크라이나어 (Українська)',
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
        'ml': 'Malayalam (മlayalamml)',
        'la': 'Latijn',
        'eu': 'Baskisch',
        'fi': 'Fins',
        'mn': 'Mongools (Latin)',
        'tt': f'Tataars ({ns["tt"]})',
        'kk': f'Kazachs ({ns["kk"]})',
        'uk': 'Oekraïens (Українська)',
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
        'ml': 'ଓlayalam (മlayalamml)',
        'la': 'ଲାଟିନ',
        'eu': 'Euskara',
        'fi': 'ଫିନ୍ନିଶ',
        'mn': 'ମଙ୍ଗୋଲୀୟ (Latin)',
        'tt': f'ତାଟାର ({ns["tt"]})',
        'kk': f'କଜାଖ ({ns["kk"]})',
        'uk': 'ୟୁକ୍ରେନୀ (Українська)',
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
        'ml': 'ਮlayalam (മlayalamml)',
        'la': 'ਲੈਟਿਨ',
        'eu': 'Euskara',
        'fi': 'ਫਿਨਿਸ਼',
        'mn': 'ਮੰਗੋਲੀਅਨ (Latin)',
        'tt': f'ਤਾਤਾਰੀ ({ns["tt"]})',
        'kk': f'ਕਜ਼ਾਖ਼ ({ns["kk"]})',
        'uk': 'ਯੂਕਰੇਨੀ (Українська)',
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
        'ml': 'Малаялам (മlayalamml)',
        'la': 'Латинский',
        'eu': 'Баскский',
        'fi': 'Финский',
        'mn': 'Монгольский (Latin)',
        'tt': f'Татарский ({ns["tt"]})',
        'kk': f'Казахский ({ns["kk"]})',
        'uk': 'Украинский (Українська)',
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
        'ml': 'mlelayalam (മlayalamml)',
        'la': 'ලතින්',
        'eu': 'Euskara',
        'fi': 'ෆින්නිෂ්',
        'mn': 'මොංගෝලියානු (Latin)',
        'tt': f'ටාටාර් ({ns["tt"]})',
        'kk': f'කසාඛ් ({ns["kk"]})',
        'uk': 'යුක්රේනියානු (Українська)',
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
        'ml': 'மlayalam (മlayalamml)',
        'la': 'லத்தீன்',
        'eu': 'Euskara',
        'fi': 'பின்னிஷ்',
        'mn': 'மங்கோலியன் (Latin)',
        'tt': f'தாதர் ({ns["tt"]})',
        'kk': f'கசாக் ({ns["kk"]})',
        'uk': 'உக்ரேனியன் (Українська)',
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
        'ml': 'มาลายาลัม (മlayalamml)',
        'la': 'ภาษาละติน',
        'eu': 'Euskara',
        'fi': 'ฟินแลนด์',
        'mn': 'ภาษามองโกเลีย (Latin)',
        'tt': f'ภาษาตาตาร์ ({ns["tt"]})',
        'kk': f'ภาษาคาซัค ({ns["kk"]})',
        'uk': 'ยูเครน (Українська)',
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
        'ml': 'Tiếng Malayalam (മlayalamml)',
        'la': 'Tiếng La-tinh',
        'eu': 'Tiếng Basque',
        'fi': 'Tiếng Phần Lan',
        'mn': 'Tiếng Mông Cổ (Latin)',
        'tt': f'Tiếng Tatar ({ns["tt"]})',
        'kk': f'Tiếng Kazakh ({ns["kk"]})',
        'uk': 'Tiếng Ukraine (Українська)',
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
        'ml': '马拉雅拉姆语 (മlayalamml)',
        'la': '拉丁语',
        'eu': '巴斯克语',
        'fi': '芬兰语',
        'mn': '蒙古语 (Latin)',
        'tt': f'鞑靼语 ({ns["tt"]})',
        'kk': f'哈萨克语 ({ns["kk"]})',
        'uk': '乌克兰语 (Українська)',
    }

    # Urdu (ur) - only te and mr
    t['ur'] = {
        'te': f'تیلگو ({ns["te"]})',
        'mr': f'مراٹھی ({ns["mr"]})',
        'ml': 'ملیالم (മlayalamml)',
        'la': f'لاطینی',
        'eu': 'Euskara',
        'fi': 'فنلش',
        'mn': 'منگولی (Latin)',
        'tt': f'تاتاری ({ns["tt"]})',
        'kk': f'قازاق ({ns["kk"]})',
        'uk': 'یوکرینی (Українська)',
    }

    # Pashto (ps) - full replacement
    t['ps'] = {
        'en': 'انګلیسي',
        'es': 'سپاینی',
        'de': 'جرمن',
        'fr': 'فرانسوي',
        'ja': f'جاپاني ({ns["ja"]})',
        'it': 'ایټالوی',
        'ru': f'روسي ({ns["ru"]})',
        'sr': 'سربیایي',
        'uk': 'اوکراینی (Українська)',
        'zh': f'چینی ({ns["zh"]})',
        'he': f'عبري ({ns["he"]})',
        'th': f'تایلنډي ({ns["th"]})',
        'vi': f'ویتنامي ({ns["vi"]})',
        'ar': f'عربي ({ns["ar"]})',
        'hi': f'هندي ({ns["hi"]})',
        'el': f'یوناني ({ns["el"]})',
        'ko': f'کوریایی ({ns["ko"]})',
        'pt': 'پرتګالی',
        'bn': f'بنګالي ({ns["bn"]})',
        'pa': f'پنجابي ({ns["pa"]})',
        'fa': f'فارسي ({ns["fa"]})',
        'sw': 'سواهیلي',
        'id': 'اندونیزیاوي',
        'pl': 'پولنډي',
        'nl': 'هالنډي',
        'sv': 'سویډني',
        'tr': f'ترکي ({ns["tr"]})',
        'hu': 'مجارستاني',
        'new': f'نیپال بهاسا ({ns["new"]})',
        'bo': f'لهاسا تیبتی ({ns["bo"]})',
        'si': f'سنهالي ({ns["si"]})',
        'or': f'اودی ({ns["or"]})',
        'ta': f'تامیل ({ns["ta"]})',
        'hy': f'ارمني ({ns["hy"]})',
        'tl': 'ټاګالوګ',
        'ka': f'ګرجستاني ({ns["ka"]})',
        'am': f'امهری ({ns["am"]})',
        'kn': f'کانناډا ({ns["kn"]})',
        'yo': 'یوروبه',
        'gu': f'ګجراتي ({ns["gu"]})',
        'ha': 'هاوسا',
        'jv': 'جاوا',
        'ur': f'اردو ({ns["ur"]})',
        'te': f'تلوګو ({ns["te"]})',
        'mr': f'ماراټي ({ns["mr"]})',
        'ml': 'مالایالام (മlayalamml)',
        'la': 'لاطیني',
        'eu': 'باسکي',
        'fi': 'فنلنډي',
        'mn': 'منګولي (Latin)',
        'tt': f'تاتاري ({ns["tt"]})',
        'kk': f'قزاقي ({ns["kk"]})',
        'ky': f'کرغیزي ({ns["ky"]})',
        'cs': 'چیکي',
        'ro': 'رومانیایی',
        'ku': 'کردي (Kurmancî)',
        'bs': 'Bosanski',
        'hr': 'Hrvatski',
        'ps': 'پښتو',
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
        'ml': 'Մalayalam (മlayalamml)',
        'la': 'Լատիներեն',
        'eu': 'Euskara',
        'fi': 'Ֆիննական',
        'mn': 'Մոնղոլ (Latin)',
        'tt': f'Թաթարերեն ({ns["tt"]})',
        'kk': f'Ղazakhstani ({ns["kk"]})',
        'uk': 'Ուկրաիներեն (Українська)',
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
        'kk': f'Kasachisch ({ns["kk"]})',
        'ml': 'Malayalam (മlayalamml)',
        'uk': 'Ukrainisch (Українська)',
    }

    # Spanish (es)
    t['es'] = {
        'gu': f'Gujaratí ({ns["gu"]})',
        'jv': 'Javanés',
        'mr': f'Maratí ({ns["mr"]})',
        'ml': 'Malayalam (മlayalamml)',
        'la': 'Latín',
        'eu': 'Euskera',
        'fi': 'Finés',
        'mn': 'Mongol (Latin)',
        'tt': f'Tártaro ({ns["tt"]})',
        'kk': f'Kazajo ({ns["kk"]})',
        'uk': 'Ucraniano (Українська)',
    }

    # French (fr)
    t['fr'] = {
        'ha': 'Haoussa',
        'jv': 'Javanais',
        'ur': f'Ourdou ({ns["ur"]})',
        'te': f'Télougou ({ns["te"]})',
        'ml': 'Malayalam (മlayalamml)',
        'la': 'Latin',
        'eu': 'Basque',
        'fi': 'Finnois',
        'mn': 'Mongol (Latin)',
        'tt': f'Tatar ({ns["tt"]})',
        'kk': f'Kazakh ({ns["kk"]})',
        'uk': 'Ukrainien (Українська)',
    }

    # Hungarian (hu)
    t['hu'] = {
        'yo': 'Joruba',
        'gu': f'Gudzsaráti ({ns["gu"]})',
        'ha': 'Hausza',
        'jv': 'Jávai',
        'mr': f'Maráthi ({ns["mr"]})',
        'ml': 'Malajálam (മlayalamml)',
        'la': 'Latin',
        'eu': 'Baszk',
        'fi': 'Finn',
        'mn': 'Mongol (Latin)',
        'tt': f'Tatár ({ns["tt"]})',
        'kk': f'Kazah ({ns["kk"]})',
        'uk': 'Ukrán (Українська)',
    }

    # Italian (it)
    t['it'] = {
        'ml': 'Malayalam (മlayalamml)',
        'jv': 'Giavanése',
        'la': 'Latino',
        'eu': 'Basco',
        'fi': 'Finlandese',
        'mn': 'Mongolo (Latino)',
        'tt': f'Tataro ({ns["tt"]})',
        'kk': f'Kazaco ({ns["kk"]})',
        'uk': 'Ucraino (Українська)',
    }

    # Javanese (jv) - minimal changes needed
    t['jv'] = {
        'ml': 'Malayalam (മlayalamml)',
        'eu': 'Euskara',
        'fi': 'Finlandia',
        'mn': 'Mongol (Latin)',
        'tt': f'Tatar ({ns["tt"]})',
        'kk': f'Kasak ({ns["kk"]})',
        'uk': 'Ukrania (Українська)',
    }

    # Newari (new) - no reliable translations available for newly missing entries
    t['new'] = {'uk': 'Українська', 'ml': 'Malayalam (മlayalamml)'}

    # Tibetan (bo) - no reliable translations available
    t['bo'] = {'uk': 'Українська', 'ml': 'Malayalam (മlayalamml)'}

    # Polish (pl)
    t['pl'] = {
        'yo': 'Joruba',
        'gu': f'Gudżarati ({ns["gu"]})',
        'jv': 'Jawajski',
        'ml': 'Malajalam (മlayalamml)',
        'la': 'Latin',
        'eu': 'Baskijski',
        'fi': 'Fiński',
        'mn': 'Mongolski (Latin)',
        'tt': f'Tatar ({ns["tt"]})',
        'kk': f'Kazachski ({ns["kk"]})',
        'uk': 'Українська',
    }

    # Portuguese (pt)
    t['pt'] = {
        'ml': 'Malayalam (മlayalamml)',
        'jv': 'Javanês',
        'la': 'Latim',
        'eu': 'Basco',
        'fi': 'Finlandês',
        'mn': 'Mongol (Latim)',
        'tt': f'ཐ་ཐར་སྐད་ ({ns["tt"]})',
        'kk': f'Cazaque ({ns["kk"]})',
        'uk': 'Ucraniano (Українська)',
    }

    # Swedish (sv)
    t['sv'] = {
        'ml': 'Malayalam (മlayalamml)',
        'jv': 'Javanesiska',
        'la': 'Latin',
        'eu': 'Euskara',
        'fi': 'Finska',
        'mn': 'Mongoliska (Latin)',
        'tt': f'Tatarski ({ns["tt"]})',
        'kk': f'Kazakiska ({ns["kk"]})',
        'uk': 'Ukrainska (Українська)',
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
        'ml': 'Kimalayalam (മlayalamml)',
        'la': 'Kilatini',
        'eu': 'Kibaski',
        'fi': 'Kifini',
        'mn': 'Kimongolia (Latin)',
        'tt': f'Tártaro ({ns["tt"]})',
        'kk': f'Kikazaki ({ns["kk"]})',
        'uk': 'Kiukrani (Українська)',
    }

    # Turkish (tr)
    t['tr'] = {
        'gu': f'Gujaratça ({ns["gu"]})',
        'jv': 'Yavanice',
        'ur': f'Urduca ({ns["ur"]})',
        'te': f'Teluguca ({ns["te"]})',
        'ml': 'Malayalamca (മlayalamml)',
        'la': 'Latince',
        'eu': 'Baskça',
        'fi': 'Fince',
        'mn': 'Moğolca (Latin)',
        'tt': f'Tatarca ({ns["tt"]})',
        'kk': f'Kazakça ({ns["kk"]})',
        'uk': 'Ukraynaca (Українська)',
    }

    # Indonesian (id) - existing entries are acceptable Indonesian forms
    t['id'] = {
        'ml': 'Malayalam (മlayalamml)',
        'eu': 'Basque',
        'fi': 'Finlandia',
        'mn': 'Mongol (Latin)',
        'tt': f'Tatar ({ns["tt"]})',
        'kk': f'Kazakh ({ns["kk"]})',
        'uk': 'Ukraina (Українська)',
    }

    # Basque (eu)
    t['eu'] = {
        'ml': 'Malayalamera (മlayalamml)',
        'fi': 'Finlandiera',
        'mn': 'Mongoliera (Latin)',
        'tt': f'Tatariera ({ns["tt"]})',
        'kk': f'Kazakhera ({ns["kk"]})',
        'uk': 'Ukrainera (Українська)',
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
        'uk': 'Ukraina (Українська)',
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
        'ml': 'Malajalam (മlayalamml)',
        'la': 'Latin',
        'eu': 'Euskara',
        'fi': 'Suomi',
        'mn': 'Mongol (Latin)',
        'tt': f'Tatar ({ns["tt"]})',
        'kk': f'Kazakh ({ns["kk"]})',
    }


    t['tt'] = {
        'en': 'Инглиз',
        'es': 'Испан',
        'de': 'Немец',
        'fr': 'Француз',
        'ja': f'Япон ({ns["ja"]})',
        'it': 'Итальян',
        'ru': f'Рус ({ns["ru"]})',
        'uk': 'Украин (Українська)',
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
        'ml': 'Малаялам (മlayalamml)',
        'la': 'Латин',
        'eu': 'Euskara',
        'fi': 'Suomi',
        'mn': 'Монгол (Latin)',
        'tt': 'Татарча',
        'kk': f'Қазақша ({ns["kk"]})',
    }

    t['kk'] = {
        'en': 'Ағылшынша',
        'es': 'Испанша',
        'de': 'Неміс',
        'fr': 'Француз',
        'ja': f'Жапон ({ns["ja"]})',
        'it': 'Итальян',
        'ru': f'Орысша ({ns["ru"]})',
        'uk': 'Украинша (Українська)',
        'zh': f'Қытайша ({ns["zh"]})',
        'he': f'Иврит ({ns["he"]})',
        'th': f'Тай ({ns["th"]})',
        'vi': f'Вьетнам ({ns["vi"]})',
        'ar': f'Арабша ({ns["ar"]})',
        'hi': f'Хинди ({ns["hi"]})',
        'el': f'Грекше ({ns["el"]})',
        'ko': f'Корей ({ns["ko"]})',
        'pt': 'Португалша',
        'bn': f'Бенгал ({ns["bn"]})',
        'pa': f'Пенджаб ({ns["pa"]})',
        'fa': f'Парсы ({ns["fa"]})',
        'sw': 'Суахили',
        'id': 'Индонезияша',
        'pl': 'Поляк',
        'nl': 'Нидерланд',
        'sv': 'Швед',
        'tr': f'Түрікше ({ns["tr"]})',
        'hu': 'Мажарша',
        'new': f'Nepal Bhasa ({ns["new"]})',
        'bo': f'Лхаса тибетше ({ns["bo"]})',
        'si': f'Сингалша ({ns["si"]})',
        'or': f'Одия ({ns["or"]})',
        'ta': f'Тамил ({ns["ta"]})',
        'hy': f'Армянша ({ns["hy"]})',
        'tl': 'Тагалог',
        'ka': f'Грузинше ({ns["ka"]})',
        'am': f'Амхарша ({ns["am"]})',
        'kn': f'Каннада ({ns["kn"]})',
        'yo': 'Йоруба',
        'gu': f'Гуджарати ({ns["gu"]})',
        'ha': 'Хауса',
        'jv': 'Яванша',
        'ur': f'Урду ({ns["ur"]})',
        'te': f'Телугу ({ns["te"]})',
        'mr': f'Маратхи ({ns["mr"]})',
        'ml': 'Малаялам (മlayalamml)',
        'la': 'Латын',
        'eu': 'Euskara',
        'fi': 'Suomi',
        'mn': 'Монғол (Latin)',
        'tt': f'Татарша ({ns["tt"]})',
        'kk': 'Қазақша',
    }

    # Ukrainian (uk) - full replacement
    t['uk'] = {
        'en': 'Англійська',
        'es': 'Іспанська',
        'de': 'Німецька',
        'fr': 'Французька',
        'ja': f'Японська ({ns["ja"]})',
        'it': 'Італійська',
        'ru': f'Російська ({ns["ru"]})',
        'uk': 'Українська',
        'zh': f'Китайська ({ns["zh"]})',
        'he': f'Іврит ({ns["he"]})',
        'th': f'Тайська ({ns["th"]})',
        'vi': f'В\'єтнамська ({ns["vi"]})',
        'ar': f'Арабська ({ns["ar"]})',
        'hi': f'Хінді ({ns["hi"]})',
        'el': f'Грецька ({ns["el"]})',
        'ko': f'Корейська ({ns["ko"]})',
        'pt': 'Португальська',
        'bn': f'Бенгальська ({ns["bn"]})',
        'pa': f'Панджабі ({ns["pa"]})',
        'fa': f'Перська ({ns["fa"]})',
        'sw': 'Суахілі',
        'id': 'Індонезійська',
        'pl': 'Польська',
        'nl': 'Нідерландська',
        'sv': 'Шведська',
        'tr': f'Турецька ({ns["tr"]})',
        'hu': 'Угорська',
        'new': f'Неварська ({ns["new"]})',
        'bo': f'Лхасський тибетський ({ns["bo"]})',
        'si': f'Сингальська ({ns["si"]})',
        'or': f'Одійська ({ns["or"]})',
        'ta': f'Тамільська ({ns["ta"]})',
        'hy': f'Вірменська ({ns["hy"]})',
        'tl': 'Тагальська',
        'ka': f'Грузинська ({ns["ka"]})',
        'am': f'Амхарська ({ns["am"]})',
        'kn': f'Каннада ({ns["kn"]})',
        'yo': 'Йоруба',
        'gu': f'Гуджараті ({ns["gu"]})',
        'ha': 'Хауса',
        'jv': 'Яванська',
        'ur': f'Урду ({ns["ur"]})',
        'te': f'Телугу ({ns["te"]})',
        'mr': f'Маратхі ({ns["mr"]})',
        'ml': 'Малаялам (മlayalamml)',
        'la': 'Латинська',
        'eu': 'Баскська',
        'fi': 'Фінська',
        'mn': 'Монгольська (Latin)',
        'tt': f'Татарська ({ns["tt"]})',
        'kk': f'Казахська ({ns["kk"]})',
        'ky': f'Киргизька ({ns["ky"]})',
    }

    # Kyrgyz (ky) - partial replacements for new entries
    t['ky'] = {
        'ml': 'Малаялам (മlayalamml)',
        'uk': 'Украинча (Українська)',
    }

    # Czech (cs) - partial replacements for new entries
    t['cs'] = {
        'ml': 'Malajálamština (മlayalamml)',
        'uk': 'Ukrainština (Українська)',
    }

    # Serbian (sr) - full replacement
    t['sr'] = {
        'en': 'Енглески',
        'es': 'Шпански',
        'de': 'Немачки',
        'fr': 'Француски',
        'ja': f'Јапански ({ns["ja"]})',
        'it': 'Италијански',
        'ru': f'Руски ({ns["ru"]})',
        'sr': 'Српски',
        'uk': 'Украјински (Українська)',
        'zh': f'Кинески ({ns["zh"]})',
        'he': f'Хебрејски ({ns["he"]})',
        'th': f'Тајски ({ns["th"]})',
        'vi': f'Вијетнамски ({ns["vi"]})',
        'ar': f'Арапски ({ns["ar"]})',
        'hi': f'Хинди ({ns["hi"]})',
        'el': f'Грчки ({ns["el"]})',
        'ko': f'Корејски ({ns["ko"]})',
        'pt': 'Португалски',
        'bn': f'Бенгалски ({ns["bn"]})',
        'pa': f'Панџаби ({ns["pa"]})',
        'fa': f'Персијски ({ns["fa"]})',
        'sw': 'Свахили',
        'id': 'Индонежански',
        'pl': 'Пољски',
        'nl': 'Холандски',
        'sv': 'Шведски',
        'tr': f'Турски ({ns["tr"]})',
        'hu': 'Мађарски',
        'new': f'Непал баса ({ns["new"]})',
        'bo': f'Ласа тибетски ({ns["bo"]})',
        'si': f'Синхалешки ({ns["si"]})',
        'or': f'Одија ({ns["or"]})',
        'ta': f'Тамилски ({ns["ta"]})',
        'hy': f'Јерменски ({ns["hy"]})',
        'tl': 'Тагалог',
        'ka': f'Грузијски ({ns["ka"]})',
        'am': f'Амхарски ({ns["am"]})',
        'kn': f'Канада ({ns["kn"]})',
        'yo': 'Јоруба',
        'gu': f'Гуџарати ({ns["gu"]})',
        'ha': 'Хауса',
        'jv': 'Јавански',
        'ur': f'Урду ({ns["ur"]})',
        'te': f'Телугу ({ns["te"]})',
        'mr': f'Марати ({ns["mr"]})',
        'ml': 'Малајалам (മlayalamml)',
        'la': 'Латински',
        'eu': 'Баскијски',
        'fi': 'Фински',
        'mn': 'Монголски (Latin)',
        'tt': f'Татарски ({ns["tt"]})',
        'kk': f'Казашки ({ns["kk"]})',
        'ky': f'Киргиски ({ns["ky"]})',
        'ro': 'Румунски',
    }

    t['hr'] = {
        'en': 'Engleski',
        'es': 'Španjolski',
        'de': 'Njemački',
        'fr': 'Francuski',
        'ja': f'Japanski ({ns["ja"]})',
        'it': 'Talijanski',
        'ru': f'Ruski ({ns["ru"]})',
        'sr': f'Srpski ({ns["sr"]})',
        'bs': 'Bosanski',
        'hr': 'Hrvatski',
        'uk': f'Ukrajinski ({ns["uk"]})',
        'zh': f'Kineski ({ns["zh"]})',
        'he': f'Hebrejski ({ns["he"]})',
        'th': f'Tajlandski ({ns["th"]})',
        'vi': f'Vijetnamski ({ns["vi"]})',
        'ar': f'Arapski ({ns["ar"]})',
        'hi': f'Hindi ({ns["hi"]})',
        'el': f'Grčki ({ns["el"]})',
        'ko': f'Korejski ({ns["ko"]})',
        'pt': 'Portugalski',
        'bn': f'Bengalski ({ns["bn"]})',
        'pa': f'Pandžabi ({ns["pa"]})',
        'fa': f'Perzijski ({ns["fa"]})',
        'sw': 'Svahili',
        'id': 'Indonežanski',
        'pl': 'Poljski',
        'nl': 'Nizozemski',
        'sv': 'Švedski',
        'tr': f'Turski ({ns["tr"]})',
        'hu': 'Mađarski',
        'new': f'Nepal Bhasa ({ns["new"]})',
        'bo': f'Lhasa Tibetski ({ns["bo"]})',
        'si': f'Singaleški ({ns["si"]})',
        'or': f'Odia ({ns["or"]})',
        'ta': f'Tamilski ({ns["ta"]})',
        'hy': f'Jermenski ({ns["hy"]})',
        'tl': 'Tagaloški',
        'ka': f'Gruzijski ({ns["ka"]})',
        'am': f'Amharski ({ns["am"]})',
        'kn': f'Kannada ({ns["kn"]})',
        'yo': 'Joruba',
        'gu': f'Gudžarati ({ns["gu"]})',
        'ha': 'Hausa',
        'jv': 'Javanski',
        'ur': f'Urdu ({ns["ur"]})',
        'te': f'Telugu ({ns["te"]})',
        'mr': f'Marati ({ns["mr"]})',
        'ml': f'Malajalam ({ns["ml"]})',
        'la': 'Latinski',
        'eu': 'Baskijski',
        'fi': 'Finski',
        'mn': 'Mongolski (Latinica)',
        'tt': f'Tatarski ({ns["tt"]})',
        'kk': f'Kazaški ({ns["kk"]})',
        'ky': f'Kirgiski ({ns["ky"]})',
        'cs': 'Češki',
        'ro': 'Rumunski',
        'ku': f'Kurdski ({ns["ku"]})',
    }

    t['af'] = {
        'en': 'Engels',
        'es': 'Spaans',
        'de': 'Duits',
        'fr': 'Frans',
        'ja': f'Japans ({ns["ja"]})',
        'it': 'Italiaans',
        'ru': f'Russies ({ns["ru"]})',
        'sr': f'Serwies ({ns["sr"]})',
        'bs': 'Bosnies',
        'hr': 'Kroaties',
        'uk': f'Oekraïens ({ns["uk"]})',
        'zh': f'Chinees ({ns["zh"]})',
        'he': f'Hebreeus ({ns["he"]})',
        'th': f'Thais ({ns["th"]})',
        'vi': f'Viëtnamees ({ns["vi"]})',
        'ar': f'Arabies ({ns["ar"]})',
        'hi': f'Hindi ({ns["hi"]})',
        'el': f'Grieks ({ns["el"]})',
        'ko': f'Koreaans ({ns["ko"]})',
        'pt': 'Portugees',
        'bn': f'Bengaals ({ns["bn"]})',
        'pa': f'Punjabi ({ns["pa"]})',
        'fa': f'Persies ({ns["fa"]})',
        'sw': 'Swahili',
        'id': 'Indonesies',
        'pl': 'Pools',
        'nl': 'Nederlands',
        'sv': 'Sweeds',
        'tr': f'Turks ({ns["tr"]})',
        'hu': 'Hongaars',
        'new': f'Nepal Bhasa ({ns["new"]})',
        'bo': f'Lhasa Tibettaans ({ns["bo"]})',
        'si': f'Sinhalees ({ns["si"]})',
        'or': f'Odia ({ns["or"]})',
        'ta': f'Tamil ({ns["ta"]})',
        'hy': f'Armeens ({ns["hy"]})',
        'tl': 'Tagalog',
        'ka': f'Georgies ({ns["ka"]})',
        'am': f'Amharies ({ns["am"]})',
        'kn': f'Kannada ({ns["kn"]})',
        'yo': 'Yoruba',
        'ig': 'Igbo',
        'gu': f'Gujarati ({ns["gu"]})',
        'ha': 'Hausa',
        'jv': 'Java',
        'ur': f'Urdu ({ns["ur"]})',
        'ps': f'Pashto ({ns["ps"]})',
        'te': f'Telugu ({ns["te"]})',
        'mr': f'Marathi ({ns["mr"]})',
        'ml': f'Malajaams ({ns["ml"]})',
        'la': 'Latyn',
        'eu': 'Baskies',
        'fi': 'Fins',
        'mn': 'Mongolies (Latin)',
        'tt': f'Tataars ({ns["tt"]})',
        'kk': f'Kazags ({ns["kk"]})',
        'ky': f'Kirgisies ({ns["ky"]})',
        'cs': 'Tsjeggies',
        'ro': 'Roemeen',
        'ku': f'Koerdies ({ns["ku"]})',
        'af': 'Afrikaans',
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


def get_source_footer_texts():
    """Read the English footer link texts from index.html as fallback labels."""
    fn = os.path.join(WORKDIR, 'index.html')
    with open(fn, 'r', encoding='utf-8') as f:
        content = f.read()
    texts = {}
    for line in content.split('\n'):
        if '&nbsp;|&nbsp;' in line and line.count('href=') >= 10:
            for m in re.finditer(r'<a href=([^>]+)>([^<]+)</a>', line):
                href, text = m.group(1), m.group(2)
                if href == '#':
                    texts['en'] = text
                else:
                    m2 = re.match(r'index-([^.]+)\.html', href)
                    if m2:
                        texts[m2.group(1)] = text
            break
    return texts


def ensure_footer_links(content, locale):
    """Insert any missing language links into the footer language-switcher line.

    Detects the footer line by looking for a <p> with many &nbsp;|&nbsp; separators.
    Any language in LANG_ORDER that is not yet present is inserted at the correct
    position using the English label from index.html as a placeholder; subsequent
    translation passes will replace the placeholder with the proper translated text.

    Returns the (possibly updated) content string.
    """
    lines = content.split('\n')
    idx = None
    for i, line in enumerate(lines):
        if '&nbsp;|&nbsp;' in line and '<a href=#>' in line and line.count('href=') >= 10:
            idx = i
            break
    if idx is None:
        return content

    line = lines[idx]

    # Parse existing anchors
    existing = {}
    for m in re.finditer(r'<a href=([^>]+)>([^<]+)</a>', line):
        href, text = m.group(1), m.group(2)
        if href == '#':
            existing[locale] = text
        elif href == 'index.html':
            existing['en'] = text
        else:
            m2 = re.match(r'index-([^.]+)\.html', href)
            if m2:
                existing[m2.group(1)] = text

    missing = [lang for lang in LANG_ORDER if lang != locale and lang not in existing]
    if not missing:
        return content

    source = get_source_footer_texts()
    for lang in missing:
        existing[lang] = source.get(lang, lang)

    # Rebuild the line in LANG_ORDER, preserving indentation
    indent = re.match(r'^\s*', line).group(0)
    parts = []
    for lang in LANG_ORDER:
        if lang not in existing and lang != locale:
            continue
        href = '#' if lang == locale else get_href(lang)
        text = existing.get(lang, '')
        if not text:
            continue
        parts.append(f'<a href={href}>{text}</a>')

    lines[idx] = indent + '<p>' + '&nbsp;|&nbsp; '.join(parts) + '</p>'
    return '\n'.join(lines)


def process_file(locale, replacements, translations_for_full=None):
    """Process a single HTML file."""
    fn = os.path.join(WORKDIR, get_href(locale))
    if not os.path.exists(fn):
        print(f'  SKIP: {fn} not found')
        return

    with open(fn, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # Ensure all expected language links are present before translating
    content = ensure_footer_links(content, locale)

    if locale == 'kn':
        content = fix_kn_footer(content, translations_for_full)
    else:
        lines = content.split('\n')
        new_lines = []
        for line in lines:
            if ('&nbsp;|&nbsp;' in line and '<a href=#>' in line and
                    line.count('href=') >= 10):
                line = update_footer_line(line, locale, replacements)
            new_lines.append(line)
        content = '\n'.join(new_lines)

    if content != original:
        with open(fn, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'  Updated: {fn}')
    else:
        print(f'  No changes: {fn}')

def ensure_links_only(locale):
    """Run only the ensure_footer_links step for a locale (no translation update)."""
    fn = os.path.join(WORKDIR, get_href(locale))
    if not os.path.exists(fn):
        print(f'  SKIP: {fn} not found')
        return

    with open(fn, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content
    content = ensure_footer_links(content, locale)

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

    # Locales whose footers are fully translated into the target language
    full_replace_locales = ['af', 'am', 'fi', 'gu', 'ha', 'hr', 'ig', 'ka', 'kk', 'kn', 'la', 'ml', 'mn', 'mr', 'ps', 'sr', 'te', 'tl', 'uk', 'yo']
    # Locales with partial replacements (only specific entries need updating)
    partial_locales = [
        'ar', 'bn', 'el', 'eu', 'fa', 'he', 'hi', 'ja', 'ko', 'nl', 'or', 'pa',
        'ru', 'si', 'ta', 'th', 'vi', 'zh', 'ur', 'hy',
        'de', 'es', 'fr', 'hu', 'id', 'it', 'jv', 'new', 'bo', 'pl', 'pt',
        'sv', 'sw', 'tr', 'tt', 'ky', 'cs',
    ]
    # Locales already fully translated whose footers only need link-insertion if new
    # languages are added (bs, ku, ro have no entries in the translation table since
    # their footers were hand-translated; en is the source of truth).
    ensure_only_locales = ['en', 'bs', 'ku', 'ro']

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

    print('\nEnsuring link completeness for remaining files...')
    for locale in ensure_only_locales:
        print(f'  {locale}:')
        ensure_links_only(locale)

    print('\nDone!')


if __name__ == '__main__':
    main()
