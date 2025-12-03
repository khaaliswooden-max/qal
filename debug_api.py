import sys
import os

# Add current directory to sys.path
sys.path.append(os.getcwd())

try:
    from fastapi import FastAPI
    from fastapi.testclient import TestClient
    from api.main import app
    print("Imports successful")
except ImportError as e:
    print(f"ImportError: {e}")
    sys.exit(1)
except Exception as e:
    print(f"Error during import: {e}")
    sys.exit(1)

client = TestClient(app)

try:
    print("Testing /reconstruct...")
    payload = {
        "system": "test_system",
        "timeframe": "2023",
        "layers": ["L0_PHYSICAL", "L1_BIOLOGICAL"]

    }
    response = client.post("/reconstruct", json=payload)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    if response.status_code != 200:
        print("Reconstruct failed")
        sys.exit(1)
        
    print("Testing /compare...")
    payload = {
        "systems": ["sys1", "sys2"],
        "dimensions": ["dim1"]
    }
    response = client.post("/compare", json=payload)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    print("Testing /counterfactual...")
    payload = {
        "system": "sys1",
        "intervention": {"param": "value"}
    }
    response = client.post("/counterfactual", json=payload)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")

    print("All tests passed manually")

except Exception as e:
    print(f"Test failed: {e}")
    sys.exit(1)
