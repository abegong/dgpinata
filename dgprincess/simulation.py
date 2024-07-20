from pydantic import BaseModel, Field
import sqlite3
from typing import Any, Dict, List, Type

from dgprincess.entity import Entity
from dgprincess.event import Event

class SimulationReport(BaseModel):
    simulation: "Simulation" = Field(..., title="The simulation that this report is based on")

    # def pprint(self):
    #     print("Entities:")
    #     for entity_type, entities in self.simulation.entities.items():
    #         print(f"{entity_type}: {len(entities)}")
    #         for entity in entities:
    #             print(entity)

    #     print("Events:")
    #     for event_type, events in self.simulation.events.items():
    #         print(f"{event_type}: {len(events)}")
    #         for event in events:
    #             print(event)

    @property
    def summary(self) -> str:
        summary_str = "=== Entities ===\n"
        for entity_type, entities in self.simulation.entities.items():
            summary_str += f"  {entity_type}: {len(entities)}\n"
        summary_str += "\n=== Events ===\n"
        for event_type, events in self.simulation.events.items():
            summary_str += f"  {event_type}: {len(events)}\n"

        return summary_str

    def __str__(self):
        return self.summary


class Simulation(BaseModel):

    entity_types: List[Type[Entity]] = Field(..., title="List of entity types")
    event_types: List[Type[Event]] = Field(..., title="List of event types")

    entities: Dict[str, List[Entity]] = {}
    events: Dict[str, List[Event]] = {}
    tables: List[str] = []

    timer: int = Field(0, title="Current time in the simulation")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Initialize entities
        for entity_type in self.entity_types:
            self.entities[entity_type.__name__] = []

            if hasattr(entity_type, "default_values") and entity_type.default_values != []:

                for default_values in entity_type.default_values:
                    default_values["simulation"] = self
                    entity = entity_type(**default_values)
                    self.entities[entity_type.__name__].append(entity)
            
            else:
                # Add a single entity
                entity = entity_type(
                    simulation=self
                )
                self.entities[entity_type.__name__].append(entity)


        # Initialize events
        for event_type in self.event_types:
            self.events[event_type.__name__] = []

        # Initialize timer
        self.timer = 0

    def run(self, steps: int, increment: int=1):
        for i in range(steps):
            self._update_entities()
            self.timer += increment

        return self.get_report()
    
    def get_report(self):
        return SimulationReport(simulation=self)

    def export(self, filename:str, overwrite:bool=False):
        if overwrite:
            open(filename, "w").close()

        sql = sqlite3.connect(filename)

        # Create all the tables that we'll need
        for event_type in self.event_types:
            sql.execute(event_type.schema_sql)
        
        # for entity_type in self.entity_types:
        #     if entity_type.schema is None:
        #         continue
        #     sql.execute(entity_type.schema)
        
        # Insert all the data
        for event_type, events in self.events.items():
            for event in events:
                sql.execute(event.insert_sql)
        
        # for entity_type, entities in self.entities.items():
        #     for entity in entities:
        #         sql.execute(entity.insert)

        sql.commit()

    # Doesn't work yet.
    # def _sort_event_types(self):
    #     def check_dependency(a,b):
    #         if b in a.dependencies and a in b.dependencies:
    #             raise ValueError("Circular dependency between {a} and {b}")
            
    #         elif b in a.dependencies:
    #             return -1
            
    #         elif a in b.dependencies:
    #             return 1
            
    #         else:
    #             return 0
            
    #     self.event_types.sort(key=lambda a,b: check_dependency(a,b))

    def _update_entities(self):
        for entity_type in self.entity_types:
            for entity in self.entities[entity_type.__name__]:
                self._update_entity(entity_type, entity)
    
    def _update_entity(self, entity_type: Type[Entity], entity: Entity):
        new_events, new_entities = entity.update(self.timer)

        for event in new_events:
            self.events[event.__class__.__name__].append(event)

        for new_entity in new_entities:
            self.entities[entity_type.__name__].append(new_entity)
