from fastapi import FastAPI
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_api_initialization():
    assert isinstance(app, FastAPI)

def test_reconstruct_endpoint():
    # Mock request
    payload = {
        "system": "test_system",
        "timeframe": "2023",
        "layers": ["L0_PHYSICAL", "L1_BIOLOGICAL"]

    }
    # We expect a 200 OK because the engine uses a placeholder implementation
    response = client.post("/reconstruct", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "world_state" in data
    assert "claims" in data
    assert "graph_summary" in data

def test_compare_endpoint():
    payload = {
        "systems": ["sys1", "sys2"],
        "dimensions": ["dim1"]
    }
    response = client.post("/compare", json=payload)
    assert response.status_code == 200
    assert response.json()["status"] == "success"

def test_counterfactual_endpoint():
    payload = {
        "system": "sys1",
        "intervention": {"param": "value"}
    }
    response = client.post("/counterfactual", json=payload)
    assert response.status_code == 200
    assert response.json()["status"] == "success"
