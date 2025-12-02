import json
import os
import sys
import unittest
from datetime import datetime

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from reasoners.causal_inference.dag_builder import DAGBuilder
from reasoners.temporal_solvers.bayesian_chronology import BayesianChronology

class TestPhase1(unittest.TestCase):

    def setUp(self):
        self.trace_schema_path = os.path.join("traces", "schema.json")
        self.l0_schema_path = os.path.join("worldmodels", "layers", "L0_physical_cosmic", "entity_schema.json")

    def test_trace_schema_exists(self):
        self.assertTrue(os.path.exists(self.trace_schema_path))
        with open(self.trace_schema_path, 'r') as f:
            schema = json.load(f)
            self.assertIn("properties", schema)

    def test_dag_builder(self):
        builder = DAGBuilder()
        
        trace1 = {
            "id": "t1",
            "type": "carbon_14",
            "timestamp": {"value": 5000, "unit": "BP"},
            "data": {"raw_value": 123}
        }
        trace2 = {
            "id": "t2",
            "type": "textual_record",
            "timestamp": {"value": 2000, "unit": "BP"},
            "data": {"text": "Ancient text"}
        }
        
        builder.add_trace(trace1)
        builder.add_trace(trace2)
        builder.build_causal_links()
        
        graph = builder.get_graph()
        self.assertEqual(len(graph.nodes), 2)
        # t1 (5000 BP) is older than t2 (2000 BP), so t1 -> t2
        self.assertTrue(graph.has_edge("t1", "t2"))

    def test_bayesian_chronology(self):
        # Test normalization
        # 1000 BP = 1000 YBP
        self.assertEqual(BayesianChronology.normalize_time(1000, "BP"), 1000)
        # 1000 BC = 1000 + 1950 = 2950 YBP
        self.assertEqual(BayesianChronology.normalize_time(1000, "BC"), 2950)
        
        # Test probability
        t1 = {"value": 5000, "unit": "BP", "uncertainty": 100}
        t2 = {"value": 2000, "unit": "BP", "uncertainty": 100}
        
        # t1 is clearly older than t2
        prob = BayesianChronology.probability_precedes(t1, t2)
        self.assertGreater(prob, 0.99)

    def test_entity_schemas_exist(self):
        layers = [
            "L0_physical_cosmic",
            "L1_biological_ecological",
            "L2_cognitive_cultural",
            "L3_techno_economic",
            "L4_metasystemic"
        ]
        for layer in layers:
            path = os.path.join("worldmodels", "layers", layer, "entity_schema.json")
            self.assertTrue(os.path.exists(path), f"Schema for {layer} missing")

if __name__ == '__main__':
    unittest.main()
