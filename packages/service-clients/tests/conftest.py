"""Shared pytest fixtures for service-clients."""

from __future__ import annotations

import pytest


def pytest_configure(config: pytest.Config) -> None:
    """Register markers when pytest is invoked from the monorepo backend (no local pyproject markers)."""
    for line in (
        "unit: fast unit scope",
        "contract: contract / pact consumer tests",
        "integration: integration scope",
        "pact_provider: Pact provider verification",
    ):
        config.addinivalue_line("markers", line)


@pytest.fixture(autouse=True)
def clear_modal_function_cache() -> None:
    """Avoid cross-test pollution from ``lru_cache`` on Modal function lookups."""
    from service_clients.modal_invoker import clear_modal_function_lookup_cache

    clear_modal_function_lookup_cache()
    yield
    clear_modal_function_lookup_cache()
