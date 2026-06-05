import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function formatMarketValue(euros: number): string {
  if (euros >= 1_000_000) return `€${(euros / 1_000_000).toFixed(1)}M`;
  if (euros >= 1_000) return `€${(euros / 1_000).toFixed(0)}K`;
  return euros === 0 ? "—" : `€${euros}`;
}

export function formatContractEnd(dateStr?: string): string {
  if (!dateStr) return "Belirsiz";
  const d = new Date(dateStr);
  return d.toLocaleDateString("tr-TR", { month: "short", year: "numeric" });
}

export function contractEndColor(dateStr?: string): string {
  if (!dateStr) return "text-zinc-400";
  const months = (new Date(dateStr).getTime() - Date.now()) / (1000 * 60 * 60 * 24 * 30);
  if (months < 6) return "text-red-400";
  if (months < 12) return "text-amber-400";
  return "text-emerald-400";
}

export function statBarColor(value: number): string {
  if (value >= 75) return "bg-emerald-500";
  if (value >= 50) return "bg-yellow-500";
  if (value >= 25) return "bg-orange-500";
  return "bg-red-500";
}
