"""Shared pytest fixtures for service-clients."""

from __future__ import annotations

import pytest


@pytest.fixture(autouse=True)
def clear_modal_function_cache() -> None:
    """Avoid cross-test pollution from ``lru_cache`` on Modal function lookups."""
    from service_clients.modal_invoker import clear_modal_function_lookup_cache

    clear_modal_function_lookup_cache()
    yield
    clear_modal_function_lookup_cache()
