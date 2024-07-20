# Overview of Core Concepts

## Entities

Entities are the core building blocks of the Data Generating Process (DGP). Each entity represents an object in the real world that can change over time. For example, a user, a product, or a company.

Entities have state. The state of an entity can change over time. For example, a user can change their email address, a product can change its price, or a company can change its name.

## Events

Entities can emit events. An event is a change in the state of an entity that is captured in the database. For example, a user signing up for a service, a product being added to a shopping cart, or a company changing its name.

## Simulation

The simulation is the process of generating data over time. The simulation is driven by the entities and events in the DGP. The simulation can be run for a fixed number of time steps or until a stopping condition is met.

You will usually only have a single Simulation.

## Other important concepts

### `update` methods

### emitting events

### Timestamps

### Random number seeds