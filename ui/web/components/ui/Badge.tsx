import type { Confidence } from '@/lib/types';

const styles: Record<Confidence, string> = {
  VERIFIED: 'bg-green-900/40 text-green-400 border border-green-700/50',
  PLAUSIBLE: 'bg-amber-900/40 text-amber-400 border border-amber-700/50',
  SPECULATIVE: 'bg-red-900/40 text-red-400 border border-red-700/50',
};

export function Badge({ confidence }: { confidence: Confidence }) {
  return (
    <span
      className={`inline-flex items-center px-2 py-0.5 rounded text-xs font-mono ${
        styles[confidence]
      }`}
    >
      {confidence}
    </span>
  );
}
