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

import warnings
from concurrent.futures import ThreadPoolExecutor, as_completed

import numpy as np
import pandas as pd
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


# ═══════════════════════════════════════════════════════════════
# BÖLÜM 3 │ VERİ YÜKLEME  (st.cache_data ile önbelleklenir)
# ═══════════════════════════════════════════════════════════════

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
# BÖLÜM 6 │ ANA UYGULAMA AKIŞI
# ═══════════════════════════════════════════════════════════════

def main() -> None:

    # ── Sayfa başlığı ────────────────────────────────────────────
    st.markdown(
        """
        <div style="text-align:center; padding:6px 0 24px;">
            <h1 style="font-size:36px;font-weight:900;color:#fff;margin:0;">
                ⚽ Kadın Futbolu Oyuncu Profil Paneli
            </h1>
            <p style="color:#8b949e;font-size:13px;margin-top:8px;">
                StatsBomb Open Data &nbsp;·&nbsp;
                WSL · Liga F · Bundesliga · Serie A · NWSL &nbsp;·&nbsp; 2023–24
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── YAN PANEL: Global arama ───────────────────────────────────
    with st.sidebar:
        st.markdown("## 🔍 Oyuncu Ara")

        # Global oyuncu indeksini yükle (lineup'lardan, önbellekli)
        # İlk seferinde ~10-15 sn, sonrası anında
        idx_placeholder = st.empty()
        idx_placeholder.caption("⏳ Oyuncu listesi hazırlanıyor…")
        player_index = build_global_player_index()
        idx_placeholder.empty()

        if player_index.empty:
            st.error("❌ Oyuncu verisi alınamadı.")
            st.stop()

        # ── Arama kutusu ─────────────────────────────────────────
        search = st.text_input(
            "İsim veya takım",
            placeholder="ör. Morgan, Harder, Chelsea, Madrid…",
        )

        # Hem oyuncu adı hem takım adında ara
        if search.strip():
            mask = (
                player_index["player"].str.contains(search, case=False, na=False)
                | player_index["team"].str.contains(search, case=False, na=False)
            )
            results = player_index[mask].reset_index(drop=True)
        else:
            results = player_index

        st.caption(f"{len(results)} oyuncu listeleniyor")

        if results.empty:
            st.warning("⚠️ Sonuç bulunamadı.")
            st.stop()

        # Seçenekleri "Ad · Takım  (Lig)" formatında göster
        display_options = [
            f"{r['player']}  ·  {r['team']}  ({r['league_label']})"
            for _, r in results.iterrows()
        ]
        chosen = st.selectbox("👤 Seç", display_options, label_visibility="collapsed")
        chosen_idx   = display_options.index(chosen)
        chosen_row   = results.iloc[chosen_idx]

        # Seçimden lig/takım bilgilerini otomatik çöz
        player_name  = chosen_row["player"]
        team         = chosen_row["team"]
        comp_id      = int(chosen_row["competition_id"])
        season_id    = int(chosen_row["season_id"])
        league_label = chosen_row["league_label"]

        # ── Seçilen oyuncunun takım verilerini yükle ─────────────
        matches       = fetch_matches(comp_id, season_id)
        n_team_matches = int(
            ((matches["home_team"] == team) | (matches["away_team"] == team)).sum()
        )
        st.caption(f"📦 {team} · {n_team_matches} maç")

        with st.spinner(f"'{team}' verileri yükleniyor…"):
            events = fetch_team_events(comp_id, season_id, team)

        if events.empty:
            st.warning("⚠️ Bu takım için veri bulunamadı.")
            st.stop()

        with st.spinner("İstatistikler hesaplanıyor…"):
            all_stats = compute_player_stats(events)

        player_pool = (
            all_stats[all_stats["matches"] >= MIN_MATCHES]
            .sort_values("player")
            .reset_index(drop=True)
        )

        if player_pool.empty:
            st.warning(f"⚠️ ≥ {MIN_MATCHES} maç oynayan oyuncu bulunamadı.")
            st.stop()

        # Seçilen oyuncu bu takımda yoksa en yakın eşleşmeyi bul
        if player_name not in player_pool["player"].values:
            st.info(f"ℹ️ {player_name} bu sezonda {MIN_MATCHES}+ maç oynamamış.")
            player_name = player_pool["player"].iloc[0]

        st.markdown("---")
        st.caption(
            "📡 Kaynak: [StatsBomb Open Data]"
            "(https://github.com/statsbomb/open-data)\n\n"
            "🛠 statsbombpy · Streamlit · Plotly"
        )

    # ══ ANA ALAN ════════════════════════════════════════════════

    pr = player_pool[player_pool["player"] == player_name].iloc[0]

    # ── Oyuncu başlık bandı ──────────────────────────────────────
    st.markdown(
        f"""
        <div class="player-banner">
            <div class="pname">👤 {pr['player']}</div>
            <div class="pmeta">
                🏟 {team}
                &nbsp;·&nbsp; 📋 {pr['position']}
                &nbsp;·&nbsp; {lig_label}
                &nbsp;·&nbsp; {pr['matches']} maç
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── İstatistik kutuları — 2 satır × 4 sütun ─────────────────
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

    # ── Radar grafiği  +  Detay tablosu ─────────────────────────
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

    # ── Takım içi sıralama tablosu ───────────────────────────────
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
    rank_df.index += 1  # 1'den başlayan sıra numarası

    def _highlight_selected(row: pd.Series):
        """Seçili oyuncunun satırını mavi vurgular."""
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

    # ── Footer ───────────────────────────────────────────────────
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
