from enum import Enum
from pydantic import BaseModel
import random
from typing import Any, Dict, List, Optional, Union

from dgpinata.message import Message, AddEvent, AddEntity

class NormalDistributionParams(BaseModel):
    mean: float
    standard_deviation: float

class UniformDistributionParams(BaseModel):
    min: int
    max: int


class ParameterBuilder(BaseModel):
    name: str
    eval_str: Optional[str] = None
    value: Optional[Any] = None


class Emitter(BaseModel):
    event_type_name: Optional[str] = None
    entity_type_name: Optional[str] = None

    # def emit(self, parent: "Entity", timestamp: int):
    #     return []

class IntervalSpacingOption(str, Enum):
    START="start"
    CONSTANT="offset"
    UNIFORM="uniform"
    EXPONENTIAL="exponential"


class IntervalEmitter(Emitter):
    """Emits zero or one events per interval.

    Events can be spaced regularly, distributed uniformly within the interval, offset according to a normal distribution, or offset according to uniform distribution.

    You can use skip_probability to skip events at random

    Args:
        event_type_name (str): The name of the event type to emit.
        entity_type_name (str): The name of the entity type to emit.
        interval (Union[int, ParameterBuilder]): The interval between events.
        skip_probability (float): The probability of skipping an event.
        spacing (IntervalSpacingOption): The spacing option.
        constant_offset (Optional[int]): The constant offset.
        normal_offset (Optional[NormalDistributionParams]): The normal distribution offset.
        uniform_offset (Optional[UniformDistributionParams]): The uniform distribution offset.
        parameter_builders (Dict[str, ParameterBuilder]): The parameter builders.
    """

    interval: Union[int, ParameterBuilder]
    skip_probability: Union[float, ParameterBuilder]
    spacing: IntervalSpacingOption
    constant_offset: Optional[int] = None
    normal_offset: Optional[NormalDistributionParams] = None
    uniform_offset: Optional[UniformDistributionParams] = None
    parameter_builders: Dict[str, ParameterBuilder]

    @classmethod
    def from_params(
        cls,
        event_type_name: Optional[str] = None,
        entity_type_name: Optional[str] = None,
        interval: Optional[Union[int, str]] = None,
        skip_probability: float = 0.0,
        spacing: Optional[Union[str, IntervalSpacingOption]] = IntervalSpacingOption.START,
        constant_offset: Optional[int] = None,
        normal_offset: Optional[NormalDistributionParams] = None,
        uniform_offset: Optional[UniformDistributionParams] = None,
        **kwargs,
    ) -> "IntervalEmitter":
        
        if entity_type_name is None and event_type_name is None:
            raise ValueError("entity_type_name and event_type_name cannot both be None.")

        if entity_type_name is not None and event_type_name is not None:
            raise ValueError("entity_type_name and event_type_name cannot both be populated.")

        if interval is None:
            interval = ParameterBuilder(name="interval", eval_str="sim.interval")

        elif type(interval) == str:
            interval = ParameterBuilder(name="interval", eval_str=interval)

        # Instantiate parameter builders
        parameter_builders = cls._define_parameter_builders(**kwargs)

        return cls(
            event_type_name=event_type_name,
            entity_type_name=entity_type_name,
            interval=interval,
            skip_probability=skip_probability,
            spacing=spacing,
            constant_offset=constant_offset,
            normal_offset=normal_offset,
            uniform_offset=uniform_offset,
            parameter_builders=parameter_builders,
        )

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
        """Return a list of start times for each interval."""

        if isinstance(self.interval, ParameterBuilder):
            interval = parent.sim._build_parameter(self.interval, parent, timestamp)
        else:
            interval = self.interval

        start_time_list = []
        for i in range(prev_timestamp, timestamp, interval):
            start_time_list.append(i)

        return start_time_list

    def _emit_event(self, parent: "Entity", timestamp: int) -> Optional[Message]:

        if self.skip_probability > 0 and random.random() < self.skip_probability:
            return None
        
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