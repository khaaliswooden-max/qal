'use client';

import { useState } from 'react';
import type {
  Layer,
  QueryMode,
  ReconstructRequest,
  CompareRequest,
  CounterfactualRequest,
} from '@/lib/types';
import { Button } from './ui/Button';

const LAYERS: Layer[] = [
  'L0_PHYSICAL',
  'L1_BIOLOGICAL',
  'L2_CULTURAL',
  'L3_TECHNO_ECONOMIC',
  'L4_METASYSTEMIC',
];

const LAYER_LABELS: Record<Layer, string> = {
  L0_PHYSICAL: 'L0 Physical — matter, energy, entropy',
  L1_BIOLOGICAL: 'L1 Biological — life, ecosystems, genetics',
  L2_CULTURAL: 'L2 Cultural — language, art, memes',
  L3_TECHNO_ECONOMIC: 'L3 Techno-Economic — markets, infrastructure',
  L4_METASYSTEMIC: 'L4 Metasystemic — climate, geopolitics',
};

const MODES: { id: QueryMode; label: string; description: string }[] = [
  {
    id: 'reconstruct',
    label: 'RECONSTRUCT',
    description: 'Rebuild the past state of a system from traces',
  },
  {
    id: 'compare',
    label: 'COMPARE',
    description: 'Contrast two or more systems across dimensions',
  },
  {
    id: 'counterfactual',
    label: 'COUNTERFACTUAL',
    description: 'Simulate an alternative timeline via an intervention',
  },
];

const inputCls =
  'w-full bg-[#0f1117] border border-[#2a2d3a] rounded-md px-3 py-2 text-sm text-slate-200 placeholder-slate-600 focus:outline-none focus:ring-1 focus:ring-indigo-500 transition-colors';

interface QueryBuilderProps {
  loading: boolean;
  onSubmit: (
    mode: QueryMode,
    payload: ReconstructRequest | CompareRequest | CounterfactualRequest
  ) => void;
}

export function QueryBuilder({ loading, onSubmit }: QueryBuilderProps) {
  const [mode, setMode] = useState<QueryMode>('reconstruct');

  // RECONSTRUCT
  const [system, setSystem] = useState('');
  const [timeframe, setTimeframe] = useState('');
  const [selectedLayers, setSelectedLayers] = useState<Layer[]>([]);

  // COMPARE
  const [systems, setSystems] = useState(['', '']);
  const [dimensions, setDimensions] = useState(['']);

  // COUNTERFACTUAL
  const [cfSystem, setCfSystem] = useState('');
  const [interventionKey, setInterventionKey] = useState('');
  const [interventionValue, setInterventionValue] = useState('');

  function toggleLayer(layer: Layer) {
    setSelectedLayers((prev) =>
      prev.includes(layer) ? prev.filter((l) => l !== layer) : [...prev, layer]
    );
  }

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (mode === 'reconstruct') {
      onSubmit('reconstruct', {
        system,
        timeframe: timeframe.trim() || undefined,
        layers: selectedLayers.length > 0 ? selectedLayers : undefined,
      });
    } else if (mode === 'compare') {
      onSubmit('compare', {
        systems: systems.filter(Boolean),
        dimensions: dimensions.filter(Boolean),
      });
    } else {
      const intervention: Record<string, unknown> = {};
      if (interventionKey.trim()) {
        intervention[interventionKey.trim()] = interventionValue.trim();
      }
      onSubmit('counterfactual', { system: cfSystem, intervention });
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-5">
      {/* Mode selector */}
      <div className="space-y-1">
        {MODES.map((m) => (
          <button
            key={m.id}
            type="button"
            onClick={() => setMode(m.id)}
            className={`w-full text-left px-3 py-2.5 rounded-md border transition-colors ${
              mode === m.id
                ? 'border-indigo-600 bg-indigo-600/10 text-indigo-300'
                : 'border-[#2a2d3a] text-slate-500 hover:text-slate-300 hover:border-[#3a3d4a]'
            }`}
          >
            <span className="block text-xs font-mono font-semibold">
              {m.label}
            </span>
            <span className="block text-xs mt-0.5 opacity-70">
              {m.description}
            </span>
          </button>
        ))}
      </div>

      <hr className="border-[#2a2d3a]" />

      {/* RECONSTRUCT fields */}
      {mode === 'reconstruct' && (
        <div className="space-y-4">
          <div>
            <label className="block text-xs font-medium text-slate-400 mb-1.5">
              System
            </label>
            <input
              type="text"
              value={system}
              onChange={(e) => setSystem(e.target.value)}
              placeholder="e.g. Bronze Age Collapse, Late Roman Empire"
              required
              className={inputCls}
            />
          </div>
          <div>
            <label className="block text-xs font-medium text-slate-400 mb-1.5">
              Timeframe
              <span className="ml-1 text-slate-600 font-normal">(optional)</span>
            </label>
            <input
              type="text"
              value={timeframe}
              onChange={(e) => setTimeframe(e.target.value)}
              placeholder="e.g. 1200–1150 BCE, 2080 to 2100"
              className={inputCls}
            />
          </div>
          <div>
            <label className="block text-xs font-medium text-slate-400 mb-2">
              Layers
              <span className="ml-1 text-slate-600 font-normal">(optional)</span>
            </label>
            <div className="space-y-1.5">
              {LAYERS.map((layer) => (
                <label
                  key={layer}
                  className="flex items-start gap-2.5 cursor-pointer group"
                >
                  <input
                    type="checkbox"
                    checked={selectedLayers.includes(layer)}
                    onChange={() => toggleLayer(layer)}
                    className="mt-0.5 w-3.5 h-3.5 rounded border-[#2a2d3a] bg-[#0f1117] accent-indigo-500 shrink-0"
                  />
                  <span className="text-xs font-mono text-slate-400 group-hover:text-slate-200 transition-colors leading-snug">
                    {LAYER_LABELS[layer]}
                  </span>
                </label>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* COMPARE fields */}
      {mode === 'compare' && (
        <div className="space-y-4">
          <div>
            <label className="block text-xs font-medium text-slate-400 mb-1.5">
              Systems
            </label>
            <div className="space-y-2">
              {systems.map((s, i) => (
                <input
                  key={i}
                  type="text"
                  value={s}
                  onChange={(e) => {
                    const next = [...systems];
                    next[i] = e.target.value;
                    setSystems(next);
                  }}
                  placeholder={`System ${i + 1}`}
                  className={inputCls}
                />
              ))}
              <button
                type="button"
                onClick={() => setSystems((prev) => [...prev, ''])}
                className="text-xs text-indigo-400 hover:text-indigo-300 font-mono transition-colors"
              >
                + Add system
              </button>
            </div>
          </div>
          <div>
            <label className="block text-xs font-medium text-slate-400 mb-1.5">
              Dimensions
            </label>
            <div className="space-y-2">
              {dimensions.map((d, i) => (
                <input
                  key={i}
                  type="text"
                  value={d}
                  onChange={(e) => {
                    const next = [...dimensions];
                    next[i] = e.target.value;
                    setDimensions(next);
                  }}
                  placeholder="e.g. trade networks, collapse triggers"
                  className={inputCls}
                />
              ))}
              <button
                type="button"
                onClick={() => setDimensions((prev) => [...prev, ''])}
                className="text-xs text-indigo-400 hover:text-indigo-300 font-mono transition-colors"
              >
                + Add dimension
              </button>
            </div>
          </div>
        </div>
      )}

      {/* COUNTERFACTUAL fields */}
      {mode === 'counterfactual' && (
        <div className="space-y-4">
          <div>
            <label className="block text-xs font-medium text-slate-400 mb-1.5">
              System
            </label>
            <input
              type="text"
              value={cfSystem}
              onChange={(e) => setCfSystem(e.target.value)}
              placeholder="e.g. Industrial Revolution"
              required
              className={inputCls}
            />
          </div>
          <div>
            <label className="block text-xs font-medium text-slate-400 mb-1.5">
              Intervention
              <span className="ml-1 text-slate-600 font-normal">
                (key / value)
              </span>
            </label>
            <div className="grid grid-cols-2 gap-2">
              <input
                type="text"
                value={interventionKey}
                onChange={(e) => setInterventionKey(e.target.value)}
                placeholder="Key (e.g. coal_access)"
                className={inputCls}
              />
              <input
                type="text"
                value={interventionValue}
                onChange={(e) => setInterventionValue(e.target.value)}
                placeholder="Value (e.g. false)"
                className={inputCls}
              />
            </div>
          </div>
        </div>
      )}

      <Button type="submit" loading={loading} className="w-full">
        Run Query
      </Button>
    </form>
  );
}
