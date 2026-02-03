
# Chat Messages API
Простой API для чатов и сообщений на FastAPI с PostgreSQL, Alembic для миграций и тестами на pytest.

## Требования

Python 3.12+
Docker (для запуска в контейнере)
Poetry для deps (если локально)

## Быстрый старт 

Клонируй репо: git clone https://github.com/Koshveptos/chat-messages-api

### Запуск приложения из контейнера

```bash
docker compose up --build api
```

Если нужно очистить БД:  
```
docker compose down -v
```


После запуска доступны 
Swagger UI: http://localhost:8000/docs

Health check: http://localhost:8000/health
### Запуск тестов 
```bash

docker compose run --rm test
```

# Если запускать локально без контейнера 

Установи зависимости:
```
poetry install
```
Применить миграции:
```
alembic upgrade head
```
Запустить сервер:
```
uvicorn app.main:app --reload
```


Лицензия: MIT. Если вопросы — пиши в issues.
