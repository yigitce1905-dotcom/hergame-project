"use client";

interface PanelProps { onClose: () => void; }

const SOURCES = [
  {
    name: "SoccerDonna.de",
    badge: "SCRAPER",
    badgeColor: "#f5c842",
    icon: "🌐",
    desc: "Kadın futbolunun en büyük veritabanı. Transfermarkt altyapısı. Piyasa değerleri, transfer geçmişi, biyografi.",
    code: `python scraper/soccerdonna_scraper.py --leagues TUR1\npython scraper/json_to_app.py`,
    warning: "ToS'a uygun kullanım. Site güncellemelerinde bozulabilir.",
  },
  {
    name: "API-Football (RapidAPI)",
    badge: "100 REQ/GÜN ÜCRETSİZ",
    badgeColor: "#6ee8c8",
    icon: "⚡",
    desc: "WSL, Liga F, D1 Féminine, NWSL dahil kadın ligleri. Canlı maç verileri + oyuncu istatistikleri.",
    code: `// TUR Women: 1074 | WSL: 493 | Liga F: 957\nfetch("https://api-football-v1.p.rapidapi.com/v3/players?league=1074&season=2024")`,
    warning: "Ücretsiz planda oyuncu fotoğrafları kısıtlı olabilir.",
  },
];

export function DataSourcePanel({ onClose }: PanelProps) {
  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/75 backdrop-blur-sm"
      onClick={(e) => e.target === e.currentTarget && onClose()}
    >
      <div className="bg-[#16161e] border border-[#3a3a4e] rounded-2xl w-full max-w-2xl max-h-[88vh] overflow-y-auto p-6">
        <div className="flex items-start justify-between mb-1">
          <h2 className="font-serif text-2xl">📊 Veri Kaynakları</h2>
          <button onClick={onClose} className="text-[#6b6685] hover:text-white text-lg ml-4">✕</button>
        </div>
        <p className="text-sm text-[#6b6685] mb-5">Kadın futbolu için uygun kaynaklar</p>
        <div className="space-y-3">
          {SOURCES.map((s) => (
            <div key={s.name} className="border border-[#2a2a38] rounded-xl p-4">
              <div className="flex items-center gap-2.5 mb-2">
                <span className="text-xl">{s.icon}</span>
                <span className="font-semibold text-sm text-white">{s.name}</span>
                <span className="ml-auto text-[10px] font-bold px-2 py-0.5 rounded border"
                  style={{ color: s.badgeColor, borderColor: `${s.badgeColor}44`, background: `${s.badgeColor}18` }}>
                  {s.badge}
                </span>
              </div>
              <p className="text-xs text-[#6b6685] mb-2">{s.desc}</p>
              <pre className="bg-[#0a0a0f] border border-[#2a2a38] rounded-lg p-3 text-xs text-[#c8a6f5] overflow-x-auto whitespace-pre-wrap">{s.code}</pre>
              {s.warning && <p className="text-xs text-[#f5c842] mt-2">⚠️ {s.warning}</p>}
            </div>
          ))}
        </div>
        <button onClick={onClose} className="mt-4 w-full py-2.5 rounded-xl border border-[#2a2a38] text-sm text-[#a09bbf] hover:border-[#c8a6f5] hover:text-[#c8a6f5] transition-colors">
          Kapat
        </button>
      </div>
    </div>
  );
}

export default DataSourcePanel;
