from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field, validator
from .types import Layer, Confidence, RelationType

class TimeSpan(BaseModel):
    start: Optional[datetime] = None
    end: Optional[datetime] = None

class Entity(BaseModel):
    """
    An object or agent that exists within a specific layer.
    """
    id: str
    type: str
    layer: Layer
    attributes: Dict[str, Any] = Field(default_factory=dict)
    timespan: Optional[TimeSpan] = None

class Event(BaseModel):
    """
    A discrete occurrence in time that changes the state of the system.
    """
    id: str
    type: str
    layer: Layer
    timestamp: datetime
    participants: List[str] = Field(default_factory=list, description="List of Entity IDs")
    confidence: Confidence
    evidence_refs: List[str] = Field(default_factory=list, description="IDs of Traces supporting this event")

class Relation(BaseModel):
    """
    A directed causal link between two entities or events.
    """
    source_id: str
    target_id: str
    type: RelationType
    weight: float = Field(..., ge=0.0, le=1.0, description="Strength of the relation")

class WorldState(BaseModel):
    """
    A snapshot or aggregate model of the reconstructed world.
    """
    model_id: str
    entities: List[Entity] = Field(default_factory=list)
    events: List[Event] = Field(default_factory=list)
    relations: List[Relation] = Field(default_factory=list)
