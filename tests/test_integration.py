import pytest
import qawm

def load_test_traces(dataset_name):
    # Mock implementation
    return ["trace1", "trace2"]

def test_end_to_end_reconstruction():
    traces = load_test_traces('bronze_age_collapse')
    reconstruction = qawm.reconstruct(
        system="Late Bronze Age",
        timeframe="1250 BCE → 1150 BCE",
        layers=["L2", "L3"],
        traces=traces
    )
    assert reconstruction is not None
    assert reconstruction.has_valid_causal_graph()
    assert len(reconstruction.claims) > 0
    assert all(claim.has_inference_level() for claim in reconstruction.claims)
