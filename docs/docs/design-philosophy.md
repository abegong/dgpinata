As I've started building DGPinata, I've made a few explicit design decisions.

* **Progressive disclosure of complexity**
* **Focus on the things that leave a paper trail.**
* **Built to be an AI tool.**

Please take these with a grain of salt. This is a young project, and I expect to learn and adjust as I go along. Being explicit and wrong is one of the fastest ways to learn. Being explicit and right is one of the fastest ways to teach.

## Progressive disclosure of complexity

New users should be able to start with a simple DGP and add complexity as they need it. They should only need to learn new concepts when they need them.

How DGPinata does this:

* *Documentation*: The main tutorial starts with a simple example, and adds complexity as it goes along.
* *Architecture*: I've opted for a small number of abstractions that can be combined in many ways. They tend to be modular and composable.
* *Sensible defaults*: Almost everything works right out of the box, with a minimum of configuration. You can always figure out how to override the defaults later.
* *Paramaterizability*: Most objects can be fully configured with parameters, so that you can change the behavior of the object without writing code or changing the object itself.
* *User-facing APIs can usually infer types*: You don't need to know all of DGPinata's internal types in order to use its APIs. You can usually just pass in a string or dict or whatever, and the object will figure out what you mean. If there's any ambiguity, the object will raise an informative error.

## Focus on the things that leave a paper trail

IMO, one of the major weaknesses of most agent-based modeling libraries is that they pack too many assumptions into an imaginary, unobservable world. Suppose we assume that "agents move around on a 2D grid." Now we need to make a whole bunch of assumptions about movement: how fast agents move, what they can see, how they decide where to go, how they avoid each other, etc.

This can make for good eye candy, but it leads to complex simluations that are disconnected from any kind of measurable reality. As a result, ABMs have mostly been useful for quantitative thought experiments, not making falsifiable predictions.

In contrast, DGPinata is designed to focus on the things that leave a paper trail. That is, things that can be measured and recorded.

If you're just using DGPinata to generate data, this is great: it lets you focus only on the aspects of the simulation required to generate the data you need.

Someday, I can imagine DGPinata being useful for other applications as well: digital twins, for example. In that case, the focus on the things that leave a paper trail could be very helpful for building models that integrate tightly with empirics.


## Built to be an AI tool

This is the squishiest of the three, because AI is evolving so quickly. Still, it's good to state the goal.

I'm building DGPinata to be usable as a tool for AI. That is, AI to be able to use DGPinata extend the DGP in ways that are hard to do by hand.