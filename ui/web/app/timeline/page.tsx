'use client';

import Link from 'next/link';
import { useWorldState } from '@/hooks/useWorldState';
import { MultiLayerTimeline } from '@/components/MultiLayerTimeline';

export default function TimelinePage() {
  const { worldState } = useWorldState();

  return (
    <div className="p-6">
      <div className="mb-5">
        <h1 className="text-xl font-semibold text-slate-100">
          Multi-Layer Timeline
        </h1>
        <p className="text-sm text-slate-500 mt-1">
          Events synchronized across all 5 ontological layers. Hover an event
          to reveal participant connections.
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
      ) : worldState.events.length === 0 ? (
        <div className="flex flex-col items-center justify-center h-64 text-center">
          <p className="text-sm text-slate-600">
            This world state contains no events.
          </p>
        </div>
      ) : (
        <MultiLayerTimeline worldState={worldState} />
      )}
    </div>
  );
}
