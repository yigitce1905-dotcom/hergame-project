import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'W-Scope — Kadın Futbolu Scout Platformu',
  description: 'Kolektif scout veri tabanı ve yönetim platformu. Kadın futboluna özel veri odaklı analiz.',
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="tr">
      <body>{children}</body>
    </html>
  )
}
