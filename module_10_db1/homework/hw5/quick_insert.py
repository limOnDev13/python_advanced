from typing import Union, List

Number = Union[int, float, complex]


def binary_search(array: list[int], number: int) -> int:
    """
    Функция реализовывает бинарный поиск позиции number в отсортированном списке array
    :param array: Отсортированный список чисел
    :param number: Число, которому нужно найти позицию в списке такую, чтобы список остался отсортированным
    :return: Позицию number
    """
    start_index: int = 0
    end_index: int = len(array) - 1
    medium: int = int((end_index - start_index) / 2)

    while end_index - start_index > 1:
        if array[medium] == number:
            return medium
        elif array[medium] < number:
            start_index, medium = medium, (end_index + medium) // 2
        elif number < array[medium]:
            end_index, medium = medium, (medium + start_index) // 2

    return end_index


def find_insert_position(array: List[Number], number: Number) -> int:
    """Функция принимает на вход отсортированный по неубыванию массив чисел и некое число X, а возвращает индекс,
     показывающий, на какое место нужно вставить число X, чтобы массив остался отсортированным"""
    # Если список пуст - вернем 0 индекс. Сложность O(1)
    if len(array) == 0:
        return 0

    # Если number больше всех чисел - вернем последний индекс
    if number > array[-1]:  # Сложность O(1)
        return len(array)
    # Если number меньше всех чисел - вернем 0 индекс
    elif number < array[0]:  # Сложность O(1)
        return 0
    # Во всех остальных случаях number находится между 2 числами из множества.
    # Вернем индекс первого большего числа, чем number
    else:
        return binary_search(array, number)


def test_find_insert_position() -> None:
    test_arrays_and_numbers: list[tuple[list[int], int]] = [
        ([], 1),
        ([2, 3, 4, 5], 1),
        ([2, 3, 4, 5], 6),
        ([2, 2, 2, 2, 2], 2),
        ([1, 2, 4, 5, 6], 3),
        ([1, 2, 3, 3, 3, 5], 4)
    ]

    for test_array, test_number in test_arrays_and_numbers:
        print(f'Тест: test_array = {test_array}; test_number = {test_number}')
        position: int = find_insert_position(test_array, test_number)
        test_array.insert(position, test_number)
        assert test_array == sorted(test_array)


if __name__ == '__main__':
    # A: List[Number] = [1, 2, 3, 3, 3, 5]
    # x: Number = 4
    # insert_position: int = find_insert_position(A, x)
    # assert insert_position == 5
    #
    # A: List[Number] = [1, 2, 3, 3, 3, 5]
    # x: Number = 4
    # A.insert(insert_position, x)
    # assert A == sorted(A)
    test_find_insert_position()
