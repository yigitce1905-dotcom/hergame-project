import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'HerGame — Women\'s Football Database',
  description: 'Women\'s football player database',
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="tr">
      <body>{children}</body>
    </html>
  )
}
