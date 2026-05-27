// src/components/HeroSearch.tsx
"use client";

interface Props {
  totalPlayers: number;
  filteredCount: number;
  allLeagues: string[];
  allCountries: string[];
  searchValue: string;
  onSearchChange: (v: string) => void;
}

export function HeroSearch({ totalPlayers, allLeagues, allCountries, searchValue, onSearchChange }: Props) {
  return (
    <section className="bg-[#111118] border-b border-[#2a2a38] px-6 py-7">
      <div className="max-w-7xl mx-auto">
        <h1 className="font-serif text-4xl md:text-5xl leading-tight mb-1">
          Kadın Futbolu<br />
          <em className="text-[#c8a6f5] not-italic">Oyuncu Veritabanı</em>
        </h1>
        <p className="text-sm text-[#6b6685] mb-5">
          Dünya genelinde milli takım oyuncularını keşfedin · Fotoğraflar profil kartında görünür
        </p>

        {/* Search */}
        <div className="relative max-w-lg">
          <span className="absolute left-3.5 top-1/2 -translate-y-1/2 text-[#6b6685] text-base">🔍</span>
          <input
            type="text"
            value={searchValue}
            onChange={(e) => onSearchChange(e.target.value)}
            placeholder="İsim veya kulüp ara…"
            className="
              w-full bg-[#18181f] border border-[#2a2a38] rounded-xl
              pl-10 pr-4 py-2.5 text-sm text-white placeholder:text-[#6b6685]
              outline-none focus:border-[#c8a6f5] transition-colors
            "
          />
        </div>

        {/* Hero stats */}
        <div className="flex gap-6 mt-5">
          {[
            { n: allCountries.length, l: "Ülke" },
            { n: allLeagues.length,   l: "Lig"  },
            { n: totalPlayers,        l: "Oyuncu" },
          ].map(({ n, l }) => (
            <div key={l}>
              <div className="font-serif text-2xl text-[#c8a6f5]">{n}</div>
              <div className="text-[10px] text-[#6b6685] uppercase tracking-widest">{l}</div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

export default HeroSearch;
