# Add more products

In this section, we'll add the concept of a product to the simulation.

Let's start by importing some modules that we'll need.

```python
import random
from typing import Dict
from uuid import uuid4
from pydantic import Field

import dgpinata as dgp
```

!!! Info
    DGPinata uses `pydantic` for type checking. Deep knowledge of type systems and `pydantic` isn't necessary to work with DGPinata. If you want to learn about them, the [Pydantic documentation](https://docs.pydantic.dev/latest/) is a good place to start.

Next, let's add a `Product` entity type to represent the products that our lemonade stand sells. In our simulation, `Products` have a `product_id`, a `name`, and a `price`.

```python
class Product(dgp.Entity):
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

* We're using the `Field` class from Pydantic to define the fields of the entity. The `default_factory` argument allows us to generate a unique `product_id` for each product. In this case, we're using the `uuid4` function from the `uuid` module.
* The `default_values` class attribute defines which products we want to include by default. When you initialize it, the `Simulation` class will automatically create instances of the `Product` entity type with these values.

Now that we have the `Product` class and we know how to use ids, we can apply what we've learned to the `Sale` event type as well.

```python
class Sale(dgp.Event):
    sale_id: str = Field(default_factory=lambda: str(uuid4()))
    product_id: str
    amount: int
    timestamp: int
```

This is the same as before, but adds fields for `sale_id` and `product_id`. `sale_id` is automatically populated with a unique id when the event is created, and `product_id` is a reference to the `product_id` of the product being sold.

Finally, we'll update the `Stand` entity type, to incorporate `Products` into the logic for emitting `Sales` events.

```python
class Stand(dgp.Entity):

    emitters : Dict = {
        "new_sale" : dgp.IntervalEmitter.from_params(
            event_type_name="Sale",
            product_id = dgp.RandomObjectAttributeChooser(
                object_eval_str='sim.entities["Product"]',
                attribute="product_id"
            ),
            amount = 1,
            timestamp = "timestamp",
        )
    }
```

This code adds a new `Emitter` to the `Stand` entity type. The `new_sale` emitter emits `Sale` events, and uses a `RandomObjectAttributeChooser` to select a random product from the `Product` entity type. The `amount` field is set to 1, and the `timestamp` field is set to the current timestamp.

Finally, let's update the `Simulation` class to include the `Product` entity type.

```python
sim = dgp.Simulation(
    event_types=[Sale],
    entity_types=[Stand, Product],
)

print(sim.run(steps=10))
```

That's it! We've added products to our simulation, and now our lemonade stand can sell lemonade, iced tea, and water. In the next section, we'll add the concept of a customer to the simulation, and learn how to use some other features of DGPinata.

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

!!! Tip
    This section of the tutorial introduced the following concepts:

    * [Fields]() : A concept from `pydantic` that allows you to define the fields of a `BaseModel.` In DGPinata, you can use Fields within `Event`s and `Entity` class.
    * [default_values](../core-concepts/entity.md): a way to define default values for an `Entity`.
    * [Choosers](../core-concepts/emitter.md): a way for an `Entity` to emit `Events`.

