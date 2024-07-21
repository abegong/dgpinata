# Overwrite an `Entity`'s `update` method

You can overwrite the `update` method for an `Entity` in order to get finer-grained control over the logic for creating Events and Actions.

```python
import dgprincess as dgp

class Sale(dgp.Event):
    amount: int
    timestamp: int

class Stand(dgp.Entity):
    def update(self, timestamp):
        new_sale = Sale(
            amount = 1,
            timestamp = timestamp,
        )
        return [new_sale], []

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
assert sim.events["Sale"][0] == Sale(amount=1, timestamp=0)
assert str(sim.get_report()) == """\
=== Entities ===
  Stand: 1

=== Events ===
  Sale: 10
"""
```
-->