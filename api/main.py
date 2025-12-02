from fastapi import FastAPI
from api.models import ReconstructRequest, CompareRequest, CounterfactualRequest
from qawm.core.engine import QAWMEngine

app = FastAPI()
qawm_engine = QAWMEngine()

@app.post("/reconstruct")
async def reconstruct(query: ReconstructRequest):
    """
    Execute QAWM-QL RECONSTRUCT query
    """
    result = qawm_engine.execute_reconstruct(
        system=query.system,
        timeframe=query.timeframe,
        layers=query.layers
    )
    return result

@app.post("/compare")
async def compare(query: CompareRequest):
    """
    Execute QAWM-QL COMPARE query
    """
    result = qawm_engine.execute_compare(
        systems=query.systems,
        dimensions=query.dimensions
    )
    return result

@app.post("/counterfactual")
async def counterfactual(query: CounterfactualRequest):
    """
    Execute QAWM-QL COUNTERFACTUAL query
    """
    result = qawm_engine.execute_counterfactual(
        system=query.system,
        intervention=query.intervention
    )
    return result
