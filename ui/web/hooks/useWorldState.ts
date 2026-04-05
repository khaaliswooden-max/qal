'use client';

import { useContext } from 'react';
import { WorldStateContext } from '@/app/providers';

export function useWorldState() {
  const ctx = useContext(WorldStateContext);
  if (!ctx) throw new Error('useWorldState must be used inside WorldStateProvider');
  return ctx;
}
