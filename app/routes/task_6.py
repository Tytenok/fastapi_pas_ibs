from typing import Dict

from fastapi import APIRouter, Form
from fastapi import Request
from app.core import DataGenerator, JSONWriter, CSVWriter, YAMLWriter

router = APIRouter(tags=["API для хранения файлов"])

"""
Задание_6. 

Изучите следущие классы в модуле app.core: BaseWriter, DataGenerator

API должно принимать json, по типу:
{
    "file_type": "json",  # или "csv", "yaml"
    "matrix_size": int    # число от 4 до 15
}
В ответ на удачную генерацию файла должен приходить id для скачивания.

Добавьте реализацию методов класса DataGenerator.
Добавьте аннотации типов и (если требуется) модели в модуль app.models.

(Подумать, как переисползовать код из задания 5)
"""


@router.post("/generate_file", description="Задание_6. Конвертер")
async def generate_file(request: Request, file_type: str = Form(...), matrix_size: int = Form(...)) -> Dict[str, str]:
    """
    Описание.

    Формат файла указывается в параметре запроса.
    Допустимые значения: `json`, `csv`, `yaml`.

    Размер матрицы указывается в параметре `matrix_size` запроса.
    Допустимые значения: от 4 до 15.
    """

    if not 4 <= matrix_size <= 15:
        raise Exception("Размер матрицы должен быть от 4 до 15!")

    data = DataGenerator()
    data.generate(matrix_size)

    if file_type == "json":
        data.to_file("data.json", JSONWriter())
    elif file_type == "csv":
        data.to_file("data.csv", CSVWriter())
    elif file_type == "yaml":
        data.to_file("data.yaml", YAMLWriter())
    else:
        raise Exception("Неизвестный формат файла!")

    file_id: str = data.file_id  # Используем тип str для идентификатора файла
    return {"file_id": file_id}  # Возвращаем словарь с идентификатором файла в качестве значения
