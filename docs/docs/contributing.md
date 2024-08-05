# Contributing

## Conventions

* Which files get imported into the `dgpinata` namespace?
* Docs-based testing

## Tests

Currently, most tests are baked into the tutorials section of the documentation. These aren't thorough tests of the full API surface area. Instead, they're more like detailed smoke tests for key features. For a very early-stage project, this is actually a pretty good way to go. As the project matures, we'll need to add more thorough tests.

You can run the tests with the following command, executed from the root of the project:

```bash
pytest
```

## Documentation

The documentation is built using [MkDocs](https://www.mkdocs.org/). You can run the documentation locally with the following command, executed from the `docs/` folder of the project:

```bash
mkdocs serve
```