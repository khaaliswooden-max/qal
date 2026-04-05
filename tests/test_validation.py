import unittest
from datetime import datetime
from typing import List, Any
from qawm.core import Event, Layer, Confidence, ClaimValidator, TraceDatabase, FabricationError

class MockTraceDatabase(TraceDatabase):
    def __init__(self):
        self.traces = {} # Map claim_id to list of traces

    def add_traces(self, claim_id: str, traces: List[str]):
        self.traces[claim_id] = traces

    def find_supporting_traces(self, claim: Any) -> List[Any]:
        if hasattr(claim, 'id'):
            return self.traces.get(claim.id, [])
        return []

class TestAntiHallucinationProtocols(unittest.TestCase):
    def setUp(self):
        self.validator = ClaimValidator()
        self.db = MockTraceDatabase()
        
        self.valid_event = Event(
            id="evt_001",
            type="Battle",
            layer=Layer.L3_TECHNO_ECONOMIC,
            timestamp=datetime.now(),
            confidence=Confidence.VERIFIED,
            evidence_refs=["trace_1", "trace_2"]
        )
        
        self.hallucinated_event = Event(
            id="evt_fake",
            type="AlienInvasion",
            layer=Layer.L0_PHYSICAL,
            timestamp=datetime.now(),
            confidence=Confidence.VERIFIED,
            evidence_refs=[]
        )

    def test_trace_linking_success(self):
        # Setup DB with traces for the valid event
        self.db.add_traces("evt_001", ["trace_doc_1", "trace_artifact_2"])
        
        traces = self.validator.validate_claim(self.valid_event, self.db)
        self.assertEqual(len(traces), 2)
        self.assertIn("trace_doc_1", traces)

    def test_trace_linking_failure(self):
        # DB has no traces for hallucinated_event
        with self.assertRaises(FabricationError):
            self.validator.validate_claim(self.hallucinated_event, self.db)

    def test_confidence_calibration(self):
        # VERIFIED event with 2 traces -> Should pass calibration check
        self.db.add_traces("evt_001", ["trace_1", "trace_2"])
        traces = self.validator.validate_claim(self.valid_event, self.db)
        self.assertTrue(self.validator.check_confidence_calibration(self.valid_event, traces))

        # VERIFIED event with 1 trace -> Should fail calibration check (heuristic)
        self.db.traces["evt_001"] = ["trace_1"]
        traces = self.validator.validate_claim(self.valid_event, self.db)
        self.assertFalse(self.validator.check_confidence_calibration(self.valid_event, traces))

if __name__ == '__main__':
    unittest.main()
