// HerGame — TypeScript Types
// All interfaces are designed to match the scraper output exactly.

export interface Transfer {
  year: string;          // "2022"
  from: string;          // "Arsenal WFC"
  to: string;            // "FC Barcelona Femení"
  fee?: string;          // "€ 500k" — if available
}

export interface SwotAnalysis {
  strengths: string[];
  weaknesses: string[];
  opportunities: string[];
  threats: string[];
  generated_at: string;  // ISO timestamp
  model: string;         // "gemini-1.5-flash"
}

export interface Player {
  // ── Identifiers ────────────────────────────────────────────────────────────
  id?: number;           // TUR1 players have sequential IDs; hidden gems may not
  soccerdonna_id: string;
  soccerdonna_url: string;

  // ── Personal ───────────────────────────────────────────────────────────────
  name: string;
  age: number;
  born: string;           // "14.07.1989"
  birth_place: string;    // "Huntington Beach, CA"
  nationality: string;    // "USA"
  flag: string;           // "🇺🇸"

  // ── Club ───────────────────────────────────────────────────────────────────
  club: string;
  league: string;
  league_code: string;    // "ENG1"

  // ── Position ───────────────────────────────────────────────────────────────
  position: "GK" | "DF" | "MF" | "FW";
  position_detail: string; // "Centre-Forward"

  // ── Physical ───────────────────────────────────────────────────────────────
  height: string;         // "170 cm"
  foot: string;           // "Right" | "Left" | "Both"

  // ── Club Statistics ────────────────────────────────────────────────────────
  goals: number;
  assists: number;
  appearances: number;
  yellow_cards: number;
  red_cards: number;

  // ── National Team ──────────────────────────────────────────────────────────
  caps: number;
  national_team: string;
  national_goals: number;

  // ── Market Value ───────────────────────────────────────────────────────────
  market_value: string;      // "€2.5M"
  market_value_num: number;  // 2500000

  // ── Media ──────────────────────────────────────────────────────────────────
  photo_url: string;

  // ── Rich Content ───────────────────────────────────────────────────────────
  bio: string;
  transfers: Transfer[];
  achievements: string[];

  // ── FM26 Hidden Gems ───────────────────────────────────────────────────────
  hidden_gem?: boolean;    // true = FM26 hidden gem listesinden
  fm_rating?: number;      // FM26 scout rating (50–99)
  fm_position?: string;    // FM26 position string, e.g. "AM (RC), ST (C)"
  swot?: SwotAnalysis;
}

// ── Filter / Sort types used by the UI ────────────────────────────────────────
export type Position = "GK" | "DF" | "MF" | "FW" | "";

export interface PlayerFilters {
  search: string;
  country: string;
  league: string;
  position: Position;
  ageMin: number;
  ageMax: number;
  clubSearch: string;
  hiddenGem: boolean;  // FM26 hidden gem filtresi
}

export type SortKey =
  | "name"
  | "age"
  | "goals"
  | "assists"
  | "appearances"
  | "caps"
  | "market_value_num";

export type SortDir = "asc" | "desc";

export interface SortConfig {
  key: SortKey;
  dir: SortDir;
}

// ── API response shapes ────────────────────────────────────────────────────────
export interface PlayersApiResponse {
  players: Player[];
  total: number;
  leagues: string[];
  countries: string[];
  lastUpdated: string;
}

// ── Scraper metadata (stored alongside player data) ───────────────────────────
export interface ScraperMeta {
  scrapedAt: string;       // ISO timestamp
  leagueCode: string;
  leagueName: string;
  playerCount: number;
  source: "soccerdonna";
  version: string;
}
