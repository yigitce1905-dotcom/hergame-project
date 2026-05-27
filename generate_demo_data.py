"""Generate realistic demo data for TUR1 (Turkcell Kadın Futbol Ligi)"""
import json, random
from pathlib import Path

random.seed(42)

TUR_TEAMS = [
    "Fenerbahçe SK", "Galatasaray SK", "Beşiktaş JK", "Trabzonspor",
    "Konak Belediyespor", "Çaykur Rizespor", "İstanbul Başakşehir",
    "Kocaeli Büyükşehir Belediyespor", "Ataşehir Belediyespor", "Burdur YMSK",
    "Karacabey Belediyespor", "Giresun Belediyespor",
]

POSITIONS = ["GK","DF","DF","DF","MF","MF","MF","FW","FW"]
POSITION_DETAILS = {
    "GK": ["Goalkeeper"],
    "DF": ["Centre-Back","Left-Back","Right-Back"],
    "MF": ["Central Midfield","Defensive Midfield","Attacking Midfield","Left Midfield"],
    "FW": ["Centre-Forward","Left Winger","Right Winger","Second Striker"],
}

TR_NAMES = [
    "Melike Pekel","Büşra Yıldız","Selin Çetin","Buse Arslan","Emine Kaya",
    "Fatma Doğan","Havva Şahin","İlknur Özkan","Kübra Altun","Lale Aydın",
    "Merve Bozkurt","Neslihan Çakır","Özge Demirci","Pınar Ekici","Rabia Fırat",
    "Seda Güneş","Tuğba Yılmaz","Ülkü Arslan","Vildan Bozkurt","Zeynep Çelik",
    "Ayşe Karaca","Bahar Koç","Cansu Demir","Didem Ersoy","Elif Çalışkan",
    "Filiz Aktaş","Gülsüm Polat","Hülya Yıldız","İpek Sarı","Jale Kurt",
    "Kardelen Güler","Latife Öztürk","Miray Aydın","Nilüfer Çelik","Oya Şimşek",
    "Perihan Keskin","Reyhan Altunbaş","Şennur Bal","Tuğba Gök","Umay Ergin",
    "Nazlı Çetin","Derya Yıldız","Ebru Korkmaz","Betül Duman","Selin Gürbüz",
]

FOREIGN_NAMES = [
    "Sofia Andersen","Elena Petrova","María García","Amina Diallo","Hannah Schmidt",
    "Yuki Tanaka","Valentina Rossi","Grace Okonkwo","Ana Kovačević","Lea Müller",
    "Fatou Mbaye","Kim Soo-Jin","Andreea Iordan","Natasha Kovács","Camille Dupont",
]

NATIONALITIES = [
    ("Turkey","🇹🇷"),("Turkey","🇹🇷"),("Turkey","🇹🇷"),("Turkey","🇹🇷"),("Turkey","🇹🇷"),
    ("Denmark","🇩🇰"),("Sweden","🇸🇪"),("Germany","🇩🇪"),("Spain","🇪🇸"),("France","🇫🇷"),
    ("Nigeria","🇳🇬"),("Japan","🇯🇵"),("Italy","🇮🇹"),("Serbia","🇷🇸"),("Romania","🇷🇴"),
]

players = []
pid = 1
for team in TUR_TEAMS:
    n_players = random.randint(14, 20)
    for _ in range(n_players):
        nat, flag = random.choice(NATIONALITIES)
        is_foreign = nat != "Turkey"
        name = random.choice(FOREIGN_NAMES if is_foreign else TR_NAMES)
        pos = random.choice(POSITIONS)
        pos_detail = random.choice(POSITION_DETAILS[pos])
        age = random.randint(17, 34)
        apps = random.randint(0, 22)
        goals = random.randint(0, apps // 3 + 1) if pos in ("FW","MF") else random.randint(0, 2)
        assists = random.randint(0, apps // 4 + 1)
        caps = random.randint(0, 60) if random.random() > 0.4 else 0
        mv_choices = [0, 50000, 100000, 150000, 200000, 300000, 500000]
        mv_num = random.choice(mv_choices)
        mv_str = f"€{mv_num//1000}K" if mv_num >= 1000 else "N/A"
        players.append({
            "id": pid,
            "soccerdonna_id": str(pid),
            "soccerdonna_url": f"https://www.soccerdonna.de/en/player/spieler_{pid}.html",
            "name": name,
            "age": age,
            "born": f"{random.randint(1,28):02d}.{random.randint(1,12):02d}.{2025-age}",
            "birth_place": "İstanbul" if nat=="Turkey" else "",
            "nationality": nat,
            "flag": flag,
            "club": team,
            "league": "Turkcell Kadın Futbol Ligi",
            "league_code": "TUR1",
            "position": pos,
            "position_detail": pos_detail,
            "height": f"{random.randint(158,180)} cm",
            "foot": random.choice(["Right","Right","Right","Left","Both"]),
            "goals": goals,
            "assists": assists,
            "appearances": apps,
            "yellow_cards": random.randint(0, 5),
            "red_cards": random.randint(0, 1),
            "caps": caps,
            "national_team": nat,
            "national_goals": random.randint(0, caps // 8) if caps > 0 else 0,
            "market_value": mv_str,
            "market_value_num": mv_num,
            "photo_url": "",
            "bio": "",
            "transfers": [],
            "achievements": [],
        })
        pid += 1

Path("data/raw").mkdir(parents=True, exist_ok=True)
with open("data/raw/TUR1_players.json", "w", encoding="utf-8") as f:
    json.dump(players, f, ensure_ascii=False, indent=2)
with open("data/players_all.json", "w", encoding="utf-8") as f:
    json.dump(players, f, ensure_ascii=False, indent=2)
print(f"✅ Generated {len(players)} demo players across {len(TUR_TEAMS)} clubs")
