import pytest
from starlette.testclient import TestClient
from task_1 import find_in_different_registers
from task_1 import router

client = TestClient(router)


@pytest.mark.asyncio
async def test_find_in_different_registers():
    """
    Проверяет функцию на правильность работы.
    """
    result = await find_in_different_registers(
        ['Мама', 'МАМА', 'Мама', 'папа', 'ПАПА', 'Мама', 'ДЯдя', 'брАт', 'Дядя', 'Дядя', 'Дядя'])
    assert result == ['папа', 'брат']


@pytest.mark.asyncio
async def test_find_in_different_registers_empty_list():
    """
    Проверяет функцию на обработку пустого списка.
    """
    result = await find_in_different_registers([])
    assert result == []


@pytest.mark.asyncio
async def test_find_in_different_registers_non_string_elements():
    """
    Проверяет функцию на обработку списка с нестроковыми элементами.
    """
    with pytest.raises(TypeError):
        await find_in_different_registers([1, 2, 3])
