"""Anti-Fabrication Bot.

Enforces QAWM Ethical Guardrail Principle #4: Anti-Fabrication
"The model must never 'hallucinate' evidence. Gaps must be explicitly
rendered as gaps (voids), not filled with convenient fiction."

This governance agent:
1. Validates all claims have trace support
2. Rejects unsupported assertions
3. Identifies and marks epistemic gaps
4. Prevents confidence inflation
"""
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum


class GapType(Enum):
    """Types of epistemic gaps in reconstruction."""
    TEMPORAL = "temporal"        # Missing time period
    CAUSAL = "causal"           # Missing causal link  
    EVIDENTIAL = "evidential"   # Missing evidence
    SPATIAL = "spatial"         # Missing location data


@dataclass
class EpistemicGap:
    """Represents a gap in knowledge that cannot be filled."""
    gap_id: str
    gap_type: GapType
    description: str
    time_range: Optional[Tuple[str, str]] = None
    affected_entities: List[str] = None
    
    def __post_init__(self):
        if self.affected_entities is None:
            self.affected_entities = []


@dataclass
class ValidationResult:
    """Result of anti-fabrication validation."""
    is_valid: bool
    claim_id: str
    supporting_traces: List[str]
    confidence_appropriate: bool
    violations: List[str]
    identified_gaps: List[EpistemicGap]


class AntiFabricationBot:
    """
    Governance agent that prevents hallucination and enforces trace-backing.
    
    Core responsibilities:
    - Every claim must link to source traces
    - Confidence levels must match evidence strength
    - Gaps must be explicitly identified, not papered over
    """
    
    def __init__(self, min_traces_for_verified: int = 2):
        """
        Initialize the anti-fabrication bot.
        
        Args:
            min_traces_for_verified: Minimum trace count for VERIFIED confidence
        """
        self.min_traces_for_verified = min_traces_for_verified
        self.validation_log: List[ValidationResult] = []
    
    def validate_claim(
        self, 
        claim: Dict[str, Any], 
        available_traces: List[Dict[str, Any]]
    ) -> ValidationResult:
        """
        Validate a single claim against available traces.
        
        Args:
            claim: The claim to validate (must have 'id', 'confidence', 'evidence_refs')
            available_traces: List of available trace objects
            
        Returns:
            ValidationResult with pass/fail and any identified issues
        """
        violations = []
        gaps = []
        
        claim_id = claim.get("id", "unknown")
        confidence = claim.get("confidence", "SPECULATIVE")
        evidence_refs = claim.get("evidence_refs", [])
        
        # Build trace lookup
        trace_ids = {t.get("id") for t in available_traces}
        
        # Check 1: All referenced traces exist
        missing_traces = [ref for ref in evidence_refs if ref not in trace_ids]
        if missing_traces:
            violations.append(f"Referenced traces not found: {missing_traces}")
        
        # Check 2: Claim has supporting traces
        supporting_traces = [ref for ref in evidence_refs if ref in trace_ids]
        if not supporting_traces:
            violations.append("Claim has no valid supporting traces - FABRICATION DETECTED")
            gaps.append(EpistemicGap(
                gap_id=f"gap_{claim_id}",
                gap_type=GapType.EVIDENTIAL,
                description=f"No evidence supports claim {claim_id}",
                affected_entities=[claim_id]
            ))
        
        # Check 3: Confidence level appropriate for evidence
        confidence_appropriate = self._check_confidence_calibration(
            confidence, len(supporting_traces)
        )
        if not confidence_appropriate:
            violations.append(
                f"Confidence '{confidence}' not supported by {len(supporting_traces)} traces"
            )
        
        result = ValidationResult(
            is_valid=len(violations) == 0,
            claim_id=claim_id,
            supporting_traces=supporting_traces,
            confidence_appropriate=confidence_appropriate,
            violations=violations,
            identified_gaps=gaps
        )
        
        self.validation_log.append(result)
        return result
    
    def _check_confidence_calibration(self, confidence: str, trace_count: int) -> bool:
        """
        Check if confidence level matches evidence strength.
        
        Rules:
        - VERIFIED: requires 2+ independent traces
        - PLAUSIBLE: requires 1+ traces  
        - SPECULATIVE: can have 0 traces (but must be labeled as such)
        """
        if confidence == "VERIFIED":
            return trace_count >= self.min_traces_for_verified
        elif confidence == "PLAUSIBLE":
            return trace_count >= 1
        elif confidence == "SPECULATIVE":
            return True  # Always valid, just needs proper labeling
        else:
            return False  # Unknown confidence level
    
    def identify_temporal_gaps(
        self, 
        events: List[Dict[str, Any]], 
        expected_continuity: bool = True
    ) -> List[EpistemicGap]:
        """
        Identify gaps in temporal coverage.
        
        Args:
            events: List of events with timestamps
            expected_continuity: Whether continuous coverage is expected
            
        Returns:
            List of identified temporal gaps
        """
        if not events or not expected_continuity:
            return []
        
        # Sort by timestamp
        sorted_events = sorted(
            [e for e in events if e.get("timestamp")],
            key=lambda x: x["timestamp"]
        )
        
        gaps = []
        for i in range(len(sorted_events) - 1):
            current = sorted_events[i]
            next_event = sorted_events[i + 1]
            
            # In a real implementation, check if gap is significant
            # based on expected event frequency
            gap_duration = next_event["timestamp"] - current["timestamp"]
            
            # Placeholder: flag gaps > threshold as significant
            # This would need domain-specific configuration
            
        return gaps
    
    def render_void(self, gap: EpistemicGap) -> Dict[str, Any]:
        """
        Render an epistemic gap as an explicit void in the reconstruction.
        
        Per QAWM Ethics: "Gaps must be explicitly rendered as gaps (voids)"
        
        Returns:
            Void representation suitable for output
        """
        return {
            "type": "EPISTEMIC_VOID",
            "gap_id": gap.gap_id,
            "gap_type": gap.gap_type.value,
            "description": gap.description,
            "message": "Insufficient evidence for reconstruction in this region",
            "affected_entities": gap.affected_entities,
            "time_range": gap.time_range
        }
    
    def audit_reconstruction(
        self, 
        claims: List[Dict[str, Any]], 
        traces: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Full audit of a reconstruction for fabrication.
        
        Args:
            claims: All claims in the reconstruction
            traces: All available traces
            
        Returns:
            Audit report
        """
        results = []
        all_gaps = []
        fabrication_count = 0
        
        for claim in claims:
            result = self.validate_claim(claim, traces)
            results.append(result)
            all_gaps.extend(result.identified_gaps)
            
            if not result.is_valid:
                fabrication_count += 1
        
        return {
            "total_claims": len(claims),
            "valid_claims": len(claims) - fabrication_count,
            "fabrication_detected": fabrication_count > 0,
            "fabrication_count": fabrication_count,
            "identified_gaps": len(all_gaps),
            "gaps": [self.render_void(g) for g in all_gaps],
            "validation_details": [
                {
                    "claim_id": r.claim_id,
                    "valid": r.is_valid,
                    "violations": r.violations
                }
                for r in results
            ]
        }


if __name__ == "__main__":
    # Example usage
    bot = AntiFabricationBot()
    
    # Sample traces
    traces = [
        {"id": "trace_1", "type": "carbon_14", "data": {}},
        {"id": "trace_2", "type": "textual_record", "data": {}},
    ]
    
    # Valid claim with evidence
    valid_claim = {
        "id": "claim_1",
        "confidence": "VERIFIED",
        "evidence_refs": ["trace_1", "trace_2"]
    }
    
    # Invalid claim - no evidence
    invalid_claim = {
        "id": "claim_2", 
        "confidence": "VERIFIED",
        "evidence_refs": []
    }
    
    print("Validating claims...")
    result1 = bot.validate_claim(valid_claim, traces)
    print(f"Claim 1: Valid={result1.is_valid}")
    
    result2 = bot.validate_claim(invalid_claim, traces)
    print(f"Claim 2: Valid={result2.is_valid}, Violations={result2.violations}")
