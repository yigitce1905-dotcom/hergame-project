// Scout Pro — TypeScript Types
// Kadın Futbolu Kolektif Scout Veri Tabanı

// ─── Enums ─────────────────────────────────────────────────────────────────────

export type Position = "GK" | "RB" | "LB" | "CB" | "RCB" | "LCB" | "DM" | "CM" | "AM" | "RM" | "LM" | "RW" | "LW" | "SS" | "CF";

export type PlayerRole =
  | "ATTACKING_BACK" | "DEFENDING_BACK" | "BALL_PLAYING_CB"
  | "DEFENSIVE_CM" | "CREATIVE_CM" | "BOX_TO_BOX" | "PLAYMAKER"
  | "WINGER" | "INSIDE_FORWARD" | "TARGET_FORWARD"
  | "PRESSING_FORWARD" | "SECOND_STRIKER"
  | "SWEEPER_KEEPER" | "SHOT_STOPPER";

export type Foot = "RIGHT" | "LEFT" | "BOTH";
export type TransferStatus = "INTERESTED" | "CONTACTED" | "NEGOTIATING" | "SIGNED" | "REJECTED" | "ON_HOLD";

export type GradeLetter = "AA" | "AB" | "BB" | "BC" | "CC" | "CD" | "DD" | "DE" | "EE" | "FF";

// ─── Grade System ──────────────────────────────────────────────────────────────

export const GRADE_WEIGHTS: Record<GradeLetter, number> = {
  AA: 95, AB: 85, BB: 78, BC: 68, CC: 58, CD: 48, DD: 38, DE: 28, EE: 18, FF: 5,
};

export const GRADE_ORDER: GradeLetter[] = ["AA", "AB", "BB", "BC", "CC", "CD", "DD", "DE", "EE", "FF"];

export function gradeToScore(grade: GradeLetter): number {
  return GRADE_WEIGHTS[grade];
}

export function scoreToGrade(score: number): GradeLetter {
  const entry = Object.entries(GRADE_WEIGHTS)
    .sort(([, a], [, b]) => Math.abs(score - a) - Math.abs(score - b))[0];
  return entry[0] as GradeLetter;
}

export function gradeColor(grade: GradeLetter): string {
  const score = GRADE_WEIGHTS[grade];
  if (score >= 85) return "#22c55e"; // green-500
  if (score >= 68) return "#84cc16"; // lime-500
  if (score >= 48) return "#eab308"; // yellow-500
  if (score >= 28) return "#f97316"; // orange-500
  return "#ef4444";                  // red-500
}

// ─── Player Models ─────────────────────────────────────────────────────────────

export interface ScoutPlayerPosition {
  position: Position;
  role?: PlayerRole;
  isPrimary: boolean;
}

export interface PlayerStats90 {
  id?: number;
  season: string;
  competition?: string;
  matches: number;
  minutes: number;
  // Attack
  goals: number;
  xG: number;
  xG90: number;
  shots90: number;
  penAreaTouch90: number;
  assists: number;
  // Passing
  passes90: number;
  passAccuracy: number;
  forwardPasses90: number;
  longPasses90: number;
  keyPasses90: number;
  smartPasses90: number;
  throughBalls90: number;
  throughBallAccuracy: number;
  longPassAccuracy: number;
  // Carrying
  dribbles90: number;
  dribbleSuccess: number;
  progressiveRuns90: number;
  carries90: number;
  // Defense
  defActions90: number;
  defDuels90: number;
  defDuelSuccess: number;
  aerialDuels90: number;
  aerialSuccess: number;
  interceptions90: number;
  tackles90: number;
  pressures90: number;
  pressureSuccess: number;
  // GK optional
  saves90?: number;
  saveRate?: number;
}

export interface ScoutEvaluation {
  id?: number;
  evaluatedAt?: string;
  evaluatedBy?: string;
  // BECERİ
  technicalSkill: GradeLetter;
  ballControl: GradeLetter;
  finishing: GradeLetter;
  passing: GradeLetter;
  dribbling: GradeLetter;
  crossing: GradeLetter;
  setPieces: GradeLetter;
  // BEŞERİ Mental
  decisionMaking: GradeLetter;
  positioning: GradeLetter;
  leadership: GradeLetter;
  workRate: GradeLetter;
  composure: GradeLetter;
  // BEŞERİ Sosyal
  teamwork: GradeLetter;
  communication: GradeLetter;
  attitude: GradeLetter;
  // FİZİKİ
  pace: GradeLetter;
  strength: GradeLetter;
  stamina: GradeLetter;
  agility: GradeLetter;
  jumping: GradeLetter;
  // TARZ
  pressingIntensity: GradeLetter;
  buildUpPlay: GradeLetter;
  defensiveShape: GradeLetter;
  // Computed
  overallScore?: number;
  overallGrade?: GradeLetter;
  notes?: string;
}

export interface ScoutPlayer {
  id: number;
  name: string;
  birthDate?: string;
  age: number;
  birthPlace?: string;
  nationality: string;
  flag?: string;
  height?: number;
  foot: Foot;
  photo_url?: string;
  // Club
  currentClub: string;
  league: string;
  leagueCode?: string;
  contractEnd?: string;
  agentName?: string;
  marketValue: number;
  // External
  soccerdonnaId?: string;
  soccerdonnaUrl?: string;
  // Relations
  positions: ScoutPlayerPosition[];
  stats?: PlayerStats90[];
  evaluation?: ScoutEvaluation;
}

// ─── Radar Chart Axes ──────────────────────────────────────────────────────────

export interface RadarAxis {
  key: string;
  label: string;
  value: number; // 0–100
}

export function computeRadarAxes(stats?: PlayerStats90): RadarAxis[] {
  if (!stats) {
    return [
      { key: "press", label: "Ön Pres", value: 50 },
      { key: "aerial", label: "Hava", value: 50 },
      { key: "passing", label: "Pas", value: 50 },
      { key: "carrying", label: "Taşıma", value: 50 },
      { key: "creativity", label: "Yaratıcılık", value: 50 },
      { key: "finishing", label: "Bitiricilik", value: 50 },
    ];
  }
  const clamp = (v: number, max: number) => Math.min(100, (v / max) * 100);
  return [
    { key: "press", label: "Ön Pres", value: Math.round((clamp(stats.pressures90, 15) + stats.pressureSuccess) / 2) },
    { key: "aerial", label: "Hava", value: Math.round((clamp(stats.aerialDuels90, 8) + stats.aerialSuccess) / 2) },
    { key: "passing", label: "Pas", value: Math.round((stats.passAccuracy + clamp(stats.keyPasses90, 3)) / 2) },
    { key: "carrying", label: "Taşıma", value: Math.round((stats.dribbleSuccess + clamp(stats.progressiveRuns90, 4)) / 2) },
    { key: "creativity", label: "Yaratıcılık", value: Math.round((clamp(stats.smartPasses90, 5) * 100 + clamp(stats.keyPasses90, 3) * 100) / 2 / 100) },
    { key: "finishing", label: "Bitiricilik", value: Math.round((clamp(stats.xG90, 0.8) + clamp(stats.shots90, 6)) / 2) },
  ];
}

// ─── Filter Types ──────────────────────────────────────────────────────────────

export interface ScoutFilters {
  search: string;
  positions: Position[];
  roles: PlayerRole[];
  ageMin: number;
  ageMax: number;
  marketValueMin: number;
  marketValueMax: number;
  contractEndBefore?: string;
  foot?: Foot;
  nationality: string;
  league: string;
  club: string;
  agent: string;
  freeAgentOnly: boolean;
}

export const DEFAULT_FILTERS: ScoutFilters = {
  search: "",
  positions: [],
  roles: [],
  ageMin: 15,
  ageMax: 40,
  marketValueMin: 0,
  marketValueMax: 50_000_000,
  nationality: "",
  league: "",
  club: "",
  agent: "",
  freeAgentOnly: false,
};

// ─── UI Types ──────────────────────────────────────────────────────────────────

export type ScoutTab = "all" | "free-agents" | "incoming" | "favorites" | "squad";

export type SortKey =
  | "name" | "age" | "marketValue" | "contractEnd"
  | "xG90" | "passes90" | "dribbleSuccess" | "defActions90" | "overallScore";

export type SortDir = "asc" | "desc";

// ─── Incoming / Favorites ──────────────────────────────────────────────────────

export interface IncomingEntry {
  id: number;
  player?: ScoutPlayer;
  rawName?: string;
  soccerdonnaUrl?: string;
  recommendedBy: string;
  recommendedAt: string;
  status: TransferStatus;
  notes?: string;
  priority: 1 | 2 | 3;
}

export interface FavoriteEntry {
  id: number;
  player: ScoutPlayer;
  addedAt: string;
  addedBy?: string;
  notes?: string;
}

// ─── Squad Building ────────────────────────────────────────────────────────────

export interface SquadSlot {
  position: Position;
  slotIndex: number; // 0=starter, 1=1st sub, 2=2nd sub
  player?: ScoutPlayer;
  isTarget?: boolean;
}

export interface SquadPlan {
  id: number;
  name: string;
  teamName: string;
  formation: string;
  season: string;
  slots: SquadSlot[];
}

// Formation definitions: position => [x%, y%] for pitch display
export const FORMATION_POSITIONS: Record<string, { pos: Position; x: number; y: number }[]> = {
  "4-3-3": [
    { pos: "GK", x: 50, y: 90 },
    { pos: "RB", x: 80, y: 72 }, { pos: "RCB", x: 63, y: 72 },
    { pos: "LCB", x: 37, y: 72 }, { pos: "LB", x: 20, y: 72 },
    { pos: "CM", x: 65, y: 50 }, { pos: "DM", x: 50, y: 55 }, { pos: "CM", x: 35, y: 50 },
    { pos: "RW", x: 75, y: 28 }, { pos: "CF", x: 50, y: 20 }, { pos: "LW", x: 25, y: 28 },
  ],
  "4-2-3-1": [
    { pos: "GK", x: 50, y: 90 },
    { pos: "RB", x: 80, y: 72 }, { pos: "RCB", x: 63, y: 72 },
    { pos: "LCB", x: 37, y: 72 }, { pos: "LB", x: 20, y: 72 },
    { pos: "DM", x: 60, y: 58 }, { pos: "DM", x: 40, y: 58 },
    { pos: "RM", x: 75, y: 38 }, { pos: "AM", x: 50, y: 38 }, { pos: "LM", x: 25, y: 38 },
    { pos: "CF", x: 50, y: 20 },
  ],
  "3-5-2": [
    { pos: "GK", x: 50, y: 90 },
    { pos: "RCB", x: 68, y: 72 }, { pos: "CB", x: 50, y: 72 }, { pos: "LCB", x: 32, y: 72 },
    { pos: "RB", x: 85, y: 52 }, { pos: "CM", x: 65, y: 52 }, { pos: "DM", x: 50, y: 55 },
    { pos: "CM", x: 35, y: 52 }, { pos: "LB", x: 15, y: 52 },
    { pos: "CF", x: 62, y: 22 }, { pos: "CF", x: 38, y: 22 },
  ],
};

// ─── Position display helpers ──────────────────────────────────────────────────

export const POSITION_LABELS: Record<Position, string> = {
  GK: "Kaleci", RB: "Sağ Bek", LB: "Sol Bek", CB: "Stoper",
  RCB: "Sağ Stoper", LCB: "Sol Stoper",
  DM: "Def. Orta Saha", CM: "Orta Saha", AM: "Ofansif Orta Saha",
  RM: "Sağ Kanat Orta", LM: "Sol Kanat Orta",
  RW: "Sağ Kanat", LW: "Sol Kanat", SS: "İkinci Santrfor", CF: "Santrfor",
};

export const ROLE_LABELS: Record<PlayerRole, string> = {
  ATTACKING_BACK: "Hücumcu Bek", DEFENDING_BACK: "Savunmacı Bek",
  BALL_PLAYING_CB: "Top Oynatan Stoper", DEFENSIVE_CM: "Savunmacı Orta",
  CREATIVE_CM: "Yaratıcı Orta", BOX_TO_BOX: "Box-to-Box",
  PLAYMAKER: "Oyun Kurucu", WINGER: "Kanatçı",
  INSIDE_FORWARD: "İçe Kesen Kanat", TARGET_FORWARD: "Pivot Santrfor",
  PRESSING_FORWARD: "Pres Forvet", SECOND_STRIKER: "İkinci Forvet",
  SWEEPER_KEEPER: "Libero Kaleci", SHOT_STOPPER: "Kale Bekçisi",
};

export const POSITION_GROUPS: { label: string; positions: Position[] }[] = [
  { label: "Kaleci", positions: ["GK"] },
  { label: "Defans", positions: ["RB", "LB", "CB", "RCB", "LCB"] },
  { label: "Orta Saha", positions: ["DM", "CM", "AM", "RM", "LM"] },
  { label: "Hücum", positions: ["RW", "LW", "SS", "CF"] },
];
