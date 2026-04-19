"""Unit tests for ``EmbeddingClient`` (httpx ``MockTransport``)."""

from __future__ import annotations

import httpx
import pytest

import service_clients.embedding_client as embedding_client_mod

from service_clients.embedding_client import EmbeddingClient, EmbeddingUpstreamError


@pytest.fixture
def base_url() -> str:
    return "https://embedding.test"


@pytest.mark.asyncio
async def test_embed_success(base_url: str, monkeypatch: pytest.MonkeyPatch) -> None:
    async def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/embed"
        return httpx.Response(
            200, json={"embedding": [0.1, 0.2], "model_version": None}
        )

    transport = httpx.MockTransport(handler)

    def _async_client(*, timeout: float = 60.0, **_kw: object) -> httpx.AsyncClient:
        return httpx.AsyncClient(transport=transport, timeout=timeout)

    monkeypatch.setattr(embedding_client_mod, "AsyncClient", _async_client)

    result = await EmbeddingClient(base_url).embed("hello")
    assert result.embedding == [0.1, 0.2]


@pytest.mark.asyncio
async def test_embed_upstream_5xx_maps_to_stable_error(
    base_url: str, monkeypatch: pytest.MonkeyPatch
) -> None:
    async def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(502, json={"detail": "dpg-secret-host failure"})

    transport = httpx.MockTransport(handler)

    def _async_client(*, timeout: float = 60.0, **_kw: object) -> httpx.AsyncClient:
        return httpx.AsyncClient(transport=transport, timeout=timeout)

    monkeypatch.setattr(embedding_client_mod, "AsyncClient", _async_client)

    with pytest.raises(EmbeddingUpstreamError) as ei:
        await EmbeddingClient(base_url).embed("hello")
    assert "dpg-" not in str(ei.value).lower()
    assert ei.value.mapped_http_status == 502


@pytest.mark.asyncio
async def test_embed_client_error_preserves_status(
    base_url: str, monkeypatch: pytest.MonkeyPatch
) -> None:
    async def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(400, json={"detail": "bad"})

    transport = httpx.MockTransport(handler)

    def _async_client(*, timeout: float = 60.0, **_kw: object) -> httpx.AsyncClient:
        return httpx.AsyncClient(transport=transport, timeout=timeout)

    monkeypatch.setattr(embedding_client_mod, "AsyncClient", _async_client)

    with pytest.raises(EmbeddingUpstreamError) as ei:
        await EmbeddingClient(base_url).embed("hello")
    assert ei.value.mapped_http_status == 400


@pytest.mark.asyncio
async def test_health_connect_error_maps_to_503(
    base_url: str, monkeypatch: pytest.MonkeyPatch
) -> None:
    async def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("refused", request=request)

    transport = httpx.MockTransport(handler)

    def _async_client(*, timeout: float = 60.0, **_kw: object) -> httpx.AsyncClient:
        return httpx.AsyncClient(transport=transport, timeout=timeout)

    monkeypatch.setattr(embedding_client_mod, "AsyncClient", _async_client)

    with pytest.raises(EmbeddingUpstreamError) as ei:
        await EmbeddingClient(base_url).health()
    assert ei.value.mapped_http_status == 503
