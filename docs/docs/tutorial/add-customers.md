# Add customers

```python
from faker import Faker
import random
from typing import Dict
from uuid import uuid4
from pydantic import Field

import dgprincess as dgp

faker = Faker()

class Customer(dgp.Entity):
    customer_id: str = Field(default_factory=lambda: str(uuid4()))
    first_name: str = Field(default_factory=faker.first_name)
    last_name: str = Field(default_factory=faker.last_name)
    created_at: int

    emitters : Dict = {
        "new_sale" : dgp.IntervalEmitter.from_params(
            event_type_name="Sale",
            skip_probability=0.90,
            customer_id = "parent.customer_id",
            product_id = dgp.RandomObjectAttributeChooser(
                object_eval_str='sim.entities["Product"]',
                attribute="product_id"
            ),
            amount = 1,
            timestamp = "timestamp",
        )
    }

    default_values = [
        {"first_name": "Alfred", "last_name": "Adams", "created_at": 0}
    ]

class Sale(dgp.Event):
    sale_id: str = Field(default_factory=lambda: str(uuid4()))
    customer_id: str
    product_id: str
    amount: int
    timestamp: int

class Product(dgp.Entity):
    product_id: str = Field(default_factory=lambda: str(uuid4()))
    name: str
    price: float

    default_values = [
        {"name": "Lemonade", "price": 2.50},
        {"name": "Iced Tea", "price": 3.75},
        {"name": "Water", "price": 0.50},
    ]

class Stand(dgp.Entity):

    emitters : Dict = {
        "new_customer" : dgp.IntervalEmitter.from_params(
            entity_type_name="Customer",
            skip_probability=0.8,
            created_at="timestamp",
        )        
    }

from dgprincess.simulation import Simulation
Product.model_rebuild()
Customer.model_rebuild()

sim = dgp.Simulation(
    event_types=[Sale],
    entity_types=[Stand, Customer, Product],
    rand_seed=42,
)
print(sim.run(steps=100))
```

<!--
```python
assert str(sim.get_report()) == """\
=== Entities ===
  Stand: 1
  Customer: 22
  Product: 3

=== Events ===
  Sale: 103
"""
```
-->