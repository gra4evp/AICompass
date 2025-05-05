# services/backend/main.py
import os
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import base_router, ml_router, github_router


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(f"uvicorn.{__name__}")

# Количество попыток подключения
MAX_DB_CONNECTION_RETRIES = 5
# Задержка между попытками (в секундах)
RETRY_DB_CONNECTION_DELAY = 5


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


# Создаем FastAPI приложение
app = FastAPI(
    title="BACKEND",
    description="Интерактивный учебник по ML с анимациями",
    version="1.0.0",
    lifespan=lifespan,
    openapi_url="/openapi.json",  # URL для получения OpenAPI схемы
    docs_url="/docs",  # URL для Swagger UI
    redoc_url="/redoc",  # URL для ReDoc
    swagger_ui_parameters={
        "persistAuthorization": True,  # Сохранять токен авторизации между запросами
        "displayRequestDuration": True,  # Показывать время выполнения запросов
        "filter": True,  # Включать фильтрацию эндпоинтов
        "deepLinking": True,  # Включать глубокие ссылки на эндпоинты
        "displayOperationId": False,  # Показывать ID операций
        "defaultModelsExpandDepth": -1,  # Глубина раскрытия моделей по умолчанию (-1 = все)
        "defaultModelExpandDepth": 1,  # Глубина раскрытия одной модели
        "defaultModelRendering": "model",  # Способ отображения моделей
        "docExpansion": "list",  # Начальное состояние документации (none/list/full)
        "showExtensions": True,  # Показывать расширения OpenAPI
        "showCommonExtensions": True,  # Показывать общие расширения
        "supportedSubmitMethods": [  # Поддерживаемые HTTP методы
            "get", "post", "put", "delete", "options", "head", "patch", "trace"
        ],
        "tryItOutEnabled": True,  # Включать кнопку "Try it out"
        "syntaxHighlight": {  # Настройки подсветки синтаксиса
            "activated": True,
            "theme": "monokai"  # Тема подсветки
        }
    }
)

ZONEMINDER_URL = os.getenv("ZONEMINDER_URL", "http://localhost:1080")
EXTERNAL_API_URL = os.getenv("EXTERNAL_API_URL", "http://localhost:8002")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[ZONEMINDER_URL, EXTERNAL_API_URL],  # Разрешить запросы с фронтенда
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(base_router)
app.include_router(ml_router)
app.include_router(github_router)

# Запуск сервер
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("APP_PORT", 8015))  # Берём порт из переменной или 8000 по умолчанию
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=True
    )
