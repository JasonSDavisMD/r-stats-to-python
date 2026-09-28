# Contributing

Thank you for helping improve this reference. There are two parts:

* **The guide** (`README.md`): narrative R-to-Python translations.
* **The statsbench toolkit** (`workbench/`): the searchable catalog behind
  `stats find`, worked examples, and helpers.

## Reporting an issue

Use the issue forms (**Issues -> New issue**):

* **Request or correct a catalog entry**: a task, R function, or Python call
  that is missing or wrong.
* **Bug report**: something in setup, the toolkit, or an example fails.

For guide corrections, include the section, the R operation, the current
Python translation, the proposed correction, and supporting documentation.

## Adding or correcting catalog entries

Most contributions are a few lines of TOML in
`workbench/src/statsbench/catalog/<topic>.toml`. Field reference and steps:
[`workbench/docs/adding-a-topic.md`](workbench/docs/adding-a-topic.md).

```bash
cd workbench
uv sync --all-extras          # core + optional add-ons, so every example can run
uv run pytest                 # runs every catalog example against real library versions
uv run stats find "<the phrase a user would type>"
```

The tests treat `FutureWarning` and `DeprecationWarning` as failures, so
outdated APIs never enter the catalog. CI repeats the tests on Linux, Windows
and macOS for every pull request.

## Submitting a change

1. Fork the repository and create a branch.
2. Make and verify your changes (`uv run pytest` in `workbench/`).
3. Open a pull request and complete the checklist in the template.
4. Explain why the change is more accurate or useful.

## Style

- Label R and Python examples explicitly. Use `=` for assignment in R examples.
- Include required imports; examples must run on their own.
- Prefer readable statistical code over condensed code.
- Explain important differences in defaults or interpretation.
- Use synthetic or openly licensed data only.
- **Never include homework or exam answers, copyrighted course materials,
  private data, or any patient information.**
