# Task Manager API

Минимальный API управления задачами на FastAPI с in-memory хранилищем и документацией в Swagger UI.

## Запуск

```bash
cd taskManagerApi
python -m venv .venv

# Для macOS / Linux:
source .venv/bin/activate

# Для Windows (PowerShell):
.venv\Scripts\Activate.ps1

pip install -r requirements.txt
uvicorn main:app --reload
```

Откройте Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## Эндпоинты

| Метод | Путь | Описание |
|-------|------|----------|
| `POST` | `/tasks` | Создать задачу (201) |
| `GET` | `/tasks/{task_id}` | Получить задачу по ID (200 / 404) |

## Промпты для ИИ (формулировка описаний)

ИИ использовался только для генерации текстовых описаний (summary, description, Field, ошибки), а не для проектирования логики API.

### a. Описание эндпоинтов

```
Сформулируй краткий summary (до 8 слов) и развёрнутый description
для эндпоинтов Task Manager API на FastAPI:

1) POST /tasks — создание задачи; валидация title (3–100),
   description (опционально), priority (1–5); ответ 201 с id.
2) GET /tasks/{task_id} — получение задачи по id; 200 если найдена,
   404 если нет.

Стиль: деловой русский, однозначный, без жаргона.
Текст должен хорошо читаться в Swagger UI.
```

### b. Описание моделей данных (Pydantic)

```
Для моделей TaskCreate и TaskResponse напиши:
- docstring класса;
- description для каждого Field (title, description, priority, id);
- краткие example-значения для полей создания задачи.

Учти ограничения: title 3–100 символов, priority целое 1–5,
description необязателен. Язык: русский, формулировки для OpenAPI/Swagger.
```

### c. Формулировка ошибок

```
Опиши для OpenAPI responses смысл ошибок:
- 422 на POST /tasks (невалидные поля тела);
- 404 на GET /tasks/{task_id} (задача не найдена);
- 422 на GET /tasks/{task_id} (некорректный формат path-параметра);
- 200 на GET (успешный ответ).

Каждое описание — одно предложение на русском, понятное в Swagger UI.
```
