"use client";

// src/app/page.tsx
// HerGame — Women's Football Player Database
// Main page: search, filter, sort, player cards (no photo), modal (with photo)

import { useState, useEffect, useMemo, useCallback } from "react";
import type { Player, PlayerFilters, SortKey, SortDir } from "@/types";
import { PLAYERS } from "@/data/players";
import { HIDDEN_GEMS } from "@/data/hidden_gems";

// ── TUR1 + FM26 Hidden Gems merge ─────────────────────────────────────────────
function mergePlayers(tur1: Player[], gems: Player[]): Player[] {
  const gemsByName = new Map(gems.map((g) => [g.name.toLowerCase(), g]));
  let nextId = tur1.length + 1;

  // TUR1 oyuncularını FM26 verileriyle zenginleştir
  const enriched: Player[] = tur1.map((p) => {
    const gem = gemsByName.get(p.name.toLowerCase());
    if (gem) {
      gemsByName.delete(p.name.toLowerCase());
      return {
        ...p,
        hidden_gem: true,
        fm_rating: gem.fm_rating,
        fm_position: gem.fm_position,
        swot: gem.swot,
      };
    }
    return p;
  });

  // Kalan hidden gems'i ekle (TUR1'de olmayan)
  for (const gem of gemsByName.values()) {
    enriched.push({ ...gem, id: nextId++ });
  }

  return enriched;
}

const ALL_PLAYERS = mergePlayers(PLAYERS, HIDDEN_GEMS);
import PlayerCard from "@/components/PlayerCard";
import PlayerModal from "@/components/PlayerModal";
import FilterBar from "@/components/FilterBar";
import HeroSearch from "@/components/HeroSearch";
import DataSourcePanel from "@/components/DataSourcePanel";

export default function HomePage() {
  // ── State ──────────────────────────────────────────────────────────────────
  const [filters, setFilters] = useState<PlayerFilters>({
    search: "",
    country: "",
    league: "",
    position: "",
    ageMin: 0,
    ageMax: 45,
    clubSearch: "",
    hiddenGem: false,
  });
  const [sortKey, setSortKey]     = useState<SortKey>("name");
  const [sortDir, setSortDir]     = useState<SortDir>("asc");
  const [selectedPlayer, setSelectedPlayer] = useState<Player | null>(null);
  const [showDataSources, setShowDataSources] = useState(false);
  const [isDark, setIsDark]       = useState(true);

  // ── Derived lists for dropdowns ───────────────────────────────────────────
  const allCountries = useMemo(
    () => [...new Set(ALL_PLAYERS.map((p) => p.nationality).filter(Boolean))].sort(),
    []
  );
  const allLeagues = useMemo(
    () => [...new Set(ALL_PLAYERS.map((p) => p.league).filter(Boolean))].sort(),
    []
  );

  // ── Filtered + sorted players ─────────────────────────────────────────────
  const filtered = useMemo(() => {
    let list = [...ALL_PLAYERS];

    const q = filters.search.toLowerCase().trim();
    if (q) {
      list = list.filter(
        (p) =>
          p.name.toLowerCase().includes(q) ||
          p.club.toLowerCase().includes(q) ||
          p.nationality.toLowerCase().includes(q)
      );
    }
    if (filters.country)   list = list.filter((p) => p.nationality === filters.country);
    if (filters.league)    list = list.filter((p) => p.league === filters.league);
    if (filters.position)  list = list.filter((p) => p.position === filters.position);
    if (filters.ageMin > 0)   list = list.filter((p) => p.age >= filters.ageMin);
    if (filters.ageMax < 45)  list = list.filter((p) => p.age <= filters.ageMax);
    if (filters.hiddenGem) list = list.filter((p) => p.hidden_gem === true);

    // Sort
    list.sort((a, b) => {
      if (sortKey === "name") {
        return sortDir === "asc"
          ? a.name.localeCompare(b.name)
          : b.name.localeCompare(a.name);
      }
      const av = a[sortKey] as number;
      const bv = b[sortKey] as number;
      return sortDir === "asc" ? av - bv : bv - av;
    });

    return list;
  }, [filters, sortKey, sortDir]);

  // ── Keyboard: close modal on Escape ──────────────────────────────────────
  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if (e.key === "Escape") {
        setSelectedPlayer(null);
        setShowDataSources(false);
      }
    };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, []);

  // ── Scroll lock when modal open ───────────────────────────────────────────
  useEffect(() => {
    document.body.style.overflow = selectedPlayer || showDataSources ? "hidden" : "";
  }, [selectedPlayer, showDataSources]);

  const handleFilterChange = useCallback(
    (key: keyof PlayerFilters, value: string | number | boolean) => {
      setFilters((prev) => ({ ...prev, [key]: value }));
    },
    []
  );

  return (
    <div className={isDark ? "dark" : ""}>
      <div className="min-h-screen bg-[#0a0a0f] dark:bg-[#0a0a0f] text-white transition-colors">

        {/* ── Header ─────────────────────────────────────────────────────── */}
        <header className="sticky top-0 z-50 bg-[#111118] border-b border-[#2a2a38]">
          <div className="max-w-7xl mx-auto px-6 h-16 flex items-center gap-4">
            <div className="flex items-center gap-2.5">
              <div className="w-9 h-9 rounded-lg bg-violet-600 flex items-center justify-center text-sm font-black text-white">
                W
              </div>
              <span className="font-bold text-xl tracking-tight">
                W-<span className="text-violet-400">Scope</span>
              </span>
            </div>

            <div className="ml-auto flex items-center gap-2">
              <button
                onClick={() => setShowDataSources(true)}
                className="text-xs px-3 py-1.5 rounded-lg border border-[#c8a6f5]/30 bg-[#c8a6f5]/10 text-[#c8a6f5] hover:bg-[#c8a6f5]/20 transition-colors"
              >
                📊 Veri Kaynakları
              </button>
              <button
                onClick={() => setIsDark(!isDark)}
                className="w-9 h-9 rounded-lg border border-[#2a2a38] bg-transparent hover:bg-[#18181f] transition-colors text-sm"
                title="Tema değiştir"
              >
                {isDark ? "🌙" : "☀️"}
              </button>
            </div>
          </div>
        </header>

        {/* ── Hero ───────────────────────────────────────────────────────── */}
        <HeroSearch
          totalPlayers={ALL_PLAYERS.length}
          filteredCount={filtered.length}
          allLeagues={allLeagues}
          allCountries={allCountries}
          searchValue={filters.search}
          onSearchChange={(v) => handleFilterChange("search", v)}
        />

        {/* ── Filter Bar ─────────────────────────────────────────────────── */}
        <FilterBar
          filters={filters}
          sortKey={sortKey}
          sortDir={sortDir}
          allCountries={allCountries}
          allLeagues={allLeagues}
          resultCount={filtered.length}
          onFilterChange={handleFilterChange}
          onSortKeyChange={setSortKey}
          onSortDirChange={setSortDir}
        />

        {/* ── Player Grid ────────────────────────────────────────────────── */}
        <main className="max-w-7xl mx-auto px-6 py-6">
          {filtered.length === 0 ? (
            <div className="text-center py-20 text-[#6b6685]">
              <div className="text-4xl mb-4">⚽</div>
              <p>Oyuncu bulunamadı. Filtreleri kontrol edin.</p>
            </div>
          ) : (
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
              {filtered.map((player) => (
                <PlayerCard
                  key={player.id ?? player.soccerdonna_id}
                  player={player}
                  onClick={() => setSelectedPlayer(player)}
                />
              ))}
            </div>
          )}
        </main>

        {/* ── Player Modal ───────────────────────────────────────────────── */}
        {selectedPlayer && (
          <PlayerModal
            player={selectedPlayer}
            onClose={() => setSelectedPlayer(null)}
          />
        )}

        {/* ── Data Sources Panel ─────────────────────────────────────────── */}
        {showDataSources && (
          <DataSourcePanel onClose={() => setShowDataSources(false)} />
        )}
      </div>
    </div>
  );
}
