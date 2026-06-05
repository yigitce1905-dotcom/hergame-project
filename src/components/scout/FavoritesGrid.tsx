"use client";

import { useState } from "react";
import { Star, Trash2, Check, ExternalLink } from "lucide-react";
import { cn, formatMarketValue, formatContractEnd, contractEndColor } from "@/lib/utils";
import type { FavoriteEntry } from "@/types/scout";
import { gradeColor, GRADE_WEIGHTS } from "@/types/scout";

interface Props {
  entries: FavoriteEntry[];
  onRemove: (id: number) => void;
  onNotesChange: (id: number, notes: string) => void;
  onViewPlayer: (entry: FavoriteEntry) => void;
}

export default function FavoritesGrid({ entries, onRemove, onNotesChange, onViewPlayer }: Props) {
  const [editingId, setEditingId] = useState<number | null>(null);
  const [draft, setDraft] = useState("");

  if (entries.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center py-24 text-zinc-600">
        <Star size={36} className="mb-3 opacity-30" />
        <p className="text-sm font-medium text-zinc-500">Henüz favori oyuncu yok</p>
        <p className="text-xs text-zinc-600 mt-1">Oyuncu listesinden ★ ikonuna tıklayarak favorilere ekleyin.</p>
      </div>
    );
  }

  return (
    <div className="p-6">
      <div className="flex items-center justify-between mb-5">
        <div>
          <h2 className="text-sm font-bold text-white">Favoriler</h2>
          <p className="text-xs text-zinc-500 mt-0.5">{entries.length} oyuncu takipte</p>
        </div>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-4">
        {entries.map((entry) => {
          const p = entry.player;
          const score = p.evaluation?.overallScore ?? null;
          const grade = p.evaluation?.overallGrade ?? null;
          const scoreColor = score ? gradeColor(p.evaluation?.overallGrade ?? "CC") : "#6b7280";
          const primaryPos = p.positions.find((pos) => pos.isPrimary)?.position ?? p.positions[0]?.position;
          const isEditing = editingId === entry.id;

          return (
            <div key={entry.id} className="bg-[#111118] border border-[#2a2a38] rounded-xl overflow-hidden group hover:border-[#3a3a4e] transition-colors">
              {/* Card header */}
              <div className="p-4 border-b border-[#1e1e2e]">
                <div className="flex items-start gap-3">
                  {/* Avatar */}
                  <div
                    className="w-12 h-12 rounded-xl flex items-center justify-center text-xl font-black border-2 shrink-0"
                    style={{ borderColor: scoreColor, backgroundColor: `${scoreColor}18`, color: scoreColor }}
                  >
                    {p.name.charAt(0)}
                  </div>

                  {/* Info */}
                  <div className="flex-1 min-w-0">
                    <div className="flex items-start justify-between gap-1">
                      <button onClick={() => onViewPlayer(entry)} className="font-bold text-zinc-100 hover:text-violet-300 transition-colors text-sm text-left leading-tight">
                        {p.name}
                      </button>
                      {grade && (
                        <span className="text-xs font-black shrink-0 ml-1" style={{ color: scoreColor }}>
                          {grade}
                        </span>
                      )}
                    </div>
                    <p className="text-[11px] text-zinc-400 mt-0.5">{p.flag} {p.nationality}</p>
                    <p className="text-[11px] text-zinc-500 truncate">{p.currentClub} · {p.league}</p>
                  </div>
                </div>

                {/* Stats row */}
                <div className="mt-3 grid grid-cols-4 gap-1 text-center">
                  <div className="bg-[#1a1a28] rounded-lg py-1.5">
                    <p className="text-[9px] text-zinc-600 mb-0.5">YAŞ</p>
                    <p className="text-xs font-bold text-zinc-200">{p.age}</p>
                  </div>
                  <div className="bg-[#1a1a28] rounded-lg py-1.5">
                    <p className="text-[9px] text-zinc-600 mb-0.5">POS</p>
                    <p className="text-xs font-bold text-zinc-200">{primaryPos ?? "—"}</p>
                  </div>
                  <div className="bg-[#1a1a28] rounded-lg py-1.5">
                    <p className="text-[9px] text-zinc-600 mb-0.5">DEĞER</p>
                    <p className="text-xs font-bold text-zinc-200">{formatMarketValue(p.marketValue)}</p>
                  </div>
                  <div className="bg-[#1a1a28] rounded-lg py-1.5">
                    <p className="text-[9px] text-zinc-600 mb-0.5">KONTR.</p>
                    <p className={cn("text-xs font-bold", contractEndColor(p.contractEnd))}>{formatContractEnd(p.contractEnd)}</p>
                  </div>
                </div>

                {/* Agent */}
                {p.agentName && p.agentName !== "—" && (
                  <p className="text-[10px] text-zinc-500 mt-2 flex items-center gap-1">
                    <span className="text-zinc-600">Temsilci:</span>
                    <span className="text-zinc-400">{p.agentName}</span>
                  </p>
                )}
              </div>

              {/* Notes section */}
              <div className="p-3">
                <div className="flex items-center justify-between mb-1.5">
                  <p className="text-[10px] text-zinc-500 uppercase tracking-widest">Scout Notu</p>
                  <div className="flex gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                    <button onClick={() => onViewPlayer(entry)} title="Profili Görüntüle"
                      className="w-5 h-5 rounded flex items-center justify-center text-zinc-600 hover:text-violet-400 transition-colors">
                      <ExternalLink size={10} />
                    </button>
                    <button onClick={() => onRemove(entry.id)} title="Favorilerden Çıkar"
                      className="w-5 h-5 rounded flex items-center justify-center text-zinc-600 hover:text-red-400 transition-colors">
                      <Trash2 size={10} />
                    </button>
                  </div>
                </div>

                {isEditing ? (
                  <div className="space-y-1.5">
                    <textarea
                      autoFocus
                      value={draft}
                      onChange={(e) => setDraft(e.target.value)}
                      rows={4}
                      className="w-full bg-[#1a1a28] border border-violet-500/40 rounded-lg px-2.5 py-2 text-[11px] text-zinc-200 placeholder-zinc-600 focus:outline-none resize-none"
                    />
                    <div className="flex gap-1.5">
                      <button onClick={() => setEditingId(null)} className="flex-1 py-1.5 text-[11px] rounded border border-[#2a2a38] text-zinc-500 hover:text-zinc-300 transition-colors">İptal</button>
                      <button onClick={() => { onNotesChange(entry.id, draft); setEditingId(null); }}
                        className="flex-1 py-1.5 text-[11px] rounded bg-violet-600 hover:bg-violet-700 text-white font-medium flex items-center justify-center gap-1 transition-colors">
                        <Check size={10} /> Kaydet
                      </button>
                    </div>
                  </div>
                ) : (
                  <div
                    onClick={() => { setEditingId(entry.id); setDraft(entry.notes ?? ""); }}
                    className="min-h-[60px] text-[11px] text-zinc-400 leading-relaxed cursor-text hover:text-zinc-300 transition-colors rounded-lg hover:bg-[#1a1a28] p-1.5 -m-1.5"
                  >
                    {entry.notes ?? <span className="text-zinc-600 italic">Not eklemek için tıklayın...</span>}
                  </div>
                )}
              </div>

              {/* Footer */}
              <div className="px-3 pb-2.5 flex items-center justify-between">
                <p className="text-[9px] text-zinc-700">
                  {entry.addedBy && `${entry.addedBy} · `}
                  {new Date(entry.addedAt).toLocaleDateString("tr-TR")}
                </p>
                {score && (
                  <div className="flex items-center gap-1">
                    <div className="w-1.5 h-1.5 rounded-full" style={{ backgroundColor: scoreColor }} />
                    <span className="text-[10px] font-mono" style={{ color: scoreColor }}>{score}/100</span>
                  </div>
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
