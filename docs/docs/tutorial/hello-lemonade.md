# Hello, lemonade!

We'll start with a basic "hello world" example for a DGP describing a lemonade stand. Imagine a lemonade stand that (drumroll) ... sells lemonade. For starters, all we want to do is track sales.

We start by importing `dgpinata`, using the `dgp` namespace as a shorthand.

```python
import dgpinata as dgp
from typing import Dict
```

Next, we define a `Sale` object, with two properties: `amount` and `timestamp`. It's important that each of these properties is annotated with a type hint. Even with no additional context, DGPinata can use these type hints to guess how to generate the schema for a database table.

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
        "new_sale": dgp.IntervalEmitter.from_params(
            event_type_name="Sale",
            amount=1,
            timestamp="timestamp",
        ),
    }
```

 To keep things simple for now, `Stand` doesn't have any properties of its own. It only has an `emitters` dictionary containing a single entry with the key "new_sale". This entry enables our `Stand` to create `Sale` events.
 
 For now, we just want to create a single `Sale` in every update cycle. `amount` is always 1, and the `timestamp` will be the current timestamp in the simulation.

Finally, we create a `Simulation` object. This object is the backbone of a DGPinata DGP. It manages all the `Entities`, `Events`, and the flow of time. `Simulations` can also handle creating and destroying `Entities`, handing interactions between `Entities`, I/O to our simulation database, and so on&mdash;but we're doing any of those things yet.

```python
sim = dgp.Simulation(
    event_types=[Sale],
    entity_types=[Stand],
)
```

In this case, our `Simulation` is just a thin wrapper that allows us to run the simulation. We create it with two arguments: `event_types` and `entity_types`. `event_types` is a list of all the `Event` types that can be emitted by the simulation. `entity_types` is a list of all the entity types that can emit `Events`.

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

That's it! You've just run your first DGP. In the next section of the tutorial, we'll add some complexity to our lemonade stand by adding a `Customer` entity that buys lemonade, plus additional `Products`.

!!! Tip
    This section of the tutorial introduced the following concepts:

    * [Event](../core-concepts/event.md): something that happens in the real world that could create or update a record in our database.
    * [Entity](../core-concepts/entity.md): a thing in the real world that can emit `Events`.
    * [emitters](../core-concepts/entity.md#emitters): a property of an `Entity` that enables configuration of `Events` to be emitted.
    * [Simulation](../core-concepts/simulation.md): The backbone of a DGP. Manages all the `Entities`, `Events`, and the flow of time.

