from typing import Dict, List, Optional, Union

import numpy as np

from dgpinata.message import Message, AddEvent, AddEntity
from dgpinata.emitters.base import Emitter, ParameterBuilder

class PoissonEmitter(Emitter):
    
    # event_type_name: Optional[str] = None
    # entity_type_name: Optional[str] = None
    rate: Union[int, ParameterBuilder]
    time_interval: Union[int, ParameterBuilder]
    # parameter_builders: Dict[str, ParameterBuilder]

    @classmethod
    def from_params(
        cls,
        event_type_name: Optional[str] = None,
        entity_type_name: Optional[str] = None,
        rate: Optional[Union[int, str]] = None,
        time_interval: Optional[Union[int, str]] = None,
        # parameter_builders: Optional[Dict[str, ParameterBuilder]] = None,
        **kwargs,
    ):
        """Creates a PoissonEmitter from parameters.

        Args:
            event_type_name (Optional[str]): The name of the event type to emit.
            entity_type_name (Optional[str]): The name of the entity type to emit.
            rate (Optional[Union[int, str]]): The rate of the Poisson process.
            time_interval (Optional[Union[int, str]]): The time interval.
            parameter_builders (Optional[Dict[str, ParameterBuilder]]): The parameter builders.

        Returns:
            PoissonEmitter: The PoissonEmitter instance.
        """
        parameter_builders = cls._define_parameter_builders(**kwargs)
        return cls(
            event_type_name=event_type_name,
            entity_type_name=entity_type_name,
            rate=rate,
            time_interval=time_interval,
            parameter_builders=parameter_builders,
        )

    def _get_interval_start_time_list(self, parent: "Entity", prev_timestamp: int, timestamp: int):
        duration = timestamp - prev_timestamp

        # Generate the number of events
        num_events = np.random.poisson(self.rate * duration)

        # Generate event times uniformly in the interval [start_time, end_time]
        points = np.random.uniform(timestamp, prev_timestamp, num_events)

        # Sort the points in ascending order (optional, for easier interpretation)
        points = np.sort(points)

        return points
