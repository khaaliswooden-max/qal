import type { Layer } from '@/lib/types';

const labels: Record<Layer, string> = {
  L0_PHYSICAL: 'L0 Physical',
  L1_BIOLOGICAL: 'L1 Biological',
  L2_CULTURAL: 'L2 Cultural',
  L3_TECHNO_ECONOMIC: 'L3 Techno-Economic',
  L4_METASYSTEMIC: 'L4 Metasystemic',
};

const colors: Record<Layer, string> = {
  L0_PHYSICAL: 'bg-slate-800 text-slate-300 border-slate-600',
  L1_BIOLOGICAL: 'bg-emerald-900/40 text-emerald-400 border-emerald-700/50',
  L2_CULTURAL: 'bg-violet-900/40 text-violet-400 border-violet-700/50',
  L3_TECHNO_ECONOMIC: 'bg-blue-900/40 text-blue-400 border-blue-700/50',
  L4_METASYSTEMIC: 'bg-orange-900/40 text-orange-400 border-orange-700/50',
};

export function LayerTag({ layer }: { layer: Layer }) {
  return (
    <span
      className={`inline-flex items-center px-2 py-0.5 rounded text-xs font-mono border ${
        colors[layer]
      }`}
    >
      {labels[layer]}
    </span>
  );
}
