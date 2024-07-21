# Hello, lemonade!

We'll start with a basic "hello world" example for a DGP describing a lemonade stand. Imagine a lemonade stand that (drumroll) ... sells lemonade. For starters, all we want to do is track sales.

We start by importing `dgprincess`, using the `dgp` namespace as a shorthand.

```python
import dgprincess as dgp
from typing import Dict
```

Next, we define a `Sale` object, with two properties: `amount` and `timestamp`. It's important that each of these properties is annotated with a type hint. Even with no additional context from us, DGPrincess can use these type hints to guess how to generate the schema for a database table.

```python
class Sale(dgp.Event):
    amount: int
    timestamp: int
```

`Sale` is an `Event`, which means it describes something that happens in the real world that could create or update a record in our database. In this case, it's a sale of lemonade. `amount` is the amount of lemonade sold, and the `timestamp` is the time of the sale.

In order to emit an `Event`, we need an `Entity`. In this case, we define the `Stand` class as a barebones `Entity`.

```python
class Stand(dgp.Entity):
    emitters : Dict = {
        "new_sale": dgp.IntervalEmitter.define(
            interval="self.interval",
            event_type_name="Sale",
            amount=1,
            timestamp="timestamp",
        ),
    }
```

 To keep things simple for now, `Stand` doesn't have any properties of its own. It only has an `update` method that returns a list of `Events`, and an empty list. (The empty list is for creating additional `Entities`. We'll worry about it later.)
 
 For now, the list of events is just a single `Sale` in every update cycle. `amount` is always 1, and the `timestamp` is just an integer of the update cycle in which the sale occurred.

Finally, we create a `Simulation` object and run it.

```python
sim = dgp.Simulation(
    event_types=[Sale],
    entity_types=[Stand],
)
```

The `Simulation` object is the backbone of a DGPrincess DGP. It manages all the `Entities`, `Events`, and the flow of time. It also handles creating and destroying `Entities`, handing interactions between `Entities`, I/O to our simulation database, and so on---but we're doing any of those things yet.

In this case, it's just a thin wrapper that allows us to run the simulation. We create it with two arguments: `event_types` and `entity_types`. `event_types` is a list of all the `Event` types that can be emitted by the simulation. `entity_types` is a list of all the entity types that can emit `Events`.

We run the simulation with a simple call to `run`. `print`ing the result will give us a summary of the simulation.
```python
print(sim.run(steps=10))
```

You should see something like this:

```
=== Entities ===
  Stand: 1

=== Events ===
  Sale: 10
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

That's it! You've just run your first DGP. In the next tutorial, we'll add some complexity to our lemonade stand by adding a `Customer` entity that buys lemonade, plus additional `Products`.