from pydantic import BaseModel
from typing import Any, Dict, List, Optional

from dgpinata.message import Message, AddEvent, AddEntity

class ParameterBuilder(BaseModel):
    name: str
    eval_str: Optional[str] = None
    value: Optional[Any] = None


class Emitter(BaseModel):
    event_type_name: Optional[str] = None
    entity_type_name: Optional[str] = None
    parameter_builders: Dict[str, ParameterBuilder]

    def emit(
        self,
        parent: "Entity",
        prev_timestamp: int,
        timestamp: int
    ) -> List[Message]:
        raise NotImplementedError

    @classmethod
    def _define_parameter_builders(cls, **kwargs):
        parameter_builders = {}
        for parameter_name, value in kwargs.items():
            if type(value) == str:
                parameter_builders[parameter_name] = ParameterBuilder(
                    name=parameter_name,
                    eval_str=value,
                )
            else:
                parameter_builders[parameter_name] = ParameterBuilder(
                    name=parameter_name,
                    value=value,
                )
        return parameter_builders

    def emit(self,
        parent: "Entity",
        prev_timestamp: int,
        timestamp: int,
    ) -> List[Message]:
        """

        Note: prev_timestamp is inclusive, timestamp is exclusive.
        If prev_timestamp == timestamp, no events are emitted.
        """
        intervals = self._get_interval_start_time_list(parent, prev_timestamp, timestamp)

        actions = []
        for interval_start in intervals:
            new_action = self._emit_event(parent, interval_start)
            if new_action is not None:
                actions.append(new_action)
        
        return actions

    def _get_interval_start_time_list(self, parent: "Entity", prev_timestamp: int, timestamp: int):
        raise NotImplementedError
    
    def _emit_event(self, parent: "Entity", timestamp: int) -> Optional[Message]:

        if self.event_type_name is not None:
            return AddEvent(
                event_type_name=self.event_type_name,
                parameter_builders=self.parameter_builders,
                parent=parent,
                timestamp=timestamp,
            )
        
        elif self.entity_type_name is not None:
            return AddEntity(
                entity_type_name=self.entity_type_name,
                parameter_builders=self.parameter_builders,
                parent=parent,
                timestamp=timestamp,
            )

        return None    
