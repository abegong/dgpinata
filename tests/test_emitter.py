from dgpinata import Event
from dgpinata import Emitter, IntervalEmitter
from dgpinata.action import AddEvent

def _extract_event_timestamps(events):
    return [event.timestamp for event in events]

def test__interval_emitter__from_params():
    # class MyEvent(Event):
    #     foo: int
    #     bar: int

    emitter = IntervalEmitter.from_params(
        event_type_name="MyEvent",
        interval=3600,
        offset=0,
        skip_probability=0.8,
        created_at="timestamp",
    )

def test__interval_emitter__interval_ranges():

    emitter = IntervalEmitter.from_params(
        event_type_name="SomeEvent",
        interval=60,
    )

    # If no time has elapsed, no events are emitted
    assert len(emitter.emit(
        parent=None,
        prev_timestamp=0,
        timestamp=0
    )) == 0

    # If a partial interval has elapsed, one event is emitted
    assert len(emitter.emit(
        parent=None,
        prev_timestamp=0,
        timestamp=30
    )) == 1

    # If a full interval has elapsed, an event is emitted
    assert len(emitter.emit(
        parent=None,
        prev_timestamp=0,
        timestamp=60
    )) == 1

    # If multiple intervals have elapsed, multiple events are emitted
    assert len(emitter.emit(
        parent=None,
        prev_timestamp=0,
        timestamp=120
    )) == 2

    # If multiple intervals have elapsed, multiple events are emitted
    assert len(emitter.emit(
        parent=None,
        prev_timestamp=0,
        timestamp=3600
    )) == 60

    # Intervals are inclusive
    assert len(emitter.emit(
        parent=None,
        prev_timestamp=60,
        timestamp=120
    )) == 1

    # assert emitter.emit(
    #     parent=None,
    #     prev_timestamp=0,
    #     timestamp=0
    # )[0] == AddEvent(
    #     event_type_name="SomeEvent",
    #     parameter_builders={},
    #     parent=None,
    #     timestamp=0,
    # )
    # print(emitter.emit(parent=None, timestamp=1))
    # print(emitter.emit(parent=None, timestamp=3600))

    # assert False


    # If a full interval has elapsed, an event is emitted
    # If multiple intervals have elapsed, multiple events are emitted

def test__interval_emitter__skip_probability():
    # If `skip_probability` is 0, all events are emitted
    # If `skip_probability` is 1, no events are emitted
    # If `skip_probability` is 0.5, half of the events are emitted
    pass

    # Space events by `spacing`

    # Event timestamps should be offset by `offset`
    # `offset` can be a fixed value or a callable



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