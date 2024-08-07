from typing import Dict, Optional, Union

import numpy as np
from dgpinata.emitters.base import Emitter, ParameterBuilder

class GammaEmitter(Emitter):

    # event_type_name: Optional[str] = None
    # entity_type_name: Optional[str] = None
    shape: Union[int, ParameterBuilder]
    scale: Union[int, ParameterBuilder]
    # parameter_builders: Dict[str, ParameterBuilder]

    @classmethod
    def from_params(
        cls,
        event_type_name: Optional[str] = None,
        entity_type_name: Optional[str] = None,
        shape: Optional[Union[int, str]] = None,
        scale: Optional[Union[int, str]] = None,
        **kwargs,
    ):
        """Creates a GammaEmitter from parameters.

        Args:
            event_type_name (Optional[str]): The name of the event type to emit.
            entity_type_name (Optional[str]): The name of the entity type to emit.
            shape (Optional[Union[int, str]]): The shape parameter of the gamma distribution.
            scale (Optional[Union[int, str]]): The scale parameter of the gamma distribution.
            parameter_builders (Optional[Dict[str, ParameterBuilder]]): The parameter builders.

        Returns:
            GammaEmitter: The GammaEmitter instance.
        """
        parameter_builders = cls._define_parameter_builders(**kwargs)
        return cls(
            event_type_name=event_type_name,
            entity_type_name=entity_type_name,
            shape=shape,
            scale=scale,
            parameter_builders=parameter_builders,
        )
    
    def _get_interval_start_time_list(self, parent: "Entity", prev_timestamp: int, timestamp: int):
        duration = timestamp - prev_timestamp

        inter_arrival_times = np.random.gamma(self.shape, 1/self.rate, size=1000)

        # Generate cumulative event times
        event_times = np.cumsum(inter_arrival_times)
        
        # Filter out event times that are beyond the specified interval
        event_times = event_times[event_times < duration]

        # Adjust event times to start from start_time
        event_times = event_times + prev_timestamp

        return event_times