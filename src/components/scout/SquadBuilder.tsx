"use client";

import { useState } from "react";
import { Plus, X, AlertTriangle } from "lucide-react";
import { cn, formatContractEnd, contractEndColor } from "@/lib/utils";
import type { ScoutPlayer, SquadPlan, Position } from "@/types/scout";
import { FORMATION_POSITIONS, POSITION_LABELS, GRADE_WEIGHTS } from "@/types/scout";

const FORMATIONS = ["4-3-3", "4-2-3-1", "3-5-2"];

interface SlotCardProps {
  position: Position;
  slotIndex: number;
  player?: ScoutPlayer;
  isTarget?: boolean;
  availablePlayers: ScoutPlayer[];
  onAssign: (pos: Position, slotIndex: number, playerId: number | null) => void;
}

function SlotCard({ position, slotIndex, player, isTarget, availablePlayers, onAssign }: SlotCardProps) {
  const [open, setOpen] = useState(false);
  const isExpiringContract = player?.contractEnd
    ? (new Date(player.contractEnd).getTime() - Date.now()) / (1000 * 60 * 60 * 24 * 30) < 12
    : false;

  const bgColor = slotIndex === 0 ? "bg-[#1a1a28]" : slotIndex === 1 ? "bg-[#151520]" : "bg-[#111118]";
  const borderColor = slotIndex === 0 ? "border-violet-500/30" : slotIndex === 1 ? "border-[#2a2a38]" : "border-[#1e1e2e]";
  const label = slotIndex === 0 ? "STARTER" : slotIndex === 1 ? "1. YEDEK" : "2. YEDEK";
  const score = player?.evaluation?.overallScore;
  const scoreGrade = player?.evaluation?.overallGrade;

  return (
    <div className={cn("relative border rounded-lg", bgColor, borderColor, isTarget && "border-dashed border-amber-500/40")}>
      {/* Slot label */}
      <div className="flex items-center justify-between px-2 py-1 border-b border-[#1e1e2e]">
        <span className="text-[8px] font-bold uppercase tracking-widest text-zinc-600">{label}</span>
        {isExpiringContract && (
          <span title="Kontrat bitiyor!" className="text-amber-400"><AlertTriangle size={9} /></span>
        )}
      </div>

      {/* Player slot */}
      <div className="p-2">
        {player ? (
          <div className="flex items-center gap-1.5">
            <div className="w-6 h-6 rounded-full bg-[#2a2a38] flex items-center justify-center text-[10px] font-bold text-violet-400 shrink-0">
              {player.name.charAt(0)}
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-[10px] font-medium text-zinc-200 truncate leading-tight">{player.name}</p>
              {score && <p className="text-[9px] text-violet-400 font-mono">{scoreGrade} · {score}</p>}
            </div>
            <button onClick={() => onAssign(position, slotIndex, null)}
              className="w-4 h-4 rounded flex items-center justify-center text-zinc-600 hover:text-red-400 transition-colors shrink-0">
              <X size={9} />
            </button>
          </div>
        ) : (
          <button onClick={() => setOpen(true)}
            className="w-full flex items-center justify-center gap-1 py-1.5 text-zinc-600 hover:text-violet-400 transition-colors group">
            <Plus size={10} className="group-hover:text-violet-400" />
            <span className="text-[9px]">Oyuncu Ekle</span>
          </button>
        )}
      </div>

      {/* Player picker dropdown */}
      {open && (
        <div className="absolute top-full left-0 w-52 bg-[#1a1a28] border border-[#2a2a38] rounded-lg shadow-xl z-20 overflow-hidden mt-1">
          <div className="p-1.5 border-b border-[#2a2a38]">
            <p className="text-[10px] text-zinc-500 px-1">{POSITION_LABELS[position]} seç</p>
          </div>
          <div className="max-h-40 overflow-y-auto">
            {availablePlayers.map((p) => (
              <button key={p.id}
                onClick={() => { onAssign(position, slotIndex, p.id); setOpen(false); }}
                className="w-full flex items-center gap-2 px-2.5 py-1.5 hover:bg-[#2a2a38] transition-colors text-left">
                <div className="w-5 h-5 rounded-full bg-[#2a2a38] flex items-center justify-center text-[9px] font-bold text-violet-400 shrink-0">
                  {p.name.charAt(0)}
                </div>
                <div className="flex-1 min-w-0">
                  <p className="text-[10px] text-zinc-200 truncate">{p.name}</p>
                  <p className="text-[9px] text-zinc-500">{p.currentClub}</p>
                </div>
                {p.evaluation?.overallGrade && (
                  <span className="text-[9px] text-violet-400 font-bold shrink-0">{p.evaluation.overallGrade}</span>
                )}
              </button>
            ))}
            {availablePlayers.length === 0 && (
              <p className="text-[10px] text-zinc-600 px-3 py-3 text-center">Bu mevki için oyuncu yok</p>
            )}
          </div>
          <button onClick={() => setOpen(false)}
            className="w-full py-1.5 text-[10px] text-zinc-600 hover:text-zinc-300 transition-colors border-t border-[#2a2a38]">
            Kapat
          </button>
        </div>
      )}
    </div>
  );
}

interface Props {
  allPlayers: ScoutPlayer[];
  favoritePlayers: ScoutPlayer[];
  incomingPlayers: ScoutPlayer[];
}

export default function SquadBuilder({ allPlayers, favoritePlayers, incomingPlayers }: Props) {
  const [formation, setFormation] = useState<string>("4-3-3");
  const [teamName, setTeamName] = useState("Takımım");
  const [season, setSeason] = useState("2025-26");
  // slots: key = `${position}_${slotIndex}` => playerId
  const [slots, setSlots] = useState<Record<string, number | null>>({});

  const positionDefs = FORMATION_POSITIONS[formation] ?? [];

  const getAssignedPlayer = (pos: Position, slotIdx: number) => {
    const key = `${pos}_${slotIdx}`;
    const id = slots[key];
    return id != null ? allPlayers.find((p) => p.id === id) : undefined;
  };

  const handleAssign = (pos: Position, slotIdx: number, playerId: number | null) => {
    setSlots((prev) => ({ ...prev, [`${pos}_${slotIdx}`]: playerId }));
  };

  const getAvailableForPosition = (pos: Position) => {
    const matchingPlayerIds = new Set(Object.values(slots).filter(Boolean));
    const posGroup = pos === "GK" ? ["GK"] :
      ["RB", "LB", "CB", "RCB", "LCB"].includes(pos) ? ["RB", "LB", "CB", "RCB", "LCB"] :
      ["DM", "CM", "AM", "RM", "LM"].includes(pos) ? ["DM", "CM", "AM", "RM", "LM"] :
      ["RW", "LW", "SS", "CF"];

    return [...allPlayers, ...favoritePlayers.filter((p) => !allPlayers.find((ap) => ap.id === p.id))]
      .filter((p) => p.positions.some((pp) => posGroup.includes(pp.position)))
      .filter((p) => !matchingPlayerIds.has(p.id));
  };

  // Count expiring contracts in plan
  const expiringCount = positionDefs.flatMap((_, i) =>
    [0, 1, 2].map((si) => getAssignedPlayer(_ as any, si))
  ).filter((p) => {
    if (!p?.contractEnd) return false;
    return (new Date(p.contractEnd).getTime() - Date.now()) / (1000 * 60 * 60 * 24 * 30) < 12;
  }).length;

  return (
    <div className="p-6 space-y-5">
      {/* Controls */}
      <div className="flex flex-wrap items-center gap-3">
        <div>
          <label className="text-[10px] text-zinc-500 uppercase tracking-widest block mb-1">Takım Adı</label>
          <input value={teamName} onChange={(e) => setTeamName(e.target.value)}
            className="bg-[#1a1a28] border border-[#2a2a38] rounded-lg px-3 py-2 text-xs text-zinc-200 focus:outline-none focus:border-violet-500 w-44"
          />
        </div>
        <div>
          <label className="text-[10px] text-zinc-500 uppercase tracking-widest block mb-1">Sezon</label>
          <input value={season} onChange={(e) => setSeason(e.target.value)}
            className="bg-[#1a1a28] border border-[#2a2a38] rounded-lg px-3 py-2 text-xs text-zinc-200 focus:outline-none focus:border-violet-500 w-28"
          />
        </div>
        <div>
          <label className="text-[10px] text-zinc-500 uppercase tracking-widest block mb-1">Diziliş</label>
          <div className="flex gap-1">
            {FORMATIONS.map((f) => (
              <button key={f} onClick={() => setFormation(f)}
                className={cn("px-3 py-2 rounded-lg text-xs border transition-colors", formation === f ? "bg-violet-600 border-violet-500 text-white" : "bg-[#1a1a28] border-[#2a2a38] text-zinc-400 hover:border-violet-500/50")}>
                {f}
              </button>
            ))}
          </div>
        </div>
        {expiringCount > 0 && (
          <div className="flex items-center gap-1.5 px-3 py-2 rounded-lg bg-amber-500/10 border border-amber-500/30 text-amber-400">
            <AlertTriangle size={12} />
            <span className="text-xs">{expiringCount} kontrat bitiyor</span>
          </div>
        )}
      </div>

      {/* Depth chart grid */}
      <div>
        <p className="text-[10px] text-zinc-500 uppercase tracking-widest mb-3">
          Derinlik Şeması — {teamName} · {season} · {formation}
        </p>

        {/* Column headers */}
        <div className="grid grid-cols-4 gap-2 mb-2">
          <div className="text-[9px] font-bold text-zinc-600 uppercase tracking-widest">Pozisyon</div>
          <div className="text-[9px] font-bold text-violet-500 uppercase tracking-widest">Starter</div>
          <div className="text-[9px] font-bold text-zinc-500 uppercase tracking-widest">1. Yedek</div>
          <div className="text-[9px] font-bold text-zinc-600 uppercase tracking-widest">2. Yedek</div>
        </div>

        <div className="space-y-2">
          {positionDefs.map((posDef, rowIdx) => (
            <div key={`${posDef.pos}-${rowIdx}`} className="grid grid-cols-4 gap-2 items-start">
              {/* Position label */}
              <div className="flex items-center gap-2 py-2">
                <span className="bg-[#2a2a38] text-zinc-300 px-2 py-0.5 rounded text-[10px] font-mono">{posDef.pos}</span>
                <span className="text-[10px] text-zinc-600 truncate">{POSITION_LABELS[posDef.pos]}</span>
              </div>

              {/* Three depth slots */}
              {[0, 1, 2].map((slotIdx) => (
                <SlotCard
                  key={slotIdx}
                  position={posDef.pos}
                  slotIndex={slotIdx}
                  player={getAssignedPlayer(posDef.pos, slotIdx)}
                  availablePlayers={getAvailableForPosition(posDef.pos)}
                  onAssign={handleAssign}
                />
              ))}
            </div>
          ))}
        </div>
      </div>

      {/* Legend */}
      <div className="flex items-center gap-4 pt-2 text-[10px] text-zinc-600">
        <span className="flex items-center gap-1"><AlertTriangle size={9} className="text-amber-400" /> Kontrat bitiyor (&lt;12 ay)</span>
        <span className="flex items-center gap-1"><span className="w-2 h-px border-t border-dashed border-amber-500/60" /> Hedef (transfer edilmemiş)</span>
      </div>
    </div>
  );
}
