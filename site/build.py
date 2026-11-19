#!/usr/bin/env python3
"""Builds Cingle Remote's website into ../docs, which GitHub Pages serves.

Run `python3 site/build.py` from the repository's root after changing anything here. Every page's text lives in this
file; the media in docs/assets is made by hand (see site/README.md). Plain HTML and CSS, no Jekyll (docs/.nojekyll).
"""

from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs"
BASE = "https://ryudexter.github.io/cingle-remote"
APP_ID = "6826505353"
REPO = "https://github.com/ryudexter/cingle-remote"


def store_link(ppid=None):
    # No country in the path, so the App Store opens in the visitor's own storefront.
    url = f"https://apps.apple.com/app/id{APP_ID}"
    return f"{url}?ppid={ppid}" if ppid else url


BADGE = {
    "en": "https://toolbox.marketingtools.apple.com/api/v2/badges/download-on-the-app-store/black/en-us",
    "tr": "https://toolbox.marketingtools.apple.com/api/v2/badges/download-on-the-app-store/black/tr-tr",
}

# ---------------------------------------------------------------------------------------------------------------------
# Words that every page in a language shares.

UI = {
    "en": {
        "site": "Cingle Remote",
        "nav_tvs": "TVs",
        "nav_support": "Support",
        "other_lang": ("Türkçe", "tr/"),
        "badge_alt": "Download on the App Store",
        "video_label": "Cingle Remote: typing a search on an iPhone shows it on the TV, then the remote, the TV's apps, "
                       "the Apple Watch and the Mac at work.",
        "pause": "Pause the video",
        "play": "Play the video",
        "support": "Support",
        "privacy": "Privacy Policy",
        "terms": "Terms of Use",
        "privacy_url": f"{REPO}/blob/main/privacy/en.md",
        "terms_url": f"{REPO}/blob/main/terms/en.md",
        "made_by": "Cingle Remote is made by Fatih Ziya Cengel.",
        "not_affiliated": "Cingle Remote isn't affiliated with or endorsed by any of the TV brands named here; their "
                          "names are used only to say which TVs Cingle supports.",
        "apple": "Apple, the Apple logo, iPhone, iPad, Apple Watch, Mac and Apple TV are trademarks of Apple Inc., "
                 "registered in the U.S. and other countries and regions. App Store is a service mark of Apple Inc.",
        "requires": "For iOS 18, iPadOS 18, watchOS 10 and macOS 15 or later.",
        "home": "Home",
        "other_tvs": "Other TVs Cingle supports",
        "full_list": "Every TV Cingle supports",
        "get": "Get Cingle Remote",
        "get_sub": "Your iPhone, iPad, Apple Watch and Mac, ready for your TV. No ads, ever.",
        "questions": "Questions? The <a href=\"{repo}\">support page</a> has answers, and how to reach the developer.",
    },
    "tr": {
        "site": "Cingle Remote",
        "nav_tvs": "TV'ler",
        "nav_support": "Destek",
        "other_lang": ("English", ""),
        "badge_alt": "App Store'dan İndirin",
        "video_label": "Cingle Remote: iPhone'da yazılan bir arama TV'de görünüyor; ardından kumanda, TV'nin "
                       "uygulamaları, Apple Watch ve Mac iş başında.",
        "pause": "Videoyu duraklat",
        "play": "Videoyu oynat",
        "support": "Destek",
        "privacy": "Gizlilik Politikası",
        "terms": "Kullanım Koşulları",
        "privacy_url": f"{REPO}/blob/main/privacy/tr.md",
        "terms_url": f"{REPO}/blob/main/terms/tr.md",
        "made_by": "Cingle Remote'u Fatih Ziya Cengel geliştiriyor.",
        "not_affiliated": "Cingle Remote, burada adı geçen TV markalarının hiçbiriyle bağlantılı değildir ve onlar "
                          "tarafından onaylanmamıştır; markaların adları yalnızca Cingle'ın hangi TV'leri "
                          "desteklediğini belirtmek için kullanılır.",
        "apple": "Apple, Apple logosu, iPhone, iPad, Apple Watch, Mac ve Apple TV, Apple Inc.'in ABD'de ve diğer "
                 "ülke ve bölgelerde tescilli ticari markalarıdır. App Store, Apple Inc.'in hizmet markasıdır.",
        "requires": "iOS 18, iPadOS 18, watchOS 10 ve macOS 15 veya üstüyle çalışır.",
        "home": "Ana sayfa",
        "other_tvs": "Cingle'ın desteklediği diğer TV'ler",
        "full_list": "Cingle'ın desteklediği tüm TV'ler",
        "get": "Cingle Remote'u edinin",
        "get_sub": "iPhone'unuz, iPad'iniz, Apple Watch'unuz ve Mac'iniz TV'niz için hazır. Hiç reklam yok.",
        "questions": "Sorunuz mu var? <a href=\"{repo}\">Destek sayfası</a> sık sorulanları yanıtlıyor ve "
                     "geliştiriciye nasıl ulaşacağınızı anlatıyor.",
    },
}

# The full list, as the support page (README.md) and the App Store description give it.
COMPAT = {
    "en": [
        "LG webOS TVs, and LG NetCast TVs from 2012 and 2013",
        "Samsung smart TVs from 2016 on, and many from 2010 to 2015",
        "Roku TVs and players",
        "Google TV and Android TV, including Chromecast with Google TV, Google TV Streamer, NVIDIA Shield and "
        "Xiaomi TV Box",
        "Apple TV HD and Apple TV 4K with tvOS 15 or later",
        "Amazon Fire TV sticks, Cube and TVs; the volume stays with their own remote",
        "Philips TVs with Titan OS or Saphi, and older ones from about 2011",
        "Panasonic Viera TVs from about 2012 to 2024",
        "Sony Bravia TVs from about 2013 on",
        "Sharp AQUOS TVs with IP control, from about 2010 to 2016",
        "TCL and Thomson TVs on TCL's own system, from about 2014 to 2019",
        "TVs on Vestel's own smart system, sold as Vestel, Regal, Toshiba, Hitachi, JVC, Sharp, Telefunken, Finlux, "
        "Medion, Bush, Alba, ProCaster and Celcus",
    ],
    "tr": [
        "LG webOS TV'ler ve 2012–2013 LG NetCast TV'ler",
        "2016 ve sonrası Samsung akıllı TV'ler ve 2010–2015 arasının birçok modeli",
        "Roku TV'ler ve oynatıcılar",
        "Google TV ve Android TV; Chromecast with Google TV, Google TV Streamer, NVIDIA Shield ve Xiaomi TV Box dahil",
        "tvOS 15 veya üstü yüklü Apple TV HD ve Apple TV 4K",
        "Amazon Fire TV Stick, Cube ve Fire TV'ler; ses düzeyi kendi kumandalarıyla ayarlanır",
        "Titan OS veya Saphi sistemli Philips TV'ler ve yaklaşık 2011 sonrası eski modeller",
        "Yaklaşık 2012–2024 arası Panasonic Viera TV'ler",
        "Yaklaşık 2013 ve sonrası Sony Bravia TV'ler",
        "IP kontrollü, yaklaşık 2010–2016 arası Sharp AQUOS TV'ler",
        "TCL'nin kendi sistemini kullanan, yaklaşık 2014–2019 arası TCL ve Thomson TV'ler",
        "Vestel'in kendi akıllı sistemini kullanan TV'ler: Vestel, Regal, Toshiba, Hitachi, JVC, Sharp, Telefunken, "
        "Finlux, Medion, Bush, Alba, ProCaster ve Celcus",
    ],
}

COMPAT_AFTER = {
    "en": [
        "That includes Sony, Philips, Panasonic, Sharp, Toshiba, Insignia, TCL, Hisense, Xiaomi, Skyworth, Haier, "
        "Nokia, Motorola, Thomson, Grundig, Beko, onn., RCA and Pioneer TVs that run Google TV, Android TV, Fire TV "
        "or Roku.",
        "Hisense's VIDAA TVs, and Beko and Grundig TVs on their own systems, aren't supported.",
        "Your TV needs to be on the same Wi-Fi as your iPhone, iPad or Mac.",
    ],
    "tr": [
        "Google TV, Android TV, Fire TV veya Roku kullanan Sony, Philips, Panasonic, Sharp, Toshiba, TCL, Hisense, "
        "Xiaomi, Arçelik, Beko, Grundig ve pek çok markanın TV'si de buna dahildir.",
        "Hisense'in VIDAA sistemli TV'leri ile kendi sistemini kullanan Arçelik, Beko ve Grundig TV'ler "
        "desteklenmiyor.",
        "TV'nizin, iPhone'unuz, iPad'iniz veya Mac'inizle aynı Wi-Fi ağında olması gerekir.",
    ],
}

# ---------------------------------------------------------------------------------------------------------------------
# One entry per brand page. `features` and `pairing` follow the support page and what TVPlatform says each platform
# can do (typing: canType; number pad: hasNumberKeys; channel list: listsChannels; pointer: hasPointer).

PAD = "Swipe and tap on a large pad, or use the arrows and OK"
VOLUME = "Volume, mute, channels, play/pause and 10-second skips, and the volume buttons on your iPhone change the " \
         "TV's volume"
TYPE = "Type searches with your keyboard instead of picking letters on the TV"
NUMBERS = "A number pad for channel numbers"
APPS = "Open the TV's apps in one tap"
WATCH_VIA_IPHONE = "Pair the TV on your iPhone and your Apple Watch is ready, with no code to type: swipe and tap to " \
                   "move around, and turn the Digital Crown for volume. The Watch goes through your iPhone, which " \
                   "needs to be nearby."
MAC = "Your Mac finds the same TVs. The arrow keys move around, Return selects, Space plays or pauses and Delete " \
      "goes back; the Remote menu has the rest."

BRANDS = [
    {
        "key": "lg", "slug": "lg-tv-remote", "name": "LG", "card": "webOS, and NetCast from 2012 and 2013",
        "title": "Use your iPhone as an LG TV remote",
        "h1": ("Use your iPhone", "as an LG remote"),
        "lead": "Cingle Remote controls LG webOS TVs, and LG NetCast TVs from 2012 and 2013, over your home Wi-Fi. "
                "Your iPad, Apple Watch and Mac can work the same TV.",
        "features": [
            "A trackpad for the TV's pointer on webOS, and Gyro Pointer: turn your iPhone to move it (Premium+)",
            TYPE,
            "Open the TV's apps in one tap, with their own icons on webOS",
            "Pick a channel from the TV's own channel list, or type its number on the number pad",
            VOLUME, PAD,
        ],
        "pairing": ["<b>LG webOS:</b> type the 8-digit PIN the TV shows.",
                    "<b>LG NetCast (2012 and 2013):</b> type the 6-digit key the TV shows."],
        "watch": WATCH_VIA_IPHONE,
        "mac": MAC + " On a webOS TV, your mouse or trackpad moves the TV's pointer.",
        "shots": ["lg-en-01-hero", "lg-en-02-pointer", "lg-en-05-apps"],
        "ppid": "ff1b304e-6f03-4f30-9ae8-89816c0c63b7",
    },
    {
        "key": "samsung", "slug": "samsung-tv-remote", "name": "Samsung", "card": "2016 on, and many from 2010 to 2015",
        "title": "Use your iPhone as a Samsung TV remote",
        "h1": ("Use your iPhone", "as a Samsung remote"),
        "lead": "Cingle Remote controls Samsung smart TVs from 2016 on, and many from 2010 to 2015, over your home "
                "Wi-Fi. Your iPad, Apple Watch and Mac can work the same TV.",
        "features": [TYPE, NUMBERS + ", with the TV's own channel list key", APPS, VOLUME, PAD],
        "pairing": ["Accept the prompt on the TV with its own remote.",
                    "Many from 2014 and 2015 (H and J series) show a 4-digit PIN instead: type it in Cingle."],
        "watch": WATCH_VIA_IPHONE,
        "mac": MAC,
        "shots": ["samsung-en-01-hero", "samsung-en-03-type", "samsung-en-04-numbers"],
        "ppid": "e6e4179f-265b-480e-8124-8407240eedb7",
    },
    {
        "key": "roku", "slug": "roku-remote", "name": "Roku", "card": "Roku TVs and players",
        "title": "Use your iPhone as a Roku remote",
        "h1": ("Use your iPhone", "as a Roku remote"),
        "lead": "Cingle Remote controls Roku TVs and players, including TCL and Hisense Roku TVs, over your home "
                "Wi-Fi. Your iPad, Apple Watch and Mac can work the same Roku.",
        "features": [
            TYPE,
            "Open the Roku's apps in one tap, with their own icons",
            "Your Apple Watch sends presses straight to the Roku, without your iPhone nearby",
            "Volume, mute, play/pause and 10-second skips, and the volume buttons on your iPhone change the volume",
            PAD,
        ],
        "pairing": ["No code is needed.",
                    "If presses do nothing, turn on Settings › System › Advanced system settings › Control by mobile "
                    "apps on the Roku."],
        "watch": "Pair the Roku on your iPhone and your Apple Watch is ready, with no code to type: swipe and tap to "
                 "move around, and turn the Digital Crown for volume. A Roku takes presses straight from the Watch, "
                 "so your iPhone can stay in another room.",
        "mac": MAC,
        "shots": ["roku-en-01-hero", "roku-en-03-type", "roku-en-04-together"],
        "ppid": "5e64e809-a0a6-44a4-ad82-82524990c957",
    },
    {
        "key": "googletv", "slug": "google-tv-remote", "name": "Google TV", "card": "and Android TV, Chromecast, Shield",
        "title": "Use your iPhone as a Google TV and Android TV remote",
        "h1": ("Use your iPhone", "as a Google TV remote"),
        "lead": "Cingle Remote controls Google TV and Android TV over your home Wi-Fi: Chromecast with Google TV, "
                "Google TV Streamer, NVIDIA Shield, Xiaomi TV Box, and TVs from Sony, Philips, TCL, Hisense, Xiaomi "
                "and many others that run Google TV or Android TV.",
        "features": [TYPE, NUMBERS, APPS, VOLUME, PAD],
        "pairing": ["Type the 6-character code the TV shows."],
        "watch": WATCH_VIA_IPHONE,
        "mac": MAC,
        "shots": ["googletv-en-01-hero", "googletv-en-03-type", "googletv-en-04-numbers"],
        "ppid": "1427cbc9-18d1-4465-9d50-d5447a363690",
    },
    {
        "key": "firetv", "slug": "fire-tv-remote", "name": "Fire TV", "card": "Sticks, Cube and Fire TV smart TVs",
        "title": "Use your iPhone as a Fire TV remote",
        "h1": ("Use your iPhone", "as a Fire TV remote"),
        "lead": "Cingle Remote controls Amazon Fire TV sticks, Cube and Fire TV smart TVs over your home Wi-Fi. Your "
                "iPad, Apple Watch and Mac can work the same Fire TV.",
        "features": [TYPE, APPS, "Play/pause and 10-second skips", PAD],
        "note": "Cingle can't change the volume on a Fire TV: use its own remote for that. Older Fire TV sticks "
                "(Fire OS 7 and earlier) may not answer.",
        "pairing": ["Type the 4-digit PIN the Fire TV shows."],
        "watch": WATCH_VIA_IPHONE,
        "mac": MAC,
        "shots": ["firetv-en-01-hero", "firetv-en-03-type", "firetv-en-04-together"],
        "ppid": "65712fb0-4a50-4114-81b7-510f9294fe59",
    },
    {
        "key": "sony", "slug": "sony-tv-remote", "name": "Sony", "card": "Bravia, from about 2013",
        "title": "Use your iPhone as a Sony Bravia TV remote",
        "h1": ("Use your iPhone", "as a Sony Bravia remote"),
        "lead": "Cingle Remote controls Sony Bravia TVs from about 2013 on over your home Wi-Fi: the ones on Google TV "
                "or Android TV, and the ones on Sony's own system. Your iPad, Apple Watch and Mac can work the same "
                "TV.",
        "features": [
            TYPE,
            "Pick a channel from the TV's own channel list (Bravia TVs not on Android), or type its number on the "
            "number pad",
            VOLUME, PAD,
        ],
        "pairing": ["<b>Bravia TVs not on Android:</b> type the 4-digit PIN the TV shows. The TV's IP Control "
                    "authentication has to be Normal.",
                    "<b>Sony TVs that run Google TV or Android TV</b> connect as a Google TV instead, with a "
                    "6-character code."],
        "watch": WATCH_VIA_IPHONE,
        "mac": MAC,
        "shots": ["en-02-remote", "en-07-type", "en-08-tvs"],
    },
    {
        "key": "philips", "slug": "philips-tv-remote", "name": "Philips", "card": "Titan OS, Saphi and older sets",
        "title": "Use your iPhone as a Philips TV remote",
        "h1": ("Use your iPhone", "as a Philips TV remote"),
        "lead": "Cingle Remote controls Philips TVs with Titan OS or Saphi, older ones from about 2011, and Philips "
                "TVs that run Google TV or Android TV, over your home Wi-Fi. Your iPad, Apple Watch and Mac can work "
                "the same TV.",
        "features": [
            TYPE,
            "Pick a channel from the TV's own channel list, or type its number on the number pad",
            VOLUME, PAD,
        ],
        "pairing": ["<b>Titan OS, Saphi and older sets:</b> type the 4-digit PIN if the TV shows one; sets that don't "
                    "ask for one connect without a code. Most older sets need to be added by IP address.",
                    "<b>Philips TVs that run Google TV or Android TV</b> connect as a Google TV instead, with a "
                    "6-character code."],
        "watch": WATCH_VIA_IPHONE,
        "mac": MAC,
        "shots": ["en-02-remote", "en-07-type", "en-08-tvs"],
    },
    {
        "key": "panasonic", "slug": "panasonic-tv-remote", "name": "Panasonic", "card": "Viera, about 2012 to 2024",
        "title": "Use your iPhone as a Panasonic Viera TV remote",
        "h1": ("Use your iPhone", "as a Panasonic Viera remote"),
        "lead": "Cingle Remote controls Panasonic Viera TVs from about 2012 to 2024 over your home Wi-Fi, and "
                "Panasonic TVs that run Android TV or Fire TV. Your iPad, Apple Watch and Mac can work the same TV.",
        "features": [NUMBERS, VOLUME, PAD],
        "pairing": ["Models from 2019 on show a 4-digit PIN to type; older ones connect without a code.",
                    "If nothing happens, turn on Menu › Network › TV Remote App Settings › TV Remote on the TV."],
        "watch": WATCH_VIA_IPHONE,
        "mac": MAC,
        "shots": ["en-02-remote", "en-08-tvs", "en-01-together"],
    },
    {
        "key": "sharp", "slug": "sharp-tv-remote", "name": "Sharp", "card": "AQUOS with IP control",
        "title": "Use your iPhone as a Sharp AQUOS TV remote",
        "h1": ("Use your iPhone", "as a Sharp AQUOS remote"),
        "lead": "Cingle Remote controls Sharp AQUOS TVs with IP control, from about 2010 to 2016, over your home "
                "Wi-Fi. Sharp TVs that run Google TV, Android TV or Roku work too, and so do the European ones made "
                "by Vestel.",
        "features": [NUMBERS, VOLUME, PAD],
        "pairing": ["<b>AQUOS with IP control:</b> on the TV, press Menu and go to Internet Setup (under Initial Setup "
                    "or Smart TV), then set AQUOS Remote Control (IP Control Setup on older TVs) to Enable, with port "
                    "10002. If you set a login ID and password there, Cingle asks for them once.",
                    "<b>Sharp TVs that run Google TV, Android TV or Roku</b> connect as those instead.",
                    "<b>Sharp TVs sold in Europe since 2014</b> are mostly made by Vestel: add those under Vestel."],
        "watch": WATCH_VIA_IPHONE,
        "mac": MAC,
        "shots": ["en-02-remote", "en-08-tvs", "en-01-together"],
    },
    {
        "key": "tcl", "slug": "tcl-tv-remote", "name": "TCL", "card": "Google TV, Roku and TCL's own system",
        "title": "Use your iPhone as a TCL TV remote",
        "h1": ("Use your iPhone", "as a TCL remote"),
        "lead": "Cingle Remote controls TCL TVs over your home Wi-Fi: the ones on Google TV, Android TV or Roku, and "
                "TCL and Thomson TVs on TCL's own system from about 2014 to 2019. Your iPad, Apple Watch and Mac can "
                "work the same TV.",
        "features": [
            "Type searches with your keyboard on TCL's Google TV, Android TV and Roku models",
            NUMBERS, VOLUME, PAD,
        ],
        "pairing": ["<b>TCL's own system:</b> no code is needed.",
                    "<b>TCL TVs that run Google TV or Android TV</b> connect as a Google TV, with the 6-character "
                    "code the TV shows. <b>TCL Roku TVs</b> need no code."],
        "watch": WATCH_VIA_IPHONE,
        "mac": MAC,
        "shots": ["en-02-remote", "en-07-type", "en-08-tvs"],
    },
    {
        "key": "vestel", "slug": "vestel-tv-remote", "name": "Vestel", "card": "and Regal, Toshiba, Hitachi, JVC…",
        "title": "Use your iPhone as a Vestel, Toshiba, Hitachi or JVC TV remote",
        "h1": ("Use your iPhone", "as a Vestel remote"),
        "lead": "Cingle Remote controls TVs on Vestel's own smart system over your home Wi-Fi. Vestel makes them for "
                "many brands: Vestel, Regal, Toshiba, Hitachi, JVC, Sharp, Telefunken, Finlux, Medion, Bush, Alba, "
                "ProCaster, Celcus and some Panasonic models.",
        "features": [NUMBERS, VOLUME, PAD],
        "pairing": ["No code is needed, but Virtual Remote has to be on: on the TV, press Menu, then under System › "
                    "Settings › More, turn on Virtual Remote.",
                    "<b>Models that run Google TV or Android TV</b> connect as a Google TV instead, with a "
                    "6-character code."],
        "watch": WATCH_VIA_IPHONE,
        "mac": MAC,
        "shots": ["vestel-en-01-hero", "vestel-en-02-numbers", "vestel-en-04-together"],
        "ppid": "5cda9846-3f82-490b-88b5-f86102ae1644",
        "alt": {"tr": "tr/vestel-kumanda/"},
    },
]

TR_VESTEL = {
    "key": "vestel", "slug": "tr/vestel-kumanda", "name": "Vestel",
    "title": "iPhone ile Vestel kumanda: Vestel, Regal, Toshiba ve Telefunken TV'ler için",
    "h1": ("iPhone ile", "Vestel kumanda"),
    "lead": "Cingle Remote, Vestel'in kendi akıllı sistemini kullanan TV'leri ev Wi-Fi'ınız üzerinden iPhone'unuzdan "
            "kontrol eder. Vestel bu TV'leri birçok marka için üretir: Vestel, Regal, Toshiba, Hitachi, JVC, Sharp, "
            "Telefunken, Finlux, Medion, Bush, Alba, ProCaster, Celcus ve bazı Panasonic modelleri. iPad'iniz, Apple "
            "Watch'unuz ve Mac'iniz de aynı TV'yi kontrol edebilir.",
    "features_h": "Vestel TV'nizde neler yapabilirsiniz",
    "features": [
        "Kanal numaraları için rakam tuşları: TV'nin kendi kumandasındaki gibi",
        "Ses, sessiz, kanallar, oynat/duraklat ve 10 saniye atlama; iPhone'unuzun ses düğmeleri TV'nin sesini "
        "değiştirir",
        "Geniş bir alanda kaydırın ve dokunun ya da oklar ve OK'u kullanın",
        "Birden fazla TV'yi kaydedin, tek dokunuşla geçin (Premium+)",
    ],
    "pairing_h": "Vestel TV'nizi bağlamak",
    "steps": [
        "TV'yi açın ve iPhone'unuzla aynı Wi-Fi ağına bağlı olduğundan emin olun.",
        "TV'nizde Menu'ye basın ve Sistem › Ayarlar › Diğer altında Sanal Uzaktan Kumanda'yı açın. Kod gerekmez.",
        "Cingle'ı açın. TV'yi kendisi bulur; iOS, Cingle'ın yerel ağınızdaki aygıtları bulmasına izin vermek isteyip "
        "istemediğinizi sorduğunda İzin Ver'e dokunun. TV'yi IP adresiyle de ekleyebilirsiniz: Ayarlar › Cihazlar › "
        "IP adresiyle TV ekle.",
    ],
    "pairing_after": [
        "Google TV veya Android TV kullanan modeller Google TV olarak bağlanır: TV'nin gösterdiği 6 karakterlik kodu "
        "girersiniz.",
        "Kendi sistemini kullanan Arçelik, Beko ve Grundig TV'ler desteklenmiyor; Google TV veya Android TV kullanan "
        "modelleri Google TV olarak bağlanır.",
    ],
    "devices_h": "Apple Watch ve Mac'te",
    "watch": "TV'yi iPhone'unuzda eşleştirin, Apple Watch'unuz da hazır olsun; kod girmeniz gerekmez. Gezinmek için "
             "kaydırın ve dokunun, ses için Digital Crown'u çevirin. Watch, komutları iPhone'unuz üzerinden gönderir, "
             "bu yüzden iPhone'unuz yakında olmalıdır.",
    "mac": "Mac'iniz aynı TV'leri bulur. Ok tuşlarıyla gezinin, Return ile seçin, Boşluk ile oynatın veya duraklatın, "
           "Delete ile geri gidin; \"Kumanda\" menüsünde gerisi var.",
    "shots": ["vestel-tr-01-hero", "vestel-tr-02-numbers", "vestel-tr-03-tvs"],
    "ppid": "5cda9846-3f82-490b-88b5-f86102ae1644",
    "alt": {"en": "vestel-tv-remote/"},
}

SHOT_ALT = {
    "lg-en-01-hero": "The remote on iPhone, connected to an LG TV",
    "lg-en-02-pointer": "A trackpad on iPhone moving the LG TV's pointer",
    "lg-en-05-apps": "The LG TV's apps on iPhone, one tap away",
    "samsung-en-01-hero": "The remote on iPhone, connected to a Samsung TV",
    "samsung-en-03-type": "Typing a search on iPhone for the Samsung TV",
    "samsung-en-04-numbers": "The number pad for channel numbers on iPhone",
    "roku-en-01-hero": "The remote on iPhone, connected to a Roku",
    "roku-en-03-type": "Typing a search on iPhone for the Roku",
    "roku-en-04-together": "The remote on iPhone, Apple Watch and Mac",
    "googletv-en-01-hero": "The remote on iPhone, connected to a Google TV",
    "googletv-en-03-type": "Typing a search on iPhone for the Google TV",
    "googletv-en-04-numbers": "The number pad for channel numbers on iPhone",
    "firetv-en-01-hero": "The remote on iPhone, connected to a Fire TV",
    "firetv-en-03-type": "Typing a search on iPhone for the Fire TV",
    "firetv-en-04-together": "The remote on iPhone, Apple Watch and Mac",
    "vestel-en-01-hero": "The remote on iPhone, connected to a Vestel TV",
    "vestel-en-02-numbers": "The number pad for channel numbers on iPhone",
    "vestel-en-04-together": "The remote on iPhone, Apple Watch and Mac",
    "vestel-tr-01-hero": "iPhone'da Vestel TV'ye bağlı kumanda",
    "vestel-tr-02-numbers": "iPhone'da kanal numaraları için rakam tuşları",
    "vestel-tr-03-tvs": "iPhone'da kayıtlı TV'ler arasında geçiş",
    "en-01-together": "The remote on iPhone, Apple Watch and Mac",
    "en-02-remote": "The remote on iPhone: a large pad, arrows and OK",
    "en-03-apps": "The TV's apps on iPhone, one tap away",
    "en-06-pointer": "A trackpad on iPhone for an LG TV's pointer",
    "en-07-type": "Typing a search on iPhone instead of on the TV",
    "en-08-tvs": "The TV brands Cingle works with, and switching between saved TVs",
    "tr-03-press-here": "iPhone'da kumanda: dokunduğunuz anda TV yanıt verir",
    "tr-04-remote": "iPhone'da kaydırma alanı, oklar ve OK",
    "tr-06-watch": "Apple Watch'ta kumanda",
    "tr-09-type": "iPhone'un klavyesiyle TV'de arama yazmak",
    "tr-10-tvs": "Cingle'ın çalıştığı TV markaları ve kayıtlı TV'ler",
}

# ---------------------------------------------------------------------------------------------------------------------
# Pieces.

CHECK = ('<svg class="tick" viewBox="0 0 20 20" aria-hidden="true"><path d="M5 10.5l3.2 3.2L15 7" fill="none" '
         'stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg>')


def badge(lang, ppid, up, extra=""):
    t = UI[lang]
    return (f'<a class="badge{extra}" href="{store_link(ppid)}">'
            f'<img src="{BADGE[lang]}" alt="{escape(t["badge_alt"])}" width="156" height="52"></a>')


def video(lang, up):
    t = UI[lang]
    return f"""
<figure class="film">
  <video class="film-video" autoplay muted loop playsinline preload="auto" width="1600" height="900"
         poster="{up}assets/video/poster-{lang}.jpg" aria-label="{escape(t['video_label'])}">
    <source src="{up}assets/video/cingle-{lang}.mp4" type="video/mp4">
  </video>
  <button class="film-toggle" type="button" data-pause="{escape(t['pause'])}" data-play="{escape(t['play'])}"
          aria-label="{escape(t['pause'])}"><span aria-hidden="true"></span></button>
</figure>"""


def shots(names, up):
    imgs = "\n".join(
        f'    <img src="{up}assets/shots/{n}.webp" alt="{escape(SHOT_ALT[n])}" width="600" height="1304" '
        f'loading="lazy" decoding="async">' for n in names)
    return f'<div class="shots">\n{imgs}\n</div>'


def ticks(items):
    return "<ul class=\"ticks\">" + "".join(f"<li>{CHECK}<span>{i}</span></li>" for i in items) + "</ul>"


def head(lang, title, desc, path, up, alts):
    canon = f"{BASE}/{path}"
    links = "".join(f'\n  <link rel="alternate" hreflang="{l}" href="{BASE}/{p}">' for l, p in alts.items())
    if alts:
        links += f'\n  <link rel="alternate" hreflang="x-default" href="{BASE}/{alts.get("en", path)}">'
    return f"""<!doctype html>
<html lang="{lang}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(title)}</title>
  <meta name="description" content="{escape(desc)}">
  <link rel="canonical" href="{canon}">{links}
  <meta name="apple-itunes-app" content="app-id={APP_ID}">
  <meta name="theme-color" content="#0b0d1a">
  <meta name="color-scheme" content="dark">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Cingle Remote">
  <meta property="og:title" content="{escape(title)}">
  <meta property="og:description" content="{escape(desc)}">
  <meta property="og:url" content="{canon}">
  <meta property="og:image" content="{BASE}/assets/og-{lang}.jpg">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:locale" content="{'tr_TR' if lang == 'tr' else 'en_US'}">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="icon" type="image/png" sizes="64x64" href="{up}assets/favicon-64.png">
  <link rel="apple-touch-icon" href="{up}assets/apple-touch-icon.png">
  <link rel="stylesheet" href="{up}assets/style.css">
  <script src="{up}assets/site.js" defer></script>
</head>"""


def topbar(lang, up, alt_path):
    t = UI[lang]
    home = up + ("tr/" if lang == "tr" else "")
    other_name, _ = t["other_lang"]
    other_lang = "en" if lang == "tr" else "tr"
    return f"""
<header class="top">
  <div class="wrap top-in">
    <a class="brand" href="{home}"><img src="{up}assets/icon-128.png" alt="" width="32" height="32"><span>Cingle Remote</span></a>
    <nav class="top-nav" aria-label="Site">
      <a href="{home}#tvs">{t['nav_tvs']}</a>
      <a href="{REPO}">{t['nav_support']}</a>
      <a href="{up}{alt_path}" hreflang="{other_lang}" lang="{other_lang}">{other_name}</a>
    </nav>
  </div>
</header>"""


def footer(lang, up, extra_line=""):
    t = UI[lang]
    return f"""
<footer class="foot">
  <div class="wrap">
    <nav class="foot-nav">
      <a href="{REPO}">{t['support']}</a>
      <a href="{t['privacy_url']}">{t['privacy']}</a>
      <a href="{t['terms_url']}">{t['terms']}</a>
    </nav>
    <p>{extra_line}{t['not_affiliated']}</p>
    <p>{t['apple']}</p>
    <p>{t['made_by']}</p>
  </div>
</footer>
</body>
</html>
"""


def cta(lang, up, ppid=None):
    t = UI[lang]
    return f"""
<section class="cta">
  <div class="wrap cta-in">
    <img class="cta-icon" src="{up}assets/icon-128.png" alt="" width="88" height="88">
    <h2>{t['get']}</h2>
    <p>{t['get_sub']}</p>
    {badge(lang, ppid, up)}
    <p class="small">{t['requires']}</p>
    <p class="small">{t['questions'].format(repo=REPO)}</p>
  </div>
</section>"""


def compat_section(lang, up, h2, intro):
    items = "".join(f"<li>{i}</li>" for i in COMPAT[lang])
    after = "".join(f"<p>{p}</p>" for p in COMPAT_AFTER[lang])
    return f"""
<section class="band" id="compatibility">
  <div class="wrap narrow">
    <h2>{h2}</h2>
    <p class="muted">{intro}</p>
    <ul class="compat">{items}</ul>
    <div class="muted">{after}</div>
  </div>
</section>"""


def brand_cards(up, lang="en", current=None):
    cards = []
    for b in BRANDS:
        if b["key"] == current:
            continue
        cards.append(f'<a class="card" href="{up}{b["slug"]}/"><b>{b["name"]}</b><span>{b["card"]}</span></a>')
    if current is None:
        cards.append('<a class="card card-all" href="#compatibility"><b>Every TV</b>'
                     '<span>Apple TV, Hisense, Xiaomi and more</span></a>')
    return '<div class="cards">' + "".join(cards) + "</div>"


def write(path, html):
    f = OUT / path / "index.html" if not path.endswith(".html") else OUT / path
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(html, encoding="utf-8")


# ---------------------------------------------------------------------------------------------------------------------
# Pages.

def home_en():
    up = ""
    desc = ("Cingle Remote turns your iPhone, iPad, Apple Watch and Mac into one remote for your TV over Wi-Fi: LG, "
            "Samsung, Roku, Google TV, Fire TV, Sony, Philips, Panasonic, Vestel and more. No ads.")
    html = head("en", "Cingle Remote: a universal TV remote for iPhone, iPad, Apple Watch and Mac", desc, "", up,
                {"en": "", "tr": "tr/"})
    html += "\n<body>" + topbar("en", up, "tr/")
    html += f"""
<main>
<section class="hero">
  <div class="wrap hero-in">
    <p class="eyebrow">Wi-Fi TV remote</p>
    <h1>A universal TV remote <span class="accent">for iPhone, iPad, Apple Watch and Mac</span></h1>
    <p class="lead">Cingle Remote turns your iPhone, iPad, Apple Watch and Mac into one remote for your TV, over your
      home Wi-Fi. No batteries to change, no need to aim, and no ads, ever.</p>
    <div class="hero-cta">{badge("en", None, up)}<span class="small">{UI['en']['requires']}</span></div>
  </div>
  <div class="wrap">{video("en", up)}</div>
</section>

<section class="band" id="tvs">
  <div class="wrap">
    <h2>Works with the TV you have</h2>
    <p class="muted section-lead">Cingle finds your TV on your Wi-Fi by itself, or you can add it by its IP address.
      Pick yours to see what works and how to connect.</p>
    {brand_cards(up)}
    <p class="muted also">Also Apple TV HD and Apple TV 4K, and TVs from Hisense, Xiaomi, Toshiba, Insignia, onn. and
      many more that run Google TV, Android TV, Fire TV or Roku. <a href="#compatibility">See the full list</a>.</p>
  </div>
</section>

<section class="band">
  <div class="wrap">
    <h2>One remote, all your devices</h2>
    <p class="muted section-lead">Pair a TV on your iPhone and your Apple Watch is ready, with no code to type. Your
      iPad and Mac find the same TVs, and one Premium+ purchase covers them all with the same Apple Account.</p>
    <div class="cols">
      <div class="col">
        <h3>iPhone and iPad</h3>
        {ticks([PAD, "Volume, mute, channels, a number pad, play/pause and 10-second skips",
                "The volume buttons on your iPhone change the TV's volume",
                "Open your TV's apps in one tap",
                "Type searches with your keyboard (LG, Samsung, Roku, Google TV, Fire TV, Apple TV and some others)",
                "A trackpad for the pointer on LG webOS TVs, and Gyro Pointer (Premium+)",
                "A remote widget, a TV Button in Control Center that presses a key without opening the app, and "
                "Siri (Premium+)"])}
      </div>
      <div class="col">
        <h3>Apple Watch</h3>
        <p>Control your TV from your wrist: swipe and tap to move around, with Home, Back, Mute and Power, and the
          Digital Crown for volume. A tap on your wrist tells you when the TV is ready.</p>
        <p class="muted">It needs Cingle Remote on your iPhone, and for every TV but Roku your iPhone needs to be
          nearby. For watchOS 10 or later.</p>
      </div>
      <div class="col">
        <h3>Mac</h3>
        <p>The arrow keys move around, Return selects, Space plays or pauses, Delete goes back and number keys send
          numbers. The Remote menu has volume, channels, typing and the rest, with keyboard shortcuts.</p>
        <p class="muted">On LG webOS TVs, your mouse or trackpad moves the TV's pointer. For macOS 15 or later.</p>
      </div>
    </div>
    {shots(["en-02-remote", "en-07-type", "en-06-pointer", "en-03-apps", "en-08-tvs"], up)}
  </div>
</section>

<section class="band">
  <div class="wrap split">
    <div>
      <h2>No ads. No tracking.</h2>
      <p>Cingle shows no ads and uses no analytics or tracking. It talks to your TV directly over your Wi-Fi, and what
        it saves stays on your devices. There's no account to make.</p>
    </div>
    <div>
      <h2>Premium+</h2>
      <p>Without Premium+, Cingle keeps one TV, with every basic remote function. Premium+ adds several saved TVs, the
        Apple Watch app after its first two weeks, Bigger Remote on Mac, Gyro Pointer, Siri, the remote widget and the
        TV Button. It works on all your devices with the same Apple Account, and with Family Sharing.</p>
    </div>
  </div>
</section>
"""
    html += compat_section("en", up, "Every TV Cingle supports",
                           "Cingle talks to each kind of TV in its own language, over your home Wi-Fi.")
    html += cta("en", up) + "\n</main>" + footer("en", up)
    write("", html)


def home_tr():
    up = "../"
    desc = ("Cingle Remote; iPhone, iPad, Apple Watch ve Mac'inizi Wi-Fi üzerinden TV'nizin tek kumandasına "
            "dönüştürür: LG, Samsung, Vestel, Roku, Google TV, Fire TV, Sony, Philips ve dahası. Reklamsız.")
    html = head("tr", "Cingle Remote: iPhone, iPad, Apple Watch ve Mac için Universal TV kumandası", desc, "tr/", up,
                {"en": "", "tr": "tr/"})
    html += "\n<body>" + topbar("tr", up, "")
    vestel_card = '<a class="card" href="vestel-kumanda/"><b>Vestel</b><span>ve Regal, Toshiba, Hitachi, ' \
                  'JVC, Telefunken, Finlux…</span></a>'
    cards = "".join(f'<a class="card" href="{up}{b["slug"]}/" hreflang="en"><b>{b["name"]}</b>'
                    f'<span>{TR_CARD[b["key"]]}</span></a>' for b in BRANDS if b["key"] != "vestel")
    cards += ('<a class="card card-all" href="#compatibility"><b>Tüm TV\'ler</b>'
              '<span>Apple TV, Hisense, Xiaomi ve dahası</span></a>')
    html += f"""
<main>
<section class="hero">
  <div class="wrap hero-in">
    <p class="eyebrow">Wi-Fi TV kumandası</p>
    <h1>Universal TV kumandası <span class="accent">iPhone, iPad, Apple Watch ve Mac için</span></h1>
    <p class="lead">Cingle Remote, iPhone'unuzu, iPad'inizi, Apple Watch'unuzu ve Mac'inizi ev Wi-Fi'ınız üzerinden
      TV'nizin tek kumandasına dönüştürür. Pil değiştirmek yok, doğrultmak yok, reklam hiç yok.</p>
    <div class="hero-cta">{badge("tr", None, up)}<span class="small">{UI['tr']['requires']}</span></div>
  </div>
  <div class="wrap">{video("tr", up)}</div>
</section>

<section class="band" id="tvs">
  <div class="wrap">
    <h2>Evinizdeki TV ile çalışır</h2>
    <p class="muted section-lead">Cingle, TV'nizi Wi-Fi ağınızda kendisi bulur; isterseniz IP adresiyle de
      ekleyebilirsiniz.</p>
    <div class="cards">{vestel_card}{cards}</div>
    <p class="muted also">Diğer markaların sayfaları İngilizce. Apple TV HD ve Apple TV 4K ile Google TV, Android TV,
      Fire TV veya Roku kullanan Hisense, Xiaomi, Toshiba ve pek çok markanın TV'si de desteklenir.
      <a href="#compatibility">Tam listeye bakın</a>.</p>
  </div>
</section>

<section class="band">
  <div class="wrap">
    <h2>Tüm cihazlarınızda tek kumanda</h2>
    <p class="muted section-lead">TV'yi iPhone'unuzda eşleştirin, Apple Watch'unuz da hazır olsun; kod girmeniz
      gerekmez. iPad'iniz ve Mac'iniz aynı TV'leri bulur ve tek bir Premium+ satın alımı, aynı Apple Hesabı ile
      hepsinde geçerlidir.</p>
    <div class="cols">
      <div class="col">
        <h3>iPhone ve iPad</h3>
        {ticks(["Geniş bir alanda kaydırın ve dokunun ya da oklar ve OK'u kullanın",
                "Ses, sessiz, kanallar, rakam tuşları, oynat/duraklat ve 10 saniye atlama",
                "iPhone'unuzun ses düğmeleri TV'nin sesini değiştirir",
                "TV'nizin uygulamalarını tek dokunuşla açın",
                "Klavyenizle arama yazın (LG, Samsung, Roku, Google TV, Fire TV, Apple TV ve bazı diğerleri)",
                "LG webOS TV'lerde imleç için izleme dörtgeni ve Jiroskopik İmleç (Premium+)",
                "Ana ekranda kumanda widget'ı, Denetim Merkezi'nde TV Tuşu ve Siri ile kontrol (Premium+)"])}
      </div>
      <div class="col">
        <h3>Apple Watch</h3>
        <p>TV'nizi bileğinizden kontrol edin: gezinmek için kaydırın ve dokunun; Ana ekran, Geri, Sessiz ve Güç
          düğmeleri ile ses için Digital Crown elinizin altında. Bileğinize bir dokunuş, TV hazır olunca haber verir.</p>
        <p class="muted">iPhone'unuzda Cingle Remote yüklü olmalıdır; Roku dışındaki TV'lerde iPhone'unuz yakında
          olmalıdır. watchOS 10 veya üstüyle çalışır.</p>
      </div>
      <div class="col">
        <h3>Mac</h3>
        <p>Ok tuşlarıyla gezinin, Return ile seçin, Boşluk ile oynatın veya duraklatın, Delete ile geri gidin,
          rakamlarla numara girin; "Kumanda" menüsünde ses, kanallar, yazma ve diğerleri klavye kısayollarıyla yer
          alır.</p>
        <p class="muted">LG webOS TV'lerde fareniz veya izleme dörtgeniz imleci hareket ettirir. macOS 15 veya
          üstüyle çalışır.</p>
      </div>
    </div>
    {shots(["tr-03-press-here", "tr-04-remote", "tr-09-type", "tr-06-watch", "tr-10-tvs"], up)}
  </div>
</section>

<section class="band">
  <div class="wrap split">
    <div>
      <h2>Reklam yok. Takip yok.</h2>
      <p>Cingle reklam göstermez, analiz veya takip kullanmaz. TV'nizle Wi-Fi üzerinden doğrudan konuşur ve
        kaydettikleri cihazlarınızda kalır. Hesap açmanız gerekmez.</p>
    </div>
    <div>
      <h2>Premium+</h2>
      <p>Premium+ olmadan Cingle, tüm temel kumanda işlevleriyle bir TV'yi kaydeder. Premium+ birden fazla TV, ilk iki
        haftasından sonra Apple Watch uygulaması, Mac'te daha büyük kumanda, Jiroskopik İmleç, Siri, widget ve TV Tuşu
        ekler. Aynı Apple Hesabı ile tüm cihazlarınızda ve Aile Paylaşımı ile çalışır.</p>
    </div>
  </div>
</section>
"""
    html += compat_section("tr", up, "Cingle'ın desteklediği tüm TV'ler",
                           "Cingle her TV türüyle kendi dilinde, ev Wi-Fi'ınız üzerinden konuşur.")
    html += cta("tr", up) + "\n</main>" + footer("tr", up)
    write("tr", html)


TR_CARD = {
    "lg": "webOS ve 2012–2013 NetCast",
    "samsung": "2016 sonrası ve 2010–2015 arasının birçoğu",
    "roku": "Roku TV'ler ve oynatıcılar",
    "googletv": "ve Android TV, Chromecast, Shield",
    "firetv": "Stick, Cube ve Fire TV'ler",
    "sony": "Bravia, yaklaşık 2013 sonrası",
    "philips": "Titan OS, Saphi ve eski modeller",
    "panasonic": "Viera, yaklaşık 2012–2024",
    "sharp": "IP kontrollü AQUOS",
    "tcl": "Google TV, Roku ve TCL'nin kendi sistemi",
}


def brand_page_en(b):
    up = "../"
    path = b["slug"] + "/"
    alts = {"en": path}
    for lang, p in b.get("alt", {}).items():
        alts[lang] = p
    alt_path = b.get("alt", {}).get("tr", "tr/")
    html = head("en", f'{b["title"]} · Cingle Remote', b["lead"], path, up, alts if len(alts) > 1 else {})
    html += "\n<body>" + topbar("en", up, alt_path)
    note = f'<p class="note">{b["note"]}</p>' if b.get("note") else ""
    steps = [
        "Turn on the TV and make sure it's on the same Wi-Fi as your iPhone.",
        "Open Cingle. It finds the TV by itself: when iOS asks whether Cingle can find devices on your local network, "
        "tap Allow. You can also add the TV by its IP address, in Settings › Devices › Add a TV by IP address.",
    ]
    pairing = "".join(f"<li>{p}</li>" for p in b["pairing"])
    html += f"""
<main>
<section class="hero hero-brand">
  <div class="wrap hero-in">
    <nav class="crumbs" aria-label="Breadcrumb"><a href="{up}">Cingle Remote</a> <span aria-hidden="true">›</span>
      <span>{b['name']}</span></nav>
    <h1>{b['h1'][0]} <span class="accent">{b['h1'][1]}</span></h1>
    <p class="lead">{b['lead']}</p>
    <div class="hero-cta">{badge("en", b.get("ppid"), up)}<span class="small">Also on iPad, Apple Watch and Mac.
      No ads, ever.</span></div>
  </div>
  <div class="wrap">{video("en", up)}</div>
</section>

<section class="band">
  <div class="wrap split split-shots">
    <div>
      <h2>What you can do on your {b['name']} TV</h2>
      {ticks(b['features'])}
      {note}
    </div>
    {shots(b['shots'], up)}
  </div>
</section>

<section class="band">
  <div class="wrap narrow">
    <h2>Connecting your {b['name']} TV</h2>
    <ol class="steps">{"".join(f"<li>{s}</li>" for s in steps)}<li>Then:<ul class="pairing">{pairing}</ul></li></ol>
  </div>
</section>

<section class="band">
  <div class="wrap cols cols-2">
    <div class="col"><h3>On your Apple Watch</h3><p>{b['watch']}</p></div>
    <div class="col"><h3>On your Mac</h3><p>{b['mac']}</p></div>
  </div>
</section>

<section class="band">
  <div class="wrap">
    <h2>{UI['en']['other_tvs']}</h2>
    {brand_cards(up, current=b['key'])}
    <p class="muted also"><a href="{up}#compatibility">{UI['en']['full_list']}</a>, including Apple TV and the TVs
      that run Google TV, Android TV, Fire TV or Roku.</p>
  </div>
</section>
"""
    html += cta("en", up, b.get("ppid")) + "\n</main>"
    html += footer("en", up)
    write(b["slug"], html)


def brand_page_tr(b):
    up = "../../"
    path = b["slug"] + "/"
    alts = {"tr": path, "en": b["alt"]["en"]}
    desc = b["lead"]
    html = head("tr", f'{b["title"]} · Cingle Remote', desc, path, up, alts)
    html += "\n<body>" + topbar("tr", up, b["alt"]["en"])
    steps = "".join(f"<li>{s}</li>" for s in b["steps"])
    after = "".join(f"<p>{p}</p>" for p in b["pairing_after"])
    others = "".join(f'<a class="card" href="{up}{x["slug"]}/" hreflang="en"><b>{x["name"]}</b>'
                     f'<span>{TR_CARD[x["key"]]}</span></a>' for x in BRANDS if x["key"] != "vestel")
    html += f"""
<main>
<section class="hero hero-brand">
  <div class="wrap hero-in">
    <nav class="crumbs" aria-label="Sayfa yolu"><a href="{up}tr/">Cingle Remote</a> <span aria-hidden="true">›</span>
      <span>Vestel</span></nav>
    <h1>{b['h1'][0]} <span class="accent">{b['h1'][1]}</span></h1>
    <p class="lead">{b['lead']}</p>
    <div class="hero-cta">{badge("tr", b["ppid"], up)}<span class="small">iPad, Apple Watch ve Mac'te de. Hiç reklam
      yok.</span></div>
  </div>
  <div class="wrap">{video("tr", up)}</div>
</section>

<section class="band">
  <div class="wrap split split-shots">
    <div>
      <h2>{b['features_h']}</h2>
      {ticks(b['features'])}
    </div>
    {shots(b['shots'], up)}
  </div>
</section>

<section class="band">
  <div class="wrap narrow">
    <h2>{b['pairing_h']}</h2>
    <ol class="steps">{steps}</ol>
    <div class="muted">{after}</div>
  </div>
</section>

<section class="band">
  <div class="wrap cols cols-2">
    <div class="col"><h3>Apple Watch'ta</h3><p>{b['watch']}</p></div>
    <div class="col"><h3>Mac'te</h3><p>{b['mac']}</p></div>
  </div>
</section>

<section class="band">
  <div class="wrap">
    <h2>{UI['tr']['other_tvs']}</h2>
    <div class="cards">{others}</div>
    <p class="muted also">Bu sayfalar İngilizce. <a href="{up}tr/#compatibility">{UI['tr']['full_list']}</a>.</p>
  </div>
</section>
"""
    html += cta("tr", up, b["ppid"]) + "\n</main>" + footer("tr", up)
    write(b["slug"], html)


def not_found():
    # GitHub Pages serves this for any missing path, at any depth, so it links with absolute paths.
    up = "/cingle-remote/"
    html = head("en", "Page not found · Cingle Remote", "This page isn't here.", "404.html", up, {})
    html = html.replace(f'<link rel="canonical" href="{BASE}/404.html">', '<meta name="robots" content="noindex">')
    html += "\n<body>" + topbar("en", up, "tr/")
    html += f"""
<main>
<section class="hero">
  <div class="wrap hero-in">
    <h1>This page isn't here <span class="accent">Sayfa bulunamadı</span></h1>
    <p class="lead"><a href="{up}">Go to Cingle Remote's home page</a> · <a href="{up}tr/">Ana sayfaya gidin</a></p>
  </div>
</section>
</main>"""
    html += footer("en", up)
    write("404.html", html)


def sitemap():
    pages = [("", {"en": "", "tr": "tr/"}), ("tr/", {"en": "", "tr": "tr/"})]
    for b in BRANDS:
        alts = {"en": b["slug"] + "/", **b.get("alt", {})}
        pages.append((b["slug"] + "/", alts if len(alts) > 1 else {}))
    pages.append((TR_VESTEL["slug"] + "/", {"tr": TR_VESTEL["slug"] + "/", "en": TR_VESTEL["alt"]["en"]}))
    rows = []
    for p, alts in pages:
        links = "".join(f'\n    <xhtml:link rel="alternate" hreflang="{l}" href="{BASE}/{a}"/>' for l, a in alts.items())
        rows.append(f"  <url>\n    <loc>{BASE}/{p}</loc>{links}\n  </url>")
    (OUT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
        + "\n".join(rows) + "\n</urlset>\n", encoding="utf-8")


def main():
    home_en()
    home_tr()
    for b in BRANDS:
        brand_page_en(b)
    brand_page_tr(TR_VESTEL)
    not_found()
    sitemap()
    (OUT / ".nojekyll").write_text("")
    print("Built", len(list(OUT.rglob("*.html"))), "pages into", OUT)


if __name__ == "__main__":
    main()
