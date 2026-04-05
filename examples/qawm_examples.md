# QAWM Examples Library

## Case 1: Human System (The Fall of the Bronze Age)

**Type**: L2_CULTURAL / L3_TECHNO_ECONOMIC
**Query**:

```yaml
RECONSTRUCT:
  system: "Eastern Mediterranean Civilization"
  timescale: { start: "1200 BCE", end: "1150 BCE" }
  focus: "Systems Collapse drivers"
  constraints: { min_confidence: PLAUSIBLE }
```

**Output Summary**:

- **Traces**: Linear B tablets, destruction layers in Mycenae, pollen data (drought).
- **Reconstruction**: Multi-causal feedback loop identified. Drought -> Famine -> Migration (Sea Peoples) -> Trade Network Collapse -> Palace Economy Failure.
- **Confidence**: High on destruction layers, Medium on specific migration routes.

## Case 2: Non-Human System (The Great Oxygenation Event)

**Type**: L0_PHYSICAL / L1_BIOLOGICAL
**Query**:

```yaml
RECONSTRUCT:
  system: "Planetary Atmosphere"
  timescale: { start: "2.4 Gya", end: "2.0 Gya" }
  focus: "Cyanobacteria impact on atmospheric composition"
```

**Output Summary**:

- **Traces**: Banded Iron Formations (BIFs), isotope fractionation.
- **Reconstruction**: Exponential growth of cyanobacteria -> Oxygen spike -> Mass extinction of anaerobes -> Huronian Glaciation.
- **Confidence**: Verified (Geological record).

## Case 3: Hybrid System (The 2020s AI Alignment Crisis)

**Type**: L3_TECHNO_ECONOMIC / L4_METASYSTEMIC
**Query**:

```yaml
RECONSTRUCT:
  system: "Global AI Ecosystem"
  timescale: { start: "2023", end: "2030" }
  focus: "Divergence between capability and alignment"
```

**Output Summary**:

- **Traces**: Arxiv papers, GPU cluster logs, regulatory texts, model weights.
- **Reconstruction**: Rapid capability overhang identified. Governance lag led to "The Pause" of 2026 (Counterfactual branch: "The Unchecked Takeoff").
- **Confidence**: Speculative (High entropy in digital traces).
