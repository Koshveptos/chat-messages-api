import asyncio

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_chat_success(client: AsyncClient):
    # успешное создание чата с валидным титлом
    text = "Test Chat"
    response = await client.post("/chats/", json={"title": text})
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["title"] == text
    assert "created_at" in data


@pytest.mark.asyncio
async def test_create_chat_with_spaces(client: AsyncClient):
    # пробелы по краям
    text = "        text with spaces        "
    response = await client.post("/chats/", json={"title": text})
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "text with spaces"


@pytest.mark.asyncio
async def test_create_chat_empty_title(client: AsyncClient):
    # создание чата с пустыми заголовком
    response = await client.post("/chats/", json={"title": ""})
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_chat_with__only_spaces(client: AsyncClient):
    # одни пробелы
    response = await client.post("/chats/", json={"title": "      "})
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_long_title(client: AsyncClient):
    # слишком длинное
    long_msg = "A" * 201
    response = await client.post("/chats/", json={"title": long_msg})
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_without_title(client: AsyncClient):
    response = await client.post("/chats/", json={})
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_get_chat_not_found(client: AsyncClient):
    # получение несуществующего чата
    response = await client.get("/chats/999999999")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_chat_seccess(client: AsyncClient):
    # успешный тест создания чата
    create_response = await client.post("/chats/", json={"title": "Test Chat"})
    assert create_response.status_code == 201
    chat_id = create_response.json()["id"]
    response = await client.get(f"/chats/{chat_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == chat_id
    assert "messages" in data
    assert isinstance(data["messages"], list)


@pytest.mark.asyncio
async def test_get_chat_with_limit(client: AsyncClient):
    # получение с лимитом
    create_response = await client.post("/chats/", json={"title": "Test Chat"})
    assert create_response.status_code == 201
    chat_id = create_response.json()["id"]

    for i in range(10):
        await client.post(f"/chats/{chat_id}/messages/", json={"text": f"Msg {i}"})
        # задержка нужна хотя бы 1с что б порядок соблюдался
        await asyncio.sleep(0.01)

    response = await client.get(f"/chats/{chat_id}?limit=5")
    assert response.status_code == 200
    data = response.json()
    assert len(data["messages"]) == 5
    ##проверяем порядок
    assert data["messages"][0]["text"] == "Msg 9"
    assert data["messages"][4]["text"] == "Msg 5"


@pytest.mark.asyncio
async def test_delete_chat_not_found(client: AsyncClient):
    # удаление несуществующего чата
    response = await client.delete("/chats/9999999")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_chat_success(client: AsyncClient):
    # успешное удаление чата
    create_response = await client.post("/chats/", json={"title": "Test chat"})
    assert create_response.status_code == 201
    chat_id = create_response.json()["id"]

    ##del
    response = await client.delete(f"/chats/{chat_id}")
    assert response.status_code == 204
    assert response.text == ""
