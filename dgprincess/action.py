from enum import Enum
from typing import Any, Dict, Type, Union

from dgprincess.emittable import Recordable

class MessageType(str, Enum):
    AddEvent = "AddEvent"
    AddEntity = "AddEntity"
    # RemoveEntity = "RemoveEntity"
    # ChangeEntityType = "ChangeEntityType"
    # SendMessage = "SendMessage"

class Message(Recordable):
    """Abstract base class for all Messages"""
    action_type: MessageType

class AddEvent(Message):
    action_type: MessageType = MessageType.AddEvent
    
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

class AddEntity(Message):
    action_type: MessageType = MessageType.AddEntity

    entity_type_name: str
    parameter_builders: Dict[str, Any]#Union[Any, "ParameterBuilder"]]
    parent: Any#"Entity"
    timestamp: int

# class RemoveEntity(Message):
#     action_type = MessageType.RemoveEntity
#     selection_params: Dict

# class ChangeEntityType(Message):
#     action_type = MessageType.ChangeEntityType
#     selection_params: Dict
#     new_type: Type
#     initialization_params: Dict

# class SendMessage(Message):
#     action_type = MessageType.SendMessage
#     selection_params: Dict
#     message_params: Dict