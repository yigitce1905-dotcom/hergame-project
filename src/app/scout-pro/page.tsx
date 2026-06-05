"use client";

import { useState, useMemo, useCallback, useEffect } from "react";
import {
  Users, UserCheck, Inbox, Star, Layout,
  Database, ChevronRight
} from "lucide-react";
import { cn } from "@/lib/utils";
import type { ScoutTab, ScoutPlayer, ScoutFilters, IncomingEntry, FavoriteEntry, TransferStatus } from "@/types/scout";
import { DEFAULT_FILTERS } from "@/types/scout";
import { DEMO_PLAYERS, DEMO_INCOMING, DEMO_FAVORITES } from "@/data/scout_demo";

import FilterSidebar from "@/components/scout/FilterSidebar";
import AllPlayersTable from "@/components/scout/AllPlayersTable";
import IncomingPanel from "@/components/scout/IncomingPanel";
import FavoritesGrid from "@/components/scout/FavoritesGrid";
import SquadBuilder from "@/components/scout/SquadBuilder";
import PlayerProfileModal from "@/components/scout/PlayerProfileModal";

// ─── Tab config ────────────────────────────────────────────────────────────────

const TABS: { key: ScoutTab; label: string; icon: React.ReactNode }[] = [
  { key: "all",         label: "All Players",  icon: <Users size={13} /> },
  { key: "free-agents", label: "Free Agents",  icon: <UserCheck size={13} /> },
  { key: "incoming",    label: "Incoming",      icon: <Inbox size={13} /> },
  { key: "favorites",   label: "Favoriler",     icon: <Star size={13} /> },
  { key: "squad",       label: "Kadro Müh.",    icon: <Layout size={13} /> },
];

// ─── Filtering logic ───────────────────────────────────────────────────────────

function applyFilters(players: ScoutPlayer[], filters: ScoutFilters): ScoutPlayer[] {
  return players.filter((p) => {
    const q = filters.search.toLowerCase().trim();
    if (q && !p.name.toLowerCase().includes(q) && !p.currentClub.toLowerCase().includes(q) && !p.nationality.toLowerCase().includes(q)) return false;
    if (filters.positions.length && !p.positions.some((pos) => filters.positions.includes(pos.position))) return false;
    if (filters.nationality && p.nationality !== filters.nationality) return false;
    if (filters.league && p.league !== filters.league) return false;
    if (filters.club && !p.currentClub.toLowerCase().includes(filters.club.toLowerCase())) return false;
    if (filters.agent && !p.agentName?.toLowerCase().includes(filters.agent.toLowerCase())) return false;
    if (p.age < filters.ageMin || p.age > filters.ageMax) return false;
    if (p.marketValue < filters.marketValueMin || p.marketValue > filters.marketValueMax) return false;
    if (filters.foot && p.foot !== filters.foot) return false;
    if (filters.contractEndBefore && p.contractEnd && p.contractEnd > filters.contractEndBefore) return false;
    if (filters.freeAgentOnly && p.contractEnd) {
      const months = (new Date(p.contractEnd).getTime() - Date.now()) / (1000 * 60 * 60 * 24 * 30);
      if (months > 6) return false;
    }
    return true;
  });
}

// ─── Page ──────────────────────────────────────────────────────────────────────

export default function ScoutProPage() {
  const [tab, setTab] = useState<ScoutTab>("all");
  const [filters, setFilters] = useState<ScoutFilters>(DEFAULT_FILTERS);
  const [players] = useState<ScoutPlayer[]>(DEMO_PLAYERS);
  const [incoming, setIncoming] = useState<IncomingEntry[]>(DEMO_INCOMING);
  const [favorites, setFavorites] = useState<FavoriteEntry[]>(DEMO_FAVORITES);
  const [selectedPlayer, setSelectedPlayer] = useState<ScoutPlayer | null>(null);
  const [favoriteIds, setFavoriteIds] = useState<Set<number>>(
    () => new Set(DEMO_FAVORITES.map((f) => f.player.id))
  );

  // Escape closes modal
  useEffect(() => {
    const h = (e: KeyboardEvent) => { if (e.key === "Escape") setSelectedPlayer(null); };
    window.addEventListener("keydown", h);
    return () => window.removeEventListener("keydown", h);
  }, []);

  // Body scroll lock
  useEffect(() => {
    document.body.style.overflow = selectedPlayer ? "hidden" : "";
  }, [selectedPlayer]);

  // Filtered lists
  const filteredAll = useMemo(() => applyFilters(players, filters), [players, filters]);
  const filteredFreeAgents = useMemo(() => {
    const freeFilter = { ...filters, freeAgentOnly: true };
    return applyFilters(players, freeFilter).filter((p) => {
      if (!p.contractEnd) return true;
      const months = (new Date(p.contractEnd).getTime() - Date.now()) / (1000 * 60 * 60 * 24 * 30);
      return months <= 6;
    });
  }, [players, filters]);

  // Derived counts for header
  const filterCount = filteredAll.length;
  const freeAgentCount = players.filter((p) => {
    if (!p.contractEnd) return true;
    const months = (new Date(p.contractEnd).getTime() - Date.now()) / (1000 * 60 * 60 * 24 * 30);
    return months <= 6;
  }).length;

  // Actions
  const toggleFavorite = useCallback((id: number) => {
    setFavoriteIds((prev) => {
      const next = new Set(prev);
      if (next.has(id)) {
        next.delete(id);
        setFavorites((f) => f.filter((e) => e.player.id !== id));
      } else {
        next.add(id);
        const player = players.find((p) => p.id === id);
        if (player) {
          setFavorites((f) => [...f, {
            id: Date.now(), player, addedAt: new Date().toISOString(), addedBy: "Scout",
          }]);
        }
      }
      return next;
    });
  }, [players]);

  const addToIncoming = useCallback((player: ScoutPlayer) => {
    setIncoming((prev) => {
      if (prev.some((e) => e.player?.id === player.id)) return prev;
      return [...prev, {
        id: Date.now(), player, recommendedBy: "Scout",
        recommendedAt: new Date().toISOString(), status: "INTERESTED", priority: 2,
      }];
    });
    setTab("incoming");
  }, []);

  const handleIncomingAdd = useCallback((entry: Partial<IncomingEntry>) => {
    setIncoming((prev) => [...prev, { id: Date.now(), recommendedAt: new Date().toISOString(), status: "INTERESTED", priority: 2, recommendedBy: "Scout", ...entry } as IncomingEntry]);
  }, []);

  const handleStatusChange = useCallback((id: number, status: TransferStatus) => {
    setIncoming((prev) => prev.map((e) => e.id === id ? { ...e, status } : e));
  }, []);

  const handleIncomingNotes = useCallback((id: number, notes: string) => {
    setIncoming((prev) => prev.map((e) => e.id === id ? { ...e, notes } : e));
  }, []);

  const handleFavNotes = useCallback((id: number, notes: string) => {
    setFavorites((prev) => prev.map((e) => e.id === id ? { ...e, notes } : e));
  }, []);

  const handleRemoveFav = useCallback((id: number) => {
    const entry = favorites.find((e) => e.id === id);
    if (entry) {
      setFavoriteIds((prev) => { const n = new Set(prev); n.delete(entry.player.id); return n; });
    }
    setFavorites((prev) => prev.filter((e) => e.id !== id));
  }, [favorites]);

  const displayedPlayers = tab === "free-agents" ? filteredFreeAgents : filteredAll;

  return (
    <div className="min-h-screen bg-[#0a0a0f] text-white flex flex-col">

      {/* ── Top Header ──────────────────────────────────────────────────────── */}
      <header className="sticky top-0 z-40 bg-[#0d0d16] border-b border-[#2a2a38]">
        <div className="px-6 h-14 flex items-center gap-4">
          {/* Logo */}
          <a href="/" className="flex items-center gap-2 mr-2">
            <div className="w-8 h-8 rounded-lg bg-violet-600 flex items-center justify-center text-sm font-black">W</div>
            <span className="text-sm font-bold text-white hidden sm:block">W-<span className="text-violet-400">Scope</span></span>
          </a>

          {/* Tabs */}
          <nav className="flex items-center gap-0.5 flex-1">
            {TABS.map(({ key, label, icon }) => {
              const count = key === "all" ? filterCount
                : key === "free-agents" ? freeAgentCount
                : key === "incoming" ? incoming.length
                : key === "favorites" ? favorites.length
                : null;

              return (
                <button
                  key={key}
                  onClick={() => setTab(key)}
                  className={cn(
                    "flex items-center gap-1.5 px-3 py-2 rounded-lg text-xs font-medium transition-colors relative",
                    tab === key
                      ? "bg-violet-600 text-white"
                      : "text-zinc-400 hover:text-zinc-200 hover:bg-[#1a1a28]"
                  )}
                >
                  {icon}
                  <span>{label}</span>
                  {count !== null && (
                    <span className={cn(
                      "text-[10px] px-1.5 py-0.5 rounded-full font-bold ml-0.5",
                      tab === key ? "bg-white/20 text-white" : "bg-[#2a2a38] text-zinc-400"
                    )}>
                      {count}
                    </span>
                  )}
                </button>
              );
            })}
          </nav>

          {/* Right side stats */}
          <div className="hidden lg:flex items-center gap-4 text-xs">
            <div className="flex items-center gap-1.5 text-zinc-500">
              <Database size={11} className="text-violet-400" />
              <span className="text-zinc-300 font-mono">{players.length}</span>
              <span>oyuncu</span>
            </div>
            <div className="flex items-center gap-1.5 text-zinc-500">
              <span className="w-2 h-2 rounded-full bg-amber-400 animate-pulse" />
              <span className="text-amber-400 font-mono">{freeAgentCount}</span>
              <span>serbest ajan</span>
            </div>
            <div className="flex items-center gap-1.5 text-zinc-500">
              <Star size={10} className="text-amber-400" fill="currentColor" />
              <span className="text-amber-300 font-mono">{favorites.length}</span>
              <span>favori</span>
            </div>
            <div className="flex items-center gap-1.5 text-zinc-500">
              <Inbox size={10} className="text-emerald-400" />
              <span className="text-emerald-300 font-mono">{incoming.length}</span>
              <span>öneri</span>
            </div>
          </div>

          {/* Back to HerGame */}
          <a href="/" className="flex items-center gap-1 text-[11px] text-zinc-600 hover:text-zinc-400 transition-colors ml-2">
            Ana Sayfa <ChevronRight size={10} />
          </a>
        </div>
      </header>

      {/* ── Body: Sidebar + Content ──────────────────────────────────────────── */}
      <div className="flex flex-1 overflow-hidden" style={{ height: "calc(100vh - 56px)" }}>

        {/* Sidebar (only on data tabs) */}
        {(tab === "all" || tab === "free-agents") && (
          <FilterSidebar
            filters={filters}
            onChange={setFilters}
            resultCount={displayedPlayers.length}
          />
        )}

        {/* Main content */}
        <main className="flex-1 overflow-y-auto">
          {/* All Players & Free Agents: share the same table */}
          {(tab === "all" || tab === "free-agents") && (
            <div>
              {/* Sub-header */}
              <div className="sticky top-0 z-30 bg-[#0a0a0f]/95 backdrop-blur border-b border-[#1a1a28] px-5 py-2.5 flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <span className="text-xs text-zinc-400">
                    {tab === "free-agents" ? "Serbest Ajanlar & Yakın Kontrat Bitişleri" : "Tüm Oyuncular"}
                  </span>
                  <span className="text-[10px] bg-violet-600/20 text-violet-400 border border-violet-500/30 px-1.5 py-0.5 rounded-full font-mono">
                    {displayedPlayers.length} oyuncu
                  </span>
                  {tab === "free-agents" && (
                    <span className="text-[10px] text-amber-400 border border-amber-500/30 bg-amber-500/10 px-1.5 py-0.5 rounded-full">
                      ≤ 6 ay kalan veya kontrat yok
                    </span>
                  )}
                </div>
              </div>

              <AllPlayersTable
                players={displayedPlayers}
                favorites={[...favoriteIds]}
                onViewPlayer={setSelectedPlayer}
                onToggleFavorite={toggleFavorite}
                onAddToIncoming={addToIncoming}
              />
            </div>
          )}

          {tab === "incoming" && (
            <IncomingPanel
              entries={incoming}
              onStatusChange={handleStatusChange}
              onNotesChange={handleIncomingNotes}
              onAdd={handleIncomingAdd}
            />
          )}

          {tab === "favorites" && (
            <FavoritesGrid
              entries={favorites}
              onRemove={handleRemoveFav}
              onNotesChange={handleFavNotes}
              onViewPlayer={(e) => setSelectedPlayer(e.player)}
            />
          )}

          {tab === "squad" && (
            <SquadBuilder
              allPlayers={players}
              favoritePlayers={favorites.map((f) => f.player)}
              incomingPlayers={incoming.filter((i) => i.player).map((i) => i.player!)}
            />
          )}
        </main>
      </div>

      {/* ── Player Profile Modal ─────────────────────────────────────────────── */}
      {selectedPlayer && (
        <PlayerProfileModal
          player={selectedPlayer}
          allPlayers={players}
          onClose={() => setSelectedPlayer(null)}
          onSelectPlayer={setSelectedPlayer}
        />
      )}
    </div>
  );
}
