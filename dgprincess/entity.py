from pydantic import BaseModel, Field
from typing import List, Tuple
from uuid import uuid4

from dgprincess.event import Event

class Entity(BaseModel):
    """Entities can have state and emit events."""

    def update(self, elapsed_time: int) -> Tuple[List[Event], List["Entity"]]:
        """Update the entity based on the elapsed time."""

        raise NotImplementedError

    def _emit(cls, data: dict):
        return cls(**data)
        
    @property
    def state(self):
        return self.dict()


class StaticEntity(Entity):
    """StaticEntity is a subclass of Entity that does not change over time.
    
    They are initialized at the beginning of the simulation and do not change or emit events.
    """

    def update(self, elapsed_time: int) -> Tuple[List[Event], List[Entity]]:
        return [], []