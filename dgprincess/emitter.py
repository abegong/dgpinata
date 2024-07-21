from enum import Enum
from pydantic import BaseModel
import random
from typing import Any, Dict, List, Optional, Union

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
    event_type_name: str

    def emit(self, timestamp: int, entity):
        return [], []

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
    def define(
        cls,
        event_type_name: str,
        interval: Union[int, str],
        skip_probability: float = 0.0,
        spacing: Optional[Union[str, IntervalSpacingOption]] = IntervalSpacingOption.START,
        normal_offset: Optional[NormalDistributionParams] = None,
        uniform_offset: Optional[UniformDistributionParams] = None,
        **kwargs,
    ) -> "IntervalEmitter":
        
        if type(interval) == str:
            interval = ParameterBuilder(name="interval", eval_str=interval)

        # Instantiate parameter builders
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

        return  cls(
            event_type_name=event_type_name,
            interval=interval,
            skip_probability=skip_probability,
            spacing=spacing,
            normal_offset=normal_offset,
            uniform_offset=uniform_offset,
            parameter_builders=parameter_builders,
        )
    
    def emit(self,
        parent_entity: "Entity",
        simulation: "Simulation",
        timestamp: int,
    ) -> List["Event"]:
        if self.skip_probability > 0 and random.random() < self.skip_probability:
            return [], []
        
        # Ignore the spacing for now

        # Instantiate
        new_event = simulation.instantiate_event(
            event_type_name=self.event_type_name,
            parent_entity=parent_entity,
            parameter_builders=self.parameter_builders,
            timestamp=timestamp,
        )

        return [new_event], []
        

#     created_at="timestamp",
# ),
# "add_sale": IntervalEmitter(
#     event_type=Sale,
#     interval=3600,
#     -- offset=lambda: random.randint(),
#     product_id=RandomChoice("sim.Entities['Product']"),
#     customer_id=RandomChoice("sim.Entities['Customer']"),
#     amount=1,
#     timestamp="timestamp",

