import type {
  ReconstructRequest,
  CompareRequest,
  CounterfactualRequest,
  WorldState,
} from './types';

const BASE_URL =
  process.env.NEXT_PUBLIC_QAWM_API_URL ?? 'http://localhost:8000';

async function post<T>(path: string, body: unknown): Promise<T> {
  const res = await fetch(`${BASE_URL}${path}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`QAWM API ${res.status}: ${text}`);
  }
  return res.json() as Promise<T>;
}

export function reconstruct(req: ReconstructRequest): Promise<WorldState> {
  return post<WorldState>('/reconstruct', req);
}

export function compare(req: CompareRequest): Promise<WorldState> {
  return post<WorldState>('/compare', req);
}

export function counterfactual(req: CounterfactualRequest): Promise<WorldState> {
  return post<WorldState>('/counterfactual', req);
}
