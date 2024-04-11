import os

from fastapi import APIRouter, Response

router = APIRouter(tags=["Стажировка"])

"""
Задание_8. Декоратор - счётчик запросов.

Напишите декоратор который будет считать кол-во запросов сделанных к приложению.
Оберните роут new_request() этим декоратором.
Подумать, как хранить переменную с кол-вом сделаных запросов.
"""


def count_requests():
    """Декоратор для подсчета запросов к приложению."""

    def decorator(func):
        async def wrapper():
            counter = 0
            counter_file_path = "app/files/counter_request"

            if not os.path.exists(counter_file_path):
                os.makedirs(os.path.dirname(counter_file_path), exist_ok=True)
                with open(counter_file_path, "w") as f:
                    f.write("0")
            else:
                with open(counter_file_path, "r") as f:
                    counter = int(f.read())
            counter += 1
            with open(counter_file_path, "w") as f:
                f.write(str(counter))

            return await func()

        return wrapper

    return decorator


@router.get("/new_request", description="Задание_8. Декоратор - счётчик запросов.")
@count_requests()
async def new_request():
    """Возвращает кол-во сделанных запросов."""
    counter_file_path = "app/files/counter_request"
    with open(counter_file_path, "r") as f:
        counter = int(f.read())
    return Response(content=f"Кол-во запросов: {counter}")
