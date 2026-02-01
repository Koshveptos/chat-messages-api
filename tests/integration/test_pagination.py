import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_pagination_fewer_than_limit(client: AsyncClient):
    # сообщений меньше чем лимит - возвращаются все
    chat_response = await client.post("/chats/", json={"title": "Test Chat"})
    assert chat_response.status_code == 201
    chat_id = chat_response.json()["id"]

    for i in range(3):
        msg_resp = await client.post(
            f"/chats/{chat_id}/messages/", json={"text": f"msg {i}"}
        )
        assert msg_resp.status_code == 201

    response = await client.get(f"/chats/{chat_id}?limit=20")
    assert response.status_code == 200
    data = response.json()
    assert len(data["messages"]) == 3


@pytest.mark.asyncio
async def test_pagination_zero_msg(client: AsyncClient):
    # пустой  список при 0 сообщениях
    chat_response = await client.post("/chats/", json={"title": "test chat"})
    assert chat_response.status_code == 201
    chat_id = chat_response.json()["id"]

    response = await client.get(f"/chats/{chat_id}?limit=20")
    assert response.status_code == 200
    data = response.json()
    assert data["messages"] == []
