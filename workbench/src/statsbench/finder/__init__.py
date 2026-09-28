"""Task-to-tool finder: ``from statsbench.finder import find`` works inside notebooks.

    >>> from statsbench.finder import find
    >>> for hit in find("R plogis"):
    ...     print(hit.entry.id, hit.entry.call)
"""

from .catalog import KINDS, Catalog, Entry, load_catalog
from .search import Hit, Index, find

__all__ = ["KINDS", "Catalog", "Entry", "Hit", "Index", "find", "load_catalog"]
