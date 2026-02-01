import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_message_success(client: AsyncClient):
    # успешная отправка сообщения в существующий чат
    chat_response = await client.post("/chats/", json={"title": "Test Chat"})
    assert chat_response.status_code == 201

    chat_id = chat_response.json()["id"]

    response = await client.post(
        f"/chats/{chat_id}/messages/", json={"text": "Test text"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["chat_id"] == chat_id
    assert data["text"] == "Test text"


@pytest.mark.asyncio
async def test_create_message_with_spaces(client: AsyncClient):
    # проверка уделяния пробелов по краям текста
    chat_response = await client.post("/chats/", json={"title": "Test Chat"})
    assert chat_response.status_code == 201
    chat_id = chat_response.json()["id"]

    response = await client.post(
        f"/chats/{chat_id}/messages/", json={"text": "         Test    text          "}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["text"] == "Test text"


@pytest.mark.asyncio
async def test_create_message_chat_not_found(client: AsyncClient):
    # отправка в несуществующий чат
    response = await client.post(
        "/chats/99999999999/messages/", json={"text": "Test    text"}
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_create_message_empty_text(client: AsyncClient):
    # проверка отправки с пустым текстом
    chat_response = await client.post("/chats/", json={"title": "Test Chat"})
    assert chat_response.status_code == 201
    chat_id = chat_response.json()["id"]

    response = await client.post(f"/chats/{chat_id}/messages/", json={"text": ""})
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_message_with_only_spaces(client: AsyncClient):
    # проверка отправки с пустым текстом из одних пробелов
    chat_response = await client.post("/chats/", json={"title": "Test Chat"})
    assert chat_response.status_code == 201
    chat_id = chat_response.json()["id"]

    response = await client.post(
        f"/chats/{chat_id}/messages/", json={"text": "                    "}
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_message_too_long(client: AsyncClient):
    # проверка отправки длинее 5000
    chat_response = await client.post("/chats/", json={"title": "Test Chat"})
    assert chat_response.status_code == 201
    chat_id = chat_response.json()["id"]
    text_msg = "a" * 5001
    response = await client.post(f"/chats/{chat_id}/messages/", json={"text": text_msg})
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_message_with_time(client: AsyncClient):
    # проверка что сообщения сортируются по времени
    chat_response = await client.post("/chats/", json={"title": "Test Chat"})
    assert chat_response.status_code == 201
    chat_id = chat_response.json()["id"]

    await client.post(f"/chats/{chat_id}/messages/", json={"text": "First"})
    await client.post(f"/chats/{chat_id}/messages/", json={"text": "Second"})
    await client.post(f"/chats/{chat_id}/messages/", json={"text": "Third"})

    response = await client.get(f"/chats/{chat_id}?limit=10")
    assert response.status_code == 200
    data = response.json()

    assert len(data["messages"]) == 3
    assert data["messages"][0]["text"] == "Third"
    assert data["messages"][1]["text"] == "Second"
    assert data["messages"][2]["text"] == "First"
