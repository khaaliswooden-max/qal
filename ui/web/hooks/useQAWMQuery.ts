'use client';

import { useState } from 'react';
import * as api from '@/lib/api';
import type {
  WorldState,
  QueryMode,
  ReconstructRequest,
  CompareRequest,
  CounterfactualRequest,
} from '@/lib/types';

interface QueryState {
  result: WorldState | null;
  loading: boolean;
  error: string | null;
}

export function useQAWMQuery() {
  const [state, setState] = useState<QueryState>({
    result: null,
    loading: false,
    error: null,
  });

  async function submit(
    mode: QueryMode,
    payload: ReconstructRequest | CompareRequest | CounterfactualRequest
  ) {
    setState({ result: null, loading: true, error: null });
    try {
      let result: WorldState;
      if (mode === 'reconstruct') {
        result = await api.reconstruct(payload as ReconstructRequest);
      } else if (mode === 'compare') {
        result = await api.compare(payload as CompareRequest);
      } else {
        result = await api.counterfactual(payload as CounterfactualRequest);
      }
      setState({ result, loading: false, error: null });
    } catch (err) {
      setState({
        result: null,
        loading: false,
        error: err instanceof Error ? err.message : 'Unknown error',
      });
    }
  }

  return { ...state, submit };
}
