# Add More Products

Next, we'll add more products to the simulation. In this section, we're going to use typing, so let's start by importing the necessary modules.

```python
import random
from uuid import uuid4
from pydantic import Field

import dgprincess as dgp
```

We'll also add a `Product` entity type to represent the products. In our simulation, `Products` have a `product_id`, a `name`, and a `price`.

```python
class Product(dgp.StaticEntity):
    product_id: str = Field(default_factory=lambda: str(uuid4()))
    name: str
    price: float

    default_values = [
        {"name": "Lemonade", "price": 2.50},
        {"name": "Iced Tea", "price": 3.75},
        {"name": "Water", "price": 0.50},
    ]
```

A few things to note about the `Product` entity type:

* We're using the `StaticEntity` class, which means that the entity is created once and never changes. This save us having to define an `update` method with nothing in it.
* We're using the `Field` class from Pydantic to define the fields of the entity. The `default_factory` argument allows us to generate a unique `product_id` for each product. In this case, we're using the `uuid4` function from the `uuid` module.
* We're using the `default_values` class attribute to define the initial products in the simulation. When you initialize it, the `Simulation` class will automatically create instances of the `Product` entity type with these values.

Now that we have the `Product` class and we know how to use ids, we may as well apply what we've learned to the `Sale` event type.

```python
class Sale(dgp.Event):
    sale_id: str = Field(default_factory=lambda: str(uuid4()))
    product_id: str
    amount: int
    timestamp: int
```

This is the same as before, but adds fields for `sale_id` and `product_id`. `sale_id` is automatically populated with a unique id when the event is created, and `product_id` is a reference to the `product_id` of the product being sold.

Finally, we'll add a `Stand` entity type to represent the stands that sell the products. In our simulation, `Stands` don't have any attributes, but they can generate `Sales`.

```python
class Stand(dgp.Entity):

    def update(self, timestamp):
        chosen_product = random.choice(self.simulation.entities["Product"])
        new_sale = Sale(
            product_id = chosen_product.product_id,
            amount = 1,
            timestamp = timestamp,
        )
        return [new_sale], []
```

```python
from dgprincess.simulation import Simulation
Product.model_rebuild()
```

```python
sim = dgp.Simulation(
    event_types=[Sale],
    entity_types=[Stand, Product],
)

print(sim.run(steps=10))
```

<!--
```python
assert list(sim.events.keys()) == ["Sale"]
assert len(sim.events["Sale"]) == 10
assert str(sim.get_report()) == """\
=== Entities ===
  Stand: 1
  Product: 3

=== Events ===
  Sale: 10
"""
```
-->