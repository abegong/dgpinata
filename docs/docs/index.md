# DGPinata

*Generate realistically messy multitable datasets.*

There are quite a few libraries that can generate synthetic data. However, they tend to generate data that is too clean.

Real data is messy. Real data is dirty. Real data is broken. Real data is inconsistent. Real data was collected in different formats along the way, that now sprawl across multiple tables, with incomplete backfills and lossy migrations.

DGPinata is a library for generating synthetic data that captures the messiness and complexity of real data. It does this by simulating a Data Generating Process (DGP) for data over time. The DGP can change over time, leading to changes in the data.

## Installation

```bash
git clone git@github.com:abegong/dgpinata.git
pip install dgpinata
```

## Why DGPinata?

DGP is short for [Data Generating Process](https://stats.stackexchange.com/questions/443320/what-does-a-data-generating-process-dgp-actually-mean): the things that happen in the real world in order to create data that later gets processed for analysis. A DGP can be as simple as a random number generator or as complex as a full-fledged simulation of a business process.

Most data-synthesis libraries take a database schema, JSON structure, etc. as input and generate rows to populate a corresponding table. This is fine as far as it goes, but it assumes that the data of interest lives in a single table and that the DGP stays the same forever.

In contrast to these libraries, DGPinata takes an [agent-based modeling](https://en.wikipedia.org/wiki/Agent-based_model) approach. [Entities](core-concepts/entity.md) in the DPG have state and can change over time. [Events](core-concepts/event.md) from the DGP can generate rows in multiple tables.

This allows DGPinata to simulate more realistic DGPs, including changes in the DGP over time.

## Yes, but why "pinata"?

Because when you hit it, delicious data scatters everywhere.