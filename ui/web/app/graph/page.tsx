'use client';

import dynamic from 'next/dynamic';
import Link from 'next/link';
import { useWorldState } from '@/hooks/useWorldState';

const KnowledgeGraph = dynamic(
  () =>
    import('@/components/KnowledgeGraph').then((m) => m.KnowledgeGraph),
  {
    ssr: false,
    loading: () => (
      <div className="flex items-center justify-center h-96 text-sm text-slate-500">
        Loading graph…
      </div>
    ),
  }
);

export default function GraphPage() {
  const { worldState } = useWorldState();

  return (
    <div className="p-6 flex flex-col" style={{ minHeight: 'calc(100vh - 1px)' }}>
      <div className="mb-5">
        <h1 className="text-xl font-semibold text-slate-100">Knowledge Graph</h1>
        <p className="text-sm text-slate-500 mt-1">
          Entities and causal relations as an interactive force graph. Scroll to
          zoom, click a node to inspect.
        </p>
      </div>

      {!worldState ? (
        <div className="flex flex-col items-center justify-center flex-1 text-center">
          <p className="text-sm text-slate-600 mb-3">No world state loaded.</p>
          <Link
            href="/query"
            className="text-xs text-indigo-400 hover:text-indigo-300 font-mono transition-colors"
          >
            ← Run a query first
          </Link>
        </div>
      ) : (
        <div className="flex-1" style={{ minHeight: 480 }}>
          <KnowledgeGraph worldState={worldState} />
        </div>
      )}
    </div>
  );
}
