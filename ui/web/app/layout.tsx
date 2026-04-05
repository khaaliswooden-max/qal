import type { Metadata } from 'next';
import { Inter, JetBrains_Mono } from 'next/font/google';
import { WorldStateProvider } from './providers';
import { Sidebar } from '@/components/layout/Sidebar';
import './globals.css';

const inter = Inter({
  subsets: ['latin'],
  variable: '--font-inter',
});

const jetbrainsMono = JetBrains_Mono({
  subsets: ['latin'],
  variable: '--font-mono',
});

export const metadata: Metadata = {
  title: 'QAWM — Quantum Archeological World Model',
  description:
    'Academic interface for reconstructing and analyzing historical world states.',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className={`${inter.variable} ${jetbrainsMono.variable}`}>
      <body className="bg-[#0f1117] antialiased flex min-h-screen">
        <WorldStateProvider>
          <Sidebar />
          <main className="flex-1 min-w-0 overflow-auto">{children}</main>
        </WorldStateProvider>
      </body>
    </html>
  );
}
