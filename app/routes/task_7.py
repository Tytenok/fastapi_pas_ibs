import logging
import time
from contextvars import ContextVar

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

output_log = logging.getLogger("output")
client_host: ContextVar[str | None] = ContextVar("client_host", default=None)

"""
Задание_7. Логирование в FastAPI с использованием middleware.

Написать конфигурационный файл для логгера "output"
Формат выводимых логов:
[CURRENT_DATETIME] {file: line} LOG_LEVEL - | EXECUTION_TIME_SEC | HTTP_METHOD | URL | STATUS_CODE |
[2023-12-15 00:00:00] {example:62} INFO | 12 | GET | http://localhost/example | 200 |


Дописать класс CustomMiddleware.
Добавить middleware в приложение (app).
"""
# Конфигурация логгера
output_log.setLevel(logging.INFO)

formatter = logging.Formatter(
    "[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - | %(execution_time)s | %(http_method)s | %(url)s | %("
    "status_code)s |",
    "%Y-%m-%d %H:%M:%S",
)

file_handler = logging.FileHandler("output.log")
file_handler.setFormatter(formatter)
output_log.addHandler(file_handler)


class CustomMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        execution_time = round(time.time() - start_time, 2)

        log_context = {
            "execution_time": execution_time,
            "http_method": request.method,
            "url": str(request.url),
            "status_code": response.status_code
        }
        output_log.info("Запрос принят", extra=log_context)

        return response
