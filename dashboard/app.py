"""
⚽  Kadın Futbolu — Oyuncu Profil Paneli
=========================================
StatsBomb'un ücretsiz yayınladığı kadın futbolu verisini
(WSL, Liga F, Bundesliga, Serie A, NWSL 2023-24) kullanır.

Veri kaynağı : https://github.com/statsbomb/open-data
Kütüphaneler : statsbombpy · streamlit · plotly · pandas · numpy

─── Kurulum ───────────────────────────────────────────────
    pip install -r requirements.txt

─── Çalıştırmak ───────────────────────────────────────────
    streamlit run app.py
"""

import json
import os
import warnings
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import date

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from statsbombpy import sb

warnings.filterwarnings("ignore")


# ═══════════════════════════════════════════════════════════════
# BÖLÜM 1 │ SAYFA AYARLARI & ÖZEL STİL (CSS)
# ═══════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="⚽ Kadın Futbolu – Oyuncu Profil Paneli",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Dark-tema ve özel bileşen stilleri
st.markdown(
    """
<style>
/* ── Genel arka plan ── */
.stApp { background-color: #0d1117; color: #c9d1d9; }
[data-testid="stSidebar"] { background-color: #161b22 !important; }
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span { color: #c9d1d9 !important; }

/* ── İstatistik kutusu ── */
.stat-box {
    background: linear-gradient(145deg, #1c2333, #161b22);
    border: 1px solid #30363d;
    border-radius: 14px;
    padding: 16px 8px;
    text-align: center;
    margin-bottom: 8px;
    transition: border-color .2s;
}
.stat-box:hover { border-color: #58a6ff; }
.stat-label {
    font-size: 10px;
    color: #8b949e;
    text-transform: uppercase;
    letter-spacing: 1.4px;
    margin-bottom: 7px;
}
.stat-value  { font-size: 28px; font-weight: 800; color: #58a6ff; line-height: 1.1; }
.stat-sub    { font-size: 10px; color: #6e7681; margin-top: 3px; }

/* ── Oyuncu başlık bandı ── */
.player-banner {
    background: linear-gradient(135deg, #1a2744 0%, #0d1b33 60%);
    border: 1px solid #1f6feb;
    border-radius: 16px;
    padding: 22px 28px;
    margin-bottom: 20px;
}
.pname { font-size: 32px; font-weight: 900; color: #ffffff; }
.pmeta { font-size: 13px; color: #8b949e; margin-top: 5px; }

/* ── Bölüm başlığı ── */
.section-h {
    font-size: 14px; font-weight: 700; color: #58a6ff;
    border-left: 3px solid #1f6feb;
    padding-left: 9px; margin: 18px 0 10px;
}

/* ── Tab stilleri ── */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background-color: #0d1117;
    border-bottom: 1px solid #21262d;
}
.stTabs [data-baseweb="tab"] {
    background-color: #161b22;
    border: 1px solid #30363d;
    border-radius: 8px 8px 0 0;
    color: #8b949e;
    font-weight: 600;
    padding: 8px 16px;
}
.stTabs [aria-selected="true"] {
    background-color: #1f6feb !important;
    color: #ffffff !important;
    border-color: #1f6feb !important;
}

/* ── Filtre kartı ── */
.filter-card {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 12px;
    padding: 16px;
    margin-bottom: 12px;
}
</style>
""",
    unsafe_allow_html=True,
)


# ═══════════════════════════════════════════════════════════════
# BÖLÜM 2 │ SABİTLER
# ═══════════════════════════════════════════════════════════════

# Her events() çağrısından tutulacak sütunlar (~100 sütundan 10'a düşürür)
# Bu küçük seçim, concat + memory kullanımını ~10× azaltır.
NEEDED_COLS: list[str] = [
    "player", "team", "type", "position", "_match_id",
    "pass_outcome", "pass_key_pass",
    "shot_statsbomb_xg", "shot_outcome",
    "dribble_outcome",
]

# StatsBomb'un ücretsiz yayınladığı 5 kadın ligi
TARGET_LEAGUES: dict[str, str] = {
    "FA Women's Super League": "🏴󠁧󠁢󠁥󠁮󠁧󠁿 WSL",
    "Liga F":                   "🇪🇸 Liga F",
    "1. Frauen-Bundesliga":     "🇩🇪 Bundesliga",
    "Serie A":                  "🇮🇹 Serie A",
    "NWSL":                     "🇺🇸 NWSL",
}

# Radar grafiğinde kullanılacak eksenler: {DataFrame sütunu → görünen etiket}
RADAR_AXES: dict[str, str] = {
    "shots_p90":      "Şut / 90",
    "xg_p90":         "xG / 90",
    "passes_p90":     "Pas / 90",
    "pass_pct":       "Pas %",
    "keypasses_p90":  "Anh. Pas / 90",
    "dribbles_p90":   "Dribling / 90",
    "pressures_p90":  "Baskı / 90",
    "ballrec_p90":    "Top Kaz. / 90",
}

# Radar/sıralama için minimum maç eşiği
MIN_MATCHES: int = 2

# SoccerDonna verisindeki kısaltılmış uyruk → tam ülke adı eşlemesi
NATIONALITY_FIX: dict[str, str] = {
    "United":            "United States",
    "Korea,":            "South Korea",
    "Cote":              "Ivory Coast",
    "Burkina":           "Burkina Faso",
    "Bosnia-Herzegovina":"Bosnia and Herzegovina",
    "El":                "El Salvador",
    "Costa":             "Costa Rica",
    "Puerto":            "Puerto Rico",
    "Congo":             "Republic of the Congo",
    "South":             "South Africa",
}

# Mevki kodu → Türkçe etiket
POSITION_LABELS: dict[str, str] = {
    "GK": "🧤 Kaleci",
    "DF": "🛡 Defans",
    "MF": "🎯 Orta Saha",
    "FW": "⚡ Forvet",
}


# ═══════════════════════════════════════════════════════════════
# BÖLÜM 3 │ VERİ YÜKLEME  (st.cache_data ile önbelleklenir)
# ═══════════════════════════════════════════════════════════════

_SD_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "players_all.json")


@st.cache_data(ttl=86_400, show_spinner=False)
def load_sd_players() -> pd.DataFrame:
    """SoccerDonna players_all.json dosyasını yükler ve temizler."""
    try:
        with open(_SD_PATH, encoding="utf-8") as f:
            raw = json.load(f)
    except FileNotFoundError:
        return pd.DataFrame()

    df = pd.DataFrame(raw)

    # Uyruk kısaltmalarını düzelt
    df["nationality"] = df["nationality"].replace(NATIONALITY_FIX)
    df["nationality"] = df["nationality"].fillna("Bilinmiyor").str.strip()

    # Doğum tarihini ayrıştır (DD.MM.YYYY)
    def _parse_born(val):
        try:
            return pd.to_datetime(val, format="%d.%m.%Y")
        except Exception:
            return pd.NaT

    df["born_dt"] = df["born"].apply(_parse_born)
    today = pd.Timestamp.today()
    df["age_calc"] = ((today - df["born_dt"]).dt.days / 365.25).round(1)
    df["birth_year"] = df["born_dt"].dt.year

    # Sayısal sütunları güvenli dönüştür
    df["appearances"] = pd.to_numeric(df["appearances"], errors="coerce").fillna(0).astype(int)
    df["goals"]       = pd.to_numeric(df.get("goals", 0), errors="coerce").fillna(0).astype(int)

    # Mevki etiketleri
    df["pos_label"] = df["position"].map(POSITION_LABELS).fillna(df["position"])

    return df.reset_index(drop=True)


@st.cache_data(ttl=86_400, show_spinner=False)
def fetch_competitions() -> pd.DataFrame:
    """
    StatsBomb API'sinden tüm ligleri çeker.
    Yalnızca TARGET_LEAGUES listesindeki ligleri tutar;
    her lig için en güncel sezonu seçer.
    """
    all_comps = sb.competitions()

    # Hedef ligleri filtrele
    w = all_comps[all_comps["competition_name"].isin(TARGET_LEAGUES)].copy()

    # Her lig için en son sezonu tut (sezonu alfabetik sırayla en sona al)
    w = (
        w.sort_values("season_name", ascending=False)
         .drop_duplicates(subset="competition_name", keep="first")
         .reset_index(drop=True)
    )

    # Açılır-menü için görüntü etiketi  →  "🏴󠁧󠁢󠁥󠁮󠁧󠁿 WSL – 2023/24"
    w["label"] = w.apply(
        lambda r: f"{TARGET_LEAGUES[r['competition_name']]} – {r['season_name']}",
        axis=1,
    )
    return w


@st.cache_data(ttl=86_400, show_spinner=False)
def fetch_matches(comp_id: int, season_id: int) -> pd.DataFrame:
    """Belirli lig & sezona ait maç listesini döndürür."""
    return sb.matches(competition_id=comp_id, season_id=season_id)


@st.cache_data(ttl=86_400, show_spinner=False)
def build_global_player_index() -> pd.DataFrame:
    """
    5 ligin tüm maçlarının lineup dosyalarından global oyuncu indeksi oluşturur.

    Neden lineup? Events dosyaları 1-5 MB iken lineup dosyaları ~5-20 KB.
    500 maç × lineup = ~10 sn  (ilk seferinde)
    500 maç × events = ~30 dk  (asla yapma!)

    Dönen tablo: player | team | league_label | competition_id | season_id
    """
    comps = fetch_competitions()

    # Tüm liglerin tüm maç ID'lerini topla
    tasks = []
    for _, comp in comps.iterrows():
        try:
            matches = fetch_matches(int(comp["competition_id"]), int(comp["season_id"]))
            for _, m in matches.iterrows():
                tasks.append({
                    "match_id":       int(m["match_id"]),
                    "league_label":   comp["label"],
                    "competition_id": int(comp["competition_id"]),
                    "season_id":      int(comp["season_id"]),
                })
        except Exception:
            pass

    def _load_lineup(task: dict):
        """Bir maçın lineup verisini çekip oyuncu kayıtlarına dönüştürür."""
        try:
            lineups = sb.lineups(match_id=task["match_id"])
            rows = []
            for team_name, lineup_df in lineups.items():
                for _, p in lineup_df.iterrows():
                    rows.append({
                        "player":         p["player_name"],
                        "team":           team_name,
                        "league_label":   task["league_label"],
                        "competition_id": task["competition_id"],
                        "season_id":      task["season_id"],
                    })
            return rows
        except Exception:
            return []

    all_rows = []
    # 16 thread: lineup dosyaları küçük olduğu için daha agresif parallellik
    with ThreadPoolExecutor(max_workers=16) as pool:
        for result in as_completed([pool.submit(_load_lineup, t) for t in tasks]):
            all_rows.extend(result.result())

    if not all_rows:
        return pd.DataFrame()

    df = pd.DataFrame(all_rows)
    # Aynı oyuncu + takım kombinasyonunu tek satıra indir
    df = df.drop_duplicates(subset=["player", "team"]).sort_values("player")
    return df.reset_index(drop=True)


@st.cache_data(ttl=86_400, show_spinner=False)
def fetch_team_events(comp_id: int, season_id: int, team: str) -> pd.DataFrame:
    """
    Seçilen takımın tüm maçlarını **paralel** olarak çeker
    (ThreadPoolExecutor, max 8 iş parçacığı).

    Hız kazanımları:
      1. Paralel HTTP  → sıralı ~40 sn yerine ~5-8 sn
      2. Sütun budama → ~100 sütundan 10'a, bellek ve concat ~10× hızlı
    """
    matches = fetch_matches(comp_id, season_id)
    mids = matches[
        (matches["home_team"] == team) | (matches["away_team"] == team)
    ]["match_id"].tolist()

    def _load_match(mid: int):
        """Tek bir maçı çeker, takım filtresini uygular, sütunları budayarak döndürür."""
        try:
            ev = sb.events(match_id=mid)
            if ev.empty:
                return None

            # "team" sütunu bazı sürümlerde dict olarak gelir → string'e normalize et
            if "team" in ev.columns:
                ev["team"] = ev["team"].apply(
                    lambda x: x["name"] if isinstance(x, dict) else x
                )

            ev = ev[ev["team"] == team].copy()
            ev["_match_id"] = mid

            # Sadece ihtiyaç duyduğumuz sütunları tut
            keep = [c for c in NEEDED_COLS if c in ev.columns]
            return ev[keep] if not ev.empty else None
        except Exception:
            return None   # Başarısız maçı sessizce atla

    frames = []
    # 8 iş parçacığıyla paralel çekiş; I/O-bound görev olduğu için GIL sorun değil
    with ThreadPoolExecutor(max_workers=8) as pool:
        future_to_mid = {pool.submit(_load_match, mid): mid for mid in mids}
        for fut in as_completed(future_to_mid):
            result = fut.result()
            if result is not None and not result.empty:
                frames.append(result)

    return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()


# ═══════════════════════════════════════════════════════════════
# BÖLÜM 4 │ İSTATİSTİK HESAPLAMA
# ═══════════════════════════════════════════════════════════════

def _to_str(series: pd.Series) -> pd.Series:
    """Dict içerebilen sütunları düz string'e dönüştürür."""
    return series.apply(lambda x: x.get("name", "") if isinstance(x, dict) else x)


def compute_player_stats(events: pd.DataFrame) -> pd.DataFrame:
    """
    Ham event tablosundan oyuncu başına özet istatistik tablosu üretir.

    ── Neden vektörel? ──────────────────────────────────────────────────────
    Önceki sürüm her oyuncu için ayrı bir Python döngüsü çalıştırıyordu
    (O(n_players × n_events)).  Bu sürüm pandas groupby + boolean maskeleme
    kullanır; tüm işlemler tek geçişte, C katmanında çalışır → ~20-50× daha hızlı.

    StatsBomb sütun kuralları (statsbombpy otomatik düzleştirir):
      type              → olay türü: "Pass", "Shot", "Dribble" …
      pass_outcome      → NaN = başarılı pas, string = başarısız
      pass_key_pass     → True = anahtar pas (şut öncesi son pas)
      shot_statsbomb_xg → şutun beklenen gol (xG) değeri
      shot_outcome      → "Goal" | "Saved" | "Blocked" | "Off T" …
      dribble_outcome   → "Complete" | "Incomplete"
      position          → oyuncunun mevkisi, ör. "Center Forward"
    """
    if events.empty:
        return pd.DataFrame()

    ev = events.copy()

    # Dict sütunlarını string'e normalize et (statsbombpy sürümüne göre değişebilir)
    for col in ("type", "position", "pass_outcome", "shot_outcome", "dribble_outcome"):
        if col in ev.columns:
            ev[col] = _to_str(ev[col])

    # ── 1. MAÇ SAYISI (groupby, tek geçiş) ──────────────────────────────
    n_matches = ev.groupby("player")["_match_id"].nunique().rename("matches")

    # ── 2. MEVKİ (her oyuncu için en sık görülen değer) ─────────────────
    if "position" in ev.columns:
        pos_clean = ev["position"].replace("", np.nan)
        positions = (
            ev.assign(position=pos_clean)
              .dropna(subset=["position"])
              .groupby("player")["position"]
              .agg(lambda s: s.mode().iloc[0] if len(s) else "—")
              .rename("position")
        )
    else:
        positions = pd.Series("—", index=n_matches.index, name="position")

    # ── 3. TİP MASKELERİ (bir kez hesapla, defalarca kullan) ────────────
    pass_ev = ev[ev["type"] == "Pass"]
    shot_ev = ev[ev["type"] == "Shot"]
    drib_ev = ev[ev["type"] == "Dribble"]

    # ── 4. PAS istatistikleri ────────────────────────────────────────────
    n_pass = pass_ev.groupby("player").size().rename("passes")

    # Başarılı pas: pass_outcome == NaN  (StatsBomb standardı)
    n_comp = (
        pass_ev[pass_ev["pass_outcome"].isna()]
        .groupby("player").size().rename("pass_comp")
        if "pass_outcome" in pass_ev.columns
        else n_pass.rename("pass_comp")
    )

    # Anahtar pas: pass_key_pass == True
    if "pass_key_pass" in pass_ev.columns:
        kp_mask = pass_ev["pass_key_pass"].fillna(False).astype(bool)
        kp = pass_ev[kp_mask].groupby("player").size().rename("key_passes")
    else:
        kp = pd.Series(dtype=int, name="key_passes")

    # ── 5. ŞUT & xG istatistikleri ──────────────────────────────────────
    n_shot = shot_ev.groupby("player").size().rename("shots")

    xg_tot = (
        shot_ev.groupby("player")["shot_statsbomb_xg"].sum().rename("xg")
        if "shot_statsbomb_xg" in shot_ev.columns
        else pd.Series(dtype=float, name="xg")
    )

    if "shot_outcome" in shot_ev.columns:
        goals    = shot_ev[shot_ev["shot_outcome"] == "Goal"].groupby("player").size().rename("goals")
        shots_ot = shot_ev[shot_ev["shot_outcome"].isin(["Goal","Saved"])].groupby("player").size().rename("shots_ot")
    else:
        goals    = pd.Series(dtype=int, name="goals")
        shots_ot = pd.Series(dtype=int, name="shots_ot")

    # ── 6. DRİBLİNG ─────────────────────────────────────────────────────
    n_drb = (
        drib_ev[drib_ev["dribble_outcome"] == "Complete"]
        .groupby("player").size().rename("dribbles")
        if "dribble_outcome" in drib_ev.columns
        else pd.Series(dtype=int, name="dribbles")
    )

    # ── 7. SAVUNMA / YOĞUNLUK ───────────────────────────────────────────
    n_press = ev[ev["type"] == "Pressure"].groupby("player").size().rename("pressures")
    n_inter = ev[ev["type"] == "Interception"].groupby("player").size().rename("interceptions")
    n_brec  = ev[ev["type"] == "Ball Recovery"].groupby("player").size().rename("ball_rec")
    n_carry = ev[ev["type"] == "Carry"].groupby("player").size().rename("carries")

    # ── 8. HEPSINI BİRLEŞTİR ────────────────────────────────────────────
    # Sayısal sütunlar: NaN → 0, sonra position ekle (karışmasın diye ayrı)
    num_df = pd.concat(
        [n_matches, n_pass, n_comp, kp,
         n_shot, xg_tot, goals, shots_ot,
         n_drb, n_press, n_inter, n_brec, n_carry],
        axis=1
    ).fillna(0)

    df = num_df.join(positions, how="left")
    df["position"] = df["position"].fillna("—")

    # ── 9. TÜRETİLMİŞ METRİKLER ─────────────────────────────────────────
    # Pas başarı yüzdesi
    df["pass_pct"] = (
        df["pass_comp"] / df["passes"].replace(0, np.nan) * 100
    ).fillna(0).round(1)

    # Per-90 (maç başına 75 dk varsayımı)
    p90u = (df["matches"] * 75 / 90).replace(0, np.nan)
    df["shots_p90"]     = (df["shots"]        / p90u).fillna(0).round(2)
    df["xg_p90"]        = (df["xg"]           / p90u).fillna(0).round(2)
    df["passes_p90"]    = (df["passes"]        / p90u).fillna(0).round(2)
    df["keypasses_p90"] = (df["key_passes"]    / p90u).fillna(0).round(2)
    df["dribbles_p90"]  = (df["dribbles"]      / p90u).fillna(0).round(2)
    df["pressures_p90"] = (df["pressures"]     / p90u).fillna(0).round(2)
    df["ballrec_p90"]   = (df["ball_rec"]      / p90u).fillna(0).round(2)

    df["xg"]      = df["xg"].round(2)
    df["matches"] = df["matches"].astype(int)

    # İndeks = player adı → sütuna taşı
    return df.reset_index().rename(columns={"index": "player"})


# ═══════════════════════════════════════════════════════════════
# BÖLÜM 5 │ GÖRSELLEŞTİRME YARDIMCILARI
# ═══════════════════════════════════════════════════════════════

def percentile_rank(series: pd.Series, value: float) -> float:
    """
    Bir değerin serisi içindeki yüzdelik sırasını döndürür (0–100).
    Örn: value = 0.45 xG/90, serinin %78'inden büyükse → 78.0
    """
    s = series.dropna()
    if len(s) < 2:
        return 50.0
    return float((s < value).sum() / len(s) * 100)


def build_radar_chart(player_row: pd.Series, player_pool: pd.DataFrame) -> go.Figure:
    """
    Sekiz eksenli radar (spider-web) grafiği oluşturur.
    Her eksenin değeri, oyuncunun takım içindeki yüzdelik sırasıdır
    (0 = en düşük, 100 = en yüksek).

    Parametreler
    ------------
    player_row  : Seçili oyuncunun istatistik satırı
    player_pool : Karşılaştırma havuzu (takım içi tüm oyuncular)
    """
    labels = list(RADAR_AXES.values())
    cols   = list(RADAR_AXES.keys())

    # Her eksen için yüzdelik hesapla
    pcts = [
        percentile_rank(player_pool[c], player_row[c])
        if (c in player_row.index and c in player_pool.columns)
        else 0.0
        for c in cols
    ]

    # Polar grafik kapalı poligon gerektirir → ilk değeri sona ekle
    r_vals  = pcts + pcts[:1]
    theta   = labels + labels[:1]

    fig = go.Figure(
        go.Scatterpolar(
            r=r_vals,
            theta=theta,
            fill="toself",
            fillcolor="rgba(88, 166, 255, 0.18)",
            line=dict(color="#58a6ff", width=2.5),
            marker=dict(
                size=7,
                color="#58a6ff",
                line=dict(color="#1f6feb", width=1.2),
            ),
            hovertemplate=(
                "<b>%{theta}</b><br>"
                "Yüzdelik: %{r:.0f}<extra></extra>"
            ),
        )
    )

    fig.update_layout(
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(
                range=[0, 100],
                showticklabels=True,
                tickvals=[25, 50, 75, 100],
                tickfont=dict(size=9, color="#6e7681"),
                gridcolor="#21262d",
                linecolor="#21262d",
            ),
            angularaxis=dict(
                gridcolor="#21262d",
                linecolor="#21262d",
                tickfont=dict(size=11, color="#c9d1d9"),
            ),
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#c9d1d9"),
        margin=dict(l=65, r=65, t=80, b=60),
        height=450,
        showlegend=False,
        title=dict(
            text=(
                f"<b>{player_row['player']}</b>"
                "  —  Takım İçi Yüzdelik Sıralama"
            ),
            font=dict(size=14, color="#58a6ff"),
            x=0.5,
            xanchor="center",
        ),
    )
    return fig


def stat_box(label: str, value, sub: str = "") -> str:
    """Tek istatistik kartı için HTML döndürür."""
    return (
        f'<div class="stat-box">'
        f'  <div class="stat-label">{label}</div>'
        f'  <div class="stat-value">{value}</div>'
        f'  <div class="stat-sub">{sub}</div>'
        f'</div>'
    )


# ═══════════════════════════════════════════════════════════════
# BÖLÜM 5b │ YENİ SEKME İÇERİKLERİ
# ═══════════════════════════════════════════════════════════════

def render_world_map(df: pd.DataFrame) -> None:
    """🗺️ Dünya Haritası sekmesi — uyruk başına oyuncu sayısı choropleth."""
    st.markdown(
        '<div class="section-h">🗺️ Oyuncuların Dünya Haritası</div>',
        unsafe_allow_html=True,
    )
    st.caption(
        "SoccerDonna verisi · Kadın Futbol Süper Ligi oyuncularının uyruk dağılımı"
    )

    if df.empty:
        st.warning("⚠️ SoccerDonna verisi bulunamadı.")
        return

    # Uyruk başına oyuncu sayısı
    cnt = (
        df[df["nationality"] != "Bilinmiyor"]
        .groupby("nationality")
        .size()
        .reset_index(name="oyuncu_sayisi")
        .sort_values("oyuncu_sayisi", ascending=False)
    )

    # Choropleth haritası
    fig_map = px.choropleth(
        cnt,
        locations="nationality",
        locationmode="country names",
        color="oyuncu_sayisi",
        hover_name="nationality",
        hover_data={"oyuncu_sayisi": True, "nationality": False},
        color_continuous_scale=[
            [0.0, "#1c2333"],
            [0.2, "#1f3a6e"],
            [0.5, "#1f6feb"],
            [1.0, "#58a6ff"],
        ],
        labels={"oyuncu_sayisi": "Oyuncu Sayısı"},
        title="",
    )
    fig_map.update_geos(
        bgcolor="#0d1117",
        showcoastlines=True,
        coastlinecolor="#30363d",
        showland=True,
        landcolor="#161b22",
        showocean=True,
        oceancolor="#0d1117",
        showframe=False,
        projection_type="natural earth",
    )
    fig_map.update_layout(
        paper_bgcolor="#0d1117",
        geo_bgcolor="#0d1117",
        font=dict(color="#c9d1d9"),
        margin=dict(l=0, r=0, t=10, b=0),
        height=480,
        coloraxis_colorbar=dict(
            title="Oyuncu",
            tickfont=dict(color="#8b949e"),
            titlefont=dict(color="#8b949e"),
            bgcolor="#161b22",
            bordercolor="#30363d",
        ),
    )
    st.plotly_chart(fig_map, use_container_width=True)

    # Alt istatistik çubuğu
    col_a, col_b, col_c, col_d = st.columns(4)
    col_a.markdown(stat_box("TOPLAM OYUNCU", len(df), ""), unsafe_allow_html=True)
    col_b.markdown(stat_box("FARKLI UYRUK", cnt["nationality"].nunique(), "ülke"), unsafe_allow_html=True)
    top_nat = cnt.iloc[0]
    col_c.markdown(stat_box("EN ÇOK", top_nat["oyuncu_sayisi"], top_nat["nationality"]), unsafe_allow_html=True)
    yabanci = len(df[df["nationality"] != "Turkey"])
    col_d.markdown(stat_box("YABANCI", yabanci, "Türk olmayan"), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        '<div class="section-h">🏳️ Uyruk Sıralaması</div>',
        unsafe_allow_html=True,
    )

    # Bar chart — ilk 20
    top20 = cnt.head(20).sort_values("oyuncu_sayisi")
    fig_bar = go.Figure(go.Bar(
        x=top20["oyuncu_sayisi"],
        y=top20["nationality"],
        orientation="h",
        marker=dict(
            color=top20["oyuncu_sayisi"],
            colorscale=[[0, "#1f3a6e"], [1, "#58a6ff"]],
            showscale=False,
        ),
        text=top20["oyuncu_sayisi"],
        textposition="outside",
        textfont=dict(color="#c9d1d9", size=11),
        hovertemplate="%{y}: %{x} oyuncu<extra></extra>",
    ))
    fig_bar.update_layout(
        paper_bgcolor="#0d1117",
        plot_bgcolor="#0d1117",
        xaxis=dict(showgrid=False, color="#6e7681", title=""),
        yaxis=dict(gridcolor="#21262d", color="#c9d1d9", title=""),
        margin=dict(l=10, r=40, t=10, b=10),
        height=520,
        font=dict(color="#c9d1d9"),
    )
    st.plotly_chart(fig_bar, use_container_width=True)


def render_advanced_search(df: pd.DataFrame) -> None:
    """🔍 Gelişmiş Oyuncu Arama sekmesi — çok kriterli filtre."""
    st.markdown(
        '<div class="section-h">🔍 Gelişmiş Oyuncu Arama</div>',
        unsafe_allow_html=True,
    )
    st.caption("SoccerDonna verisi · Kadın Futbol Süper Ligi — uyruk, mevki, yaş ve maç sayısına göre filtrele")

    if df.empty:
        st.warning("⚠️ SoccerDonna verisi bulunamadı.")
        return

    # ── Filtreler ─────────────────────────────────────────────
    fc1, fc2, fc3 = st.columns([2, 2, 1])
    fc4, fc5, fc6 = st.columns([2, 2, 2])

    with fc1:
        all_nats = sorted(df["nationality"].dropna().unique())
        sel_nats = st.multiselect("🌍 Uyruk", all_nats, placeholder="Tümü")

    with fc2:
        pos_opts = sorted(df["pos_label"].dropna().unique())
        sel_pos  = st.multiselect("📋 Mevki", pos_opts, placeholder="Tümü")

    with fc3:
        name_q = st.text_input("👤 İsim", placeholder="Ara…")

    age_min_val = int(df["age_calc"].dropna().min()) if not df["age_calc"].dropna().empty else 15
    age_max_val = int(df["age_calc"].dropna().max()) if not df["age_calc"].dropna().empty else 40

    with fc4:
        age_range = st.slider(
            "🎂 Yaş Aralığı",
            min_value=age_min_val,
            max_value=age_max_val,
            value=(age_min_val, age_max_val),
        )

    app_max = int(df["appearances"].max()) if not df.empty else 30
    with fc5:
        min_apps = st.slider("📅 Min. Maç Sayısı", 0, max(app_max, 1), 0)

    with fc6:
        sort_by = st.selectbox(
            "Sırala",
            ["appearances ↓", "age_calc ↑", "age_calc ↓", "name ↑"],
        )

    # ── Filtreleri uygula ──────────────────────────────────────
    mask = pd.Series(True, index=df.index)

    if sel_nats:
        mask &= df["nationality"].isin(sel_nats)
    if sel_pos:
        mask &= df["pos_label"].isin(sel_pos)
    if name_q.strip():
        mask &= df["name"].str.contains(name_q.strip(), case=False, na=False)

    mask &= df["age_calc"].between(age_range[0], age_range[1])
    mask &= df["appearances"] >= min_apps

    filtered = df[mask].copy()

    # Sıralama
    sort_map = {
        "appearances ↓": ("appearances", False),
        "age_calc ↑":    ("age_calc",    True),
        "age_calc ↓":    ("age_calc",    False),
        "name ↑":        ("name",        True),
    }
    scol, sasc = sort_map[sort_by]
    filtered = filtered.sort_values(scol, ascending=sasc).reset_index(drop=True)

    st.markdown(
        f"<div style='color:#58a6ff;font-size:13px;font-weight:700;"
        f"margin:10px 0;'>🎯 {len(filtered)} oyuncu bulundu</div>",
        unsafe_allow_html=True,
    )

    if filtered.empty:
        st.info("ℹ️ Filtrelerle eşleşen oyuncu bulunamadı.")
        return

    # Gösterilecek sütunlar
    show_cols = {
        "name":         "Oyuncu",
        "pos_label":    "Mevki",
        "age_calc":     "Yaş",
        "nationality":  "Uyruk",
        "club":         "Kulüp",
        "appearances":  "Maç",
        "goals":        "Gol",
    }
    display = filtered[[c for c in show_cols if c in filtered.columns]].rename(columns=show_cols)

    st.dataframe(
        display,
        hide_index=True,
        use_container_width=True,
        height=min(600, 45 + len(display) * 35),
        column_config={
            "Yaş": st.column_config.NumberColumn(format="%.1f"),
            "Maç": st.column_config.NumberColumn(format="%d"),
            "Gol": st.column_config.NumberColumn(format="%d"),
        },
    )


def render_age_analysis(df: pd.DataFrame) -> None:
    """🎂 Yaş Analizi sekmesi."""
    st.markdown(
        '<div class="section-h">🎂 Yaş Analizi</div>',
        unsafe_allow_html=True,
    )
    st.caption("SoccerDonna verisi · Kadın Futbol Süper Ligi")

    if df.empty:
        st.warning("⚠️ SoccerDonna verisi bulunamadı.")
        return

    valid = df.dropna(subset=["age_calc"])

    # ── Üst istatistik kutuları ────────────────────────────────
    c1, c2, c3, c4 = st.columns(4)
    avg_age = valid["age_calc"].mean()
    c1.markdown(stat_box("LİG ORT. YAŞI", f"{avg_age:.1f}", "yaşında"), unsafe_allow_html=True)

    youngest = valid.loc[valid["age_calc"].idxmin()]
    c2.markdown(
        stat_box("EN GENÇ", f"{youngest['age_calc']:.0f}",
                 youngest.get("name", "—")),
        unsafe_allow_html=True,
    )

    oldest = valid.loc[valid["age_calc"].idxmax()]
    c3.markdown(
        stat_box("EN YAŞLI", f"{oldest['age_calc']:.0f}",
                 oldest.get("name", "—")),
        unsafe_allow_html=True,
    )

    u23 = int((valid["age_calc"] < 23).sum())
    c4.markdown(stat_box("U-23 OYUNCU", u23, "toplam"), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col_hist, col_team = st.columns([3, 2], gap="large")

    with col_hist:
        st.markdown(
            '<div class="section-h">📊 Yaş Dağılımı</div>',
            unsafe_allow_html=True,
        )
        fig_hist = go.Figure()
        fig_hist.add_trace(go.Histogram(
            x=valid["age_calc"],
            nbinsx=20,
            marker=dict(
                color="#1f6feb",
                line=dict(color="#58a6ff", width=0.8),
            ),
            opacity=0.85,
            hovertemplate="Yaş: %{x:.0f}<br>Oyuncu: %{y}<extra></extra>",
        ))
        # Ortalama çizgisi
        fig_hist.add_vline(
            x=avg_age,
            line_dash="dash",
            line_color="#ff7b72",
            annotation_text=f"Ort: {avg_age:.1f}",
            annotation_position="top right",
            annotation_font=dict(color="#ff7b72", size=11),
        )
        fig_hist.update_layout(
            paper_bgcolor="#0d1117",
            plot_bgcolor="#0d1117",
            xaxis=dict(title="Yaş", color="#8b949e", gridcolor="#21262d"),
            yaxis=dict(title="Oyuncu Sayısı", color="#8b949e", gridcolor="#21262d"),
            bargap=0.08,
            margin=dict(l=10, r=10, t=10, b=10),
            height=350,
            font=dict(color="#c9d1d9"),
        )
        st.plotly_chart(fig_hist, use_container_width=True)

        # Doğum yılı dağılımı
        st.markdown(
            '<div class="section-h">📅 Doğum Yılı Dağılımı</div>',
            unsafe_allow_html=True,
        )
        by_year = (
            valid.dropna(subset=["birth_year"])
            .groupby("birth_year").size()
            .reset_index(name="count")
            .sort_values("birth_year")
        )
        fig_year = go.Figure(go.Bar(
            x=by_year["birth_year"],
            y=by_year["count"],
            marker=dict(
                color=by_year["count"],
                colorscale=[[0, "#1f3a6e"], [1, "#58a6ff"]],
                showscale=False,
            ),
            hovertemplate="%{x}: %{y} oyuncu<extra></extra>",
        ))
        fig_year.update_layout(
            paper_bgcolor="#0d1117",
            plot_bgcolor="#0d1117",
            xaxis=dict(title="Doğum Yılı", color="#8b949e", gridcolor="#21262d", dtick=2),
            yaxis=dict(title="Oyuncu Sayısı", color="#8b949e", gridcolor="#21262d"),
            bargap=0.1,
            margin=dict(l=10, r=10, t=10, b=10),
            height=280,
            font=dict(color="#c9d1d9"),
        )
        st.plotly_chart(fig_year, use_container_width=True)

    with col_team:
        st.markdown(
            '<div class="section-h">🏟 Takım Yaş Ortalamaları</div>',
            unsafe_allow_html=True,
        )
        team_age = (
            valid.groupby("club")["age_calc"]
            .agg(["mean", "min", "max", "count"])
            .round(1)
            .reset_index()
            .rename(columns={
                "club":  "Takım",
                "mean":  "Ort. Yaş",
                "min":   "En Genç",
                "max":   "En Yaşlı",
                "count": "Oyuncu",
            })
            .sort_values("Ort. Yaş")
        )
        st.dataframe(
            team_age,
            hide_index=True,
            use_container_width=True,
            height=540,
            column_config={
                "Ort. Yaş": st.column_config.NumberColumn(format="%.1f"),
                "En Genç":  st.column_config.NumberColumn(format="%.0f"),
                "En Yaşlı": st.column_config.NumberColumn(format="%.0f"),
            },
        )

        # En genç/yaşlı kadro vurgusu
        youngest_team = team_age.iloc[0]
        oldest_team   = team_age.iloc[-1]
        st.markdown(
            f"<div style='margin-top:12px;font-size:12px;color:#8b949e;'>"
            f"🟢 En genç kadro: <b style='color:#58a6ff'>{youngest_team['Takım']}</b> "
            f"({youngest_team['Ort. Yaş']} yaş)<br>"
            f"🔴 En yaşlı kadro: <b style='color:#ff7b72'>{oldest_team['Takım']}</b> "
            f"({oldest_team['Ort. Yaş']} yaş)"
            f"</div>",
            unsafe_allow_html=True,
        )

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(
            '<div class="section-h">⚡ Mevkiye Göre Ortalama Yaş</div>',
            unsafe_allow_html=True,
        )
        pos_age = (
            valid.groupby("pos_label")["age_calc"]
            .mean()
            .round(1)
            .reset_index()
            .rename(columns={"pos_label": "Mevki", "age_calc": "Ort. Yaş"})
            .sort_values("Ort. Yaş", ascending=False)
        )
        fig_pos = go.Figure(go.Bar(
            x=pos_age["Ort. Yaş"],
            y=pos_age["Mevki"],
            orientation="h",
            marker=dict(color="#1f6feb"),
            text=pos_age["Ort. Yaş"],
            textposition="outside",
            textfont=dict(color="#c9d1d9", size=12),
            hovertemplate="%{y}: %{x:.1f} yaş<extra></extra>",
        ))
        fig_pos.update_layout(
            paper_bgcolor="#0d1117",
            plot_bgcolor="#0d1117",
            xaxis=dict(range=[0, 35], color="#6e7681", showgrid=False),
            yaxis=dict(color="#c9d1d9"),
            margin=dict(l=10, r=50, t=5, b=5),
            height=180,
            font=dict(color="#c9d1d9"),
        )
        st.plotly_chart(fig_pos, use_container_width=True)


# ═══════════════════════════════════════════════════════════════
# BÖLÜM 6 │ ANA UYGULAMA AKIŞI
# ═══════════════════════════════════════════════════════════════

def main() -> None:

    # ── Sayfa başlığı ────────────────────────────────────────────
    st.markdown(
        """
        <div style="text-align:center; padding:6px 0 18px;">
            <h1 style="font-size:36px;font-weight:900;color:#fff;margin:0;">
                ⚽ Kadın Futbolu Analiz Paneli
            </h1>
            <p style="color:#8b949e;font-size:13px;margin-top:8px;">
                StatsBomb Open Data &nbsp;·&nbsp;
                WSL · Liga F · Bundesliga · Serie A · NWSL &nbsp;·&nbsp; 2023–24
                &nbsp;+&nbsp; SoccerDonna · Kadın Futbol Süper Ligi
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # SoccerDonna verisini bir kez yükle (harita, arama, yaş sekmeleri için)
    sd_df = load_sd_players()

    # ── Sekmeler ──────────────────────────────────────────────────
    tab_profile, tab_map, tab_search, tab_age = st.tabs([
        "👤 Oyuncu Profili",
        "🗺️ Dünya Haritası",
        "🔍 Gelişmiş Arama",
        "🎂 Yaş Analizi",
    ])

    with tab_map:
        render_world_map(sd_df)

    with tab_search:
        render_advanced_search(sd_df)

    with tab_age:
        render_age_analysis(sd_df)

    # ── tab_profile için sidebar + ana alan ──────────────────────
    # Sidebar Streamlit'te global çalışır; tab_profile içeriği bu seçimleri kullanır.

    profile_error: str | None = None
    player_pool: pd.DataFrame = pd.DataFrame()
    player_name: str = ""
    team: str = ""
    league_label: str = ""

    with st.sidebar:
        st.markdown("## 🔍 Oyuncu Seç")
        st.caption("👤 Oyuncu Profili sekmesi için")

        # ── Global arama kutusu (her zaman görünür) ───────────────
        search = st.text_input(
            "🔎 İsimle ara",
            placeholder="Putellas, Morgan, Hemp…",
            help="Tüm 5 ligde arar. Boş bırakırsan aşağıdan lig/takım seçebilirsin.",
        )

        if search.strip():
            # ══ ARAMA MODU ══════════════════════════════════════════
            with st.spinner("Oyuncu listesi yükleniyor…"):
                player_index = build_global_player_index()

            if player_index.empty:
                profile_error = "❌ Oyuncu verisi alınamadı."
            else:
                mask = (
                    player_index["player"].str.contains(search, case=False, na=False)
                    | player_index["team"].str.contains(search, case=False, na=False)
                )
                results = player_index[mask].reset_index(drop=True)

                if results.empty:
                    profile_error = f"⚠️ '{search}' için sonuç bulunamadı."
                else:
                    st.caption(f"{len(results)} sonuç")
                    opts = [
                        f"{r['player']}  ·  {r['team']}  ({r['league_label']})"
                        for _, r in results.iterrows()
                    ]
                    chosen     = st.selectbox("👤", opts, label_visibility="collapsed")
                    chosen_row = results.iloc[opts.index(chosen)]

                    player_name  = chosen_row["player"]
                    team         = chosen_row["team"]
                    comp_id      = int(chosen_row["competition_id"])
                    season_id    = int(chosen_row["season_id"])
                    league_label = chosen_row["league_label"]

        else:
            # ══ LİG / TAKIM / OYUNCU SEÇİCİ MODU ═══════════════════
            st.markdown(
                "<div style='color:#6e7681;font-size:11px;text-align:center;"
                "padding:2px 0 10px;'>— veya seçicilerden seç —</div>",
                unsafe_allow_html=True,
            )

            with st.spinner("Lig listesi yükleniyor…"):
                comps = fetch_competitions()

            if comps.empty:
                profile_error = "❌ Lig verisi alınamadı."
            else:
                lig_labels  = comps["label"].tolist()
                default_lig = next(
                    (i for i, l in enumerate(lig_labels) if "Liga F" in l), 0
                )
                league_label = st.selectbox("🏆 Lig", lig_labels, index=default_lig)

                sel_comp  = comps[comps["label"] == league_label].iloc[0]
                comp_id   = int(sel_comp["competition_id"])
                season_id = int(sel_comp["season_id"])

                with st.spinner("Takımlar yükleniyor…"):
                    matches = fetch_matches(comp_id, season_id)

                teams = sorted(
                    set(matches["home_team"].tolist() + matches["away_team"].tolist())
                )
                default_team = next(
                    (i for i, t in enumerate(teams) if "Barcelona" in t), 0
                )
                team = st.selectbox("🏟 Takım", teams, index=default_team)

                n_tm = int(
                    ((matches["home_team"] == team) | (matches["away_team"] == team)).sum()
                )
                st.caption(f"📦 {n_tm} maç · ilk yükleme ~{n_tm * 2} sn")

        if not profile_error:
            # ── Events yükle + istatistik hesapla ─────────────────
            with st.spinner(f"'{team}' verileri yükleniyor…"):
                events = fetch_team_events(comp_id, season_id, team)

            if events.empty:
                profile_error = "⚠️ Bu takım için veri bulunamadı."
            else:
                with st.spinner("İstatistikler hesaplanıyor…"):
                    all_stats = compute_player_stats(events)

                player_pool = (
                    all_stats[all_stats["matches"] >= MIN_MATCHES]
                    .sort_values("player")
                    .reset_index(drop=True)
                )

                if player_pool.empty:
                    profile_error = f"⚠️ ≥ {MIN_MATCHES} maç oynayan oyuncu yok."
                else:
                    players = player_pool["player"].tolist()

                    if search.strip():
                        if player_name not in players:
                            st.info(f"ℹ️ {player_name} bu sezonda {MIN_MATCHES}+ maç oynamamış.")
                            player_name = players[0]
                    else:
                        default_player = next(
                            (i for i, p in enumerate(players) if "Putellas" in p), 0
                        )
                        player_name = st.selectbox("👤 Oyuncu", players, index=default_player)

        st.markdown("---")
        st.caption(
            "📡 Kaynak: [StatsBomb Open Data]"
            "(https://github.com/statsbomb/open-data)\n\n"
            "🛠 statsbombpy · Streamlit · Plotly"
        )

    # ── tab_profile: ana içerik ───────────────────────────────────
    with tab_profile:
        if profile_error:
            st.error(profile_error)
        elif player_pool.empty or not player_name:
            st.info("⏳ Sol panelden oyuncu seçin.")
        else:
            pr = player_pool[player_pool["player"] == player_name].iloc[0]

            # ── Oyuncu başlık bandı ──────────────────────────────
            st.markdown(
                f"""
                <div class="player-banner">
                    <div class="pname">👤 {pr['player']}</div>
                    <div class="pmeta">
                        🏟 {team}
                        &nbsp;·&nbsp; 📋 {pr['position']}
                        &nbsp;·&nbsp; {league_label}
                        &nbsp;·&nbsp; {pr['matches']} maç
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # ── İstatistik kutuları — 2 satır × 4 sütun ─────────
            st.markdown(
                '<div class="section-h">📊 Temel İstatistikler</div>',
                unsafe_allow_html=True,
            )

            r1c1, r1c2, r1c3, r1c4 = st.columns(4)
            r2c1, r2c2, r2c3, r2c4 = st.columns(4)

            r1c1.markdown(stat_box("MAÇ",        pr["matches"]),                            unsafe_allow_html=True)
            r1c2.markdown(stat_box("GOL",        pr["goals"],         "toplam"),             unsafe_allow_html=True)
            r1c3.markdown(stat_box("xG",         f"{pr['xg']:.2f}",   "beklenen gol"),       unsafe_allow_html=True)
            r1c4.markdown(stat_box("ŞUT / 90",   f"{pr['shots_p90']:.1f}"),                 unsafe_allow_html=True)
            r2c1.markdown(stat_box("PAS / 90",   f"{pr['passes_p90']:.1f}"),                unsafe_allow_html=True)
            r2c2.markdown(stat_box("PAS %",      f"{pr['pass_pct']:.0f}",  "%"),            unsafe_allow_html=True)
            r2c3.markdown(stat_box("BASKI / 90", f"{pr['pressures_p90']:.1f}"),             unsafe_allow_html=True)
            r2c4.markdown(stat_box("TOP KAZ/90", f"{pr['ballrec_p90']:.1f}"),               unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # ── Radar grafiği  +  Detay tablosu ─────────────────
            col_radar, col_table = st.columns([3, 2], gap="large")

            with col_radar:
                st.markdown(
                    '<div class="section-h">🕸 Performans Radarı</div>',
                    unsafe_allow_html=True,
                )
                st.caption(
                    "Her eksen, oyuncunun takım içindeki yüzdelik sıralamasını gösterir "
                    "(0 = en düşük · 100 = en yüksek)."
                )
                st.plotly_chart(
                    build_radar_chart(pr, player_pool),
                    use_container_width=True,
                )

            with col_table:
                st.markdown(
                    '<div class="section-h">📋 Detaylı Metrikler</div>',
                    unsafe_allow_html=True,
                )
                detail_df = pd.DataFrame(
                    {
                        "Kategori": [
                            "⚽ Taarruz", "", "", "",
                            "🎯 Pas", "", "",
                            "🛡 Savunma", "", "",
                            "🏃 Hareket",
                        ],
                        "Metrik": [
                            "Şut (toplam)",
                            "İsabetli Şut",
                            "xG (toplam)",
                            "xG / 90",
                            "Pas (toplam)",
                            "Pas Başarısı",
                            "Anahtar Pas",
                            "Baskı (toplam)",
                            "Araya Girme",
                            "Top Kazanımı",
                            "Başarılı Dribling",
                        ],
                        "Değer": [
                            str(pr["shots"]),
                            str(pr["shots_ot"]),
                            f"{pr['xg']:.2f}",
                            f"{pr['xg_p90']:.2f}",
                            str(pr["passes"]),
                            f"{pr['pass_pct']:.1f} %",
                            str(pr["key_passes"]),
                            str(pr["pressures"]),
                            str(pr["interceptions"]),
                            str(pr["ball_rec"]),
                            str(pr["dribbles"]),
                        ],
                    }
                )
                st.dataframe(detail_df, hide_index=True, use_container_width=True, height=395)

            # ── Takım içi sıralama tablosu ───────────────────────
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(
                f'<div class="section-h">'
                f'🏅 Takım İçi Sıralama  (≥ {MIN_MATCHES} maç oynayanlar · xG\'ye göre)'
                f'</div>',
                unsafe_allow_html=True,
            )

            rank_df = (
                player_pool[[
                    "player", "position", "matches",
                    "goals", "xg", "shots_p90",
                    "passes_p90", "pass_pct", "pressures_p90",
                ]]
                .rename(columns={
                    "player":        "Oyuncu",
                    "position":      "Mevki",
                    "matches":       "Maç",
                    "goals":         "Gol",
                    "xg":            "xG",
                    "shots_p90":     "Şut/90",
                    "passes_p90":    "Pas/90",
                    "pass_pct":      "Pas %",
                    "pressures_p90": "Baskı/90",
                })
                .sort_values("xG", ascending=False)
                .reset_index(drop=True)
            )
            rank_df.index += 1

            def _highlight_selected(row: pd.Series):
                if row["Oyuncu"] == player_name:
                    return ["background-color:rgba(88,166,255,0.22);font-weight:700"] * len(row)
                return [""] * len(row)

            styled_rank = (
                rank_df.style
                .apply(_highlight_selected, axis=1)
                .format({
                    "xG":       "{:.2f}",
                    "Şut/90":   "{:.1f}",
                    "Pas/90":   "{:.1f}",
                    "Pas %":    "{:.0f}",
                    "Baskı/90": "{:.1f}",
                })
            )
            st.dataframe(styled_rank, use_container_width=True, height=380)

            # ── Footer ───────────────────────────────────────────
            st.markdown(
                "<p style='color:#6e7681;font-size:11px;text-align:center;margin-top:28px;'>"
                "⚡ Veri: StatsBomb Open Data &nbsp;·&nbsp; "
                "🛠 statsbombpy · Streamlit · Plotly · Pandas &nbsp;·&nbsp; "
                "📅 2023–24 Sezonu"
                "</p>",
                unsafe_allow_html=True,
            )


# ── Giriş noktası ────────────────────────────────────────────────
if __name__ == "__main__":
    main()
