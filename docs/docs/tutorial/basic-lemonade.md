# Hi, this is a basic lemonade examples


```python
from pydantic import Field
import random
from typing import ClassVar, Dict, List, Tuple
from uuid import uuid4

from dgprincess.simulation import Simulation
from dgprincess.entity import Entity, StaticEntity
from dgprincess.event import Event

class Sale(Event):
    sale_id: str = Field(uuid4, title="ID of the sale")
    stand_id: str = Field(..., title="ID of the stand where the sale was made")
    product_id: str = Field(..., title="ID of the product sold")
    timestamp: int = Field(..., title="Timestamp of the sale")

    table_name: ClassVar[str] = "sales"

    dependencies: ClassVar[Dict[str, str]] = {
        "Stand": "stand_id",
        "Product": "product_id",
    }

class Product(StaticEntity):
    product_id: str = Field(uuid4, title="ID of the product")
    name: str = Field(..., title="Name of the product")
    price: float = Field(..., title="Price of the product")

    default_values: ClassVar[List[Dict]] = [
        {"name": "Lemonade", "price": 2.0},
        {"name": "Iced Tea", "price": 2.5},
        {"name": "Water", "price": 1.0},
    ]

class Stand(Entity):
    stand_id: str = Field(str(uuid4()), title="ID of the stand")
    name: str = Field(..., title="Name of the stand")
    products: List[str] = Field(..., title="List of product IDs")

    default_values: ClassVar[List[Dict]] = [
        {"name": "Main Stand", "products": ["Lemonade", "Iced Tea", "Water"]},
        {"name": "Secondary Stand", "products": ["Lemonade", "Water"]},
    ]

    dependencies: ClassVar[Dict[str, str]] = {
        "Product": "product_id"
    }

    def update(self, elapsed_time: int) -> Tuple[List[Event], List[Entity]]:
        sales = []
        for i in range(elapsed_time):
            if random.random() > 0.9:
                product = random.choice(self.products)
                sale = Sale(stand_id=self.stand_id, product_id=product, timestamp=i)
                sales.append(sale)

        return sales, []

if __name__ == "__main__":
    sim = Simulation(
        entity_types=[Stand, Product],
        event_types=[Sale],
        duration=1000,
        interval=1,
    )
    sim.init()
    # sim.pprint()
    sim.run()
    sim.print_summary()
    sim.export("lemonade.db", overwrite=True)
```