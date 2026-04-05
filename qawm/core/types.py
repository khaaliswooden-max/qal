from enum import Enum

class Layer(str, Enum):
    """
    The 5 Hierarchical Layers of Reality in QAWM.
    """
    L0_PHYSICAL = "L0_PHYSICAL"           # Raw matter, energy, entropy
    L1_BIOLOGICAL = "L1_BIOLOGICAL"       # Life, ecosystems, genetic info
    L2_CULTURAL = "L2_CULTURAL"           # Language, art, memes, rituals
    L3_TECHNO_ECONOMIC = "L3_TECHNO_ECONOMIC" # Markets, infrastructure, networks
    L4_METASYSTEMIC = "L4_METASYSTEMIC"   # Global systems, climate, geopolitics

class Confidence(str, Enum):
    """
    Epistemic Hygiene Labels.
    """
    VERIFIED = "VERIFIED"       # Supported by multiple independent substrates with high signal-to-noise.
    PLAUSIBLE = "PLAUSIBLE"     # Supported by at least one substrate; statistically likely.
    SPECULATIVE = "SPECULATIVE" # Inferred from gaps or weak signals; low probability but possible.

class RelationType(str, Enum):
    """
    Causal interaction types.
    """
    INFLUENCES = "INFLUENCES"
    TRANSFORMS = "TRANSFORMS"
    DEPENDS_ON = "DEPENDS_ON"
    EMERGES_FROM = "EMERGES_FROM"
    DESTROYS = "DESTROYS"
