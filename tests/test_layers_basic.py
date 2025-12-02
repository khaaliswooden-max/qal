import sys
import os

# Add the project root to the python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from qawm.layers import (
    L0PhysicalLayer,
    L1BiologicalLayer,
    L2CognitiveCulturalLayer,
    L3TechnoEconomicLayer,
    L4MetasystemicLayer
)

def test_layers_instantiation():
    print("Testing L0PhysicalLayer...")
    l0 = L0PhysicalLayer()
    assert l0 is not None
    print("L0PhysicalLayer instantiated successfully.")

    print("Testing L1BiologicalLayer...")
    l1 = L1BiologicalLayer()
    assert l1 is not None
    print("L1BiologicalLayer instantiated successfully.")

    print("Testing L2CognitiveCulturalLayer...")
    l2 = L2CognitiveCulturalLayer()
    assert l2 is not None
    print("L2CognitiveCulturalLayer instantiated successfully.")

    print("Testing L3TechnoEconomicLayer...")
    l3 = L3TechnoEconomicLayer()
    assert l3 is not None
    print("L3TechnoEconomicLayer instantiated successfully.")

    print("Testing L4MetasystemicLayer...")
    l4 = L4MetasystemicLayer()
    assert l4 is not None
    print("L4MetasystemicLayer instantiated successfully.")

if __name__ == "__main__":
    test_layers_instantiation()
