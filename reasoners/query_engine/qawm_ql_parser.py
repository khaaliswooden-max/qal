"""QAWM-QL Parser.

Parses YAML-based QAWM Query Language (QAWM-QL) queries.
Supports: RECONSTRUCT, COMPARE, COUNTERFACTUAL operations.
"""
import yaml
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from enum import Enum


class QueryType(Enum):
    """Supported QAWM-QL query types."""
    RECONSTRUCT = "RECONSTRUCT"
    COMPARE = "COMPARE"
    COUNTERFACTUAL = "COUNTERFACTUAL"


class OutputFormat(Enum):
    """Supported output formats."""
    NARRATIVE = "NARRATIVE"
    TIMELINE = "TIMELINE"
    GRAPH = "GRAPH"
    JSON = "JSON"


class InferenceThreshold(Enum):
    """Minimum confidence levels for outputs."""
    VERIFIED = "VERIFIED"
    PLAUSIBLE = "PLAUSIBLE"
    SPECULATIVE = "SPECULATIVE"


@dataclass
class TimeScale:
    """Represents a time range for reconstruction."""
    start: str
    end: Optional[str] = None


@dataclass
class Constraints:
    """Query constraints."""
    min_confidence: InferenceThreshold = InferenceThreshold.SPECULATIVE
    max_entropy: float = 1.0


@dataclass
class ReconstructQuery:
    """Parsed RECONSTRUCT query."""
    system: str
    scope: Optional[str] = None
    timescale: Optional[TimeScale] = None
    focus: Optional[str] = None
    constraints: Optional[Constraints] = None
    output: OutputFormat = OutputFormat.JSON
    layers: Optional[List[str]] = None
    resolution: Optional[str] = None
    inference_threshold: Optional[InferenceThreshold] = None


@dataclass
class CompareQuery:
    """Parsed COMPARE query."""
    systems: List[str]
    dimensions: List[str]
    timeframe: Optional[str] = None
    output: Optional[str] = None


@dataclass 
class CounterfactualQuery:
    """Parsed COUNTERFACTUAL query."""
    system: str
    intervention: str
    timeframe: Optional[str] = None
    propagate_effects: bool = True
    output: Optional[str] = None


class QAWMQLParser:
    """
    Parser for QAWM Query Language (QAWM-QL).
    
    QAWM-QL is a YAML-based query format for requesting historical reconstructions.
    """
    
    def parse(self, query_text: str) -> Dict[str, Any]:
        """
        Parse a QAWM-QL query string.
        
        Args:
            query_text: YAML-formatted query string
            
        Returns:
            Parsed query object
            
        Raises:
            ValueError: If query format is invalid
        """
        try:
            parsed = yaml.safe_load(query_text)
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML syntax: {e}")
        
        if not isinstance(parsed, dict):
            raise ValueError("Query must be a YAML dictionary")
        
        # Determine query type
        query_type = self._detect_query_type(parsed)
        
        if query_type == QueryType.RECONSTRUCT:
            return self._parse_reconstruct(parsed["RECONSTRUCT"])
        elif query_type == QueryType.COMPARE:
            return self._parse_compare(parsed["COMPARE"])
        elif query_type == QueryType.COUNTERFACTUAL:
            return self._parse_counterfactual(parsed["COUNTERFACTUAL"])
        else:
            raise ValueError(f"Unknown query type. Must be one of: RECONSTRUCT, COMPARE, COUNTERFACTUAL")
    
    def _detect_query_type(self, parsed: Dict) -> QueryType:
        """Detect the type of query from parsed YAML."""
        if "RECONSTRUCT" in parsed:
            return QueryType.RECONSTRUCT
        elif "COMPARE" in parsed:
            return QueryType.COMPARE
        elif "COUNTERFACTUAL" in parsed:
            return QueryType.COUNTERFACTUAL
        else:
            raise ValueError("Query must contain RECONSTRUCT, COMPARE, or COUNTERFACTUAL key")
    
    def _parse_reconstruct(self, data: Dict) -> ReconstructQuery:
        """Parse a RECONSTRUCT query."""
        if "system" not in data:
            raise ValueError("RECONSTRUCT query requires 'system' field")
        
        timescale = None
        if "timescale" in data:
            ts = data["timescale"]
            timescale = TimeScale(
                start=str(ts.get("start", "")),
                end=str(ts.get("end")) if ts.get("end") else None
            )
        
        constraints = None
        if "constraints" in data:
            c = data["constraints"]
            constraints = Constraints(
                min_confidence=InferenceThreshold(c.get("min_confidence", "SPECULATIVE")),
                max_entropy=float(c.get("max_entropy", 1.0))
            )
        
        output = OutputFormat.JSON
        if "output" in data:
            output = OutputFormat(data["output"])
        
        inference_threshold = None
        if "inference_threshold" in data:
            inference_threshold = InferenceThreshold(data["inference_threshold"])
        
        return ReconstructQuery(
            system=data["system"],
            scope=data.get("scope"),
            timescale=timescale,
            focus=data.get("focus"),
            constraints=constraints,
            output=output,
            layers=data.get("layers"),
            resolution=data.get("resolution"),
            inference_threshold=inference_threshold
        )
    
    def _parse_compare(self, data: Dict) -> CompareQuery:
        """Parse a COMPARE query."""
        if "systems" not in data:
            raise ValueError("COMPARE query requires 'systems' field")
        if "dimensions" not in data:
            raise ValueError("COMPARE query requires 'dimensions' field")
        
        return CompareQuery(
            systems=data["systems"],
            dimensions=data["dimensions"],
            timeframe=data.get("timeframe"),
            output=data.get("output")
        )
    
    def _parse_counterfactual(self, data: Dict) -> CounterfactualQuery:
        """Parse a COUNTERFACTUAL query."""
        if "system" not in data:
            raise ValueError("COUNTERFACTUAL query requires 'system' field")
        if "intervention" not in data:
            raise ValueError("COUNTERFACTUAL query requires 'intervention' field")
        
        return CounterfactualQuery(
            system=data["system"],
            intervention=data["intervention"],
            timeframe=data.get("timeframe"),
            propagate_effects=data.get("propagate_effects", True),
            output=data.get("output")
        )
    
    def parse_file(self, filepath: str) -> Dict[str, Any]:
        """
        Parse a QAWM-QL query from a file.
        
        Args:
            filepath: Path to YAML query file
            
        Returns:
            Parsed query object
        """
        with open(filepath, 'r') as f:
            return self.parse(f.read())


# Example usage and validation
if __name__ == "__main__":
    parser = QAWMQLParser()
    
    # Test RECONSTRUCT query
    reconstruct_query = """
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
"""
    
    result = parser.parse(reconstruct_query)
    print(f"Parsed RECONSTRUCT: {result}")
    
    # Test COMPARE query
    compare_query = """
COMPARE:
  systems: ["Italian_printers", "French_printers"]
  dimensions: ["temporal_dynamics", "network_structure"]
  timeframe: "1460 → 1490"
  output: "aligned_timeline + network_comparison"
"""
    
    result = parser.parse(compare_query)
    print(f"Parsed COMPARE: {result}")
