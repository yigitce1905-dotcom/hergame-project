// src/components/FilterBar.tsx
"use client";

import type { PlayerFilters, SortKey, SortDir } from "@/types";

interface Props {
  filters: PlayerFilters;
  sortKey: SortKey;
  sortDir: SortDir;
  allCountries: string[];
  allLeagues: string[];
  resultCount: number;
  onFilterChange: (key: keyof PlayerFilters, value: string | number | boolean) => void;
  onSortKeyChange: (key: SortKey) => void;
  onSortDirChange: (dir: SortDir) => void;
}

const SELECT_CLS = `
  bg-[#18181f] border border-[#2a2a38] rounded-lg px-2.5 py-1.5
  text-sm text-white outline-none cursor-pointer
  focus:border-[#c8a6f5] transition-colors appearance-none
`;

export default function FilterBar({
  filters, sortKey, sortDir,
  allCountries, allLeagues, resultCount,
  onFilterChange, onSortKeyChange, onSortDirChange,
}: Props) {
  return (
    <div className="sticky top-16 z-40 bg-[#111118] border-b border-[#2a2a38]">
      <div className="max-w-7xl mx-auto px-6 py-2.5 flex items-center gap-2 flex-wrap">

        <span className="text-xs text-[#6b6685] whitespace-nowrap">Filtre:</span>

        {/* Country */}
        <select
          className={SELECT_CLS}
          value={filters.country}
          onChange={(e) => onFilterChange("country", e.target.value)}
        >
          <option value="">Tüm Ülkeler</option>
          {allCountries.map((c) => <option key={c} value={c}>{c}</option>)}
        </select>

        {/* League */}
        <select
          className={SELECT_CLS}
          value={filters.league}
          onChange={(e) => onFilterChange("league", e.target.value)}
        >
          <option value="">Tüm Ligler</option>
          {allLeagues.map((l) => <option key={l} value={l}>{l}</option>)}
        </select>

        {/* Position */}
        <select
          className={SELECT_CLS}
          value={filters.position}
          onChange={(e) => onFilterChange("position", e.target.value)}
        >
          <option value="">Pozisyon</option>
          <option value="GK">GK — Kaleci</option>
          <option value="DF">DF — Defans</option>
          <option value="MF">MF — Orta Saha</option>
          <option value="FW">FW — Forvet</option>
        </select>

        {/* Divider */}
        <div className="w-px h-5 bg-[#2a2a38] mx-1" />

        <span className="text-xs text-[#6b6685] whitespace-nowrap">Sırala:</span>

        {/* Sort key */}
        <select
          className={SELECT_CLS}
          value={sortKey}
          onChange={(e) => onSortKeyChange(e.target.value as SortKey)}
        >
          <option value="name">İsim</option>
          <option value="age">Yaş</option>
          <option value="goals">Gol</option>
          <option value="assists">Asist</option>
          <option value="appearances">Maç</option>
          <option value="caps">Milli Maç</option>
          <option value="market_value_num">Piyasa Değeri</option>
        </select>

        {/* Sort dir */}
        <select
          className={SELECT_CLS}
          value={sortDir}
          onChange={(e) => onSortDirChange(e.target.value as SortDir)}
        >
          <option value="asc">↑ Artan</option>
          <option value="desc">↓ Azalan</option>
        </select>

        {/* FM26 Hidden Gem toggle */}
        <button
          onClick={() => onFilterChange("hiddenGem", !filters.hiddenGem)}
          className={`
            flex items-center gap-1.5 text-xs font-semibold px-2.5 py-1.5 rounded-lg border transition-all
            ${filters.hiddenGem
              ? "bg-[#f5c842]/20 border-[#f5c842]/50 text-[#f5c842]"
              : "bg-[#18181f] border-[#2a2a38] text-[#6b6685] hover:text-white hover:border-[#f5c842]/30"
            }
          `}
          title="FM26 Hidden Gem listesindeki oyuncuları göster"
        >
          ⭐ FM26
        </button>

        {/* Result count */}
        <span className="ml-auto text-xs text-[#6b6685] whitespace-nowrap">
          {resultCount} oyuncu
        </span>
      </div>
    </div>
  );
}
