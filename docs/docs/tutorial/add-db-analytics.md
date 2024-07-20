# Add a database and analytics

We'll start with a basic "hello world" example for a DGP describing a lemonade stand. Imagine a lemonade stand that (drumroll) ... sells lemonade. For starters, all we want to do is track sales.

We start by importing `dgprincess`, using the `dgp` namespace as a shorthand.

```python
import dgprincess as dgp
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
    def update(self, timestamp):
        new_sale = Sale(
            amount = 1,
            timestamp = timestamp,
        )
        return [new_sale], []
```

 To keep things simple for now, `Stand` doesn't have any properties of its own. It only has an `update` method that returns a list of `Events`, and an empty list. (The empty list is for creating additional `Entities`. We'll worry about it later.)
 
 For now, the list of events is just a single `Sale` in every update cycle. `amount` is always 1, and the `timestamp` is just an integer of the update cycle in which the sale occurred.

Finally, we create a `Simulation` object and run it.

```python
sim = dgp.Simulation(
    event_types=[Sale],
    entity_types=[Stand],
)
print(sim.run(steps=10))
```

<!--
```python
assert list(sim.events.keys()) == ["Sale"]
assert len(sim.events["Sale"]) == 10
assert sim.events["Sale"][0] == Sale(amount=1, timestamp=0)
```
-->