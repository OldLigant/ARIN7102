"""Lazy import layer for the optional query_intelligence dependency.

Keeps the cross-package import out of preprocessor.py so the dependency
boundary is explicit and centralized.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from query_intelligence.data_loader import load_seed_entities, load_seed_aliases
    from query_intelligence.nlu.entity_resolver import EntityResolver

logger = logging.getLogger(__name__)

_entity_resolver_cls: type | None = None
_load_seed_entities = None
_load_seed_aliases = None
_import_attempted = False


def _ensure_loaded() -> bool:
    """Attempt to import query_intelligence once; return whether it succeeded."""
    global _entity_resolver_cls, _load_seed_entities, _load_seed_aliases, _import_attempted
    if _import_attempted:
        return _entity_resolver_cls is not None
    _import_attempted = True
    try:
        from query_intelligence.data_loader import load_seed_entities, load_seed_aliases
        from query_intelligence.nlu.entity_resolver import EntityResolver
        _entity_resolver_cls = EntityResolver
        _load_seed_entities = load_seed_entities
        _load_seed_aliases = load_seed_aliases
    except ImportError:
        logger.debug("query_intelligence not available — entity resolver disabled")
    return _entity_resolver_cls is not None


def get_entity_resolver_cls() -> type | None:
    """Return the EntityResolver class, or None if query_intelligence is unavailable."""
    if _ensure_loaded():
        return _entity_resolver_cls
    return None


def load_seed_data() -> tuple[list | None, list | None]:
    """Load seed entities and aliases, or (None, None) if unavailable."""
    if _ensure_loaded():
        return _load_seed_entities(), _load_seed_aliases()
    return None, None
