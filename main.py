from typing import Dict, Optional

from fastapi import FastAPI, HTTPException, Path, status
from pydantic import BaseModel, Field

app = FastAPI(
    title="Task Manager API",
    description=(
        "Данный API предназначен для управления задачами. "
        "Позволяет создавать новые задачи с валидацией полей и получать "
        "информацию о них по уникальному идентификатору. "
        "Данные хранятся во временной памяти (In-Memory)."
    ),
    version="1.0.0",
)

# Временное in-memory хранилище для задач и счетчик ID
tasks_storage: Dict[int, dict] = {}
current_id = 1


# --- МОДЕЛИ ДАННЫХ (PYDANTIC) ---


class TaskCreate(BaseModel):
    """Модель данных для создания новой задачи с валидацией входящих полей."""

    title: str = Field(
        ...,
        min_length=3,
        max_length=100,
        description="Краткое название задачи. Обязательное поле.",
        json_schema_extra={"example": "Купить продукты"},
    )
    description: Optional[str] = Field(
        None,
        description=(
            "Подробное описание задачи или дополнительные заметки. "
            "Необязательное поле."
        ),
        json_schema_extra={"example": "Молоко, хлеб, сыр и яблоки"},
    )
    priority: int = Field(
        ...,
        ge=1,
        le=5,
        description=(
            "Уровень приоритета задачи от 1 (самый низкий) до 5 "
            "(самый высокий). Обязательное поле."
        ),
        json_schema_extra={"example": 3},
    )


class TaskResponse(BaseModel):
    """Модель ответа с полной информацией о созданной или найденной задаче."""

    id: int = Field(
        ...,
        description="Уникальный числовой идентификатор задачи в системе.",
        json_schema_extra={"example": 1},
    )
    title: str = Field(
        ...,
        description="Название задачи.",
        json_schema_extra={"example": "Купить продукты"},
    )
    description: Optional[str] = Field(
        None,
        description="Описание задачи.",
        json_schema_extra={"example": "Молоко, хлеб, сыр и яблоки"},
    )
    priority: int = Field(
        ...,
        description="Приоритет задачи (от 1 до 5).",
        json_schema_extra={"example": 3},
    )


# --- ЭНДПОИНТЫ API ---


@app.post(
    "/tasks",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Создать новую задачу",
    description=(
        "Принимает JSON-тело с параметрами задачи, выполняет валидацию полей "
        "(длина заголовка, диапазон приоритета) и сохраняет задачу в оперативную "
        "память. Возвращает созданную задачу вместе с присвоенным ей ID."
    ),
    responses={
        422: {
            "description": (
                "Ошибка валидации. Переданы некорректные параметры "
                "(например, слишком короткий title или priority вне диапазона 1–5)."
            )
        }
    },
)
async def create_task(task: TaskCreate):
    global current_id
    new_task = {
        "id": current_id,
        "title": task.title,
        "description": task.description,
        "priority": task.priority,
    }
    tasks_storage[current_id] = new_task
    current_id += 1
    return new_task


@app.get(
    "/tasks/{task_id}",
    response_model=TaskResponse,
    status_code=status.HTTP_200_OK,
    summary="Получить задачу по ID",
    description=(
        "Ищет задачу во временном хранилище по её уникальному идентификатору. "
        "Если задача найдена, возвращает её структуру. Если нет — отдаёт ошибку 404."
    ),
    responses={
        200: {"description": "Задача успешно найдена и возвращена."},
        404: {
            "description": (
                "Задача с указанным идентификатором не найдена в системе."
            )
        },
        422: {
            "description": (
                "Ошибка валидации пути. Например, передан некорректный "
                "формат ID (не число)."
            )
        },
    },
)
async def get_task(
    task_id: int = Path(
        ...,
        description="Уникальный числовой идентификатор искомой задачи",
    ),
):
    if task_id not in tasks_storage:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found",
        )
    return tasks_storage[task_id]
