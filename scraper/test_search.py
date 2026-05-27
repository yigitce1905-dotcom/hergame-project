import requests, re, time
from bs4 import BeautifulSoup

s = requests.Session()
s.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
s.headers['Referer'] = 'https://www.soccerdonna.de/'
s.get('https://www.soccerdonna.de/', timeout=10)
time.sleep(1)

FORM_URL = 'https://www.soccerdonna.de/en/suche/detailsuchespieler/suche.html'

def search_by_firstname(vorname):
    r = s.post(FORM_URL, data={'vorname': vorname}, timeout=15)
    soup = BeautifulSoup(r.text, 'lxml')
    links = soup.find_all('a', href=re.compile(r'/profil/spieler_'))
    return [{'name': l.get_text(strip=True), 'url': l['href']}
            for l in links if l.get_text(strip=True)]

# Check if Selma Panengstuen is in the "Selma" results
results = search_by_firstname('Selma')
print(f"Selma results ({len(results)}):")
for r in results:
    print(f"  {r['name']} -> {r['url']}")

time.sleep(1)

# Check Natalia
results2 = search_by_firstname('Natalia')
print(f"\nNatalia results ({len(results2)}):")
for r in results2:
    print(f"  {r['name']} -> {r['url']}")
