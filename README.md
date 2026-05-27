# ⚽ HerGame — Women's Football Player Database

> Next.js 14 · TypeScript · Tailwind CSS · SoccerDonna Data Pipeline

---

## 🗂️ Proje Yapısı

```
hergame/
├── scraper/
│   ├── soccerdonna_scraper.py   ← Ana scraper (6 lig)
│   └── json_to_app.py           ← JSON → TypeScript/JSON converter
│
├── src/
│   ├── app/
│   │   ├── page.tsx             ← Ana sayfa (grid + filtreler)
│   │   └── api/players/
│   │       └── route.ts         ← REST API endpoint
│   ├── components/
│   │   ├── PlayerCard.tsx       ← Kart (fotoğrafsız)
│   │   ├── PlayerModal.tsx      ← Modal (fotoğraflı + tam profil)
│   │   ├── FilterBar.tsx        ← Filtre çubuğu
│   │   └── HeroSearch.tsx       ← Arama + DataSourcePanel
│   ├── data/
│   │   └── players.ts           ← AUTO-GENERATED (json_to_app çıktısı)
│   └── types/
│       └── index.ts             ← TypeScript interfaceleri
│
├── data/
│   ├── raw/                     ← Per-league scraped JSON
│   ├── players_all.json         ← Birleşik ham veri
│   ├── players_app.json         ← Web uygulaması formatı
│   └── players_all.xlsx         ← Excel export
│
└── package.json
```

---

## 🚀 Hızlı Başlangıç

### 1. Web uygulamasını çalıştır (demo veriyle)

```bash
npm install
npm run dev
# → http://localhost:3000
```

### 2. Gerçek veriyi çek

```bash
# Python bağımlılıklarını yükle
pip install requests beautifulsoup4 pandas openpyxl lxml

# Tüm ligleri çek (TUR1 + ENG1 + ESP1 + USA1 + FRA1 + GER1)
npm run scrape

# Sadece Türkiye ligi
npm run scrape:tur

# Büyük 5 lig
npm run scrape:top5

# JSON'u web uygulaması formatına çevir
npm run convert

# Tek komutla tümünü yap
npm run data:refresh
```

### 3. Scraper seçenekleri

```bash
python scraper/soccerdonna_scraper.py \
  --leagues TUR1 ENG1 ESP1 \
  --delay 3.0 \
  --jitter 2.0 \
  --output-dir data
```

---

## 🏟️ Desteklenen Ligler

| Kod  | Lig                       | Ülke      |
|------|---------------------------|-----------|
| TUR1 | Turkcell Kadın Futbol Ligi | 🇹🇷 Türkiye |
| ENG1 | Women's Super League       | 🏴󠁧󠁢󠁥󠁮󠁧󠁿 İngiltere |
| ESP1 | Liga F                     | 🇪🇸 İspanya |
| USA1 | NWSL                       | 🇺🇸 ABD    |
| FRA1 | Division 1 Féminine        | 🇫🇷 Fransa |
| GER1 | Frauen-Bundesliga          | 🇩🇪 Almanya |

---

## 📦 Çekilen Veri Alanları

Her oyuncu için SoccerDonna'dan çekilen alanlar:

| Alan               | Kaynak              |
|--------------------|---------------------|
| İsim, Yaş, Doğum   | Profil sayfası      |
| Milliyet, Bayrak   | Profil sayfası      |
| Kulüp, Lig         | Kadro sayfası       |
| Pozisyon (GK/DF/MF/FW) | Profil sayfası  |
| Boy, Tercih Ayak   | Profil sayfası      |
| Maç, Gol, Asist    | İstatistik tablosu  |
| Milli Maç Sayısı   | Milli takım bölümü  |
| Piyasa Değeri      | Profil başlığı      |
| Transfer Geçmişi   | Transfer tablosu    |
| Fotoğraf URL       | Profil resmi        |

---

## 🌐 API Endpoint

```
GET /api/players
  ?search=kerr
  &country=Australia
  &league=WSL
  &position=FW
  &ageMin=20&ageMax=35
  &sort=goals&dir=desc
  &page=1&pageSize=50
```

---

## ⚠️ Önemli Notlar

1. **Politeness**: Scraper varsayılan olarak 2.5s + 1.5s jitter bekler. Bunu düşürme.
2. **ToS**: SoccerDonna'yı ticari amaçlarla kullanmadan önce ToS'larını kontrol et.
3. **Rate limiting**: 429 alırsan scraper otomatik olarak 60s bekler.
4. **Site değişiklikleri**: HTML değişirse selector'lar bozulabilir — GitHub'ı takip et.
5. **Türkçe karakterler**: JSON dosyaları `ensure_ascii=False` ile kaydedilir.

---

## 🔮 Sonraki Adımlar

- [ ] Gerçek SoccerDonna verisiyle entegrasyon
- [ ] API-Football canlı istatistik entegrasyonu
- [ ] Türkiye ligi özel bölümü
- [ ] Oyuncu karşılaştırma özelliği
- [ ] Favori oyuncular (localStorage)
- [ ] Twitter/X paylaşım kartları
