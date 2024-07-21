from dgprincess import Event
from dgprincess import Emitter, IntervalEmitter

def test_smoke_interval_emitter():
    class MyEvent(Event):
        foo: int
        bar: int

    emitter = IntervalEmitter.define(
        event_type_name="MyEvent",
        interval=3600,
        offset=0,
        skip_probability=0.8,
        created_at="timestamp",
    )


# "add_customer": IntervalEmitter(
#     event_type=Customer,
#     interval=3600,
#     offset=0,
#     skip_probability=0.8,
#     created_at="timestamp",
# ),
# "add_sale": IntervalEmitter(
#     event_type=Sale,
#     interval=3600,
#     -- offset=lambda: random.randint(),
#     product_id=RandomChoice("sim.Entities['Product']"),
#     customer_id=RandomChoice("sim.Entities['Customer']"),
#     amount=1,
#     timestamp="timestamp",
# ),
# "add_customer_with_new_sale": IntervalEmitter(
#     interval=3600,
#     offset=0,
#     events=[
#         EventGenerator(
#             event_type=Customer,
#             var_name="new_customer",
#             skip_probability=0.8,
#             created_at="timestamp",
#         ),
#         EventGenerator(
#             event_type=Sale,
#             product_id=RandomChoice("sim.Entities['Product']"),
#             customer_id=SyntaxChooser("new_customer.customer_id"),
#             amount=1,
#             timestamp="timestamp",
#         ),
#     ]
# ),