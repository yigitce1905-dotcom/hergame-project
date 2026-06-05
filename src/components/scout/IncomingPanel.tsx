"use client";

import { useState } from "react";
import { Plus, Link, ChevronDown, Check } from "lucide-react";
import { cn } from "@/lib/utils";
import type { IncomingEntry, TransferStatus } from "@/types/scout";

const STATUS_CONFIG: Record<TransferStatus, { label: string; color: string; bg: string }> = {
  INTERESTED:  { label: "İlgileniyor",   color: "text-blue-400",   bg: "bg-blue-500/10 border-blue-500/30" },
  CONTACTED:   { label: "Bağlandı",      color: "text-cyan-400",   bg: "bg-cyan-500/10 border-cyan-500/30" },
  NEGOTIATING: { label: "Müzakere",      color: "text-amber-400",  bg: "bg-amber-500/10 border-amber-500/30" },
  SIGNED:      { label: "İmzalandı",     color: "text-emerald-400", bg: "bg-emerald-500/10 border-emerald-500/30" },
  REJECTED:    { label: "Reddedildi",    color: "text-red-400",    bg: "bg-red-500/10 border-red-500/30" },
  ON_HOLD:     { label: "Beklemeye Alındı", color: "text-zinc-400", bg: "bg-zinc-500/10 border-zinc-500/30" },
};

const PRIORITY_LABELS = ["", "Düşük", "Orta", "Yüksek"];
const PRIORITY_COLORS = ["", "text-zinc-400", "text-amber-400", "text-red-400"];

interface AddModalProps {
  onClose: () => void;
  onAdd: (entry: Partial<IncomingEntry>) => void;
}

function AddIncomingModal({ onClose, onAdd }: AddModalProps) {
  const [url, setUrl] = useState("");
  const [name, setName] = useState("");
  const [scout, setScout] = useState("");
  const [notes, setNotes] = useState("");
  const [priority, setPriority] = useState<1 | 2 | 3>(2);
  const [mode, setMode] = useState<"url" | "manual">("url");

  const handleSubmit = () => {
    if (mode === "url" && !url) return;
    if (mode === "manual" && !name) return;
    onAdd({
      rawName: mode === "manual" ? name : undefined,
      soccerdonnaUrl: mode === "url" ? url : undefined,
      recommendedBy: scout || "Scout",
      recommendedAt: new Date().toISOString(),
      status: "INTERESTED",
      notes: notes || undefined,
      priority,
    });
    onClose();
  };

  return (
    <div className="fixed inset-0 z-60 flex items-center justify-center p-4">
      <div className="absolute inset-0 bg-black/60 backdrop-blur-sm" onClick={onClose} />
      <div className="relative w-full max-w-md bg-[#111118] border border-[#2a2a38] rounded-xl p-5 space-y-4 shadow-2xl">
        <h3 className="text-sm font-bold text-white">Oyuncu Öner</h3>

        {/* Mode toggle */}
        <div className="flex rounded-lg overflow-hidden border border-[#2a2a38]">
          {(["url", "manual"] as const).map((m) => (
            <button key={m} onClick={() => setMode(m)}
              className={cn("flex-1 py-2 text-xs transition-colors", mode === m ? "bg-violet-600 text-white" : "bg-[#1a1a28] text-zinc-400 hover:text-zinc-200")}>
              {m === "url" ? "🔗 SoccerDonna URL" : "✏️ Elle Ekle"}
            </button>
          ))}
        </div>

        {mode === "url" ? (
          <div>
            <label className="text-[10px] text-zinc-500 uppercase tracking-widest block mb-1">SoccerDonna Linki</label>
            <div className="flex gap-2">
              <input value={url} onChange={(e) => setUrl(e.target.value)}
                placeholder="https://www.soccerdonna.de/en/player/..."
                className="flex-1 bg-[#1a1a28] border border-[#2a2a38] rounded-lg px-3 py-2 text-xs text-zinc-200 placeholder-zinc-600 focus:outline-none focus:border-violet-500"
              />
              <button className="px-3 py-2 rounded-lg bg-violet-600/20 text-violet-400 hover:bg-violet-600/30 text-xs border border-violet-500/30">
                <Link size={12} />
              </button>
            </div>
            <p className="text-[10px] text-zinc-600 mt-1">URL yapıştırdıktan sonra oyuncu verileri otomatik çekilecek.</p>
          </div>
        ) : (
          <div>
            <label className="text-[10px] text-zinc-500 uppercase tracking-widest block mb-1">Oyuncu Adı</label>
            <input value={name} onChange={(e) => setName(e.target.value)}
              placeholder="Tam ad girin..."
              className="w-full bg-[#1a1a28] border border-[#2a2a38] rounded-lg px-3 py-2 text-xs text-zinc-200 placeholder-zinc-600 focus:outline-none focus:border-violet-500"
            />
          </div>
        )}

        <div>
          <label className="text-[10px] text-zinc-500 uppercase tracking-widest block mb-1">Öneren Scout</label>
          <input value={scout} onChange={(e) => setScout(e.target.value)}
            placeholder="Scout adı..."
            className="w-full bg-[#1a1a28] border border-[#2a2a38] rounded-lg px-3 py-2 text-xs text-zinc-200 placeholder-zinc-600 focus:outline-none focus:border-violet-500"
          />
        </div>

        <div>
          <label className="text-[10px] text-zinc-500 uppercase tracking-widest block mb-1">Öncelik</label>
          <div className="flex gap-2">
            {([1, 2, 3] as const).map((p) => (
              <button key={p} onClick={() => setPriority(p)}
                className={cn("flex-1 py-2 text-xs rounded-lg border transition-colors", priority === p ? "bg-violet-600 border-violet-500 text-white" : "bg-[#1a1a28] border-[#2a2a38] text-zinc-400 hover:border-violet-500/50")}>
                {PRIORITY_LABELS[p]}
              </button>
            ))}
          </div>
        </div>

        <div>
          <label className="text-[10px] text-zinc-500 uppercase tracking-widest block mb-1">Not</label>
          <textarea value={notes} onChange={(e) => setNotes(e.target.value)}
            rows={3} placeholder="Scout gözlemi veya not..."
            className="w-full bg-[#1a1a28] border border-[#2a2a38] rounded-lg px-3 py-2 text-xs text-zinc-200 placeholder-zinc-600 focus:outline-none focus:border-violet-500 resize-none"
          />
        </div>

        <div className="flex gap-2 pt-1">
          <button onClick={onClose} className="flex-1 py-2.5 text-xs rounded-lg border border-[#2a2a38] text-zinc-400 hover:text-zinc-200 transition-colors">İptal</button>
          <button onClick={handleSubmit} className="flex-1 py-2.5 text-xs rounded-lg bg-violet-600 hover:bg-violet-700 text-white font-medium transition-colors">Ekle</button>
        </div>
      </div>
    </div>
  );
}

interface Props {
  entries: IncomingEntry[];
  onStatusChange: (id: number, status: TransferStatus) => void;
  onNotesChange: (id: number, notes: string) => void;
  onAdd: (entry: Partial<IncomingEntry>) => void;
}

export default function IncomingPanel({ entries, onStatusChange, onNotesChange, onAdd }: Props) {
  const [showAddModal, setShowAddModal] = useState(false);
  const [editingNotes, setEditingNotes] = useState<number | null>(null);
  const [notesDraft, setNotesDraft] = useState("");

  return (
    <div className="p-6">
      {/* Header actions */}
      <div className="flex items-center justify-between mb-6">
        <div>
          <h2 className="text-sm font-bold text-white">Öneri Merkezi</h2>
          <p className="text-xs text-zinc-500 mt-0.5">{entries.length} oyuncu takip ediliyor</p>
        </div>
        <div className="flex gap-2">
          <button onClick={() => setShowAddModal(true)}
            className="flex items-center gap-1.5 px-3 py-2 rounded-lg border border-violet-500/40 bg-violet-600/10 text-violet-400 hover:bg-violet-600/20 text-xs transition-colors">
            <Link size={12} />
            SoccerDonna URL ile Ekle
          </button>
          <button onClick={() => setShowAddModal(true)}
            className="flex items-center gap-1.5 px-3 py-2 rounded-lg bg-violet-600 hover:bg-violet-700 text-white text-xs font-medium transition-colors">
            <Plus size={12} />
            Elle Oyuncu Ekle
          </button>
        </div>
      </div>

      {/* Table */}
      <div className="rounded-xl border border-[#2a2a38] overflow-hidden">
        <table className="w-full text-xs">
          <thead>
            <tr className="border-b border-[#2a2a38] bg-[#111118]">
              {["Oyuncu", "Öneren Scout", "Durum", "Öncelik", "Not", "İşlem"].map((h) => (
                <th key={h} className="text-left py-2.5 px-4 text-[10px] font-semibold uppercase tracking-widest text-zinc-500">{h}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {entries.length === 0 && (
              <tr><td colSpan={6} className="text-center py-12 text-zinc-600">Henüz öneri yok.</td></tr>
            )}
            {entries.map((entry) => {
              const name = entry.player?.name ?? entry.rawName ?? "Bilinmeyen";
              const club = entry.player?.currentClub ?? (entry.soccerdonnaUrl ? "URL'den çekilecek" : "—");
              const statusCfg = STATUS_CONFIG[entry.status];

              return (
                <tr key={entry.id} className="border-b border-[#1a1a28] hover:bg-[#13131f] transition-colors">
                  {/* Player */}
                  <td className="py-3 px-4">
                    <p className="font-medium text-zinc-200">{name}</p>
                    <p className="text-[10px] text-zinc-500">{club}</p>
                    {entry.soccerdonnaUrl && !entry.player && (
                      <a href={entry.soccerdonnaUrl} target="_blank" rel="noopener noreferrer"
                        className="text-[10px] text-violet-400 hover:underline flex items-center gap-0.5 mt-0.5">
                        <Link size={8} /> SoccerDonna
                      </a>
                    )}
                  </td>

                  {/* Scout */}
                  <td className="py-3 px-4 text-zinc-400">{entry.recommendedBy}</td>

                  {/* Status */}
                  <td className="py-3 px-4">
                    <div className="relative inline-block">
                      <select
                        value={entry.status}
                        onChange={(e) => onStatusChange(entry.id, e.target.value as TransferStatus)}
                        className={cn("appearance-none pr-5 pl-2.5 py-1 rounded-full border text-[10px] font-medium cursor-pointer focus:outline-none", statusCfg.color, statusCfg.bg)}
                      >
                        {Object.entries(STATUS_CONFIG).map(([k, v]) => (
                          <option key={k} value={k}>{v.label}</option>
                        ))}
                      </select>
                      <ChevronDown size={10} className={cn("absolute right-1 top-1/2 -translate-y-1/2 pointer-events-none", statusCfg.color)} />
                    </div>
                  </td>

                  {/* Priority */}
                  <td className="py-3 px-4">
                    <span className={cn("font-medium text-[11px]", PRIORITY_COLORS[entry.priority])}>
                      {"●".repeat(entry.priority)}
                      <span className="ml-1">{PRIORITY_LABELS[entry.priority]}</span>
                    </span>
                  </td>

                  {/* Notes */}
                  <td className="py-3 px-4 max-w-[200px]">
                    {editingNotes === entry.id ? (
                      <div className="flex gap-1">
                        <input
                          autoFocus
                          value={notesDraft}
                          onChange={(e) => setNotesDraft(e.target.value)}
                          className="flex-1 bg-[#1a1a28] border border-[#2a2a38] rounded px-2 py-1 text-xs text-zinc-200 focus:outline-none focus:border-violet-500"
                        />
                        <button onClick={() => { onNotesChange(entry.id, notesDraft); setEditingNotes(null); }}
                          className="w-6 h-6 rounded bg-emerald-600/20 text-emerald-400 hover:bg-emerald-600/30 flex items-center justify-center">
                          <Check size={10} />
                        </button>
                      </div>
                    ) : (
                      <p className="text-zinc-400 line-clamp-2 cursor-pointer hover:text-zinc-200 transition-colors"
                        onClick={() => { setEditingNotes(entry.id); setNotesDraft(entry.notes ?? ""); }}>
                        {entry.notes ?? <span className="text-zinc-600 italic">Not ekle...</span>}
                      </p>
                    )}
                  </td>

                  {/* Actions */}
                  <td className="py-3 px-4">
                    <div className="flex gap-1">
                      <span className="text-[10px] text-zinc-600">
                        {new Date(entry.recommendedAt).toLocaleDateString("tr-TR")}
                      </span>
                    </div>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>

      {showAddModal && <AddIncomingModal onClose={() => setShowAddModal(false)} onAdd={onAdd} />}
    </div>
  );
}
