"use client";

import { useEffect, useMemo } from "react";
import { X, Star, ExternalLink, Shield, Zap, Brain, Dumbbell, Palette } from "lucide-react";
import { cn, formatMarketValue, formatContractEnd, contractEndColor, statBarColor } from "@/lib/utils";
import type { ScoutPlayer } from "@/types/scout";
import { computeRadarAxes, gradeColor, GRADE_WEIGHTS, POSITION_LABELS } from "@/types/scout";
import ScoutRadarChart from "./ScoutRadarChart";

// ─── Sub-components ─────────────────────────────────────────────────────────────

function GradeBadge({ grade, label }: { grade: string; label: string }) {
  const score = GRADE_WEIGHTS[grade as keyof typeof GRADE_WEIGHTS] ?? 50;
  return (
    <div className="flex items-center justify-between py-1.5 border-b border-[#1e1e2e]">
      <span className="text-[11px] text-zinc-400">{label}</span>
      <span
        className="text-xs font-bold px-2 py-0.5 rounded"
        style={{ color: gradeColor(grade as any), backgroundColor: `${gradeColor(grade as any)}22` }}
      >
        {grade}
      </span>
    </div>
  );
}

function StatBar({ label, value, max = 100, unit = "" }: { label: string; value: number; max?: number; unit?: string }) {
  const pct = Math.min(100, (value / max) * 100);
  return (
    <div className="space-y-0.5">
      <div className="flex justify-between text-[10px]">
        <span className="text-zinc-500">{label}</span>
        <span className="text-zinc-300 font-mono">{value.toFixed(2)}{unit}</span>
      </div>
      <div className="h-1.5 bg-[#1e1e2e] rounded-full overflow-hidden">
        <div
          className={cn("h-full rounded-full transition-all", statBarColor(pct))}
          style={{ width: `${pct}%` }}
        />
      </div>
    </div>
  );
}

function StatCard({ label, value, unit = "" }: { label: string; value: number | string; unit?: string }) {
  return (
    <div className="bg-[#1a1a28] rounded-lg p-2.5 text-center">
      <p className="text-[10px] text-zinc-500 mb-0.5">{label}</p>
      <p className="text-sm font-bold text-zinc-100">{typeof value === "number" ? value.toFixed(2) : value}<span className="text-xs text-zinc-500 ml-0.5">{unit}</span></p>
    </div>
  );
}

function SimilarPlayerRow({ player, onClick }: { player: ScoutPlayer; onClick: () => void }) {
  return (
    <button onClick={onClick} className="w-full flex items-center gap-2 p-2 rounded-lg hover:bg-[#1a1a28] transition-colors text-left">
      <div className="w-7 h-7 rounded-full bg-[#2a2a38] flex items-center justify-center text-xs font-bold text-violet-400">
        {player.name.charAt(0)}
      </div>
      <div className="flex-1 min-w-0">
        <p className="text-xs font-medium text-zinc-200 truncate">{player.name}</p>
        <p className="text-[10px] text-zinc-500">{player.currentClub} · {player.positions[0]?.position ?? "—"}</p>
      </div>
      <span className="text-[10px] text-violet-400 font-bold">
        {player.evaluation?.overallScore ?? "—"}
      </span>
    </button>
  );
}

// ─── Main Modal ─────────────────────────────────────────────────────────────────

interface Props {
  player: ScoutPlayer;
  allPlayers: ScoutPlayer[];
  onClose: () => void;
  onSelectPlayer: (p: ScoutPlayer) => void;
}

export default function PlayerProfileModal({ player, allPlayers, onClose, onSelectPlayer }: Props) {
  const stats = player.stats?.[0];
  const eval_ = player.evaluation;
  const radarAxes = useMemo(() => computeRadarAxes(stats), [stats]);
  const primaryPos = player.positions.find((p) => p.isPrimary)?.position ?? player.positions[0]?.position;

  const similarPlayers = useMemo(() => {
    if (!primaryPos) return [];
    return allPlayers
      .filter((p) => p.id !== player.id && p.positions.some((pos) => pos.position === primaryPos))
      .sort((a, b) => {
        const ageDiff = Math.abs(a.age - player.age) - Math.abs(b.age - player.age);
        const scoreDiff = Math.abs((b.evaluation?.overallScore ?? 50) - (eval_?.overallScore ?? 50)) -
          Math.abs((a.evaluation?.overallScore ?? 50) - (eval_?.overallScore ?? 50));
        return ageDiff + scoreDiff;
      })
      .slice(0, 5);
  }, [allPlayers, player, primaryPos, eval_]);

  useEffect(() => {
    const handler = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [onClose]);

  const overallScore = eval_?.overallScore ?? 50;
  const scoreColor = overallScore >= 85 ? "#22c55e" : overallScore >= 70 ? "#eab308" : overallScore >= 55 ? "#f97316" : "#ef4444";

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
      <div className="absolute inset-0 bg-black/70 backdrop-blur-sm" onClick={onClose} />
      <div className="relative w-full max-w-5xl max-h-[92vh] bg-[#0f0f1a] border border-[#2a2a38] rounded-2xl overflow-hidden flex flex-col shadow-2xl">

        {/* Top bar */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-[#2a2a38] bg-[#111118]">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-full bg-[#2a2a38] flex items-center justify-center text-lg font-bold text-violet-400">
              {player.name.charAt(0)}
            </div>
            <div>
              <h2 className="text-base font-bold text-white leading-tight">{player.name}</h2>
              <p className="text-xs text-zinc-400">{player.flag} {player.nationality} · {player.currentClub} · {player.league}</p>
            </div>
          </div>
          <div className="flex items-center gap-2">
            {player.soccerdonnaUrl && (
              <a href={player.soccerdonnaUrl} target="_blank" rel="noopener noreferrer"
                className="text-xs px-3 py-1.5 rounded-lg border border-[#2a2a38] text-zinc-400 hover:text-zinc-200 hover:border-zinc-600 flex items-center gap-1.5 transition-colors">
                <ExternalLink size={11} />
                SoccerDonna
              </a>
            )}
            <button onClick={onClose} className="w-8 h-8 rounded-lg bg-[#1a1a28] hover:bg-[#2a2a38] flex items-center justify-center text-zinc-400 hover:text-white transition-colors">
              <X size={16} />
            </button>
          </div>
        </div>

        {/* Body */}
        <div className="flex-1 overflow-y-auto">
          <div className="grid grid-cols-5 divide-x divide-[#2a2a38]">

            {/* ─── LEFT PANEL (2 cols) ─────────────────────────────────────── */}
            <div className="col-span-2 p-5 space-y-5">

              {/* Overall score */}
              <div className="bg-[#111118] rounded-xl p-4 flex items-center gap-4">
                <div
                  className="w-16 h-16 rounded-2xl flex items-center justify-center text-2xl font-black border-2"
                  style={{ borderColor: scoreColor, color: scoreColor, backgroundColor: `${scoreColor}18` }}
                >
                  {overallScore}
                </div>
                <div>
                  <p className="text-[10px] text-zinc-500 uppercase tracking-widest">Genel Skor</p>
                  <p className="text-lg font-bold" style={{ color: scoreColor }}>{eval_?.overallGrade ?? "—"}</p>
                  <p className="text-[10px] text-zinc-500">100 üzerinden</p>
                </div>
              </div>

              {/* Radar chart */}
              <div>
                <p className="text-[10px] text-zinc-500 uppercase tracking-widest mb-2">Performans Radar</p>
                <div className="bg-[#111118] rounded-xl p-2">
                  <ScoutRadarChart axes={radarAxes} color="#8b5cf6" size={240} />
                </div>
              </div>

              {/* Evaluation grades */}
              {eval_ && (
                <div className="space-y-3">
                  {[
                    { icon: <Shield size={11} />, title: "BECERİ", items: [
                      { key: "technicalSkill", label: "Teknik" }, { key: "ballControl", label: "Top Kontrolü" },
                      { key: "finishing", label: "Bitiricilik" }, { key: "passing", label: "Pas" },
                      { key: "dribbling", label: "Dribling" }, { key: "crossing", label: "Orta" },
                    ]},
                    { icon: <Brain size={11} />, title: "BEŞERİ — Zihinsel", items: [
                      { key: "decisionMaking", label: "Karar Alma" }, { key: "positioning", label: "Pozisyon" },
                      { key: "leadership", label: "Liderlik" }, { key: "composure", label: "Soğukkanlılık" },
                    ]},
                    { icon: <Dumbbell size={11} />, title: "FİZİKİ", items: [
                      { key: "pace", label: "Hız" }, { key: "strength", label: "Güç" },
                      { key: "stamina", label: "Kondisyon" }, { key: "agility", label: "Çeviklik" },
                    ]},
                    { icon: <Palette size={11} />, title: "TARZ", items: [
                      { key: "pressingIntensity", label: "Pres Yoğunluğu" },
                      { key: "buildUpPlay", label: "Top Çıkarma" },
                      { key: "defensiveShape", label: "Def. Düzeni" },
                    ]},
                  ].map(({ icon, title, items }) => (
                    <div key={title} className="bg-[#111118] rounded-xl p-3">
                      <div className="flex items-center gap-1.5 mb-2">
                        <span className="text-violet-400">{icon}</span>
                        <span className="text-[10px] font-semibold text-zinc-400 uppercase tracking-widest">{title}</span>
                      </div>
                      {items.map(({ key, label }) => (
                        <GradeBadge key={key} grade={(eval_ as any)[key]} label={label} />
                      ))}
                    </div>
                  ))}
                </div>
              )}

              {/* Similar players */}
              {similarPlayers.length > 0 && (
                <div>
                  <p className="text-[10px] text-zinc-500 uppercase tracking-widest mb-2">Benzer Oyuncular</p>
                  <div className="bg-[#111118] rounded-xl p-2 space-y-0.5">
                    {similarPlayers.map((p) => (
                      <SimilarPlayerRow key={p.id} player={p} onClick={() => onSelectPlayer(p)} />
                    ))}
                  </div>
                </div>
              )}
            </div>

            {/* ─── RIGHT PANEL (3 cols) ────────────────────────────────────── */}
            <div className="col-span-3 p-5 space-y-5 overflow-y-auto">

              {/* Profile info */}
              <div className="bg-[#111118] rounded-xl p-4">
                <p className="text-[10px] text-zinc-500 uppercase tracking-widest mb-3">Profil Bilgileri</p>
                <div className="grid grid-cols-2 gap-x-6 gap-y-2 text-xs">
                  {[
                    ["Takım", player.currentClub],
                    ["Lig", player.league],
                    ["Ülke", `${player.flag ?? ""} ${player.nationality}`],
                    ["Yaş", `${player.age} (${player.birthDate ? new Date(player.birthDate).getFullYear() : "—"})`],
                    ["Boy", player.height ? `${player.height} cm` : "—"],
                    ["Güçlü Ayak", player.foot === "RIGHT" ? "Sağ" : player.foot === "LEFT" ? "Sol" : "Her İkisi"],
                    ["Kontrat Bitiş", formatContractEnd(player.contractEnd)],
                    ["Piyasa Değeri", formatMarketValue(player.marketValue)],
                    ["Temsilci", player.agentName ?? "—"],
                    ["Pozisyon", player.positions.map((p) => p.position).join(", ")],
                  ].map(([label, value]) => (
                    <div key={label} className="flex items-baseline gap-1">
                      <span className="text-zinc-500 shrink-0">{label}:</span>
                      <span className={cn("text-zinc-200 truncate", label === "Kontrat Bitiş" && contractEndColor(player.contractEnd))}>{value}</span>
                    </div>
                  ))}
                </div>
              </div>

              {stats && (
                <>
                  {/* Metric progress bars */}
                  <div className="bg-[#111118] rounded-xl p-4">
                    <p className="text-[10px] text-zinc-500 uppercase tracking-widest mb-3">Metrik İlerleme</p>
                    <div className="grid grid-cols-2 gap-x-5 gap-y-2.5">
                      <StatBar label="Pas Doğruluğu" value={stats.passAccuracy} unit="%" />
                      <StatBar label="Dribling Başarı" value={stats.dribbleSuccess} unit="%" />
                      <StatBar label="Def. Düello" value={stats.defDuelSuccess} unit="%" />
                      <StatBar label="Hava Düellosu" value={stats.aerialSuccess} unit="%" />
                      <StatBar label="Pres Başarı" value={stats.pressureSuccess} unit="%" />
                      {stats.saveRate != null && <StatBar label="Kurtarış Oranı" value={stats.saveRate} unit="%" />}
                    </div>
                  </div>

                  {/* Maç & Atak */}
                  <div className="bg-[#111118] rounded-xl p-4">
                    <p className="text-[10px] text-zinc-500 uppercase tracking-widest mb-3 flex items-center gap-1">
                      <Zap size={10} className="text-amber-400" /> Maç & Atak
                    </p>
                    <div className="grid grid-cols-4 gap-2">
                      <StatCard label="Maç" value={stats.matches.toString()} />
                      <StatCard label="Dakika" value={stats.minutes.toString()} />
                      <StatCard label="Gol" value={stats.goals} />
                      <StatCard label="Asist" value={stats.assists} />
                      <StatCard label="xG" value={stats.xG} />
                      <StatCard label="xG/90" value={stats.xG90} />
                      <StatCard label="Şut/90" value={stats.shots90} />
                      <StatCard label="PA Dok./90" value={stats.penAreaTouch90} />
                    </div>
                  </div>

                  {/* Dribling & Taşıma */}
                  <div className="bg-[#111118] rounded-xl p-4">
                    <p className="text-[10px] text-zinc-500 uppercase tracking-widest mb-3 flex items-center gap-1">
                      <Zap size={10} className="text-blue-400" /> Dribling & Taşıma
                    </p>
                    <div className="grid grid-cols-4 gap-2">
                      <StatCard label="Dribling/90" value={stats.dribbles90} />
                      <StatCard label="Başarı %" value={stats.dribbleSuccess} unit="%" />
                      <StatCard label="Prog. Koşu/90" value={stats.progressiveRuns90} />
                      <StatCard label="Taşıma/90" value={stats.carries90} />
                    </div>
                  </div>

                  {/* Pas */}
                  <div className="bg-[#111118] rounded-xl p-4">
                    <p className="text-[10px] text-zinc-500 uppercase tracking-widest mb-3 flex items-center gap-1">
                      <Zap size={10} className="text-emerald-400" /> Pas
                    </p>
                    <div className="grid grid-cols-4 gap-2">
                      <StatCard label="Pas/90" value={stats.passes90} />
                      <StatCard label="Doğruluk" value={stats.passAccuracy} unit="%" />
                      <StatCard label="İleri Pas/90" value={stats.forwardPasses90} />
                      <StatCard label="Uzun Pas/90" value={stats.longPasses90} />
                      <StatCard label="Anahtar/90" value={stats.keyPasses90} />
                      <StatCard label="Smart/90" value={stats.smartPasses90} />
                      <StatCard label="Ara Pas/90" value={stats.throughBalls90} />
                      <StatCard label="Uzun Pas %" value={stats.longPassAccuracy} unit="%" />
                    </div>
                  </div>

                  {/* Defans */}
                  <div className="bg-[#111118] rounded-xl p-4">
                    <p className="text-[10px] text-zinc-500 uppercase tracking-widest mb-3 flex items-center gap-1">
                      <Shield size={10} className="text-red-400" /> Defans
                    </p>
                    <div className="grid grid-cols-4 gap-2">
                      <StatCard label="Def. Aksiyon/90" value={stats.defActions90} />
                      <StatCard label="Def. Düello/90" value={stats.defDuels90} />
                      <StatCard label="Düello %" value={stats.defDuelSuccess} unit="%" />
                      <StatCard label="Hava Düellosu/90" value={stats.aerialDuels90} />
                      <StatCard label="Hava %" value={stats.aerialSuccess} unit="%" />
                      <StatCard label="Top Kapma/90" value={stats.interceptions90} />
                      <StatCard label="Müd./90" value={stats.tackles90} />
                      <StatCard label="Pres/90" value={stats.pressures90} />
                    </div>
                  </div>

                  {/* GK stats if available */}
                  {stats.saves90 != null && (
                    <div className="bg-[#111118] rounded-xl p-4">
                      <p className="text-[10px] text-zinc-500 uppercase tracking-widest mb-3 flex items-center gap-1">
                        <Shield size={10} className="text-violet-400" /> Kaleci
                      </p>
                      <div className="grid grid-cols-4 gap-2">
                        <StatCard label="Kurtarış/90" value={stats.saves90 ?? 0} />
                        <StatCard label="Kurtarış %" value={stats.saveRate ?? 0} unit="%" />
                      </div>
                    </div>
                  )}
                </>
              )}

              {/* Scout notes */}
              {eval_?.notes && (
                <div className="bg-[#111118] rounded-xl p-4">
                  <p className="text-[10px] text-zinc-500 uppercase tracking-widest mb-2">Scout Notu</p>
                  <p className="text-xs text-zinc-300 leading-relaxed">{eval_.notes}</p>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
