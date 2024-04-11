import csv
import json
import random
import uuid
from abc import ABC, abstractmethod
from io import StringIO
import io

import yaml
from fastapi import UploadFile
import pandas as pd


def convert_arabic_to_roman(number: int) -> str:
    """
    Конвертирует арабское число в римское.
    """
    if not 1 <= number <= 3999:
        return "не поддерживается"

    roman_map = {1: 'I', 4: 'IV', 5: 'V', 9: 'IX', 10: 'X', 40: 'XL', 50: 'L', 90: 'XC', 100: 'C', 400: 'XD', 500: 'D',
                 900: 'CM', 1000: 'M'}
    i = 12
    result = ""

    while number:
        div = number // list(roman_map.keys())[i]
        number %= list(roman_map.keys())[i]

        while div:
            result += list(roman_map.values())[i]
            div -= 1
        i -= 1
    return result


def convert_roman_to_arabic(number: str) -> int:
    """
    Конвертирует римское число в арабское.
    """
    roman_map = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    i = 0
    result = 0

    while i < len(number):
        s1 = roman_map[number[i]]
        if i + 1 < len(number):
            s2 = roman_map[number[i + 1]]
            if s1 >= s2:
                result += s1
                i += 1
            else:
                result += s2 - s1
                i += 2
        else:
            result += s1
            i += 1
    return result


def average_age_by_position(file: UploadFile):
    # Чтение CSV-файла в DataFrame
    try:
        df = pd.read_csv(file.file)
    except Exception as e:
        raise ValueError("Ошибка чтения CSV-файла. " + str(e))

    # Проверка наличия ожидаемых столбцов
    expected_columns = ["Имя", "Возраст", "Должность"]
    if not all(col in df.columns for col in expected_columns):
        raise ValueError("Неверный формат CSV. Столбцы должны включать 'Имя', 'Возраст', 'Должность'.")

    # Расчет среднего возраста по должности
    average_age_dict = {}
    for position, group in df.groupby("Должность"):
        average_age_dict[position] = group["Возраст"].mean()

    return average_age_dict


"""
Задание_6.
Дан класс DataGenerator, который имеет два метода: generate(), to_file()
Метод generate генерирует данные формата list[list[int, str, float]] и записывает результат в
переменную класса data
Метод to_file сохраняет значение переменной generated_data по пути path c помощью метода
write, классов JSONWritter, CSVWritter, YAMLWritter.

Допишите реализацию методов и классов.
"""


class BaseWriter(ABC):

    @abstractmethod
    def write(self, data: list[list[int, str, float]]) -> io.StringIO:
        """
        Записывает данные в строковый объект файла StringIO

        :param data: полученные данные
        :return: Объект StringIO с данными из data
        """
        pass


class JSONWriter(BaseWriter):

    def write(self, data: list[list[int, str, float]]) -> io.StringIO:
        """Реализация метода write для json формата"""

        output = io.StringIO()
        json.dump(data, output)
        return output


class CSVWriter(BaseWriter):

    def write(self, data: list[list[int, str, float]]) -> io.StringIO:
        """Реализация метода write для csv формата"""

        output = io.StringIO()
        csv_writer = csv.writer(output)
        csv_writer.writerows(data)
        return output


class YAMLWriter(BaseWriter):

    def write(self, data: list[list[int, str, float]]) -> io.StringIO:
        """Реализация метода write для yaml формата"""

        output = io.StringIO()
        yaml.dump(data, output)
        return output


class DataGenerator:
    def __init__(self, data: list[list[int, str, float]] = None):
        self.data: list[list[int, str, float]] = data
        self.file_id = None

    def generate(self, matrix_size: int) -> None:
        """Генерирует матрицу данных заданного размера."""
        data = [[random.randint(0, 100) for _ in range(matrix_size)] for _ in range(matrix_size)]
        self.data = data

    def to_file(self, path: str, writer: BaseWriter) -> None:
        if not self.data:
            raise Exception("Нет данных для записи в файл!")

        with open(path, "w") as f:
            f.write(writer.write(self.data).getvalue())

        # Установка значения file_id
        self.file_id = str(uuid.uuid4())  # Уникальный идентификатор файла
