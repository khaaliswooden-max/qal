'use client';

import { useState, useMemo } from 'react';
import type { WorldState, Layer, Confidence, Event } from '@/lib/types';
import { Badge } from './ui/Badge';

const LAYERS: Layer[] = [
  'L0_PHYSICAL',
  'L1_BIOLOGICAL',
  'L2_CULTURAL',
  'L3_TECHNO_ECONOMIC',
  'L4_METASYSTEMIC',
];

const LAYER_LABELS: Record<Layer, string> = {
  L0_PHYSICAL: 'Physical',
  L1_BIOLOGICAL: 'Biological',
  L2_CULTURAL: 'Cultural',
  L3_TECHNO_ECONOMIC: 'Techno-Econ',
  L4_METASYSTEMIC: 'Metasystemic',
};

const CONFIDENCE_COLORS: Record<Confidence, string> = {
  VERIFIED: '#22c55e',
  PLAUSIBLE: '#f59e0b',
  SPECULATIVE: '#ef4444',
};

const TRACK_HEIGHT = 80;
const LABEL_WIDTH = 110;
const AXIS_HEIGHT = 32;
const PAD_RIGHT = 12;
const SVG_W = 900;

function parseTimestamp(ts: string): number {
  const d = new Date(ts);
  if (!isNaN(d.getTime())) return d.getTime();
  const year = parseInt(ts, 10);
  if (!isNaN(year)) return year;
  return 0;
}

function formatTick(value: number, isMs: boolean): string {
  if (isMs) return new Date(value).getFullYear().toString();
  return value.toString();
}

interface TooltipState {
  x: number;
  y: number;
  event: Event;
}

export function MultiLayerTimeline({ worldState }: { worldState: WorldState }) {
  const [filter, setFilter] = useState<Set<Confidence>>(
    new Set(['VERIFIED', 'PLAUSIBLE', 'SPECULATIVE'])
  );
  const [hoveredId, setHoveredId] = useState<string | null>(null);
  const [tooltip, setTooltip] = useState<TooltipState | null>(null);

  const totalHeight = LAYERS.length * TRACK_HEIGHT + AXIS_HEIGHT;

  const filteredEvents = useMemo(
    () => worldState.events.filter((ev) => filter.has(ev.confidence)),
    [worldState.events, filter]
  );

  const { timestamps, xMin, xMax, isMs } = useMemo(() => {
    const raw = filteredEvents.map((ev) => parseTimestamp(ev.timestamp));
    // Heuristic: if any value > 1e10, treat all as milliseconds
    const isMsMode = raw.some((v) => v > 1e10);
    const xMin = raw.length > 0 ? Math.min(...raw) : 0;
    const xMax = raw.length > 0 ? Math.max(...raw) : 1;
    return { timestamps: raw, xMin, xMax, isMs: isMsMode };
  }, [filteredEvents]);

  function xScale(value: number): number {
    const usable = SVG_W - LABEL_WIDTH - PAD_RIGHT;
    if (xMax === xMin) return LABEL_WIDTH + usable / 2;
    return LABEL_WIDTH + ((value - xMin) / (xMax - xMin)) * usable;
  }

  const ticks = useMemo(() => {
    const count = 5;
    return Array.from({ length: count }, (_, i) =>
      xMin + (i / (count - 1)) * (xMax - xMin)
    );
  }, [xMin, xMax]);

  function toggleConfidence(c: Confidence) {
    setFilter((prev) => {
      const next = new Set(prev);
      if (next.has(c) && next.size > 1) next.delete(c);
      else next.add(c);
      return next;
    });
  }

  const hoveredEvent = hoveredId
    ? worldState.events.find((e) => e.id === hoveredId)
    : null;

  return (
    <div className="space-y-4">
      {/* Confidence filter */}
      <div className="flex flex-wrap items-center gap-2">
        <span className="text-xs font-mono text-slate-500 mr-1">Show:</span>
        {(['VERIFIED', 'PLAUSIBLE', 'SPECULATIVE'] as Confidence[]).map((c) => (
          <button
            key={c}
            onClick={() => toggleConfidence(c)}
            className="text-xs px-2.5 py-1 rounded font-mono transition-colors border"
            style={
              filter.has(c)
                ? {
                    background: CONFIDENCE_COLORS[c] + '22',
                    borderColor: CONFIDENCE_COLORS[c] + '88',
                    color: CONFIDENCE_COLORS[c],
                  }
                : { borderColor: '#2a2d3a', color: '#475569' }
            }
          >
            {c}
          </button>
        ))}
        <span className="ml-auto text-xs font-mono text-slate-600">
          {filteredEvents.length} event
          {filteredEvents.length !== 1 ? 's' : ''}
        </span>
      </div>

      {/* SVG timeline */}
      <div className="rounded-xl border border-[#2a2d3a] overflow-hidden bg-[#0f1117]">
        <svg
          width="100%"
          height={totalHeight}
          viewBox={`0 0 ${SVG_W} ${totalHeight}`}
          className="block"
        >
          {/* Track bands */}
          {LAYERS.map((layer, i) => (
            <rect
              key={`band-${layer}`}
              x={0}
              y={i * TRACK_HEIGHT}
              width={SVG_W}
              height={TRACK_HEIGHT}
              fill={
                i % 2 === 0 ? 'rgba(26,29,39,0.5)' : 'transparent'
              }
            />
          ))}

          {/* Track baselines */}
          {LAYERS.map((layer, i) => (
            <line
              key={`baseline-${layer}`}
              x1={LABEL_WIDTH}
              y1={i * TRACK_HEIGHT + TRACK_HEIGHT / 2}
              x2={SVG_W - PAD_RIGHT}
              y2={i * TRACK_HEIGHT + TRACK_HEIGHT / 2}
              stroke="#2a2d3a"
              strokeWidth={1}
            />
          ))}

          {/* Layer labels */}
          {LAYERS.map((layer, i) => (
            <text
              key={`label-${layer}`}
              x={8}
              y={i * TRACK_HEIGHT + TRACK_HEIGHT / 2 + 4}
              fontSize={10}
              fill="#64748b"
              fontFamily="monospace"
            >
              {LAYER_LABELS[layer]}
            </text>
          ))}

          {/* X-axis ticks */}
          {ticks.map((tick, i) => {
            const x = xScale(tick);
            return (
              <g key={i}>
                <line
                  x1={x}
                  y1={0}
                  x2={x}
                  y2={LAYERS.length * TRACK_HEIGHT}
                  stroke="#2a2d3a"
                  strokeWidth={1}
                  strokeDasharray="3,4"
                />
                <text
                  x={x}
                  y={LAYERS.length * TRACK_HEIGHT + 22}
                  textAnchor="middle"
                  fontSize={9}
                  fill="#475569"
                  fontFamily="monospace"
                >
                  {formatTick(tick, isMs)}
                </text>
              </g>
            );
          })}

          {/* Participant connection lines for hovered event */}
          {hoveredEvent &&
            worldState.events
              .filter(
                (e) =>
                  e.id !== hoveredEvent.id &&
                  e.participants.some((p) =>
                    hoveredEvent.participants.includes(p)
                  )
              )
              .map((ce, ci) => {
                const ceTs = parseTimestamp(ce.timestamp);
                const evTs = parseTimestamp(hoveredEvent.timestamp);
                const evLi = LAYERS.indexOf(hoveredEvent.layer);
                const ceLi = LAYERS.indexOf(ce.layer);
                if (evLi === -1 || ceLi === -1) return null;
                return (
                  <line
                    key={ci}
                    x1={xScale(evTs)}
                    y1={evLi * TRACK_HEIGHT + TRACK_HEIGHT / 2}
                    x2={xScale(ceTs)}
                    y2={ceLi * TRACK_HEIGHT + TRACK_HEIGHT / 2}
                    stroke="#6366f1"
                    strokeWidth={1}
                    opacity={0.4}
                    strokeDasharray="4,3"
                  />
                );
              })}

          {/* Event circles */}
          {filteredEvents.map((ev, i) => {
            const ts = timestamps[i];
            const layerIdx = LAYERS.indexOf(ev.layer);
            if (layerIdx === -1) return null;
            const cx = xScale(ts);
            const cy = layerIdx * TRACK_HEIGHT + TRACK_HEIGHT / 2;
            const isHovered = hoveredId === ev.id;
            return (
              <circle
                key={ev.id}
                cx={cx}
                cy={cy}
                r={isHovered ? 8 : 6}
                fill={CONFIDENCE_COLORS[ev.confidence]}
                opacity={isHovered ? 1 : 0.75}
                className="cursor-pointer"
                style={
                  isHovered
                    ? {
                        filter: `drop-shadow(0 0 6px ${
                          CONFIDENCE_COLORS[ev.confidence]
                        })`,
                      }
                    : undefined
                }
                onMouseEnter={(e) => {
                  setHoveredId(ev.id);
                  setTooltip({ x: e.clientX, y: e.clientY, event: ev });
                }}
                onMouseLeave={() => {
                  setHoveredId(null);
                  setTooltip(null);
                }}
              />
            );
          })}
        </svg>
      </div>

      {/* Tooltip */}
      {tooltip && (
        <div
          className="fixed z-50 pointer-events-none bg-[#1a1d27] border border-[#2a2d3a] rounded-lg shadow-xl shadow-black/50 px-3 py-2 space-y-1"
          style={{ left: tooltip.x + 14, top: tooltip.y - 14 }}
        >
          <p className="text-xs font-mono text-slate-500 max-w-[200px] truncate">
            {tooltip.event.id}
          </p>
          <p className="text-sm font-medium text-slate-200">
            {tooltip.event.type}
          </p>
          <div className="flex items-center gap-2">
            <Badge confidence={tooltip.event.confidence} />
            <span className="text-xs font-mono text-slate-500">
              {tooltip.event.timestamp}
            </span>
          </div>
          {tooltip.event.participants.length > 0 && (
            <p className="text-xs text-slate-500">
              {tooltip.event.participants.length} participant
              {tooltip.event.participants.length !== 1 ? 's' : ''}
            </p>
          )}
        </div>
      )}
    </div>
  );
}
