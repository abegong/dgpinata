from enum import Enum
from typing import Any, Dict, Type, Union

from dgprincess.emittable import Emittable

class ActionType(str, Enum):
    AddEvent = "AddEvent"
    AddEntity = "AddEntity"
    # RemoveEntity = "RemoveEntity"
    # ChangeEntityType = "ChangeEntityType"
    # SendMessage = "SendMessage"

class Action(Emittable):
    """Abstract base class for all Actions"""
    action_type: ActionType

class AddEvent(Action):
    action_type: ActionType = ActionType.AddEvent
    
    event_type_name: str
    parameter_builders: Dict[str, Any]#Union[Any, "ParameterBuilder"]]
    parent: Any#"Entity"
    timestamp: int

    @classmethod
    def from_params(
        cls,
        event_type_name:str,
        parent:"Entity",
        timestamp:int,
        **kwargs
    ):
        return cls(
            event_type_name=event_type_name,
            parameter_builders=kwargs,
            parent=parent,
            timestamp=timestamp,
        )

class AddEntity(Action):
    action_type: ActionType = ActionType.AddEntity

    entity_type_name: str
    parameter_builders: Dict[str, Any]#Union[Any, "ParameterBuilder"]]
    parent: Any#"Entity"
    timestamp: int

# class RemoveEntity(Action):
#     action_type = ActionType.RemoveEntity
#     selection_params: Dict

# class ChangeEntityType(Action):
#     action_type = ActionType.ChangeEntityType
#     selection_params: Dict
#     new_type: Type
#     initialization_params: Dict

# class SendMessage(Action):
#     action_type = ActionType.SendMessage
#     selection_params: Dict
#     message_params: Dict