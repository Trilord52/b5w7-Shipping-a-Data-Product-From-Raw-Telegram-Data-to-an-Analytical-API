import pytest
from httpx import AsyncClient
from src.api import app

import asyncio

@pytest.mark.asyncio
async def test_root():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        resp = await ac.get("/")
    assert resp.status_code == 200
    assert "message" in resp.json()

@pytest.mark.asyncio
async def test_top_channels():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        resp = await ac.get("/api/reports/top-channels?limit=2")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)
    if resp.json():
        assert "channel_name" in resp.json()[0]
        assert "count" in resp.json()[0]

@pytest.mark.asyncio
async def test_channel_activity_valid():
    # This test assumes at least one channel exists; adjust as needed
    async with AsyncClient(app=app, base_url="http://test") as ac:
        resp = await ac.get("/api/reports/top-channels?limit=1")
        channels = resp.json()
        if channels:
            channel = channels[0]["channel_name"]
            resp2 = await ac.get(f"/api/channels/{channel}/activity")
            assert resp2.status_code == 200
            data = resp2.json()
            assert "channel_name" in data
            assert "total_messages" in data
            assert "messages_per_day" in data

@pytest.mark.asyncio
async def test_channel_activity_invalid():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        resp = await ac.get("/api/channels/this_channel_does_not_exist/activity")
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Channel not found"

@pytest.mark.asyncio
async def test_search_messages():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        resp = await ac.get("/api/search/messages?query=test")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)
    if resp.json():
        msg = resp.json()[0]
        assert "message_id" in msg
        assert "channel_name" in msg
        assert "date" in msg
        assert "text" in msg

@pytest.mark.asyncio
async def test_search_messages_empty():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        resp = await ac.get("/api/search/messages?query=")
    assert resp.status_code == 422  # Validation error for empty query 