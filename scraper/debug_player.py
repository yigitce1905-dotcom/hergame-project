"""Debug: see what's in a player profile page."""
import re, sys, time
import requests
from bs4 import BeautifulSoup

# Force UTF-8 output
sys.stdout.reconfigure(encoding="utf-8")

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

session = requests.Session()
session.headers.update(HEADERS)
session.get("https://www.soccerdonna.de/", timeout=15)
time.sleep(2)

url = "https://www.soccerdonna.de/en/goeknur-gueleryuez/profil/spieler_64901.html"
r = session.get(url, timeout=20)
print(f"HTTP {r.status_code}, length: {len(r.text)}")

soup = BeautifulSoup(r.text, "lxml")

# H1 name
h1 = soup.find("h1")
print(f"\nH1: {h1.get_text(' ', strip=True) if h1 else 'NOT FOUND'}")

# Photo
print("\n=== SPIELERFOTOS IMAGE ===")
for img in soup.find_all("img"):
    src = img.get("src","") or img.get("data-src","")
    if src and "spielerfotos" in src:
        print(f"  src={src}")

# tabelle_grafik = main info table
print("\n=== tabelle_grafik (player info) ===")
tbl = soup.find("table", class_="tabelle_grafik")
if tbl:
    for row in tbl.find_all("tr"):
        cells = row.find_all(["th", "td"])
        vals = [c.get_text(" ", strip=True)[:60] for c in cells]
        print(f"  {vals}")
else:
    print("  NOT FOUND")
    # Try to find any table with player info
    for tbl2 in soup.find_all("table"):
        cls = tbl2.get("class", [])
        if cls:
            print(f"  Table class={cls}")

# tabelle_spieler = header info
print("\n=== tabelle_spieler (header) ===")
tbl2 = soup.find("table", class_="tabelle_spieler")
if tbl2:
    for row in tbl2.find_all("tr"):
        cells = row.find_all(["th", "td"])
        vals = [c.get_text(" ", strip=True)[:80] for c in cells]
        print(f"  {vals}")

# Stats tables
print("\n=== ALL TABLES ===")
for i, table in enumerate(soup.find_all("table")):
    cls = " ".join(table.get("class", []))
    rows = table.find_all("tr")
    tfoot = table.find("tfoot")
    print(f"  Table {i}: class='{cls}', rows={len(rows)}, has_tfoot={bool(tfoot)}")
    if tfoot:
        cells = tfoot.find_all("td")
        print(f"    tfoot: {[c.get_text(strip=True) for c in cells]}")
