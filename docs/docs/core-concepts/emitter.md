# Emitters

Emitters are objects that generate events. They are the primary way to interact with the simulation. Emitters can be as simple as a single event that occurs at a fixed time, or as complex as a series of events that occur at random intervals, with random attributes.

DGPinata supports three types of emitters:

* IntervalEmitter
* PoissonEmitter
* GammaEmitter

## IntervalEmitter

The `IntervalEmitter` is the most flexible emitter. It generates events at regular intervals, with several options to add randomness to the timing

## PoissonEmitter

The `PoissonEmitter` generates events according to a Poisson distribution. This distribution is useful for modeling events that occur at random intervals

## GammaEmitter

The `GammaEmitter` generates events according to a Gamma distribution. This distribution is useful for modeling events, but with a cooldown period between them.

## Creating new Emitters

To create a new emitter, you can use the `Emitter` class. This class has a single method, `emit`, which generates a new event. You can subclass `Emitter` to create your own emitters.

```python
from dgpinata import Emitter

class MyEmitter(Emitter):
    def emit(self, timestamp):
        # Your code here
        pass
```

