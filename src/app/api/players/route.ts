// src/app/api/players/route.ts
// Next.js 14 App Router API route
// Serves player data with server-side filtering & sorting.
// Data source: either players_app.json (scraped) or fallback demo data.

import { NextRequest, NextResponse } from "next/server";
import path from "path";
import fs from "fs";
import type { Player, PlayersApiResponse, SortKey } from "@/types";

// ── Data loading ──────────────────────────────────────────────────────────────
function loadPlayers(): Player[] {
  // Try scraped data first
  const dataPath = path.join(process.cwd(), "data", "players_app.json");
  if (fs.existsSync(dataPath)) {
    const raw = fs.readFileSync(dataPath, "utf-8");
    return JSON.parse(raw) as Player[];
  }
  // Fallback: import demo data
  // eslint-disable-next-line @typescript-eslint/no-var-requires
  return require("@/data/players_demo").PLAYERS as Player[];
}

// ── Sorting ───────────────────────────────────────────────────────────────────
function sortPlayers(players: Player[], key: SortKey, dir: "asc" | "desc"): Player[] {
  return [...players].sort((a, b) => {
    let av: string | number;
    let bv: string | number;

    if (key === "name") {
      av = a.name;
      bv = b.name;
    } else {
      av = a[key] as number;
      bv = b[key] as number;
    }

    if (typeof av === "string" && typeof bv === "string") {
      return dir === "asc" ? av.localeCompare(bv) : bv.localeCompare(av);
    }
    return dir === "asc"
      ? (av as number) - (bv as number)
      : (bv as number) - (av as number);
  });
}

// ── GET handler ───────────────────────────────────────────────────────────────
export async function GET(request: NextRequest) {
  const { searchParams } = new URL(request.url);

  const search    = (searchParams.get("search") || "").toLowerCase().trim();
  const country   = searchParams.get("country") || "";
  const league    = searchParams.get("league") || "";
  const position  = searchParams.get("position") || "";
  const ageMin    = parseInt(searchParams.get("ageMin") || "0");
  const ageMax    = parseInt(searchParams.get("ageMax") || "99");
  const sortKey   = (searchParams.get("sort") || "name") as SortKey;
  const sortDir   = (searchParams.get("dir") || "asc") as "asc" | "desc";
  const page      = parseInt(searchParams.get("page") || "1");
  const pageSize  = parseInt(searchParams.get("pageSize") || "50");

  let players = loadPlayers();

  // ── Filter ──────────────────────────────────────────────────────────────────
  if (search) {
    players = players.filter(
      (p) =>
        p.name.toLowerCase().includes(search) ||
        p.club.toLowerCase().includes(search) ||
        p.nationality.toLowerCase().includes(search) ||
        p.national_team.toLowerCase().includes(search)
    );
  }
  if (country)  players = players.filter((p) => p.nationality === country);
  if (league)   players = players.filter((p) => p.league === league);
  if (position) players = players.filter((p) => p.position === position);
  if (ageMin > 0) players = players.filter((p) => p.age >= ageMin);
  if (ageMax < 99) players = players.filter((p) => p.age <= ageMax);

  // ── Sort ────────────────────────────────────────────────────────────────────
  const validSortKeys: SortKey[] = [
    "name", "age", "goals", "assists", "appearances", "caps", "market_value_num",
  ];
  const safeKey = validSortKeys.includes(sortKey) ? sortKey : "name";
  players = sortPlayers(players, safeKey, sortDir);

  // ── Paginate ────────────────────────────────────────────────────────────────
  const total = players.length;
  const start = (page - 1) * pageSize;
  const paginated = players.slice(start, start + pageSize);

  // ── Meta lists (for filter dropdowns) ───────────────────────────────────────
  const all = loadPlayers();
  const leagues   = [...new Set(all.map((p) => p.league))].sort();
  const countries = [...new Set(all.map((p) => p.nationality).filter(Boolean))].sort();

  const response: PlayersApiResponse & { page: number; pageSize: number; totalPages: number } = {
    players: paginated,
    total,
    page,
    pageSize,
    totalPages: Math.ceil(total / pageSize),
    leagues,
    countries,
    lastUpdated: new Date().toISOString(),
  };

  return NextResponse.json(response, {
    headers: {
      "Cache-Control": "s-maxage=3600, stale-while-revalidate=86400",
    },
  });
}
