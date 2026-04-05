'use client';

import { useMemo, useState, useRef } from 'react';
import type { WorldState, Layer, Confidence } from '@/lib/types';
import { LayerTag } from './ui/LayerTag';
import { Badge } from './ui/Badge';

const LAYERS: Layer[] = [
  'L0_PHYSICAL',
  'L1_BIOLOGICAL',
  'L2_CULTURAL',
  'L3_TECHNO_ECONOMIC',
  'L4_METASYSTEMIC',
];

const LAYER_FULL_NAMES: Record<Layer, string> = {
  L0_PHYSICAL: 'Physical Layer — L0',
  L1_BIOLOGICAL: 'Biological Layer — L1',
  L2_CULTURAL: 'Cultural Layer — L2',
  L3_TECHNO_ECONOMIC: 'Techno-Economic Layer — L3',
  L4_METASYSTEMIC: 'Metasystemic Layer — L4',
};

const CONFIDENCE_SUPERSCRIPT_COLORS: Record<Confidence, string> = {
  VERIFIED: '#22c55e',
  PLAUSIBLE: '#f59e0b',
  SPECULATIVE: '#ef4444',
};

interface FootnoteEntry {
  index: number;
  confidence: Confidence;
  evidenceRefs: string[];
}

interface EventEntry {
  type: string;
  confidence: Confidence;
  footnoteIndex: number;
}

interface LayerSection {
  layer: Layer;
  entityCount: number;
  entityTypes: string[];
  events: EventEntry[];
}

interface NarrativeDoc {
  intro: string;
  layerSections: LayerSection[];
  topRelations: string[];
  footnotes: FootnoteEntry[];
  plainText: string;
}

function generateNarrative(ws: WorldState): NarrativeDoc {
  const footnotes: FootnoteEntry[] = [];
  let fnCounter = 1;
  const fnMap = new Map<string, number>();

  function footnoteFor(confidence: Confidence, refs: string[]): number {
    const key = `${confidence}|${refs.join(',')}`;
    if (!fnMap.has(key)) {
      fnMap.set(key, fnCounter);
      footnotes.push({ index: fnCounter, confidence, evidenceRefs: refs });
      fnCounter++;
    }
    return fnMap.get(key)!;
  }

  // Confidence counts
  const verified = ws.events.filter((e) => e.confidence === 'VERIFIED').length;
  const plausible = ws.events.filter(
    (e) => e.confidence === 'PLAUSIBLE'
  ).length;
  const speculative = ws.events.filter(
    (e) => e.confidence === 'SPECULATIVE'
  ).length;

  // Timespan
  const parsedDates = ws.events
    .map((e) => new Date(e.timestamp))
    .filter((d) => !isNaN(d.getTime()))
    .map((d) => d.getFullYear());

  const timespanStr =
    parsedDates.length >= 2
      ? ` spanning ${Math.min(...parsedDates)} to ${Math.max(...parsedDates)}`
      : '';

  const layerSet = new Set([
    ...ws.entities.map((e) => e.layer),
    ...ws.events.map((e) => e.layer),
  ]);

  const intro =
    `The world state model \u201c${ws.model_id}\u201d encompasses ` +
    `${ws.entities.length} ${ws.entities.length === 1 ? 'entity' : 'entities'}, ` +
    `${ws.events.length} ${ws.events.length === 1 ? 'event' : 'events'}, and ` +
    `${ws.relations.length} causal ` +
    `${ws.relations.length === 1 ? 'relation' : 'relations'} distributed across ` +
    `${layerSet.size} ontological ` +
    `${layerSet.size === 1 ? 'layer' : 'layers'}${timespanStr}. ` +
    `Of the recorded events, ${verified} ` +
    `${verified === 1 ? 'is' : 'are'} empirically verified, ` +
    `${plausible} assessed as plausible, and ` +
    `${speculative} remain${speculative === 1 ? 's' : ''} speculative.`;

  // Layer sections
  const layerSections: LayerSection[] = LAYERS.filter(
    (layer) =>
      ws.entities.some((e) => e.layer === layer) ||
      ws.events.some((e) => e.layer === layer)
  ).map((layer) => {
    const layerEntities = ws.entities.filter((e) => e.layer === layer);
    const layerEvents = ws.events.filter((e) => e.layer === layer);
    const entityTypes = [...new Set(layerEntities.map((e) => e.type))];
    return {
      layer,
      entityCount: layerEntities.length,
      entityTypes,
      events: layerEvents.map((ev) => ({
        type: ev.type,
        confidence: ev.confidence,
        footnoteIndex: footnoteFor(ev.confidence, ev.evidence_refs),
      })),
    };
  });

  // Top relations by weight
  const topRelations = [...ws.relations]
    .sort((a, b) => b.weight - a.weight)
    .slice(0, 5)
    .map(
      (rel) =>
        `${rel.source_id} \u2192 ${rel.type.replace(/_/g, ' ')} \u2192 ${rel.target_id} (weight: ${rel.weight.toFixed(2)})`
    );

  // Plain text
  const lines: string[] = [
    'QAWM World State Narrative',
    `Model: ${ws.model_id}`,
    `Generated: ${new Date().toISOString()}`,
    '',
    intro,
    '',
  ];
  for (const s of layerSections) {
    lines.push(`--- ${LAYER_FULL_NAMES[s.layer]} ---`);
    if (s.entityTypes.length > 0)
      lines.push(`Entities (${s.entityCount}): ${s.entityTypes.join(', ')}`);
    if (s.events.length > 0)
      lines.push(
        `Events: ${s.events.map((e) => `${e.type} [${e.confidence}]`).join('; ')}`
      );
    lines.push('');
  }
  if (topRelations.length > 0) {
    lines.push('--- Causal Relations ---');
    for (const r of topRelations) lines.push(`  \u2022 ${r}`);
    lines.push('');
  }
  lines.push('--- Epistemic Footnotes ---');
  for (const fn of footnotes) {
    const refs =
      fn.evidenceRefs.length > 0
        ? ` Evidence: ${fn.evidenceRefs.join(', ')}`
        : '';
    lines.push(`[${fn.index}] ${fn.confidence}.${refs}`);
  }

  return {
    intro,
    layerSections,
    topRelations,
    footnotes,
    plainText: lines.join('\n'),
  };
}

export function NarrativeGenerator({
  worldState,
}: {
  worldState: WorldState;
}) {
  // eslint-disable-next-line react-hooks/exhaustive-deps
  const doc = useMemo(() => generateNarrative(worldState), [worldState.model_id]);
  const [copied, setCopied] = useState(false);
  const anchorRef = useRef<HTMLAnchorElement>(null);

  function handleCopy() {
    navigator.clipboard.writeText(doc.plainText).then(() => {
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    });
  }

  function handleDownload() {
    const blob = new Blob([doc.plainText], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = anchorRef.current!;
    a.href = url;
    a.download = `qawm-${worldState.model_id}.txt`;
    a.click();
    URL.revokeObjectURL(url);
  }

  return (
    <div>
      {/* Export toolbar */}
      <div className="sticky top-0 z-10 flex items-center justify-between bg-[#0f1117] border-b border-[#2a2d3a] py-3 mb-8">
        <div>
          <p className="text-xs font-mono text-slate-500">model_id</p>
          <p className="text-sm font-mono text-indigo-400 mt-0.5">
            {worldState.model_id}
          </p>
        </div>
        <div className="flex items-center gap-2">
          <button
            onClick={handleCopy}
            className="text-xs px-3 py-1.5 rounded border border-[#2a2d3a] text-slate-400 hover:text-slate-200 hover:border-[#3a3d4a] transition-colors font-mono"
          >
            {copied ? '\u2713 Copied' : 'Copy'}
          </button>
          <button
            onClick={handleDownload}
            className="text-xs px-3 py-1.5 rounded border border-[#2a2d3a] text-slate-400 hover:text-slate-200 hover:border-[#3a3d4a] transition-colors font-mono"
          >
            Download .txt
          </button>
          <a ref={anchorRef} className="hidden" aria-hidden />
        </div>
      </div>

      {/* Article */}
      <article className="max-w-3xl mx-auto pb-24 space-y-10">
        {/* Intro */}
        <section>
          <p className="text-[15px] text-slate-300 leading-8">{doc.intro}</p>
        </section>

        {/* Layer sections */}
        {doc.layerSections.map((section) => (
          <section key={section.layer} className="space-y-3">
            <h2 className="flex items-center gap-2.5 text-base font-semibold text-slate-100">
              <LayerTag layer={section.layer} />
              <span>{LAYER_FULL_NAMES[section.layer]}</span>
            </h2>

            {section.entityCount > 0 && (
              <p className="text-[14px] text-slate-400 leading-7">
                This layer contains{' '}
                <span className="text-slate-200 font-medium">
                  {section.entityCount}{' '}
                  {section.entityCount === 1 ? 'entity' : 'entities'}
                </span>
                {section.entityTypes.length > 0 && (
                  <>
                    {' '}of type
                    {section.entityTypes.length !== 1 ? 's' : ''}{' '}
                    <span className="font-mono text-slate-300">
                      {section.entityTypes.join(', ')}
                    </span>
                  </>
                )}
                .
              </p>
            )}

            {section.events.length > 0 && (
              <p className="text-[14px] text-slate-400 leading-7">
                Key events include:{' '}
                {section.events.map((ev, i) => (
                  <span key={i}>
                    {i > 0 && <span className="text-slate-600">; </span>}
                    <span className="text-slate-300">{ev.type}</span>
                    <sup
                      className="text-[10px] ml-0.5 cursor-help"
                      title={`[${ev.footnoteIndex}] ${ev.confidence}`}
                      style={{
                        color:
                          CONFIDENCE_SUPERSCRIPT_COLORS[ev.confidence],
                      }}
                    >
                      [{ev.footnoteIndex}]
                    </sup>
                  </span>
                ))}
                .
              </p>
            )}
          </section>
        ))}

        {/* Relations */}
        {doc.topRelations.length > 0 && (
          <section className="space-y-3">
            <h2 className="text-base font-semibold text-slate-100">
              Causal Relations
            </h2>
            <p className="text-[14px] text-slate-400 leading-7">
              The model records{' '}
              <span className="text-slate-200 font-medium">
                {worldState.relations.length} causal{' '}
                {worldState.relations.length === 1 ? 'relation' : 'relations'}
              </span>
              . Strongest by weight:
            </p>
            <ul className="space-y-2">
              {doc.topRelations.map((rel, i) => (
                <li
                  key={i}
                  className="flex items-start gap-2 text-xs font-mono text-slate-400"
                >
                  <span className="text-slate-700 shrink-0 mt-0.5">•</span>
                  <span>{rel}</span>
                </li>
              ))}
            </ul>
          </section>
        )}

        {/* Footnotes */}
        {doc.footnotes.length > 0 && (
          <footer className="border-t border-[#2a2d3a] pt-6 space-y-2">
            <h3 className="text-xs font-mono text-slate-600 uppercase tracking-wider mb-3">
              Epistemic Footnotes
            </h3>
            {doc.footnotes.map((fn) => (
              <div key={fn.index} className="flex items-start gap-3 text-xs font-mono">
                <span className="text-slate-600 shrink-0">[{fn.index}]</span>
                <span className="flex flex-wrap items-center gap-2">
                  <Badge confidence={fn.confidence} />
                  {fn.evidenceRefs.length > 0 && (
                    <span className="text-slate-600">
                      Evidence: {fn.evidenceRefs.join(', ')}
                    </span>
                  )}
                </span>
              </div>
            ))}
          </footer>
        )}
      </article>
    </div>
  );
}
