'use client';

import { useState } from 'react';
import type { WorldState, Confidence } from '@/lib/types';
import { EntityCard } from './EntityCard';
import { EventList } from './EventList';

const TABS = ['Entities', 'Events', 'Relations', 'Raw JSON'] as const;
type Tab = (typeof TABS)[number];

const CONFIDENCE_FILTERS: { label: string; value: Confidence | 'ALL' }[] = [
  { label: 'All', value: 'ALL' },
  { label: 'Verified only', value: 'VERIFIED' },
  { label: 'Plausible+', value: 'PLAUSIBLE' },
  { label: 'Speculative+', value: 'SPECULATIVE' },
];

export function ResultsPanel({ result }: { result: WorldState }) {
  const [tab, setTab] = useState<Tab>('Entities');
  const [minConfidence, setMinConfidence] = useState<Confidence | 'ALL'>('ALL');

  return (
    <div className="space-y-4">
      {/* Model header */}
      <div className="flex items-center justify-between">
        <div>
          <p className="text-xs text-slate-500 font-mono">model_id</p>
          <p className="text-sm font-mono text-indigo-400 mt-0.5">
            {result.model_id}
          </p>
        </div>
        <div className="flex items-center gap-4 text-xs text-slate-500 font-mono">
          <span>{result.entities.length} entities</span>
          <span>{result.events.length} events</span>
          <span>{result.relations.length} relations</span>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex gap-1 border-b border-[#2a2d3a]">
        {TABS.map((t) => (
          <button
            key={t}
            onClick={() => setTab(t)}
            className={`px-3 py-2 text-xs font-medium transition-colors border-b-2 -mb-px ${
              tab === t
                ? 'border-indigo-500 text-indigo-400'
                : 'border-transparent text-slate-500 hover:text-slate-300'
            }`}
          >
            {t}
          </button>
        ))}
      </div>

      {/* Confidence filter (Events only) */}
      {tab === 'Events' && (
        <div className="flex flex-wrap items-center gap-1.5">
          <span className="text-xs text-slate-500 mr-1">Min confidence:</span>
          {CONFIDENCE_FILTERS.map((opt) => (
            <button
              key={opt.value}
              onClick={() => setMinConfidence(opt.value)}
              className={`text-xs px-2 py-1 rounded font-mono transition-colors ${
                minConfidence === opt.value
                  ? 'bg-indigo-600 text-white'
                  : 'text-slate-500 hover:text-slate-300 bg-[#1a1d27] border border-[#2a2d3a]'
              }`}
            >
              {opt.label}
            </button>
          ))}
        </div>
      )}

      {/* Tab content */}
      {tab === 'Entities' && (
        <div className="space-y-3">
          {result.entities.length === 0 ? (
            <p className="text-sm text-slate-500 text-center py-8">
              No entities in this world state.
            </p>
          ) : (
            result.entities.map((entity) => (
              <EntityCard key={entity.id} entity={entity} />
            ))
          )}
        </div>
      )}

      {tab === 'Events' && (
        <EventList
          events={result.events}
          minConfidence={minConfidence === 'ALL' ? undefined : minConfidence}
        />
      )}

      {tab === 'Relations' && (
        <div className="space-y-2">
          {result.relations.length === 0 ? (
            <p className="text-sm text-slate-500 text-center py-8">
              No relations in this world state.
            </p>
          ) : (
            result.relations.map((rel, i) => (
              <div
                key={i}
                className="flex items-center gap-2 rounded-lg border border-[#2a2d3a] bg-[#1a1d27] p-3"
              >
                <span className="text-xs font-mono text-slate-300 truncate max-w-[30%]">
                  {rel.source_id}
                </span>
                <span className="text-xs font-mono text-indigo-400 shrink-0 px-2">
                  {rel.type}
                </span>
                <span className="text-xs font-mono text-slate-300 truncate max-w-[30%]">
                  {rel.target_id}
                </span>
                <div className="ml-auto flex items-center gap-2 shrink-0">
                  <div className="w-16 h-1.5 rounded-full bg-[#2a2d3a] overflow-hidden">
                    <div
                      className="h-full bg-indigo-500 rounded-full"
                      style={{ width: `${Math.round(rel.weight * 100)}%` }}
                    />
                  </div>
                  <span className="text-xs font-mono text-slate-500 w-8 text-right">
                    {rel.weight.toFixed(2)}
                  </span>
                </div>
              </div>
            ))
          )}
        </div>
      )}

      {tab === 'Raw JSON' && (
        <pre className="rounded-lg border border-[#2a2d3a] bg-[#0f1117] p-4 text-xs font-mono text-slate-400 overflow-auto max-h-[60vh]">
          {JSON.stringify(result, null, 2)}
        </pre>
      )}
    </div>
  );
}
