'use client';

import { useQAWMQuery } from '@/hooks/useQAWMQuery';
import { QueryBuilder } from '@/components/QueryBuilder';
import { ResultsPanel } from '@/components/ResultsPanel';
import type {
  QueryMode,
  ReconstructRequest,
  CompareRequest,
  CounterfactualRequest,
} from '@/lib/types';

export default function QueryPage() {
  const { result, loading, error, submit } = useQAWMQuery();

  function handleSubmit(
    mode: QueryMode,
    payload: ReconstructRequest | CompareRequest | CounterfactualRequest
  ) {
    submit(mode, payload);
  }

  return (
    <div className="min-h-screen bg-[#0f1117]">
      {/* Top bar */}
      <header className="border-b border-[#2a2d3a] bg-[#1a1d27] px-6 py-3">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <div className="flex items-center gap-3">
            <span className="w-2 h-2 rounded-full bg-indigo-500 animate-pulse" />
            <span className="text-xs font-mono text-slate-500 uppercase tracking-widest">
              Quantum Archeological World Model
            </span>
          </div>
          <span className="text-xs font-mono text-slate-600">v0.1.0-alpha</span>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 py-8">
        {/* Page title */}
        <div className="mb-6">
          <h1 className="text-xl font-semibold text-slate-100">
            Query Workbench
          </h1>
          <p className="text-sm text-slate-500 mt-1">
            Reconstruct, compare, or run counterfactuals on historical world
            states. All claims are trace-backed and confidence-labelled.
          </p>
        </div>

        {/* Two-column layout */}
        <div className="grid grid-cols-1 lg:grid-cols-[360px_1fr] gap-5">
          {/* Left: Query Builder */}
          <div className="rounded-xl border border-[#2a2d3a] bg-[#1a1d27] p-5">
            <p className="text-xs font-mono text-slate-500 uppercase tracking-wider mb-4">
              Query
            </p>
            <QueryBuilder loading={loading} onSubmit={handleSubmit} />
          </div>

          {/* Right: Results */}
          <div className="rounded-xl border border-[#2a2d3a] bg-[#1a1d27] p-5">
            <p className="text-xs font-mono text-slate-500 uppercase tracking-wider mb-4">
              World State
            </p>

            {/* Empty state */}
            {!result && !loading && !error && (
              <div className="flex flex-col items-center justify-center h-64 text-center">
                <div className="w-12 h-12 rounded-full border border-[#2a2d3a] flex items-center justify-center mb-3">
                  <svg
                    className="w-5 h-5 text-slate-600"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={1.5}
                      d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
                    />
                  </svg>
                </div>
                <p className="text-sm text-slate-600">
                  Run a query to reconstruct a world state
                </p>
                <p className="text-xs text-slate-700 mt-1">
                  Results include entities, events, and causal relations
                </p>
              </div>
            )}

            {/* Loading */}
            {loading && (
              <div className="flex flex-col items-center justify-center h-64 text-center">
                <svg
                  className="animate-spin h-8 w-8 text-indigo-500 mb-3"
                  fill="none"
                  viewBox="0 0 24 24"
                >
                  <circle
                    className="opacity-25"
                    cx="12"
                    cy="12"
                    r="10"
                    stroke="currentColor"
                    strokeWidth="4"
                  />
                  <path
                    className="opacity-75"
                    fill="currentColor"
                    d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"
                  />
                </svg>
                <p className="text-sm text-slate-500">Reconstructing world state…</p>
                <p className="text-xs text-slate-600 mt-1">
                  Tracing causal chains across layers
                </p>
              </div>
            )}

            {/* Error */}
            {error && (
              <div className="rounded-lg border border-red-800/50 bg-red-900/10 p-4">
                <p className="text-xs font-mono text-red-400 font-semibold mb-1">
                  Query Error
                </p>
                <p className="text-sm text-red-300">{error}</p>
                <p className="text-xs text-red-500/70 mt-2 font-mono">
                  Ensure the QAWM backend is running at{' '}
                  {process.env.NEXT_PUBLIC_QAWM_API_URL ?? 'http://localhost:8000'}
                </p>
              </div>
            )}

            {/* Results */}
            {result && <ResultsPanel result={result} />}
          </div>
        </div>
      </main>
    </div>
  );
}
