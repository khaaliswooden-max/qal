import networkx as nx
from typing import List, Optional
from datetime import datetime
from ..core.models import Event, Relation, RelationType

class CausalGraph:
    """
    A directed acyclic graph (DAG) representing the causal structure of history.
    Nodes are Events. Edges are Relations.
    """
    def __init__(self):
        self.graph = nx.DiGraph()
        self._ancestor_cache: dict = {}
        self._descendant_cache: dict = {}

    def _invalidate_cache(self):
        self._ancestor_cache.clear()
        self._descendant_cache.clear()

    def add_event(self, event: Event):
        """
        Adds an event to the graph.
        """
        self.graph.add_node(event.id, data=event)
        self._invalidate_cache()

    def add_relation(self, relation: Relation):
        """
        Adds a causal link between events.
        Enforces temporal consistency (Cause must precede Effect).
        """
        # Retrieve events to check timestamps
        source_node = self.graph.nodes.get(relation.source_id)
        target_node = self.graph.nodes.get(relation.target_id)

        if not source_node or not target_node:
            raise ValueError(f"Source or Target event not found in graph: {relation.source_id} -> {relation.target_id}")

        source_event: Event = source_node['data']
        target_event: Event = target_node['data']

        # Temporal check: Cause cannot be after Effect
        # Note: In some relativistic contexts or with low confidence timestamps, this might be fuzzy.
        # For v1.0, we enforce strict linear time.
        if source_event.timestamp > target_event.timestamp:
            raise ValueError(
                f"Temporal Paradox: Cause ({source_event.timestamp}) occurs after Effect ({target_event.timestamp})"
            )

        self.graph.add_edge(
            relation.source_id,
            relation.target_id,
            type=relation.type,
            weight=relation.weight
        )
        self._invalidate_cache()

    def get_ancestors(self, event_id: str) -> List[Event]:
        """
        Returns all events that causally influenced the given event.
        Results are cached; cache is invalidated on any graph mutation.
        """
        if event_id not in self._ancestor_cache:
            self._ancestor_cache[event_id] = [
                self.graph.nodes[nid]['data']
                for nid in nx.ancestors(self.graph, event_id)
            ]
        return self._ancestor_cache[event_id]

    def get_descendants(self, event_id: str) -> List[Event]:
        """
        Returns all events caused by the given event.
        Results are cached; cache is invalidated on any graph mutation.
        """
        if event_id not in self._descendant_cache:
            self._descendant_cache[event_id] = [
                self.graph.nodes[nid]['data']
                for nid in nx.descendants(self.graph, event_id)
            ]
        return self._descendant_cache[event_id]
    
    def check_consistency(self) -> bool:
        """
        Checks if the graph is a valid DAG (no cycles).
        """
        return nx.is_directed_acyclic_graph(self.graph)
