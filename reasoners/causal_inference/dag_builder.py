import networkx as nx
from typing import List, Dict, Any
import uuid

from reasoners.temporal_solvers.bayesian_chronology import BayesianChronology

class DAGBuilder:
    """
    Constructs a Causal Directed Acyclic Graph (DAG) from a collection of traces.
    """

    def __init__(self):
        self.graph = nx.DiGraph()

    def add_trace(self, trace: Dict[str, Any]):
        """
        Adds a trace as a node in the graph.
        """
        node_id = trace.get("id", str(uuid.uuid4()))
        self.graph.add_node(node_id, **trace)
        return node_id

    def build_causal_links(self):
        """
        Naively builds causal links based on temporal precedence.
        Uses BayesianChronology to normalize time.
        """
        nodes = list(self.graph.nodes(data=True))
        
        def get_ybp(node_data):
            ts = node_data.get("timestamp", {})
            return BayesianChronology.normalize_time(ts.get("value", 0), ts.get("unit", "BP"))

        # Sort by YBP descending (Oldest first)
        # Higher YBP = Older
        sorted_nodes = sorted(nodes, key=lambda x: get_ybp(x[1]), reverse=True)

        for i in range(len(sorted_nodes) - 1):
            source_id, source_data = sorted_nodes[i]
            target_id, target_data = sorted_nodes[i+1]
            
            # Simple rule: Earlier events cause later events
            self.graph.add_edge(source_id, target_id, weight=0.5, type="temporal_precedence")

    def get_graph(self) -> nx.DiGraph:
        return self.graph

    def export_graph_json(self) -> Dict[str, Any]:
        return nx.node_link_data(self.graph)
