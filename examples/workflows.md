# QAWM Example Workflows

This document details specific workflows for the Quantum Archeological World Model (QAWM), demonstrating how to apply the framework to various reconstruction scenarios.

## Workflow 1: Archaeological Site Reconstruction

**Scenario**: Reconstruct social structure of ancient Indus Valley city (Harappa, ~2500 BCE)

### Inputs

* **Traces**: Archaeological site stratigraphy, artifact distributions, skeletal remains, isotope analyses
* **Layers**:
  * `L0` (geology)
  * `L1` (biological)
  * `L2` (cognitive/cultural)
  * `L3` (techno-economic)

### Process

1. **Substrate Analysis**: Ingest site data → normalize to entity schema (buildings, artifacts, individuals)
2. **Temporal Ordering**: Use stratigraphy + C-14 dates → Bayesian chronology
3. **Causal Inference**:
    * Artifact co-occurrence patterns → trade networks (`L3`)
    * Skeletal isotopes → diet/migration (`L1` → `L2`)
4. **Multi-Scenario Generation**: Ensemble of social structures (egalitarian vs. stratified)
5. **Ethical Review**: Ensure claims respect Indus Valley descendant communities

### Output

Narrative + graph + uncertainty map

### QAWM-QL Query

```yaml
RECONSTRUCT {
  system: "Harappa"
  timeframe: "2600 BCE → 2450 BCE"
  layers: ["L0", "L1", "L2", "L3"]
  resolution: "50 years"
  output: "narrative + graph"
  inference_threshold: "PLAUSIBLE"
}
```

---

## Workflow 2: Climate-Driven Extinction Event

**Scenario**: Reconstruct end-Permian mass extinction (~252 Ma)

### Inputs

* **Traces**: Geological strata, fossil distributions, geochemical proxies (carbon isotopes, mercury anomalies)
* **Layers**:
  * `L0` (volcanism, climate)
  * `L1` (extinction dynamics)

### Process

1. **Substrate Analysis**: Ingest geological data → volcanic eruption timeline, temperature proxies
2. **Causal Graph**: Siberian Traps volcanism (`L0`) → ocean anoxia (`L0`) → marine extinction (`L1`)
3. **Counterfactual**: "What if eruptions were 10x smaller?" → Reduce extinction severity
4. **Uncertainty Quantification**: Temperature estimates have ±5°C uncertainty; propagate through extinction model

### Output

Causal graph + timeline + counterfactual comparison

### QAWM-QL Query

```yaml
COUNTERFACTUAL {
  system: "Permian-Triassic Boundary"
  intervention: "scale_parameter('volcanic_CO2_flux', 0.1)"
  timeframe: "252.5 Ma → 251.5 Ma"
  propagate_effects: true
  output: "altered_timeline + divergence_points"
}
```

---

## Workflow 3: Technology Diffusion Analysis

**Scenario**: Trace the spread of printing press technology (1450-1500 CE)

### Inputs

* **Traces**: Incunabula (early printed books), printer locations, linguistic/trade networks
* **Layers**:
  * `L2` (human agents)
  * `L3` (technology)
  * `L4` (paradigm shift: manuscript → print)

### Process

1. **Substrate Analysis**: Map printer locations + dates → diffusion network
2. **Causal Inference**: Gutenberg (`L2`) → movable type (`L3`) → mass literacy (`L4`)
3. **Cross-Layer Validation**: Check if `L3` diffusion explains `L2` literacy data
4. **Scenario Ensemble**: Alternative routes of diffusion (e.g., via Italy vs. via France)

### Output

Network graph + timeline + likelihood-ranked scenarios

### QAWM-QL Query

```yaml
COMPARE {
  systems: ["Italian_printers", "French_printers"]
  dimensions: ["temporal_dynamics", "network_structure"]
  timeframe: "1460 → 1490"
  output: "aligned_timeline + network_comparison"
}
```
