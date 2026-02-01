import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_cascade_delete(client: AsyncClient):
    chat1 = await client.post("/chats/", json={"title": "Chat1"})
    chat2 = await client.post("/chats/", json={"title": "Chat2"})

    assert chat1.status_code == 201
    assert chat2.status_code == 201

    chat_1_id = chat1.json()["id"]
    chat_2_id = chat2.json()["id"]

    await client.post(f"/chats/{chat_1_id}/messages/", json={"text": "chat1 msg"})
    await client.post(f"/chats/{chat_2_id}/messages/", json={"text": "chat2 msg"})

    delete_response = await client.delete(f"/chats/{chat_1_id}")
    assert delete_response.status_code == 204

    get1 = await client.get(f"/chats/{chat_1_id}")
    assert get1.status_code == 404

    get2 = await client.get(f"/chats/{chat_2_id}")
    assert get2.status_code == 200
    data = get2.json()
    assert len(data["messages"]) == 1
    assert data["messages"][0]["text"] == "chat2 msg"
