import pytest


@pytest.mark.asyncio
async def test_create_chat(client) -> dict:
    response = await client.post("/chats/", json={"title": "Test chat"})
    assert response.status_code == 201


@pytest.mark.asyncio
async def test_health(client) -> bool:
    response = await client.get("/health")

    assert response.status_code == 200
