
from pydantic import BaseModel, Field
from typing import ClassVar, Dict, List, Optional, Tuple, TYPE_CHECKING
from uuid import uuid4

from dgprincess.event import Event
from dgprincess.emittable import Emittable
from dgprincess.emitter import Emitter
if TYPE_CHECKING:
    from dgprincess.simulation import Simulation

class Entity(Emittable):
    """Entities can have state and emit events."""

    simulation: "Simulation" = Field(..., title="The simulation that this entity belongs to")
    column_block_list = Emittable.column_block_list + [
        "simulation"
    ]
    emitters: Dict[str, "Emitter"] = {}
    default_values: ClassVar[Optional[List[Dict]]] = None

    @property
    def sim(self):
        """Alias for self.simulation"""
        return self.simulation

    def update(self, timestamp: int) -> List["Message"]:
        """Update the entity based on the elapsed time."""
        new_actions = []

        for emitter in self.emitters.values():
            emitted_actions = emitter.emit(
                parent=self,
                timestamp=timestamp,
            )
            new_actions.extend(emitted_actions)

        more_new_actions = self._update(timestamp)
        return new_actions + more_new_actions
    
    def _update(self, timestamp: int) -> List["Message"]:
        return []
        
