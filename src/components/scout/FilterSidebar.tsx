"use client";

import { useState } from "react";
import { ChevronLeft, ChevronRight, X, SlidersHorizontal } from "lucide-react";
import { cn } from "@/lib/utils";
import type { ScoutFilters, Position, PlayerRole, Foot } from "@/types/scout";
import { DEFAULT_FILTERS, POSITION_GROUPS, POSITION_LABELS, ROLE_LABELS } from "@/types/scout";

const LEAGUES = ["WSL", "Liga F", "Division 1", "Frauen-Bundesliga", "NWSL", "Serie A Femminile", "Süper Lig"];
const COUNTRIES = ["İspanya", "İngiltere", "Fransa", "Almanya", "ABD", "Avustralya", "Danimarka", "İsveç", "Norveç", "Türkiye", "Hollanda", "İtalya"];
const FEET: { value: Foot; label: string }[] = [
  { value: "RIGHT", label: "Sağ" },
  { value: "LEFT", label: "Sol" },
  { value: "BOTH", label: "Her İkisi" },
];

interface Props {
  filters: ScoutFilters;
  onChange: (filters: ScoutFilters) => void;
  resultCount: number;
}

function SectionHeader({ title }: { title: string }) {
  return <p className="text-[10px] font-semibold uppercase tracking-widest text-zinc-500 mb-2 mt-4 first:mt-0">{title}</p>;
}

export default function FilterSidebar({ filters, onChange, resultCount }: Props) {
  const [collapsed, setCollapsed] = useState(false);

  const set = <K extends keyof ScoutFilters>(key: K, value: ScoutFilters[K]) =>
    onChange({ ...filters, [key]: value });

  const togglePosition = (pos: Position) => {
    const next = filters.positions.includes(pos)
      ? filters.positions.filter((p) => p !== pos)
      : [...filters.positions, pos];
    set("positions", next);
  };

  const hasActiveFilters =
    filters.search || filters.positions.length || filters.nationality ||
    filters.league || filters.club || filters.agent || filters.freeAgentOnly ||
    filters.foot || filters.ageMin > 15 || filters.ageMax < 40 ||
    filters.marketValueMin > 0 || filters.marketValueMax < 50_000_000;

  if (collapsed) {
    return (
      <aside className="flex flex-col items-center w-10 bg-[#111118] border-r border-[#2a2a38] py-4 gap-3 shrink-0">
        <button onClick={() => setCollapsed(false)} className="text-zinc-400 hover:text-white transition-colors" title="Filtreleri aç">
          <ChevronRight size={18} />
        </button>
        <SlidersHorizontal size={14} className="text-zinc-600 rotate-90" />
        {hasActiveFilters && <span className="w-2 h-2 rounded-full bg-violet-500 animate-pulse" />}
      </aside>
    );
  }

  return (
    <aside className="w-64 shrink-0 bg-[#111118] border-r border-[#2a2a38] flex flex-col">
      {/* Header */}
      <div className="flex items-center justify-between px-4 py-3 border-b border-[#2a2a38]">
        <div className="flex items-center gap-2">
          <SlidersHorizontal size={14} className="text-violet-400" />
          <span className="text-xs font-semibold text-zinc-200">Filtreler</span>
          {hasActiveFilters && (
            <span className="text-[10px] bg-violet-600 text-white px-1.5 py-0.5 rounded-full">
              aktif
            </span>
          )}
        </div>
        <div className="flex items-center gap-1">
          {hasActiveFilters && (
            <button onClick={() => onChange(DEFAULT_FILTERS)} className="text-[10px] text-zinc-500 hover:text-red-400 transition-colors px-1" title="Sıfırla">
              <X size={12} />
            </button>
          )}
          <button onClick={() => setCollapsed(true)} className="text-zinc-500 hover:text-zinc-200 transition-colors">
            <ChevronLeft size={16} />
          </button>
        </div>
      </div>

      {/* Scrollable filter body */}
      <div className="flex-1 overflow-y-auto px-4 py-3 space-y-1 scrollbar-thin scrollbar-thumb-zinc-700">

        {/* Result count */}
        <p className="text-xs text-zinc-500 mb-3">
          <span className="text-violet-400 font-bold">{resultCount}</span> oyuncu bulundu
        </p>

        {/* Search */}
        <SectionHeader title="Oyuncu Adı" />
        <input
          value={filters.search}
          onChange={(e) => set("search", e.target.value)}
          placeholder="Ara..."
          className="w-full bg-[#1a1a28] border border-[#2a2a38] rounded-lg px-3 py-2 text-xs text-zinc-200 placeholder-zinc-600 focus:outline-none focus:border-violet-500 focus:ring-1 focus:ring-violet-500/20 transition-colors"
        />

        {/* Positions */}
        <SectionHeader title="Pozisyon" />
        <div className="space-y-1.5">
          {POSITION_GROUPS.map((group) => (
            <div key={group.label}>
              <p className="text-[10px] text-zinc-600 mb-1">{group.label}</p>
              <div className="flex flex-wrap gap-1">
                {group.positions.map((pos) => (
                  <button
                    key={pos}
                    onClick={() => togglePosition(pos)}
                    className={cn(
                      "text-[10px] px-2 py-0.5 rounded border transition-colors",
                      filters.positions.includes(pos)
                        ? "bg-violet-600 border-violet-500 text-white"
                        : "bg-[#1a1a28] border-[#2a2a38] text-zinc-400 hover:border-violet-500/50 hover:text-zinc-200"
                    )}
                  >
                    {pos}
                  </button>
                ))}
              </div>
            </div>
          ))}
        </div>

        {/* Age range */}
        <SectionHeader title="Yaş Aralığı" />
        <div className="flex gap-2">
          <div className="flex-1">
            <label className="text-[10px] text-zinc-600 block mb-1">Min</label>
            <input
              type="number" min={15} max={filters.ageMax}
              value={filters.ageMin}
              onChange={(e) => set("ageMin", Number(e.target.value))}
              className="w-full bg-[#1a1a28] border border-[#2a2a38] rounded px-2 py-1.5 text-xs text-zinc-200 focus:outline-none focus:border-violet-500"
            />
          </div>
          <div className="flex-1">
            <label className="text-[10px] text-zinc-600 block mb-1">Max</label>
            <input
              type="number" min={filters.ageMin} max={45}
              value={filters.ageMax}
              onChange={(e) => set("ageMax", Number(e.target.value))}
              className="w-full bg-[#1a1a28] border border-[#2a2a38] rounded px-2 py-1.5 text-xs text-zinc-200 focus:outline-none focus:border-violet-500"
            />
          </div>
        </div>

        {/* Market Value */}
        <SectionHeader title="Piyasa Değeri" />
        <div className="flex gap-2">
          <div className="flex-1">
            <label className="text-[10px] text-zinc-600 block mb-1">Min (€)</label>
            <input
              type="number" min={0} step={100000}
              value={filters.marketValueMin}
              onChange={(e) => set("marketValueMin", Number(e.target.value))}
              placeholder="0"
              className="w-full bg-[#1a1a28] border border-[#2a2a38] rounded px-2 py-1.5 text-xs text-zinc-200 focus:outline-none focus:border-violet-500"
            />
          </div>
          <div className="flex-1">
            <label className="text-[10px] text-zinc-600 block mb-1">Max (€)</label>
            <input
              type="number" min={0} step={500000}
              value={filters.marketValueMax}
              onChange={(e) => set("marketValueMax", Number(e.target.value))}
              placeholder="50M"
              className="w-full bg-[#1a1a28] border border-[#2a2a38] rounded px-2 py-1.5 text-xs text-zinc-200 focus:outline-none focus:border-violet-500"
            />
          </div>
        </div>

        {/* Contract end */}
        <SectionHeader title="Kontrat Bitişi (Önce)" />
        <input
          type="date"
          value={filters.contractEndBefore ?? ""}
          onChange={(e) => set("contractEndBefore", e.target.value || undefined)}
          className="w-full bg-[#1a1a28] border border-[#2a2a38] rounded px-2 py-1.5 text-xs text-zinc-300 focus:outline-none focus:border-violet-500"
        />

        {/* Foot */}
        <SectionHeader title="Güçlü Ayak" />
        <div className="flex gap-1">
          {FEET.map(({ value, label }) => (
            <button
              key={value}
              onClick={() => set("foot", filters.foot === value ? undefined : value)}
              className={cn(
                "flex-1 text-[10px] py-1.5 rounded border transition-colors",
                filters.foot === value
                  ? "bg-violet-600 border-violet-500 text-white"
                  : "bg-[#1a1a28] border-[#2a2a38] text-zinc-400 hover:border-violet-500/50"
              )}
            >
              {label}
            </button>
          ))}
        </div>

        {/* Nationality */}
        <SectionHeader title="Ülke" />
        <select
          value={filters.nationality}
          onChange={(e) => set("nationality", e.target.value)}
          className="w-full bg-[#1a1a28] border border-[#2a2a38] rounded px-2 py-2 text-xs text-zinc-300 focus:outline-none focus:border-violet-500 appearance-none"
        >
          <option value="">Tümü</option>
          {COUNTRIES.map((c) => <option key={c} value={c}>{c}</option>)}
        </select>

        {/* League */}
        <SectionHeader title="Lig" />
        <select
          value={filters.league}
          onChange={(e) => set("league", e.target.value)}
          className="w-full bg-[#1a1a28] border border-[#2a2a38] rounded px-2 py-2 text-xs text-zinc-300 focus:outline-none focus:border-violet-500 appearance-none"
        >
          <option value="">Tümü</option>
          {LEAGUES.map((l) => <option key={l} value={l}>{l}</option>)}
        </select>

        {/* Club */}
        <SectionHeader title="Kulüp" />
        <input
          value={filters.club}
          onChange={(e) => set("club", e.target.value)}
          placeholder="Kulüp ara..."
          className="w-full bg-[#1a1a28] border border-[#2a2a38] rounded-lg px-3 py-2 text-xs text-zinc-200 placeholder-zinc-600 focus:outline-none focus:border-violet-500"
        />

        {/* Agent */}
        <SectionHeader title="Temsilci" />
        <input
          value={filters.agent}
          onChange={(e) => set("agent", e.target.value)}
          placeholder="Temsilci ara..."
          className="w-full bg-[#1a1a28] border border-[#2a2a38] rounded-lg px-3 py-2 text-xs text-zinc-200 placeholder-zinc-600 focus:outline-none focus:border-violet-500"
        />

        {/* Free agent toggle */}
        <div className="flex items-center justify-between pt-3 pb-2">
          <span className="text-xs text-zinc-300">Sadece Serbest Ajanlar</span>
          <button
            onClick={() => set("freeAgentOnly", !filters.freeAgentOnly)}
            className={cn(
              "relative w-9 h-5 rounded-full transition-colors",
              filters.freeAgentOnly ? "bg-violet-600" : "bg-zinc-700"
            )}
          >
            <span className={cn(
              "absolute top-0.5 w-4 h-4 rounded-full bg-white transition-transform",
              filters.freeAgentOnly ? "translate-x-4" : "translate-x-0.5"
            )} />
          </button>
        </div>

        {/* Reset */}
        {hasActiveFilters && (
          <button
            onClick={() => onChange(DEFAULT_FILTERS)}
            className="w-full mt-2 text-xs py-2 rounded-lg border border-red-500/30 text-red-400 hover:bg-red-500/10 transition-colors"
          >
            Filtreleri Sıfırla
          </button>
        )}
      </div>
    </aside>
  );
}
