
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

    @property
    def sim(self):
        """Alias for self.simulation"""
        return self.simulation

    def update(self, timestamp: int) -> Tuple[List[Event], List["Entity"]]:
        """Update the entity based on the elapsed time."""
        new_events = []
        new_actions = []

        for emitter in self.emitters.values():
            emitted_events, emitted_actions = emitter.emit(
                parent_entity=self,
                simulation=self.simulation,
                timestamp=timestamp,
            )
            new_events.extend(emitted_events)
            new_actions.extend(emitted_actions)

        more_new_events, more_new_entities = self._update(timestamp)
        return new_events + more_new_events, new_actions + more_new_entities
    
    def _update(self, timestamp: int) -> Tuple[List[Event], List["Entity"]]:
        return [], []
        
    default_values: ClassVar[Optional[List[Dict]]] = None


class StaticEntity(Entity):
    """StaticEntity is a subclass of Entity that does not change over time.
    
    They are initialized at the beginning of the simulation and do not change or emit events.
    """

    def update(self, timestamp: int) -> Tuple[List[Event], List[Entity]]:
        return [], []