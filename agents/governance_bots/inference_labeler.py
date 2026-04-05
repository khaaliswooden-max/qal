"""Inference Labeler.

Enforces QAWM Ethical Guardrail Principle #1: Transparency of Inference
"Every claim must be tagged with a confidence level (VERIFIED, PLAUSIBLE, SPECULATIVE)."

This governance agent:
1. Automatically labels claims based on evidence strength
2. Ensures all outputs have confidence tags
3. Flags claims missing inference levels
4. Validates label consistency
"""
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum


class InferenceLevel(Enum):
    """
    Epistemic Hygiene Labels per QAWM specification.
    
    VERIFIED: Supported by multiple independent substrates with high signal-to-noise.
              Should be correct >95% of the time.
              
    PLAUSIBLE: Supported by at least one substrate; statistically likely.
               Should be correct >70% of the time.
               
    SPECULATIVE: Inferred from gaps or weak signals; low probability but possible.
                 No minimum accuracy threshold, but must be clearly marked.
    """
    VERIFIED = "VERIFIED"
    PLAUSIBLE = "PLAUSIBLE"
    SPECULATIVE = "SPECULATIVE"


@dataclass
class LabelingResult:
    """Result of inference labeling."""
    claim_id: str
    original_label: Optional[InferenceLevel]
    assigned_label: InferenceLevel
    label_changed: bool
    reasoning: str
    evidence_count: int
    evidence_types: List[str]


class InferenceLabeler:
    """
    Governance agent that ensures all claims are properly labeled with confidence levels.
    
    Implements the transparency requirement: users must always know how confident
    the system is in any given claim.
    """
    
    def __init__(self):
        """Initialize the inference labeler with default thresholds."""
        # Minimum traces required for each level
        self.thresholds = {
            InferenceLevel.VERIFIED: {
                "min_traces": 2,
                "min_independent_types": 2,  # Multiple substrate types
                "min_confidence_avg": 0.8
            },
            InferenceLevel.PLAUSIBLE: {
                "min_traces": 1,
                "min_independent_types": 1,
                "min_confidence_avg": 0.5
            },
            InferenceLevel.SPECULATIVE: {
                "min_traces": 0,
                "min_independent_types": 0,
                "min_confidence_avg": 0.0
            }
        }
        
        self.labeling_log: List[LabelingResult] = []
    
    def compute_label(
        self, 
        claim: Dict[str, Any], 
        supporting_traces: List[Dict[str, Any]]
    ) -> Tuple[InferenceLevel, str]:
        """
        Compute the appropriate inference level for a claim.
        
        Args:
            claim: The claim to label
            supporting_traces: Traces supporting this claim
            
        Returns:
            Tuple of (assigned_level, reasoning)
        """
        trace_count = len(supporting_traces)
        
        if trace_count == 0:
            return (
                InferenceLevel.SPECULATIVE,
                "No supporting traces - speculative inference from context"
            )
        
        # Count unique trace types (for multi-substrate requirement)
        trace_types = set(t.get("type", "unknown") for t in supporting_traces)
        independent_types = len(trace_types)
        
        # Calculate average confidence of traces
        confidences = [t.get("confidence", 0.5) for t in supporting_traces]
        avg_confidence = sum(confidences) / len(confidences) if confidences else 0
        
        # Check VERIFIED threshold
        verified_req = self.thresholds[InferenceLevel.VERIFIED]
        if (trace_count >= verified_req["min_traces"] and
            independent_types >= verified_req["min_independent_types"] and
            avg_confidence >= verified_req["min_confidence_avg"]):
            return (
                InferenceLevel.VERIFIED,
                f"Supported by {trace_count} traces from {independent_types} "
                f"independent sources (avg confidence: {avg_confidence:.2f})"
            )
        
        # Check PLAUSIBLE threshold
        plausible_req = self.thresholds[InferenceLevel.PLAUSIBLE]
        if (trace_count >= plausible_req["min_traces"] and
            avg_confidence >= plausible_req["min_confidence_avg"]):
            return (
                InferenceLevel.PLAUSIBLE,
                f"Supported by {trace_count} trace(s) but insufficient for "
                f"VERIFIED status (avg confidence: {avg_confidence:.2f})"
            )
        
        # Default to SPECULATIVE
        return (
            InferenceLevel.SPECULATIVE,
            f"Weak evidence: {trace_count} trace(s), "
            f"avg confidence {avg_confidence:.2f}"
        )
    
    def label_claim(
        self, 
        claim: Dict[str, Any], 
        supporting_traces: List[Dict[str, Any]],
        force_relabel: bool = False
    ) -> LabelingResult:
        """
        Label a claim with appropriate inference level.
        
        Args:
            claim: The claim to label
            supporting_traces: Supporting evidence
            force_relabel: Whether to override existing label
            
        Returns:
            LabelingResult with assigned label and reasoning
        """
        claim_id = claim.get("id", "unknown")
        original_label = None
        
        # Check for existing label
        if "confidence" in claim:
            try:
                original_label = InferenceLevel(claim["confidence"])
            except ValueError:
                pass  # Invalid label, will be relabeled
        
        # Compute appropriate label
        assigned_label, reasoning = self.compute_label(claim, supporting_traces)
        
        # Determine if label needs to change
        label_changed = (
            force_relabel or 
            original_label is None or 
            original_label != assigned_label
        )
        
        # Get evidence metadata
        trace_types = list(set(t.get("type", "unknown") for t in supporting_traces))
        
        result = LabelingResult(
            claim_id=claim_id,
            original_label=original_label,
            assigned_label=assigned_label,
            label_changed=label_changed,
            reasoning=reasoning,
            evidence_count=len(supporting_traces),
            evidence_types=trace_types
        )
        
        self.labeling_log.append(result)
        return result
    
    def validate_labeling(self, claim: Dict[str, Any]) -> bool:
        """
        Check if a claim has a valid inference label.
        
        Returns:
            True if claim has valid label, False otherwise
        """
        if "confidence" not in claim:
            return False
        
        try:
            InferenceLevel(claim["confidence"])
            return True
        except ValueError:
            return False
    
    def audit_labels(
        self, 
        claims: List[Dict[str, Any]], 
        traces_by_claim: Dict[str, List[Dict[str, Any]]]
    ) -> Dict[str, Any]:
        """
        Audit all claims for proper labeling.
        
        Args:
            claims: All claims to audit
            traces_by_claim: Mapping of claim_id to supporting traces
            
        Returns:
            Audit report
        """
        missing_labels = []
        mismatched_labels = []
        properly_labeled = []
        
        for claim in claims:
            claim_id = claim.get("id", "unknown")
            traces = traces_by_claim.get(claim_id, [])
            
            # Check if labeled
            if not self.validate_labeling(claim):
                missing_labels.append(claim_id)
                continue
            
            # Check if label matches evidence
            result = self.label_claim(claim, traces)
            
            if result.label_changed:
                mismatched_labels.append({
                    "claim_id": claim_id,
                    "current": result.original_label.value if result.original_label else None,
                    "should_be": result.assigned_label.value,
                    "reasoning": result.reasoning
                })
            else:
                properly_labeled.append(claim_id)
        
        return {
            "total_claims": len(claims),
            "properly_labeled": len(properly_labeled),
            "missing_labels": missing_labels,
            "mismatched_labels": mismatched_labels,
            "transparency_score": len(properly_labeled) / len(claims) if claims else 1.0
        }
    
    def generate_label_summary(self) -> Dict[str, int]:
        """
        Generate summary of labels assigned in current session.
        """
        summary = {level.value: 0 for level in InferenceLevel}
        
        for result in self.labeling_log:
            summary[result.assigned_label.value] += 1
        
        return summary


if __name__ == "__main__":
    # Example usage
    labeler = InferenceLabeler()
    
    # Sample traces
    traces = [
        {"id": "t1", "type": "carbon_14", "confidence": 0.95},
        {"id": "t2", "type": "textual_record", "confidence": 0.8},
        {"id": "t3", "type": "artifact", "confidence": 0.7},
    ]
    
    # Claims with varying evidence
    claims = [
        {"id": "claim_1", "content": "City founded in 2500 BCE"},
        {"id": "claim_2", "content": "Trade routes existed", "confidence": "VERIFIED"},
    ]
    
    # Label claims
    for claim in claims:
        result = labeler.label_claim(claim, traces[:2] if claim["id"] == "claim_1" else [])
        print(f"{claim['id']}: {result.assigned_label.value} - {result.reasoning}")
    
    print(f"\nLabel summary: {labeler.generate_label_summary()}")
