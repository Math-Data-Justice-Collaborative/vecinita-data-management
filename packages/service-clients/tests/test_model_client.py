"""Unit tests for ``ModelClient`` (httpx ``MockTransport``)."""

from __future__ import annotations

import httpx
import pytest

import service_clients.model_client as model_client_mod

from service_clients.model_client import ModelClient, ModelUpstreamError


@pytest.fixture
def base_url() -> str:
    return "https://model.test"


@pytest.mark.asyncio
async def test_predict_success(base_url: str, monkeypatch: pytest.MonkeyPatch) -> None:
    async def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/predict"
        return httpx.Response(
            200,
            json={"label": "housing_intake", "score": 0.88, "model_version": None},
        )

    transport = httpx.MockTransport(handler)

    def _async_client(*, timeout: float = 60.0, **_kw: object) -> httpx.AsyncClient:
        return httpx.AsyncClient(transport=transport, timeout=timeout)

    monkeypatch.setattr(model_client_mod, "AsyncClient", _async_client)

    result = await ModelClient(base_url).predict("question")
    assert result.label == "housing_intake"
    assert result.score == 0.88


@pytest.mark.asyncio
async def test_predict_upstream_5xx_maps_to_stable_error(
    base_url: str, monkeypatch: pytest.MonkeyPatch
) -> None:
    async def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(500, json={"detail": "internal dpg-zzzzz"})

    transport = httpx.MockTransport(handler)

    def _async_client(*, timeout: float = 60.0, **_kw: object) -> httpx.AsyncClient:
        return httpx.AsyncClient(transport=transport, timeout=timeout)

    monkeypatch.setattr(model_client_mod, "AsyncClient", _async_client)

    with pytest.raises(ModelUpstreamError) as ei:
        await ModelClient(base_url).predict("q")
    assert "dpg-" not in str(ei.value).lower()
    assert ei.value.mapped_http_status == 502


@pytest.mark.asyncio
async def test_predict_client_error_preserves_status(
    base_url: str, monkeypatch: pytest.MonkeyPatch
) -> None:
    async def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(422, json={"detail": "nope"})

    transport = httpx.MockTransport(handler)

    def _async_client(*, timeout: float = 60.0, **_kw: object) -> httpx.AsyncClient:
        return httpx.AsyncClient(transport=transport, timeout=timeout)

    monkeypatch.setattr(model_client_mod, "AsyncClient", _async_client)

    with pytest.raises(ModelUpstreamError) as ei:
        await ModelClient(base_url).predict("q")
    assert ei.value.mapped_http_status == 422


@pytest.mark.asyncio
async def test_health_connect_error_maps_to_503(
    base_url: str, monkeypatch: pytest.MonkeyPatch
) -> None:
    async def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("refused", request=request)

    transport = httpx.MockTransport(handler)

    def _async_client(*, timeout: float = 60.0, **_kw: object) -> httpx.AsyncClient:
        return httpx.AsyncClient(transport=transport, timeout=timeout)

    monkeypatch.setattr(model_client_mod, "AsyncClient", _async_client)

    with pytest.raises(ModelUpstreamError) as ei:
        await ModelClient(base_url).health()
    assert ei.value.mapped_http_status == 503
