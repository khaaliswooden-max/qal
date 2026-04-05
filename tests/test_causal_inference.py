import pytest
import networkx as nx
from datetime import datetime, timedelta
from qawm.inference import dag_builder
from qawm.core.models import Event

# Mock Trace object
class MockTrace:
    def __init__(self, id, timestamp):
        self.id = id
        self.timestamp = timestamp

def generate_test_traces():
    base_time = datetime(2023, 1, 1)
    return [
        MockTrace(id=f"trace_{i}", timestamp=base_time + timedelta(days=i))
        for i in range(5)
    ]

def generate_test_dag():
    # Helper to generate a DAG directly for testing temporal consistency
    # We can use dag_builder or build one manually
    traces = generate_test_traces()
    return dag_builder.infer_causal_dag(traces)

def test_dag_builder_acyclicity():
    traces = generate_test_traces()
    dag = dag_builder.infer_causal_dag(traces)
    assert nx.is_directed_acyclic_graph(dag), "DAG contains cycles"

def test_temporal_consistency():
    dag = generate_test_dag()
    for u, v in dag.edges:
        # nodes in dag are keyed by event id, data is in 'data' attribute
        cause = dag.nodes[u]['data']
        effect = dag.nodes[v]['data']
        assert cause.timestamp < effect.timestamp, "Cause must precede effect"
