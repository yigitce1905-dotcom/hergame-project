// src/components/PlayerModal.tsx
"use client";

import { useEffect, useRef, useState } from "react";
import type { Player } from "@/types";

interface Props {
  player: Player;
  onClose: () => void;
}

const POS_COLORS: Record<string, string> = {
  GK: "#f5c842",
  DF: "#6ee8c8",
  MF: "#c8a6f5",
  FW: "#f5a6c8",
};

const SWOT_CONFIG = {
  strengths:    { label: "Güçlü Yönler",   icon: "💪", color: "#6ee8c8", bg: "#6ee8c810", border: "#6ee8c830" },
  weaknesses:   { label: "Zayıf Yönler",   icon: "⚠️", color: "#f5a6c8", bg: "#f5a6c810", border: "#f5a6c830" },
  opportunities:{ label: "Fırsatlar",       icon: "🚀", color: "#c8a6f5", bg: "#c8a6f510", border: "#c8a6f530" },
  threats:      { label: "Tehditler",       icon: "🛡️", color: "#f5c842", bg: "#f5c84210", border: "#f5c84230" },
} as const;

function StatBox({ value, label }: { value: number | string; label: string }) {
  return (
    <div className="bg-[#18181f] border border-[#2a2a38] rounded-xl p-3 text-center">
      <div className="font-serif text-2xl text-white">{value}</div>
      <div className="text-[10px] text-[#6b6685] uppercase tracking-wider mt-1">{label}</div>
    </div>
  );
}

function InfoRow({ label, value }: { label: string; value: string | number }) {
  return (
    <div className="bg-[#18181f] border border-[#2a2a38] rounded-lg p-2.5">
      <div className="text-[10px] text-[#6b6685] uppercase tracking-wide">{label}</div>
      <div className="text-sm text-white font-medium mt-0.5">{value || "—"}</div>
    </div>
  );
}

function SwotCard({
  items,
  type,
}: {
  items: string[];
  type: keyof typeof SWOT_CONFIG;
}) {
  const cfg = SWOT_CONFIG[type];
  return (
    <div
      className="rounded-xl border p-4"
      style={{ background: cfg.bg, borderColor: cfg.border }}
    >
      <div className="flex items-center gap-2 mb-3">
        <span className="text-base">{cfg.icon}</span>
        <span className="text-xs font-bold uppercase tracking-widest" style={{ color: cfg.color }}>
          {cfg.label}
        </span>
      </div>
      <ul className="space-y-2">
        {items.map((item, i) => (
          <li key={i} className="flex gap-2 text-sm text-[#c8c4e0] leading-snug">
            <span className="mt-1 flex-shrink-0 w-1.5 h-1.5 rounded-full mt-[6px]" style={{ background: cfg.color }} />
            {item}
          </li>
        ))}
      </ul>
    </div>
  );
}

type Tab = "profil" | "analiz";

export default function PlayerModal({ player, onClose }: Props) {
  const posColor = POS_COLORS[player.position] ?? "#c8a6f5";
  const [imgError, setImgError] = useState(false);
  const [tab, setTab] = useState<Tab>("profil");
  const overlayRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const firstFocusable = overlayRef.current?.querySelector<HTMLElement>(
      "button, [tabindex='0']"
    );
    firstFocusable?.focus();
  }, []);

  const hasSwot = !!player.swot;

  return (
    <div
      ref={overlayRef}
      className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/75 backdrop-blur-sm animate-in fade-in duration-200"
      onClick={(e) => e.target === e.currentTarget && onClose()}
      role="dialog"
      aria-modal="true"
      aria-label={`${player.name} profili`}
    >
      <div className="bg-[#16161e] border border-[#3a3a4e] rounded-2xl w-full max-w-2xl max-h-[88vh] overflow-y-auto relative animate-in zoom-in-95 slide-in-from-bottom-4 duration-200 scrollbar-thin scrollbar-thumb-[#3a3a4e] scrollbar-track-transparent">

        {/* ── Photo Header ─────────────────────────────────────────────── */}
        <div className="relative h-64 rounded-t-2xl overflow-hidden bg-[#18181f]">
          {player.photo_url && !imgError ? (
            <img
              src={player.photo_url}
              alt={player.name}
              className="w-full h-full object-cover object-top"
              onError={() => setImgError(true)}
            />
          ) : (
            <div
              className="w-full h-full flex items-center justify-center"
              style={{ background: `linear-gradient(135deg, ${posColor}22, #18181f)` }}
            >
              <span className="font-serif text-8xl font-bold opacity-30" style={{ color: posColor }}>
                {player.name.split(" ").map((w) => w[0]).slice(0, 2).join("")}
              </span>
            </div>
          )}
          <div className="absolute bottom-0 inset-x-0 h-1/2 bg-gradient-to-t from-[#16161e] to-transparent" />

          {/* FM26 badge */}
          {player.hidden_gem && player.fm_rating && (
            <div className="absolute top-3 left-3 flex items-center gap-1.5 bg-black/70 border border-[#f5c842]/40 rounded-full px-3 py-1.5">
              <span className="text-[10px] text-[#f5c842] font-bold uppercase tracking-wider">FM26</span>
              <span className="text-[#f5c842] font-bold text-sm">{player.fm_rating}</span>
            </div>
          )}

          <button
            onClick={onClose}
            className="absolute top-3 right-3 w-9 h-9 rounded-full bg-black/60 border border-white/10 flex items-center justify-center text-white text-lg hover:bg-white/20 transition-colors"
            aria-label="Kapat"
          >
            ✕
          </button>
        </div>

        {/* ── Body ─────────────────────────────────────────────────────── */}
        <div className="p-6">

          {/* Name + badges */}
          <h2 className="font-serif text-3xl leading-tight mb-2">
            {player.name} <span className="text-2xl">{player.flag}</span>
          </h2>
          <div className="flex flex-wrap gap-2 mb-4">
            <span
              className="text-xs font-bold px-2.5 py-1 rounded border"
              style={{ color: posColor, borderColor: `${posColor}44`, background: `${posColor}18` }}
            >
              {player.position} — {player.position_detail || player.fm_position || "—"}
            </span>
            <span className="text-xs px-2.5 py-1 rounded bg-[#18181f] border border-[#2a2a38] text-[#a09bbf]">
              {player.nationality}
            </span>
            <span className="text-xs px-2.5 py-1 rounded bg-[#18181f] border border-[#2a2a38] text-[#a09bbf]">
              {player.club}
            </span>
            {player.market_value && player.market_value !== "N/A" && (
              <span className="text-xs px-2.5 py-1 rounded bg-[#18181f] border border-[#2a2a38] text-[#6ee8c8] font-semibold">
                {player.market_value}
              </span>
            )}
          </div>

          {/* ── Tabs (only if SWOT exists) ─────────────────────────────── */}
          {hasSwot && (
            <div className="flex gap-1 mb-5 bg-[#18181f] rounded-xl p-1 border border-[#2a2a38]">
              {(["profil", "analiz"] as Tab[]).map((t) => (
                <button
                  key={t}
                  onClick={() => setTab(t)}
                  className={`flex-1 py-2 rounded-lg text-xs font-bold uppercase tracking-widest transition-all ${
                    tab === t
                      ? "bg-[#c8a6f5] text-[#16161e]"
                      : "text-[#6b6685] hover:text-white"
                  }`}
                >
                  {t === "profil" ? "📋 Profil" : "🔍 Analiz"}
                </button>
              ))}
            </div>
          )}

          {/* ─────────── PROFIL TAB ────────────────────────────────────── */}
          {tab === "profil" && (
            <>
              <section className="mb-5">
                <h3 className="text-[10px] text-[#6b6685] uppercase tracking-widest mb-2.5 font-semibold">İstatistikler</h3>
                <div className="grid grid-cols-3 sm:grid-cols-5 gap-2">
                  <StatBox value={player.goals}       label="Gol" />
                  <StatBox value={player.assists}     label="Asist" />
                  <StatBox value={player.appearances} label="Maç" />
                  <StatBox value={player.caps}        label="Milli Maç" />
                  {player.position !== "GK" && (
                    <StatBox value={player.goals + player.assists} label="G+A" />
                  )}
                </div>
              </section>

              <section className="mb-5">
                <h3 className="text-[10px] text-[#6b6685] uppercase tracking-widest mb-2.5 font-semibold">Oyuncu Bilgileri</h3>
                <div className="grid grid-cols-2 gap-1.5">
                  <InfoRow label="Yaş"          value={player.age ? `${player.age} yaşında` : "—"} />
                  <InfoRow label="Doğum Yeri"   value={player.birth_place} />
                  <InfoRow label="Boy"          value={player.height} />
                  <InfoRow label="Tercih Ayak"  value={player.foot} />
                  <InfoRow label="Mevcut Kulüp" value={player.club} />
                  <InfoRow label="Lig"          value={player.league} />
                  <InfoRow label="Milli Takım"  value={player.national_team} />
                  <InfoRow label="Milli Gol"    value={player.national_goals} />
                </div>
              </section>

              {player.bio && (
                <section className="mb-5">
                  <h3 className="text-[10px] text-[#6b6685] uppercase tracking-widest mb-2.5 font-semibold">Biyografi</h3>
                  <p className="text-sm text-[#a09bbf] leading-relaxed">{player.bio}</p>
                </section>
              )}

              {player.transfers.length > 0 && (
                <section className="mb-5">
                  <h3 className="text-[10px] text-[#6b6685] uppercase tracking-widest mb-2.5 font-semibold">Transfer Geçmişi</h3>
                  <div className="space-y-1.5">
                    {player.transfers.map((t, i) => (
                      <div key={i} className="flex items-center gap-3 bg-[#18181f] border border-[#2a2a38] rounded-lg px-3 py-2 text-sm">
                        <span className="text-[#c8a6f5] font-semibold w-10 flex-shrink-0">{t.year}</span>
                        <span className="text-[#a09bbf] truncate">{t.from}</span>
                        <span className="text-[#6b6685] flex-shrink-0">→</span>
                        <span className="text-[#c8a6f5] truncate">{t.to}</span>
                      </div>
                    ))}
                  </div>
                </section>
              )}

              {player.achievements.length > 0 && (
                <section>
                  <h3 className="text-[10px] text-[#6b6685] uppercase tracking-widest mb-2.5 font-semibold">Başarılar</h3>
                  <div className="flex flex-wrap gap-1.5">
                    {player.achievements.map((a, i) => (
                      <span key={i} className="text-xs px-2.5 py-1 rounded border bg-[#c8a6f5]/10 border-[#c8a6f5]/25 text-[#c8a6f5]">
                        {a}
                      </span>
                    ))}
                  </div>
                </section>
              )}
            </>
          )}

          {/* ─────────── ANALİZ TAB ────────────────────────────────────── */}
          {tab === "analiz" && player.swot && (
            <div>
              {/* FM26 info banner */}
              {player.fm_rating && (
                <div className="mb-5 flex items-center gap-3 bg-[#f5c842]/8 border border-[#f5c842]/20 rounded-xl px-4 py-3">
                  <span className="text-2xl">⭐</span>
                  <div>
                    <div className="text-xs text-[#f5c842] font-bold uppercase tracking-wider">FM26 Hidden Gem</div>
                    <div className="text-sm text-white mt-0.5">
                      Scout Rating: <span className="font-bold text-[#f5c842]">{player.fm_rating}/100</span>
                      {player.fm_position && <span className="text-[#a09bbf] ml-2">· {player.fm_position}</span>}
                    </div>
                  </div>
                </div>
              )}

              {/* SWOT grid */}
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 mb-4">
                <SwotCard items={player.swot.strengths}     type="strengths" />
                <SwotCard items={player.swot.weaknesses}    type="weaknesses" />
                <SwotCard items={player.swot.opportunities} type="opportunities" />
                <SwotCard items={player.swot.threats}       type="threats" />
              </div>

              <p className="text-[10px] text-[#3a3a4e] text-center">
                {player.swot.model} · {new Date(player.swot.generated_at).toLocaleDateString("tr-TR")} tarihinde üretildi
              </p>
            </div>
          )}

          {/* SoccerDonna link */}
          {player.soccerdonna_url && (
            <div className="mt-5 pt-4 border-t border-[#2a2a38]">
              <a
                href={player.soccerdonna_url}
                target="_blank"
                rel="noopener noreferrer"
                className="text-xs text-[#6b6685] hover:text-[#c8a6f5] transition-colors"
              >
                🔗 SoccerDonna'da görüntüle ↗
              </a>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
