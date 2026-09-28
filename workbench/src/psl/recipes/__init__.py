"""Course recipes: thin helpers only where no single library call exists.

Rule for adding one (see docs/adding-a-topic.md): the helper must document
the exact library call it wraps, return plain data or the original library
object, and have a focused test. Each recipe lives in its own module so a
bug in one cannot break an import of another.
"""
