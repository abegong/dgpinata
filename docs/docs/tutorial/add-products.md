# Add Customers and Products

```python
import random
from uuid import uuid4
from pydantic import Field

import dgprincess as dgp

class Sale(dgp.Event):
    sale_id: str = Field(default_factory=lambda: str(uuid4()))
    product_id: str
    amount: int
    timestamp: int

class Product(dgp.StaticEntity):
    product_id: str = Field(default_factory=lambda: str(uuid4()))
    name: str
    price: float

    default_values = [
        {"name": "Lemonade", "price": 2.50},
        {"name": "Iced Tea", "price": 3.75},
        {"name": "Water", "price": 0.50},
    ]

class Stand(dgp.Entity):

    def update(self, timestamp):
        chosen_product = random.choice(self.simulation.entities["Product"])
        new_sale = Sale(
            product_id = chosen_product.product_id,
            amount = 1,
            timestamp = timestamp,
        )
        return [new_sale], []

from dgprincess.simulation import Simulation
Product.model_rebuild()

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