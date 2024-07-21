from enum import Enum
from pydantic import BaseModel
from typing import ClassVar, Dict, List, Optional, Union

class NormalDistributionParams(BaseModel):
    mean: float
    standard_deviation: float

class UniformDistributionParams(BaseModel):
    min: int
    max: int


class ParameterBuilder(BaseModel):
    name: str
    address: str
    value: str

class Emitter(BaseModel):
    event_type_name: str

class IntervalSpacingOption(str, Enum):
    START="start"
    UNIFORM="uniform"


class IntervalEmitter(Emitter):
    """Emits zero or one events per interval
    Events can be spaced regularly, distributed uniformly within the interval, offset according to a normal distribution, or offset according to uniform distribution
    You can use skip_probability to skip events at random
    """

    interval: int
    skip_probability: float
    spacing: IntervalSpacingOption
    normal_offset: Optional[NormalDistributionParams] = None
    uniform_offset: Optional[UniformDistributionParams] = None
    parameter_builders: Dict[str, ParameterBuilder]

    @classmethod
    def define(
        cls,
        event_type_name: str,
        interval: int,
        skip_probability: float = 0.0,
        spacing: Optional[Union[str, IntervalSpacingOption]] = IntervalSpacingOption.START,
        normal_offset: Optional[NormalDistributionParams] = None,
        uniform_offset: Optional[UniformDistributionParams] = None,
        **kwargs,
    ) -> "IntervalEmitter":
        #!!! Instantiate parameter builders
        return  cls(
            event_type_name=event_type_name,
            interval=interval,
            skip_probability=skip_probability,
            spacing=spacing,
            normal_offset=normal_offset,
            uniform_offset=uniform_offset,
            parameter_builders={},
        )
        

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

