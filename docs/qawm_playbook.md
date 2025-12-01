# QAWM User Playbook

## 1. Introduction

Welcome to the Quantum Archeological World Model (QAWM). This playbook guides you through reconstructing past states using the QAL infrastructure.

## 2. QAWM Query Language (QAWM-QL)

QAWM-QL is a YAML-based query format designed for QAL agents.

### Syntax

```yaml
RECONSTRUCT:
  system: [Target System Name]
  scope: [L0 | L1 | L2 | L3 | L4 | ALL]
  timescale: 
    start: [ISO Date / Era]
    end: [ISO Date / Era]
  focus: [Specific Theme or Question]
  constraints:
    min_confidence: [VERIFIED | PLAUSIBLE | SPECULATIVE]
    max_entropy: [0.0 - 1.0]
  output: [NARRATIVE | TIMELINE | GRAPH | JSON]
```

### Example Query

```yaml
RECONSTRUCT:
  system: "Late 21st Century Internet Architecture"
  scope: L3_TECHNO_ECONOMIC
  timescale:
    start: "2080-01-01"
    end: "2100-12-31"
  focus: "Protocol collapse and emergence of mesh networks"
  constraints:
    min_confidence: PLAUSIBLE
  output: NARRATIVE
```

## 3. Workflows

### Workflow A: Single-System Reconstruction

**Goal**: Reconstruct the history of a specific entity (e.g., a city, a codebase, a species).

1. **Ingest**: Load traces into `/traces/qawm_traces`.
2. **Parse**: Run `Information Substrate Analysis` to normalize data.
3. **Infer**: Execute `Causal Reconstruction` agent.
4. **Visualize**: Generate timeline and narrative.

### Workflow B: Multi-System Comparative Archeology

**Goal**: Compare two systems to find invariant laws of history.

1. **Select**: Choose System A and System B.
2. **Align**: Normalize timescales and entity definitions.
3. **Diff**: Run `Counterfactual Analysis` to see where they diverged.
4. **Synthesize**: Output a comparative report.

### Workflow C: Counterfactual Analysis

**Goal**: "What if?" scenarios.

1. **Branch**: Select a pivotal event in an existing model.
2. **Perturb**: Change the outcome of that event.
3. **Simulate**: Run the `Temporal Engine` forward to see cascading effects.

## 4. Interface

Use the CLI to interact with QAWM:

```bash
# Run a reconstruction
python -m qawm.cli reconstruct --query query.yaml

# Visualize a model
python -m qawm.cli visualize --model_id model_123 --format html
```
