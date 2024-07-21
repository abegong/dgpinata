# Add customers

```python
from faker import Faker
import random
from uuid import uuid4
from pydantic import Field

import dgprincess as dgp

faker = Faker()

class Customer(dgp.StaticEntity):
    customer_id: str = Field(default_factory=lambda: str(uuid4()))
    first_name: str = Field(default_factory=faker.first_name)
    last_name: str = Field(default_factory=faker.last_name)
    created_at: int

    default_values = []

class Sale(dgp.Event):
    sale_id: str = Field(default_factory=lambda: str(uuid4()))
    customer_id: str
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
        if random.random() < 0.2 or len(self.sim.entities["Customer"]) == 0:
            customer = Customer(
                simulation = self.sim,
                created_at = timestamp,
            )
            new_customers = [customer]
        
        else:
            customer = random.choice(self.sim.entities["Customer"])
            new_customers = []
        
        new_sale = Sale(
            product_id = random.choice(self.sim.entities["Product"]).product_id,
            customer_id = customer.customer_id,
            amount = 1,
            timestamp = timestamp,
        )
        return [new_sale], new_customers

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
  Customer: 21
  Product: 3

=== Events ===
  Sale: 100
"""
```
-->