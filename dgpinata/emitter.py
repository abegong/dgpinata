from enum import Enum
from pydantic import BaseModel
import random
from typing import Any, Dict, List, Optional, Union

from dgpinata.action import Message, AddEvent, AddEntity

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
    UNIFORM="uniform"
    EXPONENTIAL="exponential"


class IntervalEmitter(Emitter):
    """Emits zero or one events per interval
    Events can be spaced regularly, distributed uniformly within the interval, offset according to a normal distribution, or offset according to uniform distribution
    You can use skip_probability to skip events at random
    """

    interval: Union[int, ParameterBuilder]
    skip_probability: Union[float, ParameterBuilder]
    spacing: IntervalSpacingOption
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
        timestamp: int,
    ) -> List[Message]:
        #!!! Ignore spacing and interval_logic for now

        if self.skip_probability > 0 and random.random() < self.skip_probability:
            return []
        
        if self.event_type_name is not None:
            new_action = AddEvent(
                event_type_name=self.event_type_name,
                parameter_builders=self.parameter_builders,
                parent=parent,
                timestamp=timestamp,
            )
        
        elif self.entity_type_name is not None:
            new_action = AddEntity(
                entity_type_name=self.entity_type_name,
                parameter_builders=self.parameter_builders,
                parent=parent,
                timestamp=timestamp,
            )

        return [new_action]
