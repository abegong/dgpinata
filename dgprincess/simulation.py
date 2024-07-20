from pydantic import BaseModel, Field
import sqlite3
from typing import Any, Dict, List, Type

from dgprincess.entity import Entity
from dgprincess.event import Event

class Simulation(BaseModel):

    entity_types: List[Type[Entity]] = Field(..., title="List of entity types")
    event_types: List[Type[Event]] = Field(..., title="List of event types")
    duration: int = Field(..., title="Duration of the simulation")
    interval: int = Field(..., title="Interval of the simulation")

    entities: Dict[str, List[Entity]] = {}
    events: Dict[str, List[Event]] = {}
    tables: List[str] = []

    def pprint(self):
        print("Entities:")
        for entity_type, entities in self.entities.items():
            print(f"{entity_type}: {len(entities)}")
            for entity in entities:
                print(entity.state)

        print("Events:")
        for event_type, events in self.events.items():
            print(f"{event_type}: {len(events)}")
            for event in events:
                print(event.dict())
    
    def print_summary(self):
        print("Summary:")
        for event_type, events in self.events.items():
            print(f"{event_type}: {len(events)}")
        
        for entity_type, entities in self.entities.items():
            print(f"{entity_type}: {len(entities)}")

    def init(self):
        # Initialize entities
        for entity_type in self.entity_types:
            self.entities[entity_type.__name__] = []

            if not hasattr(entity_type, "default_values"):
                continue

            for default_values in entity_type.default_values:
                entity = entity_type(**default_values)
                self.entities[entity_type.__name__].append(entity)

        # Initialize events
        for event_type in self.event_types:
            self.events[event_type.__name__] = []

    def run(self):
        timer = 0.0
        while timer < self.duration:
            self._update_entities()

            timer += self.interval

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
        new_events, new_entities = entity.update(self.interval)

        for event in new_events:
            self.events[event.__class__.__name__].append(event)

        for new_entity in new_entities:
            self.entities[entity_type.__name__].append(new_entity)
