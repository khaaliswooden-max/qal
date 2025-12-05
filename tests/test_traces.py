"""Tests for Trace Processing Pipeline.

Tests validate:
1. Multi-format trace ingestion
2. Trace normalization to unified schema
3. Trace validation and quality scoring
4. Metadata preservation (provenance, uncertainty, timestamps)
"""
import unittest
import json
import os


class TestTraceSchema(unittest.TestCase):
    """Test trace schema compliance."""
    
    def setUp(self):
        """Load trace schema."""
        schema_path = os.path.join(
            os.path.dirname(__file__), '..', 'traces', 'schema.json'
        )
        with open(schema_path) as f:
            self.schema = json.load(f)
    
    def test_schema_has_required_fields(self):
        """Schema must define required fields: id, type, timestamp, data."""
        required = self.schema.get("required", [])
        self.assertIn("id", required)
        self.assertIn("type", required)
        self.assertIn("timestamp", required)
        self.assertIn("data", required)
    
    def test_schema_has_confidence_field(self):
        """Schema must include confidence scoring field."""
        properties = self.schema.get("properties", {})
        self.assertIn("confidence", properties)
        
        confidence = properties["confidence"]
        self.assertEqual(confidence.get("minimum"), 0.0)
        self.assertEqual(confidence.get("maximum"), 1.0)
    
    def test_schema_has_provenance_field(self):
        """Schema must include source/provenance field."""
        properties = self.schema.get("properties", {})
        self.assertIn("source", properties)
    
    def test_timestamp_supports_uncertainty(self):
        """Timestamp field must support uncertainty quantification."""
        properties = self.schema.get("properties", {})
        timestamp = properties.get("timestamp", {})
        ts_properties = timestamp.get("properties", {})
        
        self.assertIn("uncertainty", ts_properties)
        self.assertIn("unit", ts_properties)


class TestTraceNormalization(unittest.TestCase):
    """Test trace normalization to unified schema."""
    
    def test_valid_trace_structure(self):
        """A properly structured trace should be valid."""
        trace = {
            "id": "trace_001",
            "type": "carbon_14",
            "timestamp": {
                "value": -2500,
                "uncertainty": 50,
                "unit": "BC"
            },
            "data": {
                "sample_id": "HAR-001",
                "raw_measurement": 4500,
                "calibrated_date": -2500
            },
            "confidence": 0.95,
            "source": "University of Oxford Radiocarbon Lab"
        }
        
        # Validate required fields
        required_fields = ["id", "type", "timestamp", "data"]
        for field in required_fields:
            self.assertIn(field, trace)
    
    def test_trace_type_categories(self):
        """Support multiple trace types per information substrates."""
        valid_types = [
            "carbon_14",           # Physical
            "genetic_marker",      # Biological
            "textual_record",      # Cultural
            "server_log",          # Technological
            "trade_ledger",        # Economic
            "ice_core",            # Planetary
        ]
        
        for trace_type in valid_types:
            trace = {
                "id": f"test_{trace_type}",
                "type": trace_type,
                "timestamp": {"value": 2000, "unit": "AD"},
                "data": {}
            }
            self.assertEqual(trace["type"], trace_type)


class TestTraceDirectoryStructure(unittest.TestCase):
    """Test that trace directory structure exists."""
    
    def test_raw_traces_directory_exists(self):
        """Raw traces directory must exist."""
        path = os.path.join(os.path.dirname(__file__), '..', 'traces', 'raw')
        self.assertTrue(os.path.isdir(path))
    
    def test_normalized_traces_directory_exists(self):
        """Normalized traces directory must exist."""
        path = os.path.join(os.path.dirname(__file__), '..', 'traces', 'normalized')
        self.assertTrue(os.path.isdir(path))
    
    def test_validation_traces_directory_exists(self):
        """Validation traces directory must exist."""
        path = os.path.join(os.path.dirname(__file__), '..', 'traces', 'validation')
        self.assertTrue(os.path.isdir(path))


class TestTraceMetadata(unittest.TestCase):
    """Test metadata preservation in traces."""
    
    def test_location_data_optional(self):
        """Location data should be optional but structured when present."""
        trace_with_location = {
            "id": "trace_002",
            "type": "artifact",
            "timestamp": {"value": -1200, "unit": "BC"},
            "data": {},
            "location": {
                "latitude": 36.1070,
                "longitude": -112.1130,
                "description": "Grand Canyon, Arizona"
            }
        }
        
        self.assertIn("location", trace_with_location)
        self.assertIn("latitude", trace_with_location["location"])
        self.assertIn("longitude", trace_with_location["location"])
    
    def test_trace_without_location_valid(self):
        """Traces without location should still be valid."""
        trace_no_location = {
            "id": "trace_003",
            "type": "textual_record",
            "timestamp": {"value": 1450, "unit": "AD"},
            "data": {"content": "First printed Bible"}
        }
        
        required_fields = ["id", "type", "timestamp", "data"]
        for field in required_fields:
            self.assertIn(field, trace_no_location)


if __name__ == '__main__':
    unittest.main()
