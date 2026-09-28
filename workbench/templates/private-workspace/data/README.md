# data/

Put local data files here. **Everything in this folder except this README is
ignored by Git**, so data isn't pushed by accident, even to a private repository.

Before you put data anywhere in the cloud (GitHub, Codespaces, Binder):

* **No protected health information (PHI) or other identifiable patient
  data** unless your institution has explicitly approved that service for it.
  A private GitHub repository is *not* an approved clinical data store by default.
* Prefer de-identified, synthetic, or publicly released datasets.
* Course-provided data may have its own sharing rules; check them.

To version a small, shareable dataset on purpose, force-add it:
`git add -f data/example.csv`.
