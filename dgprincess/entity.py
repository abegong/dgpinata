
from pydantic import BaseModel, Field
from typing import ClassVar, Dict, List, Optional, Tuple, TYPE_CHECKING
from uuid import uuid4

from dgprincess.event import Event
if TYPE_CHECKING:
    from dgprincess.simulation import Simulation

class Entity(BaseModel):
    """Entities can have state and emit events."""

    simulation: "Simulation" = Field(..., title="The simulation that this entity belongs to")

    @property
    def sim(self):
        """Alias for self.simulation"""
        return self.simulation

    def update(self, elapsed_time: int) -> Tuple[List[Event], List["Entity"]]:
        """Update the entity based on the elapsed time."""

        raise NotImplementedError

    def _emit(cls, data: dict):
        return cls(**data)
        
    @property
    def state(self):
        return self.dict()
    
    default_values: ClassVar[Optional[List[Dict]]] = None


class StaticEntity(Entity):
    """StaticEntity is a subclass of Entity that does not change over time.
    
    They are initialized at the beginning of the simulation and do not change or emit events.
    """

    def update(self, elapsed_time: int) -> Tuple[List[Event], List[Entity]]:
        return [], []