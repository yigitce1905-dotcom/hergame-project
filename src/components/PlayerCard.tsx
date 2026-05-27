// src/components/PlayerCard.tsx
// Card shown in the grid — NO photo, just initials avatar + stats.
// Photo only appears in the PlayerModal.

import type { Player } from "@/types";

interface Props {
  player: Player;
  onClick: () => void;
}

const POS_STYLES: Record<string, string> = {
  GK: "text-[#f5c842] bg-[#f5c842]/10 border-[#f5c842]/30",
  DF: "text-[#6ee8c8] bg-[#6ee8c8]/10 border-[#6ee8c8]/30",
  MF: "text-[#c8a6f5] bg-[#c8a6f5]/10 border-[#c8a6f5]/30",
  FW: "text-[#f5a6c8] bg-[#f5a6c8]/10 border-[#f5a6c8]/30",
};

function initials(name: string): string {
  const parts = name.trim().split(" ");
  if (parts.length === 1) return parts[0][0]?.toUpperCase() ?? "?";
  return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase();
}

export default function PlayerCard({ player, onClick }: Props) {
  const posStyle = POS_STYLES[player.position] ?? POS_STYLES.MF;

  return (
    <article
      onClick={onClick}
      className="
        bg-[#16161e] border border-[#2a2a38] rounded-2xl p-4 cursor-pointer
        transition-all duration-200
        hover:border-[#c8a6f5] hover:-translate-y-0.5 hover:shadow-[0_6px_24px_rgba(200,166,245,0.12)]
        focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#c8a6f5]
      "
      role="button"
      tabIndex={0}
      onKeyDown={(e) => e.key === "Enter" && onClick()}
      aria-label={`${player.name} profili — tıkla`}
    >
      {/* Top row: initials avatar + flag + position badge */}
      <div className="flex items-start justify-between mb-3">
        <div className="
          w-12 h-12 rounded-xl bg-[#18181f] border border-[#2a2a38]
          flex items-center justify-center
          text-[#c8a6f5] font-bold text-lg tracking-tight font-serif
          flex-shrink-0
        ">
          {initials(player.name)}
        </div>
        <div className="flex flex-col items-end gap-1.5">
          <span className="text-2xl leading-none" aria-label={player.nationality}>
            {player.flag}
          </span>
          <div className="flex items-center gap-1">
            {player.hidden_gem && player.fm_rating && (
              <span className="text-[10px] font-bold px-1.5 py-0.5 rounded bg-[#f5c842]/15 border border-[#f5c842]/35 text-[#f5c842]">
                ⭐{player.fm_rating}
              </span>
            )}
            <span className={`text-xs font-bold px-2 py-0.5 rounded border ${posStyle}`}>
              {player.position}
            </span>
          </div>
        </div>
      </div>

      {/* Name + Club */}
      <h2 className="font-serif text-[17px] leading-tight text-white mb-0.5">
        {player.name}
      </h2>
      <p className="text-xs text-[#6b6685] mb-3 truncate">
        {player.club} &middot; {player.league}
      </p>

      {/* Stats: goals / assists / appearances */}
      <div className="grid grid-cols-3 gap-1.5 mb-3">
        {[
          { n: player.goals,       l: "Gol" },
          { n: player.assists,     l: "Asist" },
          { n: player.appearances, l: "Maç" },
        ].map(({ n, l }) => (
          <div
            key={l}
            className="bg-[#18181f] border border-[#2a2a38] rounded-lg py-2 text-center"
          >
            <div className="text-[18px] font-semibold text-white leading-none">{n}</div>
            <div className="text-[10px] text-[#6b6685] uppercase tracking-wide mt-0.5">{l}</div>
          </div>
        ))}
      </div>

      {/* Footer: age / caps / market value */}
      <div className="flex items-center justify-between pt-2.5 border-t border-[#2a2a38]">
        <span className="text-xs text-[#6b6685]">{player.age} yaş</span>
        <span className="text-xs text-[#6b6685] flex items-center gap-1">
          <span className="w-1.5 h-1.5 rounded-full bg-[#f5a6c8] inline-block" />
          {player.caps} milli
        </span>
        <span className="text-xs font-semibold text-[#6ee8c8]">{player.market_value}</span>
      </div>
    </article>
  );
}
