"""Quick debug: see what the scraper actually gets from the site."""
import re
import requests

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

# Warm up
r0 = session.get("https://www.soccerdonna.de/", timeout=15)
print(f"Homepage: HTTP {r0.status_code}, cookies: {dict(r0.cookies)}")

# League page
url = "https://www.soccerdonna.de/en/kadin-futbol-sueper-ligi/startseite/wettbewerb_TUR1.html"
r = session.get(url, timeout=20)
print(f"\nLeague page: HTTP {r.status_code}")
print(f"Content-Length: {len(r.text)} chars")
print(f"Content-Type: {r.headers.get('Content-Type', '?')}")

# Count verein_ links
verein_links = re.findall(r'href="([^"]*verein_\d+[^"]*)"', r.text)
print(f"\nverein_ links found: {len(verein_links)}")
for link in verein_links[:20]:
    print(f"  {link}")

# Count spieler_ links
spieler_links = re.findall(r'href="([^"]*spieler_\d+[^"]*)"', r.text)
print(f"\nspieler_ links found: {len(spieler_links)}")

# Check if it's a bot challenge page
if "captcha" in r.text.lower() or "cloudflare" in r.text.lower() or "challenge" in r.text.lower():
    print("\n⚠ Possible bot challenge detected!")
elif len(r.text) < 5000:
    print("\n⚠ Response very short — possible redirect or empty page")
    print(r.text[:500])

# Save raw HTML for inspection
with open("debug_league.html", "w", encoding="utf-8") as f:
    f.write(r.text)
print("\nRaw HTML saved to debug_league.html")

# Test squad page
squad_url = "https://www.soccerdonna.de/en/fenerbahce-sk/kader/verein_9522.html"
import time; time.sleep(2)
r2 = session.get(squad_url, timeout=20)
print(f"\nSquad page: HTTP {r2.status_code}, length: {len(r2.text)}")
profil_links = re.findall(r'href="([^"]*profil/spieler_\d+[^"]*)"', r2.text)
print(f"profil/spieler_ links: {len(profil_links)}")
for link in profil_links[:5]:
    print(f"  {link}")
