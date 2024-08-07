from enum import Enum
from pydantic import BaseModel
import random
from typing import Dict, Optional, Union

from dgpinata.message import Message
from dgpinata.emitters.base import Emitter, ParameterBuilder


class NormalDistributionParams(BaseModel):
    mean: float
    standard_deviation: float

class UniformDistributionParams(BaseModel):
    min: int
    max: int

class ExponentialDistributionParams(BaseModel):
    lambda_: float

class IntervalSpacingOption(str, Enum):
    START="start"
    UNIFORM="uniform"


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
    exponential_offset: Optional[ExponentialDistributionParams] = None
    # parameter_builders: Dict[str, ParameterBuilder]

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
        exponential_offset: Optional[ExponentialDistributionParams] = None,
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
            exponential_offset=exponential_offset,
            parameter_builders=parameter_builders,
        )
    
    def _get_interval_start_time_list(self, parent: "Entity", prev_timestamp: int, timestamp: int):
        """Return a list of start times for each interval."""

        if isinstance(self.interval, ParameterBuilder):
            interval = parent.sim._build_parameter(self.interval, parent, timestamp)
        else:
            interval = self.interval

        start_time_list = []
        for i in range(prev_timestamp, timestamp, interval):

            if self.spacing == IntervalSpacingOption.START:
                start_time_list.append(i)
            elif self.spacing == IntervalSpacingOption.UNIFORM:
                start_time_list.append(i + random.randint(0, interval))
            else:
                raise ValueError(f"Unsupported spacing option: {self.spacing}")

        return start_time_list

    def _emit_event(self, parent: "Entity", timestamp: int) -> Optional[Message]:

        if self.skip_probability > 0 and random.random() < self.skip_probability:
            return None
        
        self._get_offset(parent, timestamp)

        return super()._emit_event(parent, timestamp)
    
    def _get_offset(self, parent: "Entity", timestamp: int) -> int:
        offset = 0

        if self.constant_offset is not None:
            offset += self.constant_offset

        if self.normal_offset is not None:
            offset += int(random.normalvariate(
                self.normal_offset.mean,
                self.normal_offset.standard_deviation,
            ))

        if self.uniform_offset is not None:
            offset += random.randint(
                self.uniform_offset.min,
                self.uniform_offset.max,
            )

        if self.exponential_offset is not None:
            offset += int(random.expovariate(self.exponential_offset.lambda_))
        
        return 0