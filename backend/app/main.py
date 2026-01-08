"""
Главный файл Backend API
"""
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
import os
import traceback
import logging
from dotenv import load_dotenv
from app.api.routes import router

load_dotenv()

# Настройка логирования
log_level = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(
    level=getattr(logging, log_level, logging.INFO),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Импорт limiter из core
from app.core.limiter import limiter

app = FastAPI(
    title="TicTacToe API",
    description="API для игры Крестики-нолики",
    version="1.0.0"
)

# Настройка Rate Limiter
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Настройка Prometheus метрик
Instrumentator().instrument(app).expose(app)

# CORS для работы с frontend
cors_origins_str = os.getenv("CORS_ORIGINS", "http://localhost:3000")
cors_origins = [origin.strip() for origin in cors_origins_str.split(",") if origin.strip()]

logger.info(f"CORS разрешенные домены: {cors_origins}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)

# Применение rate limiting через middleware (должно быть до include_router)
app.add_middleware(SlowAPIMiddleware)

# Подключение роутов
app.include_router(router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "TicTacToe API", "version": "1.0.0"}

@app.get("/health")
async def health():
    """Health check endpoint"""
    from app.storage.redis_client import get_storage
    
    checks = {
        "status": "ok",
        "checks": {}
    }
    
    # Проверка Redis
    try:
        storage = await get_storage()
        client = await storage._get_client()
        await client.ping()
        checks["checks"]["redis"] = "ok"
    except Exception as e:
        logger.error(f"Redis health check failed: {e}")
        checks["checks"]["redis"] = "error"
        checks["status"] = "degraded"
    
    return checks

# Глобальный обработчик исключений
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Обработка всех необработанных исключений"""
    logger.error(f"Необработанная ошибка: {exc}", exc_info=True)
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "Внутренняя ошибка сервера",
            "error": str(exc) if os.getenv("DEBUG", "False").lower() == "true" else "Произошла ошибка при обработке запроса"
        }
    )

# Обработчик ошибок валидации
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Обработка ошибок валидации запросов"""
    logger.warning(f"Ошибка валидации: {exc.errors()}")
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": "Ошибка валидации данных",
            "errors": exc.errors()
        }
    )

