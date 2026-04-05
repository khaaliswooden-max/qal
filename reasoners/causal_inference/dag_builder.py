import networkx as nx
from typing import List, Dict, Any, Optional
import uuid
from concurrent.futures import ProcessPoolExecutor, as_completed
import os

from reasoners.temporal_solvers.bayesian_chronology import BayesianChronology


class DAGBuilder:
    """
    Constructs a Causal DAG from traces using probabilistic temporal reasoning.

    Previous implementation linked every consecutive trace with weight=0.5,
    producing a naive chain where all N events form a single causal sequence.
    This made every event an ancestor of every later event (wrong) and produced
    O(N) edge traversal for any ancestor/descendant query.

    This implementation:
    - Uses BayesianChronology.probability_precedes() for evidence-weighted edges
    - Applies a temporal window to limit connectivity to proximate events
    - Only adds edges where P(t1 precedes t2) >= min_causal_probability
    - Parallelizes pairwise comparison for large trace sets
    - Produces sparse, accurate graphs: O(n*k) edges where k << n
    """

    def __init__(
        self,
        min_causal_probability: float = 0.6,
        temporal_window_size: Optional[float] = None,
        parallel_threshold: int = 500,
    ):
        """
        Args:
            min_causal_probability: Minimum P(t1 precedes t2) to add an edge.
                0.5 = any directional evidence (same as coin flip baseline)
                0.6 = moderate confidence (default, eliminates most noise)
                0.8 = high-confidence edges only (sparse, conservative graph)
            temporal_window_size: Max YBP gap between connected traces.
                None = auto-detect as 5x mean inter-trace gap.
            parallel_threshold: Trace count above which parallel processing activates.
        """
        self.graph = nx.DiGraph()
        self.min_causal_probability = min_causal_probability
        self.temporal_window_size = temporal_window_size
        self.parallel_threshold = parallel_threshold
        self._sorted_nodes: Optional[List] = None

    def add_trace(self, trace: Dict[str, Any]) -> str:
        node_id = trace.get("id", str(uuid.uuid4()))
        self.graph.add_node(node_id, **trace)
        self._sorted_nodes = None  # Invalidate sort cache on mutation
        return node_id

    def _get_ybp(self, node_data: Dict[str, Any]) -> float:
        ts = node_data.get("timestamp", {})
        return BayesianChronology.normalize_time(ts.get("value", 0), ts.get("unit", "BP"))

    def _get_sorted_nodes(self) -> List:
        """Sort nodes by YBP descending (oldest first). Result is cached."""
        if self._sorted_nodes is None:
            nodes = list(self.graph.nodes(data=True))
            self._sorted_nodes = sorted(
                nodes, key=lambda x: self._get_ybp(x[1]), reverse=True
            )
        return self._sorted_nodes

    def build_causal_links(self):
        """
        Build probabilistic causal links between temporally proximate traces.

        Algorithm:
          1. Sort traces by YBP (oldest first) — O(n log n)
          2. Auto-detect temporal window from mean inter-trace gap
          3. For each trace, scan forward within the temporal window
          4. Add an edge only if P(precedes) >= min_causal_probability
          5. Set edge weight = actual causal probability (not hardcoded 0.5)

        Complexity: O(n * k) where k = mean traces per temporal window.
        For typical historical datasets k << n, yielding near-linear performance
        with accurate, sparse causal structure instead of a dense false chain.
        """
        sorted_nodes = self._get_sorted_nodes()
        n = len(sorted_nodes)
        if n < 2:
            return

        ybp_values = [self._get_ybp(data) for _, data in sorted_nodes]

        # Auto-detect window: 5x the mean inter-trace gap
        if self.temporal_window_size is None:
            total_span = ybp_values[0] - ybp_values[-1] if n > 1 else 1.0
            mean_gap = total_span / max(n - 1, 1)
            window = max(mean_gap * 5, 1.0)
        else:
            window = self.temporal_window_size

        if n >= self.parallel_threshold:
            self._build_links_parallel(sorted_nodes, ybp_values, window)
        else:
            self._build_links_sequential(sorted_nodes, ybp_values, window)

    def _build_links_sequential(self, sorted_nodes, ybp_values, window):
        """O(n * k) sequential build for small-to-medium trace sets."""
        n = len(sorted_nodes)

        for i in range(n - 1):
            source_id, source_data = sorted_nodes[i]
            source_ybp = ybp_values[i]
            source_ts = source_data.get("timestamp", {})

            for j in range(i + 1, n):
                target_id, target_data = sorted_nodes[j]
                target_ybp = ybp_values[j]

                # Exit inner loop once we're past the temporal window
                if source_ybp - target_ybp > window:
                    break

                target_ts = target_data.get("timestamp", {})
                prob = BayesianChronology.probability_precedes(source_ts, target_ts)

                if prob >= self.min_causal_probability:
                    self.graph.add_edge(
                        source_id,
                        target_id,
                        weight=prob,
                        type="temporal_precedence",
                        causal_probability=prob,
                    )

    def _build_links_parallel(self, sorted_nodes, ybp_values, window):
        """Parallel edge computation for large trace sets (>= parallel_threshold)."""
        n = len(sorted_nodes)
        cpu_count = os.cpu_count() or 4
        chunk_size = max(n // cpu_count, 50)

        # Extract only what's needed for pickling across process boundaries
        node_data = [
            (sorted_nodes[i][0], sorted_nodes[i][1].get("timestamp", {}), ybp_values[i])
            for i in range(n)
        ]

        edges_to_add = []
        with ProcessPoolExecutor(max_workers=cpu_count) as executor:
            futures = [
                executor.submit(
                    _compute_edges_for_chunk,
                    node_data,
                    chunk_start,
                    min(chunk_start + chunk_size, n),
                    window,
                    self.min_causal_probability,
                )
                for chunk_start in range(0, n, chunk_size)
            ]
            for future in as_completed(futures):
                edges_to_add.extend(future.result())

        for source_id, target_id, prob in edges_to_add:
            self.graph.add_edge(
                source_id,
                target_id,
                weight=prob,
                type="temporal_precedence",
                causal_probability=prob,
            )

    def get_graph(self) -> nx.DiGraph:
        return self.graph

    def export_graph_json(self) -> Dict[str, Any]:
        return nx.node_link_data(self.graph)

    def stats(self) -> Dict[str, Any]:
        """Graph statistics for benchmarking and debugging."""
        n = self.graph.number_of_nodes()
        e = self.graph.number_of_edges()
        return {
            "nodes": n,
            "edges": e,
            "density": e / max(n * (n - 1), 1),
            "avg_out_degree": e / max(n, 1),
        }


def _compute_edges_for_chunk(
    node_data: List,
    chunk_start: int,
    chunk_end: int,
    window: float,
    min_probability: float,
) -> List:
    """
    Module-level function for multiprocessing (must be picklable).
    Computes probabilistic edges for a slice of source nodes.
    """
    from reasoners.temporal_solvers.bayesian_chronology import BayesianChronology

    edges = []
    n = len(node_data)

    for i in range(chunk_start, chunk_end):
        source_id, source_ts, source_ybp = node_data[i]

        for j in range(i + 1, n):
            target_id, target_ts, target_ybp = node_data[j]

            if source_ybp - target_ybp > window:
                break

            prob = BayesianChronology.probability_precedes(source_ts, target_ts)
            if prob >= min_probability:
                edges.append((source_id, target_id, prob))

    return edges
