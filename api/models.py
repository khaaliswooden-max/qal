from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from qawm.core.types import Layer

class ReconstructRequest(BaseModel):
    system: str
    timeframe: Optional[str] = None
    layers: Optional[List[Layer]] = None

class CompareRequest(BaseModel):
    systems: List[str]
    dimensions: List[str]

class CounterfactualRequest(BaseModel):
    system: str
    intervention: Dict[str, Any]
