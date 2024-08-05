from pydantic import BaseModel, Field
import random
import sqlite3
from typing import Any, Dict, List, Optional, Type

from dgpinata.entity import Entity
from dgpinata.event import Event
from dgpinata.emitter import ParameterBuilder
from dgpinata.action import Message, MessageType
from dgpinata.chooser import Chooser

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

    prev_timestamp: int = Field(0, title="Previous time in the simulation")
    timestamp: int = Field(0, title="Current time in the simulation")
    interval: int = 3600
    rand_seed: Optional[int] = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Initialize entities
        for entity_type in self.entity_types:
            self.entities[entity_type.__name__] = []

            if hasattr(entity_type, "default_values") and entity_type.default_values is not None:

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

        if self.rand_seed is not None:
            random.seed(self.rand_seed)

    def run(self, steps: int):
        for i in range(steps):
            self.prev_timestamp = self.timestamp
            self.timestamp += self.interval
            print(self.prev_timestamp, self.timestamp)
            self._update_entities()

        return self.get_report()
    
    def get_report(self):
        return SimulationReport(simulation=self)

    def export(self, filename:str, overwrite:bool=False):
        if overwrite:
            open(filename, "w").close()

        sql = sqlite3.connect(filename)

        # Create all the tables that we'll need
        for event_type in self.event_types:
            sql.execute(event_type.get_create_table_sql())
        
        for entity_type in self.entity_types:
            if entity_type.table_name is None:
                continue
            sql.execute(entity_type.get_create_table_sql())
        
        # Insert all the data
        #!!! If multiple objects are written to the same table, this will sort them by type, then timestamp.
        #!!! Instead, they should be sorted by timestamp
        for event_type, events in self.events.items():
            for event in events:
                sql.execute(event.get_insert_sql())

        for entity_type in self.entity_types:
            if entity_type.table_name is None:
                continue

            for entity in self.entities[entity_type.__name__]:
                sql.execute(entity.get_insert_sql())

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
                self._update_entity(entity)
    
    def _update_entity(self, entity: Entity):
        new_actions : List[Message] = entity.update(
            prev_timestamp=self.prev_timestamp,
            timestamp=self.timestamp
        )

        for action in new_actions:
            self._process_action(action)

    def _process_action(self, action: Message):
        if action.action_type == MessageType.AddEvent:
            new_event = self._instantiate_event(
                event_type_name=action.event_type_name,
                parameter_builders=action.parameter_builders,
                parent=action.parent,
                timestamp=action.timestamp,
            )
            self.events[action.event_type_name].append(new_event)

        elif action.action_type == MessageType.AddEntity:
            new_entity = self._instantiate_entity(
                entity_type_name=action.entity_type_name,
                parameter_builders=action.parameter_builders,
                parent=action.parent,
                timestamp=action.timestamp,
            )
            self.entities[action.entity_type_name].append(new_entity)

    @property
    def event_type_lookup(self):
        return dict([(et.__name__, et) for et in self.event_types])

    @property
    def entity_type_lookup(self):
        return dict([(et.__name__, et) for et in self.entity_types])
    
    def _instantiate_event(
        self,
        event_type_name: str,
        parameter_builders: Dict[str, ParameterBuilder],
        parent: Entity,
        timestamp: int,
    ) -> Event:
        event_type = self.event_type_lookup[event_type_name]

        parameters = self._build_parameters(
            parameter_builders=parameter_builders,
            parent=parent,
            timestamp=timestamp,
        )

        # Instatiate the new event
        new_event = event_type(
            **parameters
        )

        return new_event
    
    def _instantiate_entity(
        self,
        entity_type_name: str,
        parameter_builders: Dict[str, ParameterBuilder],
        parent: Entity,
        timestamp: int,
    ) -> Event:
        entity_type = self.entity_type_lookup[entity_type_name]

        parameters = self._build_parameters(
            parameter_builders=parameter_builders,
            parent=parent,
            timestamp=timestamp,
        )

        # Instatiate the new event
        new_event = entity_type(
            simulation=self,
            **parameters
        )

        return new_event
    
    def _build_parameters(self, parameter_builders, parent, timestamp) -> Dict:
        """Iterate over parameter_builders to build up the keyword args for an Event or Entity"""

        parameters = {}
        sim = self
        
        for name, pb in parameter_builders.items():
            if pb.eval_str is not None:
                new_param = eval(pb.eval_str)

            elif isinstance(pb.value, Chooser):
                new_param = pb.value.invoke(
                    sim=sim,
                    parent=parent,
                    timestamp=timestamp,
                )
            else:
                new_param = pb.value

            parameters[pb.name] = new_param        
        
        return parameters

    def _build_parameter(self, parameter_builder, parent, timestamp) -> Dict:
        """Iterate over parameter_builders to build up the keyword args for an Event or Entity"""

        sim = self
        
        if parameter_builder.eval_str is not None:
            return eval(parameter_builder.eval_str)

        elif isinstance(parameter_builder.value, Chooser):
            return parameter_builder.value.invoke(
                sim=sim,
                parent=parent,
                timestamp=timestamp,
            )

        else:
            return parameter_builder.value