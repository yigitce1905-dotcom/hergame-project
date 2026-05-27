"""
HerGame — SoccerDonna TUR1 Scraper (v3)
========================================
Scrapes Kadın Futbol Süper Ligi player data from soccerdonna.de

Usage (from project root):
  python scraper/soccerdonna_scraper.py
  python scraper/soccerdonna_scraper.py --delay 3
  python scraper/soccerdonna_scraper.py --limit 5   # quick test: first 5 teams only
"""

import argparse
import json
import logging
import os
import random
import re
import sys
import time
from dataclasses import asdict, dataclass, field
from datetime import date
from pathlib import Path
from typing import Optional

import requests
from bs4 import BeautifulSoup

# ── Paths ─────────────────────────────────────────────────────────────────────
ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
SRC_DATA_DIR = ROOT / "src" / "data"

# ── Logging ───────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("hergame")

# ── Constants ─────────────────────────────────────────────────────────────────
BASE_URL = "https://www.soccerdonna.de"
LEAGUE_URL = "https://www.soccerdonna.de/en/kadin-futbol-sueper-ligi/startseite/wettbewerb_TUR1.html"
LEAGUE_NAME = "Kadın Futbol Süper Ligi"
LEAGUE_CODE = "TUR1"

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

POSITION_MAP = {
    "goalkeeper": "GK",
    "centre-back": "DF", "center-back": "DF", "left-back": "DF",
    "right-back": "DF", "defender": "DF", "innenverteidiger": "DF",
    "linker verteidiger": "DF", "rechter verteidiger": "DF",
    "defensive midfield": "MF", "central midfield": "MF",
    "attacking midfield": "MF", "left midfield": "MF",
    "right midfield": "MF", "midfield": "MF",
    "centre-forward": "FW", "center-forward": "FW",
    "left winger": "FW", "right winger": "FW",
    "second striker": "FW", "striker": "FW", "forward": "FW",
    "mittelstürmer": "FW", "linksaußen": "FW", "rechtsaußen": "FW",
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
    "czech republic": "🇨🇿", "slovakia": "🇸🇰", "croatia": "🇭🇷",
    "serbia": "🇷🇸", "greece": "🇬🇷", "azerbaijan": "🇦🇿",
    "georgia": "🇬🇪", "kazakhstan": "🇰🇿", "moldova": "🇲🇩",
    "hungary": "🇭🇺", "bulgaria": "🇧🇬", "dr congo": "🇨🇩",
    "ivory coast": "🇨🇮", "senegal": "🇸🇳", "south africa": "🇿🇦",
    "costa rica": "🇨🇷", "ecuador": "🇪🇨", "peru": "🇵🇪",
    "venezuela": "🇻🇪", "uruguay": "🇺🇾", "paraguay": "🇵🇾",
    "latvia": "🇱🇻", "estonia": "🇪🇪", "lithuania": "🇱🇹",
    "belarus": "🇧🇾", "russia": "🇷🇺", "north macedonia": "🇲🇰",
    "albania": "🇦🇱", "kosovo": "🇽🇰", "bosnia-herzegovina": "🇧🇦",
    "montenegro": "🇲🇪", "cyprus": "🇨🇾", "luxembourg": "🇱🇺",
    "malta": "🇲🇹", "liechtenstein": "🇱🇮", "andorra": "🇦🇩",
    "morocco": "🇲🇦", "algeria": "🇩🇿", "tunisia": "🇹🇳",
    "egypt": "🇪🇬", "ethiopia": "🇪🇹", "kenya": "🇰🇪",
    "tanzania": "🇹🇿", "uganda": "🇺🇬", "zambia": "🇿🇲",
    "zimbabwe": "🇿🇼", "angola": "🇦🇴", "mozambique": "🇲🇿",
    "mali": "🇲🇱", "guinea": "🇬🇳", "sierra leone": "🇸🇱",
    "liberia": "🇱🇷", "togo": "🇹🇬", "benin": "🇧🇯",
    "india": "🇮🇳", "indonesia": "🇮🇩", "thailand": "🇹🇭",
    "vietnam": "🇻🇳", "philippines": "🇵🇭", "myanmar": "🇲🇲",
    "taiwan": "🇹🇼", "hong kong": "🇭🇰",
}


# ── Data Model ─────────────────────────────────────────────────────────────────
@dataclass
class Player:
    id: str = ""
    soccerdonna_url: str = ""
    name: str = ""
    age: Optional[int] = None
    born: str = ""
    birth_place: str = ""
    nationality: str = ""
    second_nationality: str = ""
    flag: str = "🌍"
    club: str = ""
    club_url: str = ""
    league: str = LEAGUE_NAME
    league_code: str = LEAGUE_CODE
    league_flag: str = "🇹🇷"
    position: str = "MF"
    position_detail: str = ""
    height: str = ""
    foot: str = ""
    appearances: int = 0
    goals: int = 0
    assists: int = 0
    yellow_cards: int = 0
    red_cards: int = 0
    caps: int = 0
    national_team: str = ""
    national_goals: int = 0
    market_value: str = ""
    market_value_num: float = 0.0
    transfers: list = field(default_factory=list)
    achievements: list = field(default_factory=list)
    bio: str = ""
    photo_url: str = ""
    contract_until: str = ""


# ── HTTP Session ───────────────────────────────────────────────────────────────
class SoccerDonnaScraper:
    def __init__(self, delay: float = 2.5, jitter: float = 1.5):
        self.delay = delay
        self.jitter = jitter
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
        self._warm_up()

    def _warm_up(self):
        try:
            r = self.session.get(BASE_URL + "/", timeout=15)
            log.info("Session warm-up: HTTP %s", r.status_code)
        except Exception as exc:
            log.warning("Warm-up failed (continuing anyway): %s", exc)

    def _get(self, url: str, retries: int = 3) -> Optional[BeautifulSoup]:
        for attempt in range(1, retries + 1):
            wait = self.delay + random.uniform(0, self.jitter)
            time.sleep(wait)
            try:
                r = self.session.get(url, timeout=25)
                if r.status_code == 200:
                    return BeautifulSoup(r.text, "lxml")
                elif r.status_code == 429:
                    backoff = 90 * attempt
                    log.warning("Rate-limited (429). Backing off %ds…", backoff)
                    time.sleep(backoff)
                elif r.status_code in (301, 302):
                    redirect = r.headers.get("Location", "")
                    log.info("Redirect → %s", redirect)
                    if redirect:
                        url = redirect if redirect.startswith("http") else BASE_URL + redirect
                else:
                    log.warning("HTTP %s for %s (attempt %d/%d)", r.status_code, url, attempt, retries)
            except requests.RequestException as exc:
                log.warning("Request error (attempt %d/%d): %s", attempt, retries, exc)
        log.error("Gave up after %d attempts: %s", retries, url)
        return None

    # ── League → Teams ────────────────────────────────────────────────────────
    def get_team_urls(self) -> list[dict]:
        log.info("Fetching team list from league page…")
        soup = self._get(LEAGUE_URL)
        if not soup:
            log.error("Could not load league page.")
            return []

        seen_hrefs: set[str] = set()
        teams: list[dict] = []

        # Match any link pointing to a club startseite page
        for a in soup.find_all("a", href=True):
            href: str = a["href"]
            if re.search(r"/startseite/verein_\d+", href):
                name = a.get_text(strip=True)
                if not name or href in seen_hrefs:
                    continue
                seen_hrefs.add(href)
                full_url = BASE_URL + href if href.startswith("/") else href
                teams.append({"name": name, "url": full_url})

        log.info("Found %d teams.", len(teams))
        return teams

    # ── Team → Players ────────────────────────────────────────────────────────
    def get_player_urls(self, team_url: str, team_name: str) -> list[dict]:
        squad_url = re.sub(r"/startseite/", "/kader/", team_url)
        log.info("  Squad page: %s", squad_url)
        soup = self._get(squad_url)
        if not soup:
            return []

        seen_hrefs: set[str] = set()
        players: list[dict] = []

        for a in soup.find_all("a", href=True):
            href: str = a["href"]
            if re.search(r"/profil/spieler_\d+", href):
                name = a.get_text(strip=True)
                if not name or href in seen_hrefs:
                    continue
                seen_hrefs.add(href)
                full_url = BASE_URL + href if href.startswith("/") else href
                players.append({"name": name, "url": full_url, "club": team_name, "club_url": team_url})

        log.info("  %d players found for %s", len(players), team_name)
        return players

    # ── Player Profile ─────────────────────────────────────────────────────────
    def scrape_player(self, ref: dict) -> Optional[Player]:
        url = ref["url"]
        soup = self._get(url)
        if not soup:
            return None

        p = Player(
            soccerdonna_url=url,
            club=ref["club"],
            club_url=ref.get("club_url", ""),
        )

        # ID from URL
        m = re.search(r"spieler_(\d+)", url)
        if m:
            p.id = m.group(1)

        # ── Name ──────────────────────────────────────────────────────────────
        # Try multiple heading strategies
        for sel in ["h1", "h1.data-header__headline-wrapper", ".spielername"]:
            el = soup.select_one(sel)
            if el:
                raw = el.get_text(" ", strip=True)
                # Remove shirt-number prefix: "10  Büşra Yıldız"
                raw = re.sub(r"^\s*\d{1,2}\s+", "", raw).strip()
                if raw:
                    p.name = raw
                    break
        if not p.name:
            p.name = ref.get("name", "")

        # ── Photo ─────────────────────────────────────────────────────────────
        # "somebody.jpg" is SoccerDonna's generic silhouette placeholder — skip it
        for img in soup.find_all("img", src=True):
            src: str = img["src"]
            if "spielerfotos" in src and "somebody" not in src:
                p.photo_url = src
                break
        if not p.photo_url:
            for img in soup.find_all("img", {"data-src": True}):
                src: str = img["data-src"]
                if "spielerfotos" in src and "somebody" not in src:
                    p.photo_url = src
                    break

        # ── Info Table / Steckbrief ───────────────────────────────────────────
        # SoccerDonna renders a definition-list-style info block.
        # We look for <span> pairs or <th>/<td> label+value patterns.
        self._parse_info_table(soup, p)

        # ── National Team ─────────────────────────────────────────────────────
        self._parse_national_team(soup, p)

        # ── Season Stats ──────────────────────────────────────────────────────
        self._parse_stats(soup, p)

        # ── Transfer History ──────────────────────────────────────────────────
        self._parse_transfers(soup, p)

        # Derive flag from nationality
        p.flag = COUNTRY_FLAGS.get(p.nationality.lower().strip(), "🌍")
        if not p.nationality and p.league_code == "TUR1":
            # Most TUR1 players are Turkish if no nationality found
            pass

        log.info("  ✓ %-30s | %-4s | %s", (p.name or "?")[:30], p.position, p.club)
        return p

    # ── Parsing helpers ────────────────────────────────────────────────────────
    def _parse_info_table(self, soup: BeautifulSoup, p: Player):
        """Parse the player info from tabelle_grafik (the steckbrief table)."""
        # Primary: tabelle_grafik — rows 1+ have [label_td, value_td] pairs.
        # Row 0 is a merged summary row; skip it.
        tbl = soup.find("table", class_="tabelle_grafik")
        if tbl:
            rows = tbl.find_all("tr")
            for row in rows[1:]:
                cells = row.find_all(["th", "td"])
                if len(cells) >= 2:
                    label = cells[0].get_text(" ", strip=True).rstrip(":").strip().lower()
                    val = cells[1].get_text(" ", strip=True)
                    self._apply_label(label, val, p)

        # Fallback: scan all table rows (covers other table structures)
        if not p.born and not p.nationality:
            for row in soup.find_all("tr"):
                cells = row.find_all(["th", "td"])
                if len(cells) == 2:
                    label = cells[0].get_text(" ", strip=True).rstrip(":").strip().lower()
                    val = cells[1].get_text(" ", strip=True)
                    self._apply_label(label, val, p)

    def _apply_label(self, label: str, val: str, p: Player) -> bool:
        """Map a label+value pair onto the Player object. Returns True if matched."""
        if not val or not label:
            return False
        label = label.strip().lower().rstrip(":")

        if label in ("date of birth", "geboren", "birthday", "birth date", "dob"):
            if not p.born:
                # Normalise "04.02.2003" → keep as-is; "February 4, 2003" → convert
                date_m = re.search(r"(\d{1,2})[./](\d{1,2})[./](\d{4})", val)
                if date_m:
                    p.born = f"{date_m.group(1).zfill(2)}.{date_m.group(2).zfill(2)}.{date_m.group(3)}"
                else:
                    p.born = val.strip()
            if p.age is None:
                yr_m = re.search(r"\b(19|20)(\d{2})\b", val)
                if yr_m:
                    p.age = date.today().year - int(yr_m.group(0))
            return True

        if label in ("age",):
            if p.age is None:
                try:
                    p.age = int(re.search(r"\d+", val).group())
                except (AttributeError, ValueError):
                    pass
            return True

        if label in ("place of birth", "geburtsort", "birth place", "birthplace"):
            if not p.birth_place:
                p.birth_place = val.strip()
            return True

        if label in ("nationality", "nationalität", "citizenship"):
            if not p.nationality:
                # SoccerDonna puts multiple nationalities space-separated: "Turkey Azerbaijan"
                parts = val.strip().split()
                if parts:
                    p.nationality = parts[0]
                    if len(parts) >= 2:
                        p.second_nationality = " ".join(parts[1:])
            return True

        if label in ("height", "größe", "size"):
            if not p.height:
                # SoccerDonna format: "1,76" (meters with comma) → "176 cm"
                h_m = re.search(r"1[,.](\d{2})", val)
                if h_m:
                    p.height = f"1{h_m.group(1)} cm"
                else:
                    digits = re.sub(r"[^\d]", "", val)
                    if len(digits) == 3:
                        p.height = f"{digits} cm"
                    elif digits:
                        p.height = f"{digits} cm"
            return True

        if label in ("foot", "fuß", "strong foot", "preferred foot"):
            if not p.foot:
                p.foot = val.strip().capitalize()
            return True

        if label in ("position", "spielposition"):
            raw_pos = val.strip()
            if not p.position_detail:
                p.position_detail = raw_pos
            k = raw_pos.lower()
            mapped = POSITION_MAP.get(k)
            if mapped:
                p.position = mapped
            else:
                # Keyword fallback
                if "keeper" in k or "torwart" in k or "goalkeeper" in k:
                    p.position = "GK"
                elif any(x in k for x in ("back", "defender", "abwehr", "vertei")):
                    p.position = "DF"
                elif any(x in k for x in ("forward", "striker", "stürmer", "winger", "außen")):
                    p.position = "FW"
                else:
                    p.position = "MF"
            return True

        if label in ("market value", "marktwert"):
            if not p.market_value and val.lower() not in ("unknown", "unbekannt", "-", ""):
                p.market_value = val.strip()
                mv_m = re.search(r"([\d,.]+)\s*([mk])", val, re.IGNORECASE)
                if mv_m:
                    try:
                        num = float(mv_m.group(1).replace(",", "."))
                        suffix = mv_m.group(2).lower()
                        p.market_value_num = num * 1_000_000 if suffix == "m" else num * 1_000
                    except ValueError:
                        pass
            return True

        if label in ("contract until", "vertrag bis", "contract"):
            if not p.contract_until:
                p.contract_until = val.strip()
            return True

        return False

    def _parse_national_team(self, soup: BeautifulSoup, p: Player):
        """Extract national team from tabelle_spieler header row."""
        # tabelle_spieler row 2: "Current national player: Türkei"
        header_tbl = soup.find("table", class_="tabelle_spieler")
        if header_tbl:
            rows = header_tbl.find_all("tr")
            if len(rows) >= 3:
                cell_text = rows[2].get_text(" ", strip=True)
                m = re.search(r"(?:current national player|national)[\s:]+(.+)", cell_text, re.IGNORECASE)
                if m:
                    nat = m.group(1).strip()
                    if nat and nat.lower() not in ("nein", "no", "-"):
                        p.national_team = nat

        # Count caps from tabelle_spieler (Table 2, 12 rows) — national career table
        # Each row (after header) is one national team stint
        all_tbls = soup.find_all("table", class_="tabelle_spieler")
        if len(all_tbls) >= 2:
            nat_tbl = all_tbls[1]
            total_apps = 0
            total_goals = 0
            for row in nat_tbl.find_all("tr")[1:]:  # skip header
                cells = row.find_all("td")
                nums = []
                for c in cells:
                    t = c.get_text(strip=True).replace(".", "").replace(",", "")
                    try:
                        nums.append(int(t))
                    except ValueError:
                        pass
                if len(nums) >= 2:
                    total_apps += nums[-2] if len(nums) >= 2 else 0
                    total_goals += nums[-1] if len(nums) >= 1 else 0
            if total_apps > 0:
                p.caps = total_apps
                p.national_goals = total_goals

    def _parse_stats(self, soup: BeautifulSoup, p: Player):
        """Extract current-season club stats from standard_tabelle."""
        # standard_tabelle appears 3 times on the page; first one is club stats
        std_tables = soup.find_all("table", class_="standard_tabelle")
        if not std_tables:
            return

        club_tbl = std_tables[0]
        rows = club_tbl.find_all("tr")
        # Skip header row, sum all data rows
        total_apps = total_goals = total_assists = total_yellow = total_red = 0
        for row in rows[1:]:
            cells = row.find_all("td")
            nums = []
            for c in cells:
                t = c.get_text(strip=True).replace(".", "").replace(",", "")
                try:
                    nums.append(int(t))
                except ValueError:
                    pass
            # standard_tabelle columns: Appearances, Goals, Assists, Yellow, Red (approx.)
            if len(nums) >= 1:
                total_apps += nums[0]
            if len(nums) >= 2:
                total_goals += nums[1]
            if len(nums) >= 3:
                total_assists += nums[2]
            if len(nums) >= 4:
                total_yellow += nums[3]
            if len(nums) >= 5:
                total_red += nums[4]

        p.appearances = total_apps
        p.goals = total_goals
        p.assists = total_assists
        p.yellow_cards = total_yellow
        p.red_cards = total_red

    def _parse_transfers(self, soup: BeautifulSoup, p: Player):
        """Extract transfer history from transfer table."""
        for table in soup.find_all("table"):
            cls = " ".join(table.get("class", []))
            if "transfer" in cls.lower():
                for row in table.find_all("tr"):
                    cells = row.find_all("td")
                    if len(cells) >= 3:
                        year = cells[0].get_text(strip=True)
                        from_club = cells[-2].get_text(strip=True)
                        to_club = cells[-1].get_text(strip=True)
                        if year and re.match(r"\d{4}", year):
                            p.transfers.append({"year": year, "from": from_club, "to": to_club})
                break

    # ── Full Pipeline ──────────────────────────────────────────────────────────
    def run(self, team_limit: Optional[int] = None) -> list[Player]:
        teams = self.get_team_urls()
        if not teams:
            log.error("No teams found — check league URL or site structure.")
            return []

        if team_limit:
            teams = teams[:team_limit]
            log.info("(Limited to first %d teams for testing)", team_limit)

        all_players: list[Player] = []
        seen_ids: set[str] = set()

        for i, team in enumerate(teams, 1):
            log.info("[%d/%d] ⚽ %s", i, len(teams), team["name"])
            refs = self.get_player_urls(team["url"], team["name"])

            for ref in refs:
                player = self.scrape_player(ref)
                if not player or not player.name:
                    continue
                key = player.id or f"{player.name}|{player.club}"
                if key in seen_ids:
                    continue
                seen_ids.add(key)
                all_players.append(player)

        log.info("=== Scraping complete: %d players ===", len(all_players))
        return all_players


# ── Output helpers ─────────────────────────────────────────────────────────────
NATIONALITY_NORMALIZE = {
    "Türkei": "Turkey", "Türkiye": "Turkey",
    "Deutschland": "Germany", "Almanya": "Germany",
    "Frankreich": "France", "İspanya": "Spain", "Espagne": "Spain",
    "İngiltere": "England", "Angleterre": "England",
    "Brasilien": "Brazil", "Brezilya": "Brazil",
    "Vereinigte Staaten": "USA", "ABD": "USA",
    "Niederlande": "Netherlands", "Hollanda": "Netherlands",
    "Australien": "Australia", "Avustralya": "Australia",
    "Nigeria": "Nigeria", "Polen": "Poland", "Polónia": "Poland",
    "Portugal": "Portugal", "Italien": "Italy", "İtalya": "Italy",
    "Kanada": "Canada", "Japan": "Japan", "Japonya": "Japan",
    "Südkorea": "South Korea", "Güney Kore": "South Korea",
    "Kolumbien": "Colombia", "Kolombiya": "Colombia",
    "Argentinien": "Argentina", "Arjantin": "Argentina",
    "Irland": "Ireland", "Österreich": "Austria", "Avusturya": "Austria",
    "Belgien": "Belgium", "Belçika": "Belgium",
    "Island": "Iceland", "İzlanda": "Iceland",
    "Finnland": "Finland", "Finlandiya": "Finland",
    "Schweiz": "Switzerland", "İsviçre": "Switzerland",
    "Neuseeland": "New Zealand", "Yeni Zelanda": "New Zealand",
    "Jamaika": "Jamaica", "Mexiko": "Mexico", "Meksika": "Mexico",
    "Ghana": "Ghana", "Kamerun": "Cameroon",
    "Rumänien": "Romania", "Romanya": "Romania",
    "Ukraine": "Ukraine", "Ukrayna": "Ukraine",
    "Kroatien": "Croatia", "Hırvatistan": "Croatia",
    "Serbien": "Serbia", "Sırbistan": "Serbia",
    "Griechenland": "Greece", "Yunanistan": "Greece",
    "Aserbaidschan": "Azerbaijan", "Azerbaycan": "Azerbaijan",
    "Georgien": "Georgia", "Gürcistan": "Georgia",
    "Kasachstan": "Kazakhstan", "Kazakistan": "Kazakhstan",
    "Marokko": "Morocco", "Fas": "Morocco",
    "Ägypten": "Egypt", "Mısır": "Egypt",
    "Elfenbeinküste": "Ivory Coast", "Fildişi Sahili": "Ivory Coast",
}


def normalize_nationality(raw: str) -> str:
    if not raw:
        return ""
    return NATIONALITY_NORMALIZE.get(raw.strip(), raw.strip())


def normalize_market_value(val: str, num: float) -> str:
    if num >= 1_000_000:
        return f"€{num / 1_000_000:.1f}M"
    if num >= 1_000:
        return f"€{int(num / 1_000)}K"
    if val and val.lower() not in ("unknown", "unbekannt", "-", ""):
        return val
    return "N/A"


def player_to_app_dict(p: Player, idx: int) -> dict:
    nationality = normalize_nationality(p.nationality)
    flag = COUNTRY_FLAGS.get(nationality.lower(), "🌍")
    mv_display = normalize_market_value(p.market_value, p.market_value_num)
    age = p.age or 0

    return {
        "id": idx + 1,
        "soccerdonna_id": p.id or str(idx + 1),
        "soccerdonna_url": p.soccerdonna_url,
        "name": p.name,
        "age": age,
        "born": p.born,
        "birth_place": p.birth_place,
        "nationality": nationality,
        "flag": flag,
        "club": p.club,
        "league": p.league,
        "league_code": p.league_code,
        "position": p.position if p.position in ("GK", "DF", "MF", "FW") else "MF",
        "position_detail": p.position_detail,
        "height": p.height,
        "foot": p.foot,
        "goals": p.goals,
        "assists": p.assists,
        "appearances": p.appearances,
        "yellow_cards": p.yellow_cards,
        "red_cards": p.red_cards,
        "caps": p.caps,
        "national_team": p.national_team or nationality,
        "national_goals": p.national_goals,
        "market_value": mv_display,
        "market_value_num": p.market_value_num,
        "photo_url": p.photo_url,
        "bio": p.bio,
        "transfers": p.transfers,
        "achievements": p.achievements,
    }


def players_to_typescript(players: list[dict]) -> str:
    leagues = sorted(set(p["league"] for p in players))
    countries = sorted(set(p["nationality"] for p in players if p["nationality"]))
    return "\n".join([
        "// AUTO-GENERATED by scraper/soccerdonna_scraper.py — do not edit manually",
        "",
        'import type { Player } from "@/types";',
        "",
        "export const PLAYERS: Player[] = ",
        json.dumps(players, ensure_ascii=False, indent=2),
        ";",
        "",
        f"export const TOTAL_PLAYERS = {len(players)};",
        f"export const LEAGUES = {json.dumps(leagues, ensure_ascii=False)};",
        f"export const COUNTRIES = {json.dumps(countries, ensure_ascii=False)};",
    ])


def save_outputs(players: list[Player]):
    app_dicts = [player_to_app_dict(p, i) for i, p in enumerate(players)]

    # Raw JSON (per-league)
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    raw_path = RAW_DIR / "TUR1_players.json"
    with open(raw_path, "w", encoding="utf-8") as f:
        json.dump([asdict(p) for p in players], f, ensure_ascii=False, indent=2)
    log.info("Raw JSON → %s (%d players)", raw_path, len(players))

    # App JSON
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    app_json_path = DATA_DIR / "players_app.json"
    with open(app_json_path, "w", encoding="utf-8") as f:
        json.dump(app_dicts, f, ensure_ascii=False, indent=2)
    log.info("App JSON → %s", app_json_path)

    # Also write players_all.json (for compatibility with json_to_app.py)
    all_json_path = DATA_DIR / "players_all.json"
    with open(all_json_path, "w", encoding="utf-8") as f:
        json.dump([asdict(p) for p in players], f, ensure_ascii=False, indent=2)
    log.info("All JSON → %s", all_json_path)

    # TypeScript data file
    SRC_DATA_DIR.mkdir(parents=True, exist_ok=True)
    ts_path = SRC_DATA_DIR / "players.ts"
    with open(ts_path, "w", encoding="utf-8") as f:
        f.write(players_to_typescript(app_dicts))
    log.info("TypeScript → %s", ts_path)

    # Summary
    log.info("─" * 50)
    log.info("✅ Done!  %d players saved.", len(players))
    positions = {}
    for p in app_dicts:
        pos = p["position"]
        positions[pos] = positions.get(pos, 0) + 1
    for pos, cnt in sorted(positions.items()):
        log.info("   %-4s  %d", pos, cnt)


# ── CLI ────────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="HerGame SoccerDonna TUR1 Scraper")
    parser.add_argument("--delay", type=float, default=2.5,
                        help="Base delay between requests in seconds (default: 2.5)")
    parser.add_argument("--jitter", type=float, default=1.5,
                        help="Random jitter added to each delay (default: 1.5)")
    parser.add_argument("--limit", type=int, default=None,
                        help="Limit to first N teams (for testing)")
    args = parser.parse_args()

    scraper = SoccerDonnaScraper(delay=args.delay, jitter=args.jitter)
    players = scraper.run(team_limit=args.limit)

    if not players:
        log.error("No players scraped. Exiting.")
        sys.exit(1)

    save_outputs(players)


if __name__ == "__main__":
    main()
