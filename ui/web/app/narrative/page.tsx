'use client';

import Link from 'next/link';
import { useWorldState } from '@/hooks/useWorldState';
import { NarrativeGenerator } from '@/components/NarrativeGenerator';

export default function NarrativePage() {
  const { worldState } = useWorldState();

  return (
    <div className="p-6">
      <div className="mb-5">
        <h1 className="text-xl font-semibold text-slate-100">Narrative</h1>
        <p className="text-sm text-slate-500 mt-1">
          Academic prose generated from the current world state, with inline
          epistemic footnotes and plain-text export.
        </p>
      </div>

      {!worldState ? (
        <div className="flex flex-col items-center justify-center h-64 text-center">
          <p className="text-sm text-slate-600 mb-3">No world state loaded.</p>
          <Link
            href="/query"
            className="text-xs text-indigo-400 hover:text-indigo-300 font-mono transition-colors"
          >
            ← Run a query first
          </Link>
        </div>
      ) : (
        <NarrativeGenerator worldState={worldState} />
      )}
    </div>
  );
}
