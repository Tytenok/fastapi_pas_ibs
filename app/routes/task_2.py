from typing import Annotated

from fastapi import APIRouter, Body, HTTPException

from app.core import convert_arabic_to_roman, convert_roman_to_arabic
from app.models import ConverterResponse

router = APIRouter(tags=["Стажировка"])

"""
Задание_2. Конвертер
    1. Реализовать функции convert_arabic_to_roman() и convert_roman_to_arabic() из пакета app.core
    2. Написать логику и проверки для вводимых данных. Учитывать, что если арабское число выходит за пределы 
    от 1 до 3999, то возвращать "не поддерживается"
    3. Запустить приложение и проверить результат через swagger
"""


@router.post("/converter", description="Задание_2. Конвертер")
async def convert_number(number: Annotated[int | str, Body()]) -> ConverterResponse:
    """
    принимает арабское или римское число и конвертирует его в соответствующий формат
    """
    if isinstance(number, int):
        converter_response = ConverterResponse(arabic=number, roman=convert_arabic_to_roman(number))
    elif isinstance(number, str):
        converter_response = ConverterResponse(roman=number, arabic=convert_roman_to_arabic(number))
    else:
        raise HTTPException(status_code=400, detail="Неверный тип данных")

    return converter_response
