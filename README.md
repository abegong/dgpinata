# DGPrincess
*Generate realistically messy multitable datasets.*

There are quite a few libraries that can generate synthetic data. However, they tend to generate data that is too clean.

Real data is messy. Real data is dirty. Real data is broken. Real data is inconsistent. Real data is incomplete. Real data is wrong. Also, real data usually has multiple tables.

DGPrincess is a library for generating synthetic data that captures the messiness and complexity of real data. It does this by simulating a Data Generating Process (DGP) for data over time. The DGP can change over time, leading to changes in the data.

## Installation

```bash
git clone git@github.com:abegong/dgprincess.git
pip install dgprincess
```

## Why DGPrincess?

DGP is short for Data Generating Process: the things that happen in the real world in order to create data that later gets processed for analysis. real-world process that generates data. A DGP can be as simple as a random number generator or as complex as a full-fledged simulation of a business process.

Most data-synthesis libraries take a database schema, JSON structure, etc. as input and generate rows to populate a corresponding table. This is fine as far as it goes, but it assumes that the data of interest lives in a single table and that the DGP stays the same forever.

In contrast to these libraries, DGPrincess takes an agent-based modeling approach. Entities in the DPG have state and can change over time. Events in the DGP can generate rows in multiple tables.

This allows DGPrincess to simulate more realistic DGPs, including changes in the DGP over time.

## Yes, but why "princess"?

A proper princess is not put off by a little dirt. She is not afraid to get her hands dirty. She can deal with the world as it is, not as she wishes it to be.