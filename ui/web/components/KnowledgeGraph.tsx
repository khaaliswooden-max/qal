'use client';

import { useEffect, useRef, useState } from 'react';
import type { WorldState, Entity, Relation, Layer, RelationType } from '@/lib/types';
import { EntityCard } from './EntityCard';
import { Badge } from './ui/Badge';

const LAYER_COLORS: Record<Layer, string> = {
  L0_PHYSICAL: '#94a3b8',
  L1_BIOLOGICAL: '#4ade80',
  L2_CULTURAL: '#a78bfa',
  L3_TECHNO_ECONOMIC: '#60a5fa',
  L4_METASYSTEMIC: '#fb923c',
};

const RELATION_COLORS: Record<RelationType, string> = {
  INFLUENCES: '#6366f1',
  TRANSFORMS: '#f59e0b',
  DEPENDS_ON: '#22c55e',
  EMERGES_FROM: '#a78bfa',
  DESTROYS: '#ef4444',
};

interface SimNode {
  id: string;
  x: number;
  y: number;
  vx: number;
  vy: number;
  entity: Entity;
  connectionCount: number;
}

interface SimEdge {
  source: string;
  target: string;
  relation: Relation;
}

const SVG_W = 900;
const SVG_H = 560;

function runSimulation(
  nodes: SimNode[],
  edges: SimEdge[],
  ticks: number
): SimNode[] {
  const ns = nodes.map((n) => ({ ...n }));
  const nodeMap = new Map(ns.map((n) => [n.id, n]));

  const REPULSION = 4000;
  const SPRING_LENGTH = 130;
  const SPRING_K = 0.04;
  const CENTER_FORCE = 0.008;
  const DAMPING = 0.82;

  for (let t = 0; t < ticks; t++) {
    // Pairwise repulsion
    for (let i = 0; i < ns.length; i++) {
      for (let j = i + 1; j < ns.length; j++) {
        const a = ns[i], b = ns[j];
        const dx = b.x - a.x || 0.01;
        const dy = b.y - a.y || 0.01;
        const dist = Math.sqrt(dx * dx + dy * dy) || 1;
        const force = REPULSION / (dist * dist);
        const fx = (dx / dist) * force;
        const fy = (dy / dist) * force;
        a.vx -= fx;
        a.vy -= fy;
        b.vx += fx;
        b.vy += fy;
      }
    }

    // Spring attraction along edges
    for (const edge of edges) {
      const a = nodeMap.get(edge.source);
      const b = nodeMap.get(edge.target);
      if (!a || !b) continue;
      const dx = b.x - a.x;
      const dy = b.y - a.y;
      const dist = Math.sqrt(dx * dx + dy * dy) || 1;
      const displacement = dist - SPRING_LENGTH;
      const force = SPRING_K * displacement * (1 + edge.relation.weight);
      const fx = (dx / dist) * force;
      const fy = (dy / dist) * force;
      a.vx += fx;
      a.vy += fy;
      b.vx -= fx;
      b.vy -= fy;
    }

    // Center gravity
    const cx = SVG_W / 2, cy = SVG_H / 2;
    for (const n of ns) {
      n.vx += (cx - n.x) * CENTER_FORCE;
      n.vy += (cy - n.y) * CENTER_FORCE;
    }

    // Apply + damp + clamp
    for (const n of ns) {
      n.vx *= DAMPING;
      n.vy *= DAMPING;
      n.x = Math.max(24, Math.min(SVG_W - 24, n.x + n.vx));
      n.y = Math.max(24, Math.min(SVG_H - 24, n.y + n.vy));
    }
  }

  return ns;
}

interface TooltipState {
  x: number;
  y: number;
  entity: Entity;
}

export function KnowledgeGraph({ worldState }: { worldState: WorldState }) {
  const [nodes, setNodes] = useState<SimNode[]>([]);
  const [edges, setEdges] = useState<SimEdge[]>([]);
  const [selectedNode, setSelectedNode] = useState<SimNode | null>(null);
  const [tooltip, setTooltip] = useState<TooltipState | null>(null);
  const [zoom, setZoom] = useState(1);

  useEffect(() => {
    const { entities, relations } = worldState;
    if (entities.length === 0) return;

    const connCounts = new Map<string, number>();
    for (const rel of relations) {
      connCounts.set(rel.source_id, (connCounts.get(rel.source_id) ?? 0) + 1);
      connCounts.set(rel.target_id, (connCounts.get(rel.target_id) ?? 0) + 1);
    }

    const initNodes: SimNode[] = entities.map((entity) => ({
      id: entity.id,
      x: SVG_W / 2 + (Math.random() - 0.5) * 360,
      y: SVG_H / 2 + (Math.random() - 0.5) * 360,
      vx: 0,
      vy: 0,
      entity,
      connectionCount: connCounts.get(entity.id) ?? 0,
    }));

    const simEdges: SimEdge[] = relations.map((rel) => ({
      source: rel.source_id,
      target: rel.target_id,
      relation: rel,
    }));

    setNodes(runSimulation(initNodes, simEdges, 300));
    setEdges(simEdges);
    setSelectedNode(null);
  }, [worldState]);

  function handleWheel(e: React.WheelEvent) {
    e.preventDefault();
    setZoom((z) => Math.min(3, Math.max(0.3, z - e.deltaY * 0.001)));
  }

  const nodeMap = new Map(nodes.map((n) => [n.id, n]));

  const connectedEvents = selectedNode
    ? worldState.events.filter((ev) =>
        ev.participants.includes(selectedNode.id)
      )
    : [];

  return (
    <div className="flex gap-4 h-full">
      {/* Canvas */}
      <div
        className="flex-1 rounded-xl border border-[#2a2d3a] overflow-hidden relative"
        style={{ background: '#0a0c12', minHeight: 400 }}
      >
        {nodes.length === 0 ? (
          <div className="flex items-center justify-center h-full text-sm text-slate-600">
            No entities to visualize
          </div>
        ) : (
          <svg
            width="100%"
            height="100%"
            viewBox={`0 0 ${SVG_W} ${SVG_H}`}
            className="select-none"
            onWheel={handleWheel}
          >
            <g
              transform={`translate(${(SVG_W * (1 - zoom)) / 2} ${
                (SVG_H * (1 - zoom)) / 2
              }) scale(${zoom})`}
            >
              {/* Edges */}
              {edges.map((edge, i) => {
                const src = nodeMap.get(edge.source);
                const tgt = nodeMap.get(edge.target);
                if (!src || !tgt) return null;
                return (
                  <line
                    key={i}
                    x1={src.x}
                    y1={src.y}
                    x2={tgt.x}
                    y2={tgt.y}
                    stroke={RELATION_COLORS[edge.relation.type]}
                    strokeWidth={1 + edge.relation.weight * 3}
                    opacity={0.45}
                    strokeLinecap="round"
                  />
                );
              })}

              {/* Nodes */}
              {nodes.map((node) => {
                const isSelected = selectedNode?.id === node.id;
                const isDimmed =
                  selectedNode !== null && !isSelected;
                const color = LAYER_COLORS[node.entity.layer];
                const r = 6 + node.connectionCount * 1.5;
                return (
                  <circle
                    key={node.id}
                    cx={node.x}
                    cy={node.y}
                    r={r}
                    fill={color}
                    opacity={isDimmed ? 0.25 : 0.9}
                    className="cursor-pointer"
                    style={
                      isSelected
                        ? { filter: `drop-shadow(0 0 8px ${color})` }
                        : undefined
                    }
                    onClick={() =>
                      setSelectedNode(
                        isSelected ? null : node
                      )
                    }
                    onMouseEnter={(e) =>
                      setTooltip({
                        x: e.clientX,
                        y: e.clientY,
                        entity: node.entity,
                      })
                    }
                    onMouseLeave={() => setTooltip(null)}
                  />
                );
              })}
            </g>
          </svg>
        )}

        {/* Tooltip */}
        {tooltip && (
          <div
            className="fixed z-50 pointer-events-none bg-[#1a1d27] border border-[#2a2d3a] rounded-lg shadow-xl shadow-black/50 px-3 py-2"
            style={{ left: tooltip.x + 14, top: tooltip.y - 14 }}
          >
            <p className="text-xs font-mono text-slate-500 max-w-[180px] truncate">
              {tooltip.entity.id}
            </p>
            <p className="text-sm font-medium text-slate-200">
              {tooltip.entity.type}
            </p>
            <p className="text-xs text-slate-500 mt-0.5 font-mono">
              {tooltip.entity.layer.replace(/_/g, ' ')}
            </p>
          </div>
        )}

        {/* Legend */}
        <div className="absolute bottom-3 left-3 flex flex-wrap gap-x-4 gap-y-1.5 bg-[#0a0c12]/80 backdrop-blur rounded-lg px-3 py-2">
          <p className="w-full text-[10px] font-mono text-slate-600 uppercase tracking-wider mb-0.5">
            Layers
          </p>
          {(Object.entries(LAYER_COLORS) as [Layer, string][]).map(
            ([layer, color]) => (
              <div key={layer} className="flex items-center gap-1.5">
                <span
                  className="w-2 h-2 rounded-full shrink-0"
                  style={{ background: color }}
                />
                <span className="text-[10px] font-mono text-slate-500">
                  {layer.replace(/_/g, ' ')}
                </span>
              </div>
            )
          )}
          <p className="w-full text-[10px] font-mono text-slate-600 uppercase tracking-wider mt-1 mb-0.5">
            Relations
          </p>
          {(Object.entries(RELATION_COLORS) as [RelationType, string][]).map(
            ([type, color]) => (
              <div key={type} className="flex items-center gap-1.5">
                <span
                  className="w-4 h-0.5 shrink-0"
                  style={{ background: color }}
                />
                <span className="text-[10px] font-mono text-slate-500">
                  {type}
                </span>
              </div>
            )
          )}
        </div>

        {/* Zoom hint */}
        <div className="absolute top-3 right-3 text-[10px] font-mono text-slate-700">
          Scroll to zoom · click node to inspect
        </div>
      </div>

      {/* Side panel */}
      {selectedNode && (
        <div className="w-72 shrink-0 space-y-4 overflow-y-auto">
          <div className="flex items-center justify-between">
            <p className="text-xs font-mono text-slate-500 uppercase tracking-wider">
              Entity
            </p>
            <button
              onClick={() => setSelectedNode(null)}
              className="text-slate-600 hover:text-slate-300 transition-colors p-1"
              aria-label="Close panel"
            >
              <svg
                className="w-4 h-4"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M6 18L18 6M6 6l12 12"
                />
              </svg>
            </button>
          </div>

          <EntityCard entity={selectedNode.entity} />

          {connectedEvents.length > 0 && (
            <div>
              <p className="text-xs font-mono text-slate-500 uppercase tracking-wider mb-2">
                Connected Events ({connectedEvents.length})
              </p>
              <div className="space-y-2">
                {connectedEvents.map((ev) => (
                  <div
                    key={ev.id}
                    className="rounded-lg border border-[#2a2d3a] bg-[#1a1d27] p-3"
                  >
                    <div className="flex items-start justify-between gap-2">
                      <p className="text-xs text-slate-300 font-medium truncate">
                        {ev.type}
                      </p>
                      <Badge confidence={ev.confidence} />
                    </div>
                    <p className="text-xs font-mono text-slate-600 mt-1">
                      {ev.timestamp}
                    </p>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
