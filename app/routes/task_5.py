import os

from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from io import BytesIO
import zipfile

router = APIRouter(tags=["API для хранения файлов"])

"""
Задание_5. API для хранения файлов

a.  Написать API для добавления(POST) "/upload_file" и скачивания (GET) "/download_file/{id}" файлов. В ответ на удачную загрузку файла должен приходить id для скачивания.
b.  Добавить архивирование к post запросу, то есть файл должен сжиматься и сохраняться в ZIP формате.
с*.Добавить аннотации типов.
"""


@router.post("/upload_file", description="Задание_5. API для хранения файлов")
async def upload_file(file: UploadFile = File(...)) -> dict:
    """
    Добавление файла.

    Возвращает id файла для скачивания.
    """

    # Создаем байтовый поток для записи ZIP архива
    buffer = BytesIO()

    # Создаем ZIP архив
    with zipfile.ZipFile(buffer, "w") as zip_file:
        # Добавляем файл в архив
        zip_file.writestr(file.filename, file.file.read())

    # Сохраняем архив на диск
    filename = str(len(file.filename))
    filepath = os.path.join("app/files", filename + ".zip")
    with open(filepath, "wb") as f:
        f.write(buffer.getvalue())

    return {"file_id": int(filename)}  # Возвращаем длину имени файла в виде целого числа (ID)


@router.get("/download_file/{file_id}", description="Задание_5. API для хранения файлов")
async def download_file(file_id: int) -> FileResponse:
    """
    Скачивание файла по его id (длине имени файла).
    """

    # Формируем имя файла
    filename = str(file_id) + ".zip"
    # Проверяем, существует ли файл
    filepath = os.path.join("app/files", filename)
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="Файл не найден")

    # Возвращаем файл для скачивания
    return FileResponse(filepath, media_type="application/octet-stream", filename=filename)
