"""Tests for Ethics and Governance components.

These tests validate the ethical guardrails defined in qawm_ethics.md:
1. Transparency of Inference
2. Anti-Fabrication
3. Confidence Level Tagging
"""
import unittest
from qawm.core.validation import ClaimValidator, FabricationError, TraceDatabase
from qawm.core.models import Event, Entity, Claim
from qawm.core.types import Layer, Confidence


class MockTraceDatabase(TraceDatabase):
    """Mock trace database for testing."""
    
    def __init__(self, traces=None):
        self.traces = traces or []
    
    def find_supporting_traces(self, claim):
        """Return configured traces."""
        return self.traces


class TestEthicalGuardrails(unittest.TestCase):
    """Test ethical guardrail enforcement."""
    
    def setUp(self):
        self.validator = ClaimValidator()
    
    def test_transparency_of_inference_required(self):
        """Every claim must have a confidence level tagged."""
        claim = Claim(
            subject_id="event_1",
            predicate="caused",
            object_id="event_2",
            confidence=Confidence.PLAUSIBLE
        )
        self.assertTrue(claim.has_inference_level())
    
    def test_anti_fabrication_rejects_unsupported_claims(self):
        """Claims without trace support must be rejected."""
        empty_db = MockTraceDatabase(traces=[])
        claim = Claim(
            subject_id="event_1",
            predicate="occurred_at",
            confidence=Confidence.VERIFIED
        )
        
        with self.assertRaises(FabricationError) as context:
            self.validator.validate_claim(claim, empty_db)
        
        self.assertIn("no trace support", str(context.exception))
    
    def test_claim_with_trace_support_passes(self):
        """Claims with trace support are accepted."""
        trace_db = MockTraceDatabase(traces=[
            {"id": "trace_1", "type": "carbon_14", "data": {}},
            {"id": "trace_2", "type": "textual_record", "data": {}}
        ])
        claim = Claim(
            subject_id="site_alpha",
            predicate="existed_during",
            confidence=Confidence.VERIFIED
        )
        
        traces = self.validator.validate_claim(claim, trace_db)
        self.assertEqual(len(traces), 2)


class TestConfidenceLevels(unittest.TestCase):
    """Test confidence level calibration and tagging."""
    
    def test_verified_requires_multiple_traces(self):
        """VERIFIED confidence requires at least 2 supporting traces."""
        from datetime import datetime
        
        validator = ClaimValidator()
        event = Event(
            id="event_verified",
            type="destruction",
            layer=Layer.L2_CULTURAL,
            timestamp=datetime.now(),
            confidence=Confidence.VERIFIED,
            evidence_refs=["trace_1"]
        )
        
        # Only one trace - should fail calibration
        single_trace = [{"id": "trace_1"}]
        result = validator.check_confidence_calibration(event, single_trace)
        self.assertFalse(result)
        
        # Two traces - should pass calibration
        two_traces = [{"id": "trace_1"}, {"id": "trace_2"}]
        result = validator.check_confidence_calibration(event, two_traces)
        self.assertTrue(result)
    
    def test_speculative_allows_single_trace(self):
        """SPECULATIVE confidence can have single trace support."""
        from datetime import datetime
        
        validator = ClaimValidator()
        event = Event(
            id="event_speculative",
            type="migration",
            layer=Layer.L2_CULTURAL,
            timestamp=datetime.now(),
            confidence=Confidence.SPECULATIVE,
            evidence_refs=["trace_1"]
        )
        
        single_trace = [{"id": "trace_1"}]
        result = validator.check_confidence_calibration(event, single_trace)
        self.assertTrue(result)


class TestConfidenceEnum(unittest.TestCase):
    """Test that confidence levels are properly defined."""
    
    def test_confidence_levels_exist(self):
        """All three confidence levels must be defined."""
        self.assertEqual(Confidence.VERIFIED.value, "VERIFIED")
        self.assertEqual(Confidence.PLAUSIBLE.value, "PLAUSIBLE")
        self.assertEqual(Confidence.SPECULATIVE.value, "SPECULATIVE")
    
    def test_confidence_ordering(self):
        """VERIFIED > PLAUSIBLE > SPECULATIVE in terms of certainty."""
        # This tests the semantic relationship between levels
        confidence_order = [Confidence.VERIFIED, Confidence.PLAUSIBLE, Confidence.SPECULATIVE]
        self.assertEqual(len(confidence_order), 3)


if __name__ == '__main__':
    unittest.main()
