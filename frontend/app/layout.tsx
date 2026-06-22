import './globals.css'
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'AI Manga Translator Pro',
  description: 'Translate manga/manhwa chapters inside images with AI',
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="ar" dir="rtl">
      <body>{children}</body>
    </html>
  )
}
