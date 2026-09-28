# Maintainers' guide: adding a function, a topic, an example, or a recipe

No VS Code extension and no central program to edit. Everything is a small,
separate file.

## Add a function to an existing topic

1. Open the topic file, e.g. `catalog/trees.toml`, and copy an existing `[[entry]]`.
2. Fill in the fields (reference below). Keep `example` short and
   **self-contained**: it must import everything it uses and run on its own.
3. Test it:

   ```powershell
   uv run pytest tests/test_catalog.py -q
   uv run psl find "<a phrase you would type>"
   ```

   The test executes your example against the installed library versions.
   It fails on a `FutureWarning` or `DeprecationWarning`, so outdated APIs
   never enter the catalog.
4. If your phrasing doesn't come up first, add it to `aliases`. Optionally
   add it as a case in `tests/test_search.py`.

## Add a new topic

Create `catalog/<topic>.toml`. The file name becomes the topic name (`psl
list --topic <topic>`). Start the file with a comment line stating the topic's
key distinction, as the existing files do. No registration step is needed.
If a file has a syntax error, only that file is skipped, and the problem is
reported as a warning by `psl` and by `python -m psl.envcheck`.

## Entry fields

| Field | Required | Meaning |
|---|---|---|
| `id` | yes | Unique short name used by `psl show` and `see_also` (kebab-case) |
| `title` | yes | One line: the task, in words you'd search for |
| `kind` | yes | `fit`, `evaluate`, `optimize`, `solve`, `compute` or `visualize` (see operation-kinds.md) |
| `library` | yes | Display name, e.g. `SciPy` |
| `import` | yes | Exact import line(s); use `\n` between lines |
| `call` | yes | The exact callable with typical arguments |
| `example` | yes | Runnable, self-contained code (TOML `'''...'''` literal string) |
| `docs` | yes | Official documentation URL (https) |
| `aliases` | no | Other phrasings, including concept names |
| `r` | no | R equivalents, e.g. `"plogis"`, `"MASS::lda"`, `"glm(family = binomial)"` |
| `inputs` / `returns` | no | What goes in and what comes out (types and meaning) |
| `caveats` | no | Differences from R defaults, tie rules, common mistakes |
| `see_also` | no | Related entry ids (must exist; tested) |
| `recipe` | no | Path to a worked example in `examples/` (must exist; tested) |

## Add a worked example

Copy `templates/exercise.py` to `examples/NN_topic.py` and keep the section
order: **Given, Operation requested, Library choice, Code, What the output
means, Validation checks** (with `assert`s). Use synthetic, seeded data. Never
put assignment answers in the repository. `tests/test_examples.py` runs every
file in `examples/` automatically.

## Add a recipe (rarely)

Only add a helper to `src/psl/recipes/` when **no single library call**
performs the step. `best_subset` exists because scikit-learn has no
exhaustive subset search. A recipe must:

* live in its own module, so an error in it can't break other imports;
* say in its docstring the exact library call it wraps;
* return plain data or the original library object, and never hide the method;
* have a focused test of *its own* logic, not re-test the library.
