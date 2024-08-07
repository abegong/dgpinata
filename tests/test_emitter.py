import random

from dgpinata.emitters.interval import IntervalEmitter
from dgpinata.emitters.poisson import PoissonEmitter
from dgpinata.emitters.gamma import GammaEmitter

def _extract_event_timestamps(events):
    return [event.timestamp for event in events]

def test__interval_emitter__from_params():

    emitter = IntervalEmitter.from_params(
        event_type_name="MyEvent",
        interval=3600,
        offset=0,
        skip_probability=0.8,
        created_at="timestamp",
    )

def test__poisson_emitter__from_params():
    
    emitter = PoissonEmitter.from_params(
        event_type_name="MyEvent",
        rate=1,
        time_interval=3600,
        created_at="timestamp",
    )

def test__gamma_emitter__from_params():
    
    emitter = GammaEmitter.from_params(
        event_type_name="MyEvent",
        shape=1,
        scale=1,
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

    # If exactly one full interval has elapsed, then exactly one event is emitted
    assert len(emitter.emit(
        parent=None,
        prev_timestamp=0,
        timestamp=60
    )) == 1

    # If more than one full interval has elapsed, then two events are emitted
    assert len(emitter.emit(
        parent=None,
        prev_timestamp=0,
        timestamp=61
    )) == 2

    # If multiple intervals have elapsed, multiple events are emitted
    assert len(emitter.emit(
        parent=None,
        prev_timestamp=0,
        timestamp=200
    )) == 4

    # If multiple intervals have elapsed, multiple events are emitted
    assert len(emitter.emit(
        parent=None,
        prev_timestamp=0,
        timestamp=3600
    )) == 60

    # Intervals are inclusive of `prev_timestamp` and exclusive of `timestamp`
    assert len(emitter.emit(
        parent=None,
        prev_timestamp=60,
        timestamp=120
    )) == 1

def test__interval_emitter__skip_probability():
    random.seed(1)
    
    # If `skip_probability` is 0, all events are emitted
    emitter = IntervalEmitter.from_params(
        event_type_name="SomeEvent",
        interval=60,
        skip_probability=0.0,
    )
    assert len(emitter.emit(
        parent=None,
        prev_timestamp=0,
        timestamp=3600
    )) == 60

    # If `skip_probability` is 1, no events are emitted
    emitter = IntervalEmitter.from_params(
        event_type_name="SomeEvent",
        interval=60,
        skip_probability=1.0,
    )
    assert len(emitter.emit(
        parent=None,
        prev_timestamp=0,
        timestamp=3600
    )) == 0

    # If `skip_probability` is 0.5, half of the events are emitted
    emitter = IntervalEmitter.from_params(
        event_type_name="SomeEvent",
        interval=60,
        skip_probability=0.5,
    )
    assert len(emitter.emit(
        parent=None,
        prev_timestamp=0,
        timestamp=3600
    )) == 37