import type { Entity } from '@/lib/types';
import { LayerTag } from './ui/LayerTag';

export function EntityCard({ entity }: { entity: Entity }) {
  const attrEntries = Object.entries(entity.attributes);
  return (
    <div className="rounded-lg border border-[#2a2d3a] bg-[#1a1d27] p-4 space-y-2">
      <div className="flex items-start justify-between gap-2">
        <div className="min-w-0">
          <p className="font-mono text-xs text-slate-500 truncate">{entity.id}</p>
          <p className="text-sm font-medium text-slate-200 mt-0.5">{entity.type}</p>
        </div>
        <LayerTag layer={entity.layer} />
      </div>
      {entity.timespan && (
        <p className="text-xs text-slate-500 font-mono">
          {entity.timespan.start ?? '?'} → {entity.timespan.end ?? '?'}
        </p>
      )}
      {attrEntries.length > 0 && (
        <dl className="grid grid-cols-2 gap-x-4 gap-y-1 pt-1 border-t border-[#2a2d3a]">
          {attrEntries.map(([k, v]) => (
            <div key={k} className="contents">
              <dt className="text-xs text-slate-500 truncate">{k}</dt>
              <dd className="text-xs text-slate-300 truncate font-mono">{String(v)}</dd>
            </div>
          ))}
        </dl>
      )}
    </div>
  );
}
