// TypeScript types mirroring qawm/core/types.py and qawm/core/models.py

export type Layer =
  | 'L0_PHYSICAL'
  | 'L1_BIOLOGICAL'
  | 'L2_CULTURAL'
  | 'L3_TECHNO_ECONOMIC'
  | 'L4_METASYSTEMIC';

export type Confidence = 'VERIFIED' | 'PLAUSIBLE' | 'SPECULATIVE';

export type RelationType =
  | 'INFLUENCES'
  | 'TRANSFORMS'
  | 'DEPENDS_ON'
  | 'EMERGES_FROM'
  | 'DESTROYS';

export interface TimeSpan {
  start?: string;
  end?: string;
}

export interface Entity {
  id: string;
  type: string;
  layer: Layer;
  attributes: Record<string, unknown>;
  timespan?: TimeSpan;
}

export interface Event {
  id: string;
  type: string;
  layer: Layer;
  timestamp: string;
  participants: string[];
  confidence: Confidence;
  evidence_refs: string[];
}

export interface Relation {
  source_id: string;
  target_id: string;
  type: RelationType;
  weight: number;
}

export interface WorldState {
  model_id: string;
  entities: Entity[];
  events: Event[];
  relations: Relation[];
}

// Request types mirroring api/models.py
export interface ReconstructRequest {
  system: string;
  timeframe?: string;
  layers?: Layer[];
}

export interface CompareRequest {
  systems: string[];
  dimensions: string[];
}

export interface CounterfactualRequest {
  system: string;
  intervention: Record<string, unknown>;
}

export type QueryMode = 'reconstruct' | 'compare' | 'counterfactual';
