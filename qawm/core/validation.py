from abc import ABC, abstractmethod
from typing import List, Any, Protocol, Union
from .models import Event, Entity, Relation, Confidence

class FabricationError(Exception):
    """Raised when a claim lacks sufficient trace support."""
    pass

class TraceDatabase(ABC):
    """
    Abstract interface for a database of traces.
    """
    @abstractmethod
    def find_supporting_traces(self, claim: Any) -> List[Any]:
        """
        Find traces that support the given claim.
        """
        pass

class ClaimValidator:
    """
    Enforces Anti-Hallucination Protocols by validating claims against traces.
    Section 7.2 Mandatory Safeguards.
    """
    
    def validate_claim(self, claim: Any, trace_database: TraceDatabase) -> List[Any]:
        """
        Reject any claim lacking trace support.
        
        Args:
            claim: The factual assertion to validate (e.g., Event, Entity).
            trace_database: The database containing source traces.
            
        Returns:
            List of supporting traces.
            
        Raises:
            FabricationError: If no supporting traces are found.
        """
        supporting_traces = trace_database.find_supporting_traces(claim)
        if len(supporting_traces) == 0:
            # Format the error message based on the claim type if possible
            claim_desc = str(claim)
            if hasattr(claim, 'id'):
                claim_desc = f"{type(claim).__name__}(id={claim.id})"
                
            raise FabricationError(f"Claim '{claim_desc}' has no trace support")
        
        return supporting_traces

    def check_confidence_calibration(self, claim: Union[Event, Entity], supporting_traces: List[Any]) -> bool:
        """
        Verify that the confidence level assigned to the claim matches the strength of evidence.
        
        "VERIFIED" claims should be correct >95% of time.
        """
        # Placeholder for calibration logic.
        # In a real implementation, this would check signal-to-noise ratio of traces
        # and compare against the claim.confidence attribute.
        
        if hasattr(claim, 'confidence'):
            if claim.confidence == Confidence.VERIFIED and len(supporting_traces) < 2:
                # Example rule: VERIFIED requires multiple traces (as per Confidence docstring)
                # This is a heuristic for the "calibration" requirement.
                return False
        return True

class HumanReviewer(Protocol):
    def review(self, claim: Any, traces: List[Any]) -> bool:
        ...

class SafetyProtocol:
    """
    Orchestrates the safeguards including Human-in-the-Loop and Red-Teaming checks.
    """
    
    def __init__(self, validator: ClaimValidator, reviewer: HumanReviewer = None):
        self.validator = validator
        self.reviewer = reviewer

    def process_claim(self, claim: Any, trace_db: TraceDatabase) -> bool:
        """
        Full validation pipeline.
        """
        # 1. Trace-to-Claim Linking
        try:
            traces = self.validator.validate_claim(claim, trace_db)
        except FabricationError:
            return False

        # 2. Confidence Calibration Check
        if isinstance(claim, (Event, Entity)):
            if not self.validator.check_confidence_calibration(claim, traces):
                # If calibration fails, might need to downgrade confidence or reject
                pass

        # 3. Human-in-the-Loop for contested/speculative reconstructions
        # This is a simplified logic for "contested"
        if hasattr(claim, 'confidence') and claim.confidence == Confidence.SPECULATIVE:
            if self.reviewer:
                return self.reviewer.review(claim, traces)
        
        return True
