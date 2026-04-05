'use client';

import {
  createContext,
  useContext,
  useState,
  useEffect,
  type ReactNode,
} from 'react';
import type { WorldState } from '@/lib/types';

const STORAGE_KEY = 'qawm_world_state';

interface WorldStateContextValue {
  worldState: WorldState | null;
  setWorldState: (ws: WorldState) => void;
}

export const WorldStateContext = createContext<WorldStateContextValue | null>(null);

export function WorldStateProvider({ children }: { children: ReactNode }) {
  const [worldState, setWorldStateRaw] = useState<WorldState | null>(null);

  // Hydrate from sessionStorage on client mount (never during SSR)
  useEffect(() => {
    try {
      const stored = sessionStorage.getItem(STORAGE_KEY);
      if (stored) {
        setWorldStateRaw(JSON.parse(stored) as WorldState);
      }
    } catch {
      // ignore malformed data
    }
  }, []);

  function setWorldState(ws: WorldState) {
    setWorldStateRaw(ws);
    try {
      sessionStorage.setItem(STORAGE_KEY, JSON.stringify(ws));
    } catch {
      // ignore storage quota errors
    }
  }

  return (
    <WorldStateContext.Provider value={{ worldState, setWorldState }}>
      {children}
    </WorldStateContext.Provider>
  );
}
