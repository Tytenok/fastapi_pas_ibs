from typing import Union

from datetime import datetime
from typing import List, Optional, Set

from pydantic import BaseModel, Field, validator


class ConverterRequest(BaseModel):
    number: Union[int, str]


class ConverterResponse(BaseModel):
    arabic: int
    roman: str


class User(BaseModel):
    name: str
    age: int = Field(ge=0, le=100)  # Возраст от 0 до 100
    adult: Optional[bool] = None

    @validator("adult", always=True)
    def calculate_adult(cls, v, values):
        # Вычислить на основе возраста
        return values["age"] >= 18


class Meta(BaseModel):
    last_modification: str
    list_of_skills: Optional[List[str]] = None
    mapping: dict = Field(
        ...,
        example={
            "list_of_ids": [1, "два"],
            "tags": {"стажировка", "практика"},
        },
    )

    @validator("last_modification")
    def validate_date_format(cls, value):
        try:
            datetime.strptime(value, "%d/%m/%Y")
        except ValueError:
            raise ValueError("Дата должна быть в формате dd/mm/yyyy (например: 20/05/2023)")
        return value

    @validator("mapping")
    def validate_mapping_structure(cls, v):
        if not ("list_of_ids" in v and "tags" in v):
            raise ValueError("Словарь должен содержать ключи 'list_of_ids' и 'tags'")
        return v


class BigJson(BaseModel):
    """Использует модель User и добавляет валидацию."""

    user: User
    meta: Meta

# class UserRequest(BaseModel):
#     name: str
#     message: str
#
#
# class User(BaseModel):
#     name: str
#     age: str
#     is_adult: bool
#     message: str = None
#
#
# class UserResponse(BaseModel):
#     pass
