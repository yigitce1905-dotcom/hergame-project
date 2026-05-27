"""
HerGame — FM26 Hidden Gems Scraper + SWOT Analysis
=====================================================
SoccerDonna'dan 99 FM26 hidden gem oyuncusunun profilini çeker
ve Google Gemini API ile Türkçe SWOT analizi üretir.

Kullanım (proje kökünden):
  python scraper/hidden_gems_scraper.py
  python scraper/hidden_gems_scraper.py --resume      # kaldığı yerden devam et
  python scraper/hidden_gems_scraper.py --limit 5     # ilk 5 oyuncuyu test et
  python scraper/hidden_gems_scraper.py --no-swot     # SWOT üretimi atla
  python scraper/hidden_gems_scraper.py --swot-only   # sadece SWOT üret (scrape etme)
"""

import argparse
import json
import logging
import random
import re
import sys
import time
import unicodedata
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

import requests
from bs4 import BeautifulSoup

# ── AI Provider API Keys ──────────────────────────────────────────────────────
# Her provider için API key gir. Boş olanlar atlanır.
# Sıra: Gemini → Grok → OpenAI → Claude

GEMINI_API_KEY  = ""   # aistudio.google.com → buraya kendi key'ini yaz
GROK_API_KEY    = ""   # console.x.ai       → buraya kendi key'ini yaz
OPENAI_API_KEY  = ""   # platform.openai.com/api-keys
CLAUDE_API_KEY  = ""   # console.anthropic.com

GEMINI_MODEL = "gemini-flash-latest"
GROK_MODEL   = "grok-3-mini"
OPENAI_MODEL = "gpt-4o-mini"
CLAUDE_MODEL = "claude-haiku-4-5"

# ── Gemini SDK ────────────────────────────────────────────────────────────────
try:
    from google import genai as _genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

# ── Paths ─────────────────────────────────────────────────────────────────────
ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
SRC_DATA_DIR = ROOT / "src" / "data"

CHECKPOINT_PATH  = DATA_DIR / "hidden_gems_checkpoint.json"
OUTPUT_JSON_PATH = DATA_DIR / "hidden_gems.json"
OUTPUT_TS_PATH   = SRC_DATA_DIR / "hidden_gems.ts"
EXISTING_PATH    = DATA_DIR / "players_app.json"

# ── Logging ───────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("hidden_gems")

# ── Constants ─────────────────────────────────────────────────────────────────
BASE_URL   = "https://www.soccerdonna.de"
SEARCH_URL = "https://www.soccerdonna.de/en/suche/detailsuchespieler/suche.html"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9,tr;q=0.8",
    "Referer": "https://www.soccerdonna.de/",
}

COUNTRY_FLAGS = {
    "turkey": "🇹🇷", "england": "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "scotland": "🏴󠁧󠁢󠁳󠁣󠁴󠁿",
    "wales": "🏴󠁧󠁢󠁷󠁬󠁳󠁿", "spain": "🇪🇸", "germany": "🇩🇪",
    "france": "🇫🇷", "usa": "🇺🇸", "united states": "🇺🇸",
    "brazil": "🇧🇷", "norway": "🇳🇴", "sweden": "🇸🇪",
    "denmark": "🇩🇰", "netherlands": "🇳🇱", "australia": "🇦🇺",
    "nigeria": "🇳🇬", "chile": "🇨🇱", "poland": "🇵🇱",
    "portugal": "🇵🇹", "italy": "🇮🇹", "canada": "🇨🇦",
    "japan": "🇯🇵", "china": "🇨🇳", "south korea": "🇰🇷",
    "colombia": "🇨🇴", "argentina": "🇦🇷", "ireland": "🇮🇪",
    "austria": "🇦🇹", "belgium": "🇧🇪", "iceland": "🇮🇸",
    "finland": "🇫🇮", "switzerland": "🇨🇭", "new zealand": "🇳🇿",
    "jamaica": "🇯🇲", "mexico": "🇲🇽", "ghana": "🇬🇭",
    "cameroon": "🇨🇲", "romania": "🇷🇴", "ukraine": "🇺🇦",
    "croatia": "🇭🇷", "serbia": "🇷🇸", "greece": "🇬🇷",
    "hungary": "🇭🇺", "slovenia": "🇸🇮", "montenegro": "🇲🇪",
    "malawi": "🇲🇼", "china pr": "🇨🇳",
}

POSITION_MAP = {
    "goalkeeper": "GK", "torwart": "GK",
    "centre-back": "DF", "center-back": "DF", "left-back": "DF",
    "right-back": "DF", "defender": "DF", "innenverteidiger": "DF",
    "linker verteidiger": "DF", "rechter verteidiger": "DF",
    "defensive midfield": "MF", "central midfield": "MF",
    "attacking midfield": "MF", "left midfield": "MF",
    "right midfield": "MF", "midfield": "MF",
    "centre-forward": "FW", "center-forward": "FW",
    "left winger": "FW", "right winger": "FW",
    "second striker": "FW", "striker": "FW", "forward": "FW",
}


def fm_position_to_code(fm_pos: str) -> str:
    """FM26 pozisyon string → GK/DF/MF/FW"""
    if not fm_pos:
        return "MF"
    p = fm_pos.strip().upper()
    if p.startswith("GK"):
        return "GK"
    if re.match(r"^(D[\s/(]|WB[\s/(]|D/WB)", p):
        return "DF"
    if re.match(r"^ST[\s/(]", p):
        return "FW"
    return "MF"


# ── FM26 Hidden Gems — 99 Oyuncu ──────────────────────────────────────────────
FM26_HIDDEN_GEMS = [
    {"name": "Federica D'Auria",        "fm_position": "D (C)",                     "nationality": "Italy",       "club": "Juventus",               "fm_rating": 90},
    {"name": "Selma Panengstuen",        "fm_position": "GK",                        "nationality": "Norway",      "club": "Brann",                  "fm_rating": 90},
    {"name": "Marthine Østenstad",       "fm_position": "D (C)",                     "nationality": "Norway",      "club": "Eintracht Frankfurt",    "fm_rating": 86},
    {"name": "Mia Authen",               "fm_position": "D (RC)",                    "nationality": "Norway",      "club": "Brann",                  "fm_rating": 85},
    {"name": "Sara Hørte",               "fm_position": "D (C)",                     "nationality": "Norway",      "club": "Vålerenga",              "fm_rating": 84},
    {"name": "Mari Paz Vilas",           "fm_position": "AM (C), ST (C)",            "nationality": "Spain",       "club": "Free Agent",             "fm_rating": 83},
    {"name": "Thea Kyvåg",              "fm_position": "M/AM (L)",                  "nationality": "Norway",      "club": "Milan",                  "fm_rating": 83},
    {"name": "Amy Gallacher",            "fm_position": "M/AM (RC)",                 "nationality": "Scotland",    "club": "Celtic",                 "fm_rating": 83},
    {"name": "Monique Ngock",            "fm_position": "DM, M (C)",                 "nationality": "Cameroon",    "club": "FC Fleury 91",           "fm_rating": 82},
    {"name": "Emma Braut Brunes",        "fm_position": "D (C)",                     "nationality": "Norway",      "club": "Brøndby IF",             "fm_rating": 82},
    {"name": "Alena Bienz",              "fm_position": "AM (RC), ST (C)",           "nationality": "Switzerland", "club": "SC Freiburg",            "fm_rating": 81},
    {"name": "Joanna Tynnilä",           "fm_position": "D (C)",                     "nationality": "Finland",     "club": "Brann",                  "fm_rating": 81},
    {"name": "Astrid Gilardi",           "fm_position": "GK",                        "nationality": "Italy",       "club": "Como Women",             "fm_rating": 81},
    {"name": "Hillary Diaz",             "fm_position": "D (C)",                     "nationality": "France",      "club": "Inter Milan",            "fm_rating": 80},
    {"name": "Annaëlle Tchakounté",     "fm_position": "D (C)",                     "nationality": "France",      "club": "Strasbourg",             "fm_rating": 80},
    {"name": "Lilli Purtscheller",       "fm_position": "M/AM (R)",                  "nationality": "Austria",     "club": "SGS Essen",              "fm_rating": 80},
    {"name": "Holly Ward",               "fm_position": "AM (R), ST (C)",            "nationality": "Canada",      "club": "Vancouver Rise",         "fm_rating": 79},
    {"name": "Fiona Gaißer",            "fm_position": "DM, M (C)",                 "nationality": "Germany",     "club": "Carl Zeiss Jena",        "fm_rating": 79},
    {"name": "Elin Sørum",              "fm_position": "D (C), DM, M/AM (C)",       "nationality": "Norway",      "club": "Rosenborg",              "fm_rating": 78},
    {"name": "Elise Thorsnes",           "fm_position": "D (C), ST (C)",             "nationality": "Norway",      "club": "Vålerenga",              "fm_rating": 78},
    {"name": "Beke Sterner",             "fm_position": "D/WB (R)",                  "nationality": "Germany",     "club": "SGS Essen",              "fm_rating": 78},
    {"name": "Julie Jorde",              "fm_position": "DM, M (C)",                 "nationality": "Norway",      "club": "Brøndby IF",             "fm_rating": 78},
    {"name": "Manon Wahl",               "fm_position": "GK",                        "nationality": "France",      "club": "Strasbourg",             "fm_rating": 78},
    {"name": "Anna Aahjem",              "fm_position": "ST (C)",                    "nationality": "Norway",      "club": "Brann",                  "fm_rating": 78},
    {"name": "Josefine Birkelund",       "fm_position": "D (RC), WB (R)",            "nationality": "Norway",      "club": "Brann",                  "fm_rating": 77},
    {"name": "Mille Ivi Christensen",    "fm_position": "DM, M/AM (C)",              "nationality": "Norway",      "club": "LSK",                    "fm_rating": 77},
    {"name": "Synne Aunehaugen",         "fm_position": "D (C)",                     "nationality": "Norway",      "club": "Rosenborg",              "fm_rating": 77},
    {"name": "Karoline Haugland",        "fm_position": "DM, M (C)",                 "nationality": "Norway",      "club": "Brann",                  "fm_rating": 77},
    {"name": "Stine Brekken",            "fm_position": "DM, M (C)",                 "nationality": "Norway",      "club": "Vålerenga",              "fm_rating": 77},
    {"name": "Eline Hegg",               "fm_position": "WB (R), M (RC), AM (RLC)",  "nationality": "Norway",      "club": "Vålerenga",              "fm_rating": 77},
    {"name": "Jelena Karličić",         "fm_position": "D (RL), AM (R)",            "nationality": "Montenegro",  "club": "Fatih Vatan Spor",       "fm_rating": 76},
    {"name": "Aurora Mikalsen",          "fm_position": "GK",                        "nationality": "Norway",      "club": "1. FC Köln",             "fm_rating": 76},
    {"name": "Sunniva Skoglund",         "fm_position": "GK",                        "nationality": "Norway",      "club": "Stabæk",                 "fm_rating": 76},
    {"name": "Sofia Reidy",              "fm_position": "D (RLC)",                   "nationality": "Sweden",      "club": "Hammarby IF",            "fm_rating": 75},
    {"name": "Maïté Boucly",            "fm_position": "D/WB/M/AM (L), ST (C)",     "nationality": "France",      "club": "Havre FC",               "fm_rating": 75},
    {"name": "Maja Sternad",             "fm_position": "M (L), AM (RL)",            "nationality": "Slovenia",    "club": "SV Werder Bremen",       "fm_rating": 75},
    {"name": "Monica Renzotti",          "fm_position": "M/AM (R)",                  "nationality": "Italy",       "club": "Milan",                  "fm_rating": 75},
    {"name": "Poppy Lawson",             "fm_position": "D (C)",                     "nationality": "England",     "club": "Hibernian",              "fm_rating": 74},
    {"name": "Julia Magerl",             "fm_position": "D (C)",                     "nationality": "Austria",     "club": "RB Leipzig",             "fm_rating": 74},
    {"name": "Selma Pettersen",          "fm_position": "D (LC)",                    "nationality": "Norway",      "club": "Vålerenga",              "fm_rating": 74},
    {"name": "Julia Pollak",             "fm_position": "D/WB (L)",                  "nationality": "Germany",     "club": "1. FC Nürnberg",         "fm_rating": 74},
    {"name": "Maja Hagermann",           "fm_position": "DM, M (LC)",                "nationality": "Denmark",     "club": "Sassuolo",               "fm_rating": 74},
    {"name": "Duda Serrana",             "fm_position": "AM (C)",                    "nationality": "Brazil",      "club": "São Paulo",              "fm_rating": 73},
    {"name": "Emma Reshane",             "fm_position": "D (RL), WB (L), M/AM (RL)","nationality": "Norway",      "club": "LSK",                    "fm_rating": 71},
    {"name": "Lucie Calba",              "fm_position": "AM (LC), ST (C)",           "nationality": "France",      "club": "FC Nantes",              "fm_rating": 71},
    {"name": "Laura Pucks",              "fm_position": "D (C)",                     "nationality": "Germany",     "club": "SGS Essen",              "fm_rating": 71},
    {"name": "Léa Notel",               "fm_position": "D (LC)",                    "nationality": "France",      "club": "Free Agent",             "fm_rating": 71},
    {"name": "Maria Grazia Petrara",     "fm_position": "M (C)",                     "nationality": "Italy",       "club": "Ternana Women",          "fm_rating": 71},
    {"name": "Jenna Ferguson",           "fm_position": "D (C)",                     "nationality": "Scotland",    "club": "Partick Thistle",        "fm_rating": 70},
    {"name": "Macey Fraser",             "fm_position": "M/AM (C)",                  "nationality": "New Zealand", "club": "Wellington Phoenix",     "fm_rating": 70},
    {"name": "Silje Helgesen",           "fm_position": "D (C)",                     "nationality": "Norway",      "club": "Stabæk",                 "fm_rating": 70},
    {"name": "Tuana Mahmoud",            "fm_position": "M/AM (L)",                  "nationality": "Germany",     "club": "SV Werder Bremen",       "fm_rating": 70},
    {"name": "Azzurra Gallo",            "fm_position": "D (C)",                     "nationality": "Italy",       "club": "Juventus",               "fm_rating": 69},
    {"name": "Solveig Slemmem",          "fm_position": "D/WB (RL)",                 "nationality": "Norway",      "club": "Lyn",                    "fm_rating": 69},
    {"name": "Nikayla Small",            "fm_position": "M (RC), AM (C)",            "nationality": "Canada",      "club": "AFC Toronto",            "fm_rating": 69},
    {"name": "Natalia Oleszkiewicz",     "fm_position": "ST (C)",                    "nationality": "Poland",      "club": "Trabzonspor",            "fm_rating": 69},
    {"name": "Laurel Ansbrow",           "fm_position": "D (C)",                     "nationality": "USA",         "club": "Boston Legacy",          "fm_rating": 68},
    {"name": "Ilayda Açıkgöz",         "fm_position": "M/AM (C)",                  "nationality": "Germany",     "club": "Eintracht Frankfurt",    "fm_rating": 68},
    {"name": "Ronja Arnesen",            "fm_position": "WB (R), M (RC), AM (RLC)",  "nationality": "Norway",      "club": "Vålerenga",              "fm_rating": 68},
    {"name": "Nelly Da Cruz Rodrigues",  "fm_position": "D (RC), WB (R)",            "nationality": "Portugal",    "club": "FC Nantes",              "fm_rating": 67},
    {"name": "Katja Skupień",           "fm_position": "WB/M/AM (RL)",              "nationality": "Poland",      "club": "Sassuolo",               "fm_rating": 67},
    {"name": "Bente Fischer",            "fm_position": "D (LC)",                    "nationality": "Germany",     "club": "Carl Zeiss Jena",        "fm_rating": 67},
    {"name": "Bruna Ramos",              "fm_position": "D/WB (R)",                  "nationality": "Portugal",    "club": "Torreense",              "fm_rating": 67},
    {"name": "Julia Jędrzejewska",      "fm_position": "D/WB/M (R)",                "nationality": "Poland",      "club": "Śląsk Wrocław",          "fm_rating": 67},
    {"name": "Meret Günster",           "fm_position": "DM, M (C)",                 "nationality": "Germany",     "club": "1. FC Nürnberg",         "fm_rating": 67},
    {"name": "Kristin Krammer",          "fm_position": "GK",                        "nationality": "Austria",     "club": "1. FC Nürnberg",         "fm_rating": 67},
    {"name": "Hannah Mesch",             "fm_position": "M (L), AM (RL)",            "nationality": "Germany",     "club": "Carl Zeiss Jena",        "fm_rating": 67},
    {"name": "Magnaba Folquet",          "fm_position": "M/AM (C)",                  "nationality": "France",      "club": "Havre FC",               "fm_rating": 67},
    {"name": "Carla Tays",               "fm_position": "D (C)",                     "nationality": "Brazil",      "club": "Palmeiras",              "fm_rating": 66},
    {"name": "Natalia Radkiewicz",       "fm_position": "GK",                        "nationality": "Poland",      "club": "Pogoń Szczecin",         "fm_rating": 66},
    {"name": "Paula Flach",              "fm_position": "D (L)",                     "nationality": "Germany",     "club": "SGS Essen",              "fm_rating": 65},
    {"name": "Clara Wibaut",             "fm_position": "GK",                        "nationality": "France",      "club": "Reims",                  "fm_rating": 65},
    {"name": "Diána Németh",            "fm_position": "D/WB (L)",                  "nationality": "Hungary",     "club": "RB Leipzig",             "fm_rating": 65},
    {"name": "Adriana Achcińska",       "fm_position": "DM, M (C)",                 "nationality": "Poland",      "club": "1. FC Köln",             "fm_rating": 65},
    {"name": "Rebekka Salfelder",        "fm_position": "WB/M (L)",                  "nationality": "Germany",     "club": "Free Agent",             "fm_rating": 65},
    {"name": "Nina Varga",               "fm_position": "D (C)",                     "nationality": "Croatia",     "club": "Medimurje",              "fm_rating": 64},
    {"name": "Ana Sušak",               "fm_position": "D/WB/M (R)",                "nationality": "Croatia",     "club": "Agram",                  "fm_rating": 64},
    {"name": "Julie Swierot",            "fm_position": "DM, M (C)",                 "nationality": "France",      "club": "OLL",                    "fm_rating": 64},
    {"name": "Nina Kajzba",              "fm_position": "ST (C)",                    "nationality": "Slovenia",    "club": "Parma Calcio",           "fm_rating": 64},
    {"name": "Reese Tappan",             "fm_position": "D (C)",                     "nationality": "USA",         "club": "Spokane",                "fm_rating": 64},
    {"name": "Julia Mickenhagen",        "fm_position": "D/WB (L)",                  "nationality": "Germany",     "club": "Bayer 04 Leverkusen",    "fm_rating": 64},
    {"name": "Rose Kadzere",             "fm_position": "AM (R), ST (C)",            "nationality": "Malawi",      "club": "Montpellier",            "fm_rating": 63},
    {"name": "Barbara Živković",        "fm_position": "DM, M (RC), AM (R)",        "nationality": "Croatia",     "club": "Hadjuk",                 "fm_rating": 63},
    {"name": "Manuela Sciabica",         "fm_position": "DM, M (RLC), AM (RL)",     "nationality": "Italy",       "club": "Juventus",               "fm_rating": 63},
    {"name": "Fanney Birkisdóttir",     "fm_position": "GK",                        "nationality": "Iceland",     "club": "BK Häcken",              "fm_rating": 63},
    {"name": "Shukurath Oladipo",        "fm_position": "D (C)",                     "nationality": "Nigeria",     "club": "Roma",                   "fm_rating": 62},
    {"name": "Mana Lamine",              "fm_position": "AM (R), ST (C)",            "nationality": "Cameroon",    "club": "Free Agent",             "fm_rating": 62},
    {"name": "Melina Reuter",            "fm_position": "M (R), AM (RL), ST (C)",    "nationality": "Germany",     "club": "Carl Zeiss Jena",        "fm_rating": 60},
    {"name": "Ellie Gilbert",            "fm_position": "DM, M (C)",                 "nationality": "USA",         "club": "DC Power FC",            "fm_rating": 60},
    {"name": "Manon Le Page",            "fm_position": "GK",                        "nationality": "France",      "club": "Strasbourg",             "fm_rating": 60},
    {"name": "Sofia Määttä",            "fm_position": "M/AM (RL)",                 "nationality": "Finland",     "club": "Glasgow City",           "fm_rating": 59},
    {"name": "Savanna Duffy",            "fm_position": "GK",                        "nationality": "Norway",      "club": "Kolbotn",                "fm_rating": 57},
    {"name": "Carina Wik Alfredsen",     "fm_position": "DM, M (C)",                 "nationality": "Norway",      "club": "LSK",                    "fm_rating": 57},
    {"name": "Liu Yanqiu",               "fm_position": "D/WB/M/AM (RL)",            "nationality": "China",       "club": "WH VV Jianghan Uni. FC", "fm_rating": 55},
    {"name": "Jasmin Mansaray",          "fm_position": "D (RC)",                    "nationality": "Finland",     "club": "LSK",                    "fm_rating": 53},
    {"name": "Jo-Anne Conquist",         "fm_position": "D (C), DM",                "nationality": "Sweden",      "club": "FC Rosengård",           "fm_rating": 52},
    {"name": "Carolina Pimenta",         "fm_position": "D (RLC), WB (RL), M (C)",  "nationality": "Portugal",    "club": "Sporting CP B",          "fm_rating": 52},
    {"name": "Magdalena Sobal",          "fm_position": "ST (C)",                    "nationality": "Poland",      "club": "Juventus",               "fm_rating": 51},
    {"name": "Angel Gurhem",             "fm_position": "M (L)",                     "nationality": "France",      "club": "Free Agent",             "fm_rating": 50},
]


# ── Helpers ───────────────────────────────────────────────────────────────────
def normalize_name(name: str) -> str:
    """Küçük harfe çevir ve aksanları kaldır."""
    nfkd = unicodedata.normalize("NFD", name)
    ascii_str = "".join(c for c in nfkd if unicodedata.category(c) != "Mn")
    return ascii_str.lower().strip()


def name_similarity(a: str, b: str) -> float:
    """İki isim arasındaki kelime örtüşme skoru (Jaccard)."""
    a_words = set(normalize_name(a).split())
    b_words = set(normalize_name(b).split())
    if not a_words or not b_words:
        return 0.0
    intersection = len(a_words & b_words)
    union = len(a_words | b_words)
    return intersection / union


def best_match(target: str, candidates: list[dict], threshold: float = 0.5) -> Optional[dict]:
    """En iyi isim eşleşmesini bul. Skor threshold'un altındaysa None döner."""
    best_score = 0.0
    best = None
    for c in candidates:
        score = name_similarity(target, c["name"])
        if score > best_score:
            best_score = score
            best = c
    if best and best_score >= threshold:
        return best
    return None


# ── Scraper ───────────────────────────────────────────────────────────────────
class HiddenGemsScraper:
    def __init__(self, delay: float = 2.0, jitter: float = 1.0):
        self.delay = delay
        self.jitter = jitter
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
        self._warm_up()

        # Mevcut TUR1 oyuncularını yükle (çift scrape'den kaçın)
        self.existing: dict[str, dict] = {}
        if EXISTING_PATH.exists():
            try:
                data = json.loads(EXISTING_PATH.read_text("utf-8"))
                for p in data:
                    key = normalize_name(p.get("name", ""))
                    if key:
                        self.existing[key] = p
                log.info("Mevcut %d TUR1 oyuncusu yüklendi.", len(self.existing))
            except Exception as e:
                log.warning("players_app.json yüklenemedi: %s", e)

        # Gemini başlat
        self.gemini_client = None
        if GEMINI_AVAILABLE:
            self.gemini_client = _genai.Client(api_key=GEMINI_API_KEY)
            log.info("Gemini API hazır. Model: %s", GEMINI_MODEL)
        else:
            log.warning("google-genai bulunamadı! pip install google-genai")

    def _warm_up(self):
        try:
            r = self.session.get(BASE_URL + "/", timeout=15)
            log.info("Session warm-up: HTTP %s", r.status_code)
            time.sleep(1)
        except Exception as exc:
            log.warning("Warm-up başarısız: %s", exc)

    def _wait(self):
        time.sleep(self.delay + random.uniform(0, self.jitter))

    def _get(self, url: str, retries: int = 3) -> Optional[BeautifulSoup]:
        for attempt in range(1, retries + 1):
            self._wait()
            try:
                r = self.session.get(url, timeout=25)
                if r.status_code == 200:
                    return BeautifulSoup(r.text, "lxml")
                elif r.status_code == 429:
                    backoff = 90 * attempt
                    log.warning("Rate-limit (429). %ds bekleniyor…", backoff)
                    time.sleep(backoff)
                else:
                    log.warning("HTTP %s — %s (deneme %d/%d)", r.status_code, url, attempt, retries)
            except requests.RequestException as exc:
                log.warning("İstek hatası (deneme %d/%d): %s", attempt, retries, exc)
        return None

    # ── SoccerDonna Arama ─────────────────────────────────────────────────────
    def search_by_firstname(self, first_name: str) -> list[dict]:
        """Sadece ad ile arama yapar (SoccerDonna birleşik aramada 0 sonuç veriyor)."""
        self._wait()
        try:
            r = self.session.post(
                SEARCH_URL,
                data={"vorname": first_name},
                timeout=20,
            )
            soup = BeautifulSoup(r.text, "lxml")
            results = []
            seen = set()
            for a in soup.find_all("a", href=re.compile(r"/profil/spieler_\d+")):
                name = a.get_text(strip=True)
                href = a["href"]
                if name and href not in seen:
                    seen.add(href)
                    full_url = BASE_URL + href if href.startswith("/") else href
                    results.append({"name": name, "url": full_url})
            return results
        except Exception as exc:
            log.warning("Arama hatası (%s): %s", first_name, exc)
            return []

    # ── Profil Çekme ──────────────────────────────────────────────────────────
    def scrape_profile(self, url: str, gem: dict) -> dict:
        """Oyuncu profilini SoccerDonna'dan çek."""
        soup = self._get(url)
        if not soup:
            return {}

        data: dict = {
            "soccerdonna_url": url,
            "soccerdonna_id": "",
            "name": gem["name"],
            "club": gem["club"],
            "nationality": gem["nationality"],
            "league": "",
            "league_code": "",
            "position": fm_position_to_code(gem["fm_position"]),
            "position_detail": gem["fm_position"],
            "age": None,
            "born": "",
            "birth_place": "",
            "height": "",
            "foot": "",
            "goals": 0,
            "assists": 0,
            "appearances": 0,
            "yellow_cards": 0,
            "red_cards": 0,
            "caps": 0,
            "national_team": "",
            "national_goals": 0,
            "market_value": "N/A",
            "market_value_num": 0,
            "photo_url": "",
            "bio": "",
            "transfers": [],
            "achievements": [],
        }

        # ID
        m = re.search(r"spieler_(\d+)", url)
        if m:
            data["soccerdonna_id"] = m.group(1)

        # İsim
        for sel in ["h1", ".spielername"]:
            el = soup.select_one(sel)
            if el:
                raw = el.get_text(" ", strip=True)
                raw = re.sub(r"^\s*\d{1,2}\s+", "", raw).strip()
                if raw:
                    data["name"] = raw
                    break

        # Fotoğraf
        for img in soup.find_all("img", src=True):
            src: str = img["src"]
            if "spielerfotos" in src and "somebody" not in src:
                data["photo_url"] = src
                break
        if not data["photo_url"]:
            for img in soup.find_all("img", {"data-src": True}):
                src: str = img["data-src"]
                if "spielerfotos" in src and "somebody" not in src:
                    data["photo_url"] = src
                    break

        # Bilgi tablosu (tabelle_grafik)
        tbl = soup.find("table", class_="tabelle_grafik")
        if tbl:
            for row in tbl.find_all("tr")[1:]:
                cells = row.find_all(["th", "td"])
                if len(cells) >= 2:
                    label = cells[0].get_text(" ", strip=True).rstrip(":").strip().lower()
                    val   = cells[1].get_text(" ", strip=True)
                    self._apply_label(label, val, data)

        # Milli takım
        header_tbl = soup.find("table", class_="tabelle_spieler")
        if header_tbl:
            rows = header_tbl.find_all("tr")
            if len(rows) >= 3:
                cell_text = rows[2].get_text(" ", strip=True)
                m2 = re.search(r"(?:current national player|national)[\s:]+(.+)", cell_text, re.IGNORECASE)
                if m2:
                    nat = m2.group(1).strip()
                    if nat and nat.lower() not in ("nein", "no", "-"):
                        data["national_team"] = nat

        # Caps (milli maç)
        all_tbls = soup.find_all("table", class_="tabelle_spieler")
        if len(all_tbls) >= 2:
            nat_tbl = all_tbls[1]
            total_apps = total_goals = 0
            for row in nat_tbl.find_all("tr")[1:]:
                cells = row.find_all("td")
                nums = []
                for c in cells:
                    t = c.get_text(strip=True).replace(".", "").replace(",", "")
                    try:
                        nums.append(int(t))
                    except ValueError:
                        pass
                if len(nums) >= 2:
                    total_apps  += nums[-2]
                    total_goals += nums[-1]
            if total_apps > 0:
                data["caps"] = total_apps
                data["national_goals"] = total_goals

        # Sezon istatistikleri
        std_tables = soup.find_all("table", class_="standard_tabelle")
        if std_tables:
            club_tbl = std_tables[0]
            ta = tg = tas = ty = tr = 0
            for row in club_tbl.find_all("tr")[1:]:
                cells = row.find_all("td")
                nums = []
                for c in cells:
                    t = c.get_text(strip=True).replace(".", "").replace(",", "")
                    try:
                        nums.append(int(t))
                    except ValueError:
                        pass
                if len(nums) >= 1: ta  += nums[0]
                if len(nums) >= 2: tg  += nums[1]
                if len(nums) >= 3: tas += nums[2]
                if len(nums) >= 4: ty  += nums[3]
                if len(nums) >= 5: tr  += nums[4]
            data["appearances"] = ta
            data["goals"]       = tg
            data["assists"]     = tas
            data["yellow_cards"] = ty
            data["red_cards"]   = tr

        # Transfer geçmişi
        for table in soup.find_all("table"):
            cls = " ".join(table.get("class", []))
            if "transfer" in cls.lower():
                for row in table.find_all("tr"):
                    cells = row.find_all("td")
                    if len(cells) >= 3:
                        year = cells[0].get_text(strip=True)
                        from_club = cells[-2].get_text(strip=True)
                        to_club   = cells[-1].get_text(strip=True)
                        if year and re.match(r"\d{4}", year):
                            data["transfers"].append({"year": year, "from": from_club, "to": to_club})
                break

        # Flag
        data["flag"] = COUNTRY_FLAGS.get(data["nationality"].lower(), "🌍")
        if not data["national_team"]:
            data["national_team"] = data["nationality"]

        return data

    def _apply_label(self, label: str, val: str, data: dict):
        """Tablo etiketi → veri alanı."""
        if not val or not label:
            return
        if label in ("date of birth", "geboren", "birthday", "birth date"):
            if not data["born"]:
                dm = re.search(r"(\d{1,2})[./](\d{1,2})[./](\d{4})", val)
                if dm:
                    data["born"] = f"{dm.group(1).zfill(2)}.{dm.group(2).zfill(2)}.{dm.group(3)}"
                else:
                    data["born"] = val.strip()
            if data["age"] is None:
                ym = re.search(r"\b(19|20)\d{2}\b", val)
                if ym:
                    from datetime import date
                    data["age"] = date.today().year - int(ym.group(0))
        elif label in ("place of birth", "geburtsort", "birth place", "birthplace"):
            if not data["birth_place"]:
                data["birth_place"] = val.strip()
        elif label in ("nationality", "nationalität", "citizenship"):
            if not data["nationality"]:
                parts = val.strip().split()
                data["nationality"] = parts[0] if parts else val.strip()
        elif label in ("height", "größe", "size"):
            if not data["height"]:
                hm = re.search(r"1[,.](\d{2})", val)
                if hm:
                    data["height"] = f"1{hm.group(1)} cm"
                else:
                    digits = re.sub(r"[^\d]", "", val)
                    if digits:
                        data["height"] = f"{digits} cm"
        elif label in ("foot", "fuß", "strong foot", "preferred foot"):
            if not data["foot"]:
                data["foot"] = val.strip().capitalize()
        elif label in ("position", "spielposition"):
            raw_pos = val.strip()
            if not data.get("position_detail"):
                data["position_detail"] = raw_pos
            k = raw_pos.lower()
            mapped = POSITION_MAP.get(k)
            if mapped:
                data["position"] = mapped
            else:
                if "keeper" in k or "torwart" in k:
                    data["position"] = "GK"
                elif any(x in k for x in ("back", "defender", "vertei")):
                    data["position"] = "DF"
                elif any(x in k for x in ("forward", "striker", "stürmer", "winger")):
                    data["position"] = "FW"
        elif label in ("market value", "marktwert"):
            if not data["market_value"] or data["market_value"] == "N/A":
                if val.lower() not in ("unknown", "unbekannt", "-", ""):
                    data["market_value"] = val.strip()
                    mvm = re.search(r"([\d,.]+)\s*([mk])", val, re.IGNORECASE)
                    if mvm:
                        try:
                            num = float(mvm.group(1).replace(",", "."))
                            s = mvm.group(2).lower()
                            data["market_value_num"] = num * 1_000_000 if s == "m" else num * 1_000
                        except ValueError:
                            pass

    # ── SWOT Prompt Builder ───────────────────────────────────────────────────
    def _build_swot_prompt(self, player: dict, gem: dict) -> str:
        pos_label = {
            "GK": "Kaleci", "DF": "Defans Oyuncusu",
            "MF": "Orta Saha Oyuncusu", "FW": "Forvet",
        }.get(player.get("position", "MF"), "Futbolcu")
        return (
            f"Sen bir kadın futbolu scout ve analisti olarak görev yapıyorsun.\n"
            f"Aşağıdaki kadın futbolcusu için kapsamlı bir SWOT analizi yaz.\n"
            f"Tüm maddeleri TÜRKÇE olarak yaz. Her madde kısa (1-2 cümle) ve somut olsun.\n\n"
            f"OYUNCU BİLGİLERİ:\n"
            f"- Ad Soyad: {player.get('name', gem['name'])}\n"
            f"- Pozisyon: {pos_label} ({gem['fm_position']})\n"
            f"- Milliyet: {player.get('nationality', gem['nationality'])}\n"
            f"- Kulüp: {player.get('club', gem['club'])}\n"
            f"- FM26 Scout Notu: {gem['fm_rating']}/100\n"
            f"- Yaş: {player.get('age') or 'Bilinmiyor'}\n"
            f"- Boy: {player.get('height') or 'Bilinmiyor'}\n"
            f"- Tercih Ayak: {player.get('foot') or 'Bilinmiyor'}\n"
            f"- Sezon: {player.get('appearances', 0)} maç, {player.get('goals', 0)} gol, {player.get('assists', 0)} asist\n\n"
            f"Her kategori için tam olarak 3 madde yaz.\n"
            f"Sadece JSON formatında yanıt ver, başka hiçbir şey yazma:\n"
            f'{{\"strengths\": [\"m1\",\"m2\",\"m3\"], \"weaknesses\": [\"m1\",\"m2\",\"m3\"], \"opportunities\": [\"m1\",\"m2\",\"m3\"], \"threats\": [\"m1\",\"m2\",\"m3\"]}}'
        )

    def _parse_swot_json(self, text: str, model: str) -> Optional[dict]:
        """Ham metin içinden SWOT JSON'ını çıkar ve doğrula."""
        json_match = re.search(r"\{[\s\S]+\}", text)
        if not json_match:
            return None
        try:
            swot_data = json.loads(json_match.group())
            for key in ("strengths", "weaknesses", "opportunities", "threats"):
                if key not in swot_data or not isinstance(swot_data[key], list):
                    return None
            swot_data["generated_at"] = datetime.now(timezone.utc).isoformat()
            swot_data["model"] = model
            return swot_data
        except json.JSONDecodeError:
            return None

    # ── Gemini ────────────────────────────────────────────────────────────────
    def _swot_gemini(self, prompt: str) -> Optional[dict]:
        if not self.gemini_client:
            return None
        try:
            time.sleep(2)
            resp = self.gemini_client.models.generate_content(model=GEMINI_MODEL, contents=prompt)
            result = self._parse_swot_json(resp.text, GEMINI_MODEL)
            if result:
                log.info("    ✓ Gemini SWOT üretildi.")
            return result
        except Exception as e:
            err = str(e)
            if "PerDay" in err or "per_day" in err.lower():
                log.warning("    ⛔ Gemini günlük limit aşıldı → sonraki provider'a geçiliyor.")
                self.gemini_daily_limit = True   # flag: bu oturumda Gemini'yi atlayalım
            elif "429" in err or "quota" in err.lower():
                log.warning("    ⚠ Gemini rate limit (dakikalık) — 15s bekleniyor.")
                time.sleep(15)
            else:
                log.warning("    Gemini hatası: %s", err[:80])
            return None

    # ── Grok (xAI) ────────────────────────────────────────────────────────────
    def _swot_grok(self, prompt: str) -> Optional[dict]:
        if not GROK_API_KEY:
            return None
        try:
            time.sleep(1.5)
            r = self.session.post(
                "https://api.x.ai/v1/chat/completions",
                headers={"Authorization": f"Bearer {GROK_API_KEY}", "Content-Type": "application/json"},
                json={"model": GROK_MODEL, "messages": [{"role": "user", "content": prompt}], "max_tokens": 800},
                timeout=30,
            )
            if r.status_code == 200:
                text = r.json()["choices"][0]["message"]["content"]
                result = self._parse_swot_json(text, GROK_MODEL)
                if result:
                    log.info("    ✓ Grok SWOT üretildi.")
                return result
            elif r.status_code == 429:
                err_body = r.text[:200]
                if "day" in err_body.lower():
                    log.warning("    ⛔ Grok günlük limit → sonraki provider.")
                    self.grok_daily_limit = True
                else:
                    log.warning("    ⚠ Grok rate limit — 15s bekleniyor.")
                    time.sleep(15)
            else:
                log.warning("    Grok HTTP %s: %s", r.status_code, r.text[:80])
        except Exception as e:
            log.warning("    Grok hatası: %s", str(e)[:80])
        return None

    # ── OpenAI ────────────────────────────────────────────────────────────────
    def _swot_openai(self, prompt: str) -> Optional[dict]:
        if not OPENAI_API_KEY:
            return None
        try:
            time.sleep(1.5)
            r = self.session.post(
                "https://api.openai.com/v1/chat/completions",
                headers={"Authorization": f"Bearer {OPENAI_API_KEY}", "Content-Type": "application/json"},
                json={"model": OPENAI_MODEL, "messages": [{"role": "user", "content": prompt}], "max_tokens": 800},
                timeout=30,
            )
            if r.status_code == 200:
                text = r.json()["choices"][0]["message"]["content"]
                result = self._parse_swot_json(text, OPENAI_MODEL)
                if result:
                    log.info("    ✓ OpenAI SWOT üretildi.")
                return result
            elif r.status_code == 429:
                err_body = r.text[:200]
                if "day" in err_body.lower():
                    log.warning("    ⛔ OpenAI günlük limit → sonraki provider.")
                    self.openai_daily_limit = True
                else:
                    log.warning("    ⚠ OpenAI rate limit — 15s bekleniyor.")
                    time.sleep(15)
            else:
                log.warning("    OpenAI HTTP %s: %s", r.status_code, r.text[:80])
        except Exception as e:
            log.warning("    OpenAI hatası: %s", str(e)[:80])
        return None

    # ── Claude (Anthropic) ────────────────────────────────────────────────────
    def _swot_claude(self, prompt: str) -> Optional[dict]:
        if not CLAUDE_API_KEY:
            return None
        try:
            time.sleep(1.5)
            r = self.session.post(
                "https://api.anthropic.com/v1/messages",
                headers={
                    "x-api-key": CLAUDE_API_KEY,
                    "anthropic-version": "2023-06-01",
                    "Content-Type": "application/json",
                },
                json={
                    "model": CLAUDE_MODEL,
                    "max_tokens": 800,
                    "messages": [{"role": "user", "content": prompt}],
                },
                timeout=30,
            )
            if r.status_code == 200:
                text = r.json()["content"][0]["text"]
                result = self._parse_swot_json(text, CLAUDE_MODEL)
                if result:
                    log.info("    ✓ Claude SWOT üretildi.")
                return result
            elif r.status_code == 429:
                err_body = r.text[:200]
                if "day" in err_body.lower():
                    log.warning("    ⛔ Claude günlük limit → tüm provider'lar bitti.")
                    self.claude_daily_limit = True
                else:
                    log.warning("    ⚠ Claude rate limit — 15s bekleniyor.")
                    time.sleep(15)
            else:
                log.warning("    Claude HTTP %s: %s", r.status_code, r.text[:80])
        except Exception as e:
            log.warning("    Claude hatası: %s", str(e)[:80])
        return None

    # ── Ana SWOT — Sırayla dener ──────────────────────────────────────────────
    def generate_swot(self, player: dict, gem: dict) -> Optional[dict]:
        """Gemini → Grok → OpenAI → Claude sırasıyla dener."""
        prompt = self._build_swot_prompt(player, gem)

        providers = [
            ("Gemini", lambda: None if getattr(self, "gemini_daily_limit", False) else self._swot_gemini(prompt)),
            ("Grok",   lambda: None if getattr(self, "grok_daily_limit",   False) else self._swot_grok(prompt)),
            ("OpenAI", lambda: None if getattr(self, "openai_daily_limit", False) else self._swot_openai(prompt)),
            ("Claude", lambda: None if getattr(self, "claude_daily_limit", False) else self._swot_claude(prompt)),
        ]

        for name, fn in providers:
            result = fn()
            if result:
                return result
            # Eğer bu provider daily limit değilse kısa bir retry dene
            # (zaten _swot_* fonksiyonları retry yapıyor, burada sadece fallback)

        log.warning("    ⛔ Tüm provider'lar başarısız veya limitli. SWOT atlandı.")
        return None

    # ── Ana Döngü ─────────────────────────────────────────────────────────────
    def run(
        self,
        limit: Optional[int] = None,
        resume: bool = False,
        no_swot: bool = False,
        swot_only: bool = False,
    ) -> list[dict]:
        DATA_DIR.mkdir(parents=True, exist_ok=True)

        # Veri yükle: önce checkpoint, yoksa hidden_gems.json
        completed_names: set[str] = set()
        results: list[dict] = []
        if resume and CHECKPOINT_PATH.exists():
            try:
                ckpt = json.loads(CHECKPOINT_PATH.read_text("utf-8"))
                completed_names = set(ckpt.get("completed", []))
                results = ckpt.get("players", [])
                log.info("Checkpoint yüklendi: %d oyuncu.", len(completed_names))
            except Exception as e:
                log.warning("Checkpoint yüklenemedi: %s", e)
        elif (swot_only or resume) and OUTPUT_JSON_PATH.exists():
            # Checkpoint yok ama JSON var → JSON'dan yükle
            try:
                results = json.loads(OUTPUT_JSON_PATH.read_text("utf-8"))
                completed_names = set(p["name"] for p in results if not swot_only or p.get("swot"))
                # swot_only: SWOT'u olan oyuncuları "tamamlandı" say, olmayanları yeniden işle
                if swot_only:
                    swot_done = {p["name"] for p in results if p.get("swot")}
                    swot_missing = {p["name"] for p in results if not p.get("swot")}
                    log.info("hidden_gems.json'dan yüklendi: %d SWOT var, %d eksik.",
                             len(swot_done), len(swot_missing))
                    completed_names = swot_done  # sadece SWOT'u olanları tamamlandı say
                else:
                    completed_names = set(p["name"] for p in results)
                    log.info("hidden_gems.json'dan yüklendi: %d oyuncu.", len(results))
            except Exception as e:
                log.warning("hidden_gems.json yüklenemedi: %s", e)

        gems = FM26_HIDDEN_GEMS[:limit] if limit else FM26_HIDDEN_GEMS
        total = len(gems)

        for i, gem in enumerate(gems, 1):
            name = gem["name"]
            log.info("[%d/%d] ── %s (FM26: %d)", i, total, name, gem["fm_rating"])

            if name in completed_names:
                log.info("  ✓ Zaten tamamlandı, atlandı.")
                continue

            player_data: dict = {}

            if not swot_only:
                # 1) Mevcut TUR1 oyuncularında ara
                norm = normalize_name(name)
                if norm in self.existing:
                    log.info("  ✓ Mevcut TUR1 veritabanında bulundu.")
                    player_data = dict(self.existing[norm])
                else:
                    # 2) SoccerDonna'da ara
                    first_name = name.split()[0]
                    log.info("  → SoccerDonna araması: '%s'", first_name)
                    candidates = self.search_by_firstname(first_name)
                    log.info("  → %d aday bulundu.", len(candidates))

                    match = best_match(name, candidates)
                    if match:
                        log.info("  → Eşleşme: %s (%s)", match["name"], match["url"])
                        player_data = self.scrape_profile(match["url"], gem)
                    else:
                        log.warning("  ⚠ SoccerDonna'da bulunamadı: %s", name)
                        # Minimal entry oluştur
                        player_data = {
                            "soccerdonna_url": "",
                            "soccerdonna_id": f"fm26_{i}",
                            "name": name,
                            "club": gem["club"],
                            "nationality": gem["nationality"],
                            "league": "",
                            "league_code": "",
                            "position": fm_position_to_code(gem["fm_position"]),
                            "position_detail": gem["fm_position"],
                            "age": None,
                            "born": "",
                            "birth_place": "",
                            "height": "",
                            "foot": "",
                            "goals": 0,
                            "assists": 0,
                            "appearances": 0,
                            "yellow_cards": 0,
                            "red_cards": 0,
                            "caps": 0,
                            "national_team": gem["nationality"],
                            "national_goals": 0,
                            "market_value": "N/A",
                            "market_value_num": 0,
                            "photo_url": "",
                            "bio": "",
                            "transfers": [],
                            "achievements": [],
                            "flag": COUNTRY_FLAGS.get(gem["nationality"].lower(), "🌍"),
                        }

            # 3) SWOT analizi
            if not no_swot and (self.gemini_client or GROK_API_KEY or OPENAI_API_KEY or CLAUDE_API_KEY):
                if swot_only:
                    # swot_only modunda mevcut sonuçtan player_data al
                    existing_result = next((r for r in results if r["name"] == name), None)
                    if existing_result:
                        player_data = existing_result
                    else:
                        log.warning("  swot_only: '%s' için önceki veri bulunamadı, atlandı.", name)
                        continue

                if not player_data.get("swot"):
                    log.info("  → SWOT analizi üretiliyor…")
                    swot = self.generate_swot(player_data, gem)
                    if swot:
                        player_data["swot"] = swot
                        log.info("  ✓ SWOT üretildi.")
                    else:
                        log.warning("  ⚠ SWOT üretilemedi.")
                else:
                    log.info("  ✓ SWOT zaten mevcut, atlandı.")
            elif no_swot:
                log.info("  (--no-swot: SWOT atlandı)")

            # FM26 alanlarını ekle/güncelle
            player_data["hidden_gem"] = True
            player_data["fm_rating"]  = gem["fm_rating"]
            player_data["fm_position"] = gem["fm_position"]

            results.append(player_data)
            completed_names.add(name)

            # Checkpoint kaydet
            ckpt_data = {"completed": list(completed_names), "players": results}
            CHECKPOINT_PATH.write_text(json.dumps(ckpt_data, ensure_ascii=False, indent=2), "utf-8")
            log.info("  💾 Checkpoint güncellendi (%d/%d)", len(completed_names), total)

        log.info("=== Tamamlandı: %d oyuncu işlendi ===", len(results))
        return results


# ── Çıktı Üretimi ─────────────────────────────────────────────────────────────
def save_outputs(players: list[dict]):
    # Eksik alanları tamamla
    for i, p in enumerate(players):
        if not p.get("id"):
            p["id"] = 10000 + i + 1   # TUR1 ile çakışmayan ID aralığı
        if not p.get("soccerdonna_id"):
            p["soccerdonna_id"] = f"gem_{i+1}"
        if p.get("age") is None:
            p["age"] = 0
        for f in ("born", "birth_place", "height", "foot", "bio", "league", "league_code"):
            if not p.get(f):
                p[f] = ""
        for f in ("goals", "assists", "appearances", "yellow_cards", "red_cards", "caps", "national_goals"):
            if not isinstance(p.get(f), int):
                p[f] = 0
        if not p.get("market_value"):
            p["market_value"] = "N/A"
        if not p.get("market_value_num"):
            p["market_value_num"] = 0
        if not isinstance(p.get("transfers"), list):
            p["transfers"] = []
        if not isinstance(p.get("achievements"), list):
            p["achievements"] = []
        if not p.get("flag"):
            p["flag"] = COUNTRY_FLAGS.get(p.get("nationality", "").lower(), "🌍")
        if not p.get("national_team"):
            p["national_team"] = p.get("nationality", "")

    # JSON
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_JSON_PATH.write_text(json.dumps(players, ensure_ascii=False, indent=2), "utf-8")
    log.info("JSON → %s (%d oyuncu)", OUTPUT_JSON_PATH, len(players))

    # TypeScript
    SRC_DATA_DIR.mkdir(parents=True, exist_ok=True)
    ts_content = "\n".join([
        "// AUTO-GENERATED by scraper/hidden_gems_scraper.py — do not edit manually",
        "",
        'import type { Player } from "@/types";',
        "",
        "export const HIDDEN_GEMS: Player[] = ",
        json.dumps(players, ensure_ascii=False, indent=2),
        ";",
        "",
        f"export const TOTAL_HIDDEN_GEMS = {len(players)};",
    ])
    OUTPUT_TS_PATH.write_text(ts_content, "utf-8")
    log.info("TypeScript → %s", OUTPUT_TS_PATH)

    # Özet
    log.info("─" * 50)
    swot_count = sum(1 for p in players if p.get("swot"))
    found_count = sum(1 for p in players if p.get("soccerdonna_url"))
    log.info("✅ %d oyuncu kaydedildi", len(players))
    log.info("   SoccerDonna'da bulundu : %d", found_count)
    log.info("   SWOT analizi üretildi  : %d", swot_count)


# ── CLI ────────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="HerGame FM26 Hidden Gems Scraper")
    parser.add_argument("--delay",     type=float, default=2.0,  help="İstekler arası bekleme (sn)")
    parser.add_argument("--jitter",    type=float, default=1.0,  help="Rastgele jitter (sn)")
    parser.add_argument("--limit",     type=int,   default=None, help="Test için ilk N oyuncu")
    parser.add_argument("--resume",    action="store_true",       help="Checkpoint'ten devam et")
    parser.add_argument("--no-swot",   action="store_true",       help="SWOT analizi üretme")
    parser.add_argument("--swot-only", action="store_true",       help="Sadece SWOT üret (scrape etme)")
    args = parser.parse_args()

    if not GEMINI_AVAILABLE and not args.no_swot:
        log.error("google-genai paketi yüklü değil!")
        log.error("Çözüm: pip install google-genai")
        log.error("Veya sadece scraping için: python hidden_gems_scraper.py --no-swot")
        sys.exit(1)

    scraper = HiddenGemsScraper(delay=args.delay, jitter=args.jitter)
    players = scraper.run(
        limit=args.limit,
        resume=args.resume,
        no_swot=args.no_swot,
        swot_only=args.swot_only,
    )

    if not players:
        log.error("Hiç oyuncu işlenmedi. Çıkılıyor.")
        sys.exit(1)

    save_outputs(players)

    # Checkpoint'i temizle (başarılı tamamlama)
    if CHECKPOINT_PATH.exists() and not args.limit:
        CHECKPOINT_PATH.unlink()
        log.info("Checkpoint silindi (tamamlandı).")


if __name__ == "__main__":
    main()
