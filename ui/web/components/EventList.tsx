import type { Event, Confidence } from '@/lib/types';
import { Badge } from './ui/Badge';
import { LayerTag } from './ui/LayerTag';

const confidenceOrder: Record<Confidence, number> = {
  VERIFIED: 0,
  PLAUSIBLE: 1,
  SPECULATIVE: 2,
};

interface EventListProps {
  events: Event[];
  minConfidence?: Confidence;
}

export function EventList({ events, minConfidence }: EventListProps) {
  const filtered = minConfidence
    ? events.filter(
        (e) => confidenceOrder[e.confidence] <= confidenceOrder[minConfidence]
      )
    : events;

  const sorted = [...filtered].sort(
    (a, b) => new Date(a.timestamp).getTime() - new Date(b.timestamp).getTime()
  );

  if (sorted.length === 0) {
    return (
      <p className="text-sm text-slate-500 py-8 text-center">
        No events match the current filter.
      </p>
    );
  }

  return (
    <ul className="space-y-2">
      {sorted.map((event) => (
        <li
          key={event.id}
          className="rounded-lg border border-[#2a2d3a] bg-[#1a1d27] p-3"
        >
          <div className="flex items-start justify-between gap-2">
            <div className="min-w-0">
              <p className="font-mono text-xs text-slate-500 truncate">
                {event.id}
              </p>
              <p className="text-sm font-medium text-slate-200 mt-0.5 truncate">
                {event.type}
              </p>
            </div>
            <div className="flex items-center gap-2 shrink-0">
              <LayerTag layer={event.layer} />
              <Badge confidence={event.confidence} />
            </div>
          </div>
          <div className="mt-2 flex flex-wrap items-center gap-3 text-xs text-slate-500 font-mono">
            <span>{new Date(event.timestamp).toISOString().slice(0, 10)}</span>
            {event.evidence_refs.length > 0 && (
              <span>
                {event.evidence_refs.length} evidence ref
                {event.evidence_refs.length !== 1 ? 's' : ''}
              </span>
            )}
            {event.participants.length > 0 && (
              <span>
                {event.participants.length} participant
                {event.participants.length !== 1 ? 's' : ''}
              </span>
            )}
          </div>
        </li>
      ))}
    </ul>
  );
}
