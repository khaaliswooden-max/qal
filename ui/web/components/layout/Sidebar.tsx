'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';

const NAV_ITEMS = [
  {
    href: '/query',
    label: 'Query',
    icon: (
      <svg className="w-5 h-5 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5}
          d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
      </svg>
    ),
  },
  {
    href: '/graph',
    label: 'Graph',
    icon: (
      <svg className="w-5 h-5 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <circle cx="12" cy="5" r="2" fill="currentColor" stroke="none" />
        <circle cx="5" cy="19" r="2" fill="currentColor" stroke="none" />
        <circle cx="19" cy="19" r="2" fill="currentColor" stroke="none" />
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5}
          d="M12 7L6 17M12 7l6 10M7 19h10" />
      </svg>
    ),
  },
  {
    href: '/timeline',
    label: 'Timeline',
    icon: (
      <svg className="w-5 h-5 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5}
          d="M4 6h16M4 10h10M4 14h13M4 18h7" />
      </svg>
    ),
  },
  {
    href: '/narrative',
    label: 'Narrative',
    icon: (
      <svg className="w-5 h-5 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5}
          d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
      </svg>
    ),
  },
];

export function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="group flex flex-col h-screen w-16 hover:w-48 transition-[width] duration-200 ease-in-out overflow-hidden shrink-0 bg-[#1a1d27] border-r border-[#2a2d3a] sticky top-0 z-20">
      {/* Logo mark */}
      <div className="flex items-center gap-3 px-4 py-5 border-b border-[#2a2d3a] min-h-[60px]">
        <span className="w-2 h-2 rounded-full bg-indigo-500 animate-pulse shrink-0" />
        <span className="text-xs font-mono text-slate-500 uppercase tracking-widest opacity-0 group-hover:opacity-100 transition-opacity duration-150 delay-100 whitespace-nowrap">
          QAWM
        </span>
      </div>

      {/* Nav items */}
      <nav className="flex-1 py-3 space-y-1 px-2">
        {NAV_ITEMS.map((item) => {
          const active = pathname.startsWith(item.href);
          return (
            <Link
              key={item.href}
              href={item.href}
              className={`flex items-center gap-3 px-3 py-2.5 rounded-lg transition-colors ${
                active
                  ? 'bg-indigo-600/20 text-indigo-400'
                  : 'text-slate-500 hover:text-slate-200 hover:bg-[#2a2d3a]'
              }`}
            >
              {item.icon}
              <span className="text-sm font-medium whitespace-nowrap opacity-0 group-hover:opacity-100 transition-opacity duration-150 delay-100">
                {item.label}
              </span>
            </Link>
          );
        })}
      </nav>

      {/* Footer version */}
      <div className="px-4 py-4 border-t border-[#2a2d3a] min-h-[48px] flex items-center">
        <span className="text-xs font-mono text-slate-600 opacity-0 group-hover:opacity-100 transition-opacity duration-150 delay-100 whitespace-nowrap">
          v0.1.0-alpha
        </span>
      </div>
    </aside>
  );
}
