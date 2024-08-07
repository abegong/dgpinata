# Overwrite an `Entity`'s `update` method

You can overwrite the `_update` method for an `Entity` in order to get finer-grained control over the logic for creating Mess.

```python
import dgpinata as dgp
from dgpinata.message import AddEvent
from dgpinata.emitters.base import ParameterBuilder

class Sale(dgp.Event):
    amount: int
    timestamp: int

class Stand(dgp.Entity):
    def _update(self, prev_timestamp, timestamp):
        print(prev_timestamp, timestamp)
        new_action = AddEvent(
            event_type_name="Sale",
            parameter_builders={
                "amount" : ParameterBuilder(
                    name="amount",
                    value=1
                ),
                "timestamp" : ParameterBuilder(
                    name="timestamp",
                    eval_str="timestamp"
                )
            },
            parent=self,
            timestamp=timestamp,
        )
        return [new_action]

sim = dgp.Simulation(
    event_types=[Sale],
    entity_types=[Stand],
)
print(sim.run(10))
```


<!--
```python
assert list(sim.events.keys()) == ["Sale"]
assert len(sim.events["Sale"]) == 10
assert sim.events["Sale"][0] == Sale(amount=1, timestamp=3600)
assert str(sim.get_report()) == """\
=== Entities ===
  Stand: 1

=== Events ===
  Sale: 10
"""
```
-->