"use client";

import { useState } from "react";
import { ChevronUp, ChevronDown, Eye, Star, UserPlus } from "lucide-react";
import { cn, formatMarketValue, formatContractEnd, contractEndColor } from "@/lib/utils";
import type { ScoutPlayer, SortKey, SortDir } from "@/types/scout";
import { gradeColor, POSITION_LABELS } from "@/types/scout";

interface Props {
  players: ScoutPlayer[];
  favorites: number[];
  onViewPlayer: (p: ScoutPlayer) => void;
  onToggleFavorite: (id: number) => void;
  onAddToIncoming: (p: ScoutPlayer) => void;
}

function SortTh({ label, sortKey, current, dir, onSort }: {
  label: string; sortKey: SortKey; current: SortKey; dir: SortDir;
  onSort: (k: SortKey) => void;
}) {
  const active = current === sortKey;
  return (
    <th
      className={cn("text-left py-2.5 px-3 text-[10px] font-semibold uppercase tracking-widest cursor-pointer select-none whitespace-nowrap transition-colors", active ? "text-violet-400" : "text-zinc-500 hover:text-zinc-300")}
      onClick={() => onSort(sortKey)}
    >
      <span className="flex items-center gap-0.5">
        {label}
        {active ? (dir === "asc" ? <ChevronUp size={10} /> : <ChevronDown size={10} />) : null}
      </span>
    </th>
  );
}

const SCORE_RING = (s: number) => s >= 85 ? "text-emerald-400 border-emerald-500/50" : s >= 70 ? "text-yellow-400 border-yellow-500/50" : s >= 55 ? "text-orange-400 border-orange-500/50" : "text-red-400 border-red-500/50";

export default function AllPlayersTable({ players, favorites, onViewPlayer, onToggleFavorite, onAddToIncoming }: Props) {
  const [sortKey, setSortKey] = useState<SortKey>("overallScore");
  const [sortDir, setSortDir] = useState<SortDir>("desc");

  const handleSort = (key: SortKey) => {
    if (key === sortKey) setSortDir((d) => (d === "asc" ? "desc" : "asc"));
    else { setSortKey(key); setSortDir("desc"); }
  };

  const sorted = [...players].sort((a, b) => {
    let av: number | string = 0;
    let bv: number | string = 0;
    switch (sortKey) {
      case "name": av = a.name; bv = b.name; break;
      case "age": av = a.age; bv = b.age; break;
      case "marketValue": av = a.marketValue; bv = b.marketValue; break;
      case "contractEnd":
        av = a.contractEnd ?? ""; bv = b.contractEnd ?? ""; break;
      case "xG90": av = a.stats?.[0]?.xG90 ?? 0; bv = b.stats?.[0]?.xG90 ?? 0; break;
      case "passes90": av = a.stats?.[0]?.passAccuracy ?? 0; bv = b.stats?.[0]?.passAccuracy ?? 0; break;
      case "dribbleSuccess": av = a.stats?.[0]?.dribbleSuccess ?? 0; bv = b.stats?.[0]?.dribbleSuccess ?? 0; break;
      case "defActions90": av = a.stats?.[0]?.defActions90 ?? 0; bv = b.stats?.[0]?.defActions90 ?? 0; break;
      case "overallScore": av = a.evaluation?.overallScore ?? 0; bv = b.evaluation?.overallScore ?? 0; break;
    }
    if (typeof av === "string") return sortDir === "asc" ? av.localeCompare(bv as string) : (bv as string).localeCompare(av);
    return sortDir === "asc" ? (av as number) - (bv as number) : (bv as number) - (av as number);
  });

  return (
    <div className="overflow-x-auto">
      <table className="w-full text-xs">
        <thead>
          <tr className="border-b border-[#2a2a38]">
            <SortTh label="Oyuncu" sortKey="name" current={sortKey} dir={sortDir} onSort={handleSort} />
            <th className="text-left py-2.5 px-3 text-[10px] font-semibold uppercase tracking-widest text-zinc-500 whitespace-nowrap">Pozisyon</th>
            <th className="text-left py-2.5 px-3 text-[10px] font-semibold uppercase tracking-widest text-zinc-500 whitespace-nowrap">Kulüp / Lig</th>
            <SortTh label="Yaş" sortKey="age" current={sortKey} dir={sortDir} onSort={handleSort} />
            <SortTh label="Kontrat" sortKey="contractEnd" current={sortKey} dir={sortDir} onSort={handleSort} />
            <SortTh label="Değer" sortKey="marketValue" current={sortKey} dir={sortDir} onSort={handleSort} />
            <SortTh label="xG/90" sortKey="xG90" current={sortKey} dir={sortDir} onSort={handleSort} />
            <SortTh label="Pas %" sortKey="passes90" current={sortKey} dir={sortDir} onSort={handleSort} />
            <SortTh label="Drib %" sortKey="dribbleSuccess" current={sortKey} dir={sortDir} onSort={handleSort} />
            <SortTh label="Def./90" sortKey="defActions90" current={sortKey} dir={sortDir} onSort={handleSort} />
            <SortTh label="Skor" sortKey="overallScore" current={sortKey} dir={sortDir} onSort={handleSort} />
            <th className="py-2.5 px-3" />
          </tr>
        </thead>
        <tbody>
          {sorted.length === 0 && (
            <tr>
              <td colSpan={12} className="text-center py-16 text-zinc-600">
                Filtrelerle eşleşen oyuncu bulunamadı.
              </td>
            </tr>
          )}
          {sorted.map((player) => {
            const stats = player.stats?.[0];
            const score = player.evaluation?.overallScore ?? null;
            const grade = player.evaluation?.overallGrade ?? null;
            const primaryPos = player.positions.find((p) => p.isPrimary)?.position ?? player.positions[0]?.position;
            const isFav = favorites.includes(player.id);

            return (
              <tr
                key={player.id}
                className="border-b border-[#1a1a28] hover:bg-[#13131f] transition-colors group"
              >
                {/* Player name */}
                <td className="py-3 px-3">
                  <div className="flex items-center gap-2.5">
                    <div className="w-7 h-7 rounded-full bg-[#2a2a38] flex items-center justify-center text-xs font-bold text-violet-400 shrink-0">
                      {player.name.charAt(0)}
                    </div>
                    <div>
                      <button onClick={() => onViewPlayer(player)} className="font-medium text-zinc-100 hover:text-violet-300 transition-colors text-left">
                        {player.name}
                      </button>
                      <p className="text-[10px] text-zinc-500">{player.flag} {player.nationality}</p>
                    </div>
                  </div>
                </td>

                {/* Position */}
                <td className="py-3 px-3">
                  {primaryPos && (
                    <span className="bg-[#2a2a38] text-zinc-300 px-1.5 py-0.5 rounded text-[10px] font-mono">
                      {primaryPos}
                    </span>
                  )}
                </td>

                {/* Club / League */}
                <td className="py-3 px-3">
                  <p className="text-zinc-300 truncate max-w-[140px]">{player.currentClub}</p>
                  <p className="text-[10px] text-zinc-500 truncate">{player.league}</p>
                </td>

                {/* Age */}
                <td className="py-3 px-3 text-zinc-300 font-mono">{player.age}</td>

                {/* Contract end */}
                <td className={cn("py-3 px-3 font-mono whitespace-nowrap", contractEndColor(player.contractEnd))}>
                  {formatContractEnd(player.contractEnd)}
                </td>

                {/* Market value */}
                <td className="py-3 px-3 text-zinc-300 font-mono whitespace-nowrap">
                  {formatMarketValue(player.marketValue)}
                </td>

                {/* Stats */}
                <td className="py-3 px-3 text-zinc-300 font-mono">{stats?.xG90.toFixed(2) ?? "—"}</td>
                <td className="py-3 px-3 text-zinc-300 font-mono">{stats ? `${stats.passAccuracy.toFixed(0)}%` : "—"}</td>
                <td className="py-3 px-3 text-zinc-300 font-mono">{stats ? `${stats.dribbleSuccess.toFixed(0)}%` : "—"}</td>
                <td className="py-3 px-3 text-zinc-300 font-mono">{stats?.defActions90.toFixed(2) ?? "—"}</td>

                {/* Score */}
                <td className="py-3 px-3">
                  {score !== null ? (
                    <div className="flex items-center gap-1.5">
                      <span className={cn("w-7 h-7 rounded-full border flex items-center justify-center text-[10px] font-bold", SCORE_RING(score))}>
                        {grade}
                      </span>
                      <span className="text-zinc-400 font-mono text-[10px]">{score}</span>
                    </div>
                  ) : <span className="text-zinc-600">—</span>}
                </td>

                {/* Actions */}
                <td className="py-3 px-3">
                  <div className="flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                    <button onClick={() => onViewPlayer(player)} title="Profili Görüntüle"
                      className="w-7 h-7 rounded bg-[#2a2a38] hover:bg-violet-600 flex items-center justify-center text-zinc-400 hover:text-white transition-colors">
                      <Eye size={12} />
                    </button>
                    <button onClick={() => onToggleFavorite(player.id)} title={isFav ? "Favorilerden Çıkar" : "Favorilere Ekle"}
                      className={cn("w-7 h-7 rounded flex items-center justify-center transition-colors",
                        isFav ? "bg-amber-600/20 text-amber-400" : "bg-[#2a2a38] hover:bg-amber-600/20 text-zinc-400 hover:text-amber-400")}>
                      <Star size={12} fill={isFav ? "currentColor" : "none"} />
                    </button>
                    <button onClick={() => onAddToIncoming(player)} title="Gelen Kutusu'na Ekle"
                      className="w-7 h-7 rounded bg-[#2a2a38] hover:bg-emerald-600/20 flex items-center justify-center text-zinc-400 hover:text-emerald-400 transition-colors">
                      <UserPlus size={12} />
                    </button>
                  </div>
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}
