import functools
import timeit
from collections import namedtuple
from typing import Literal, Callable, Optional, Any

_OPERATIONS_NAMES = Literal['labyrinth', 'search']
_OPERATION_ANSWERS = {
    'labyrinth': 'Время генерации лабиринта',
    'search': 'Время поиска пути',
}
_OBJECT_TYPES = Literal['dfs', 'bfs', 'lee', 'prims', 'eller', 'cycle_dfs', 'dijkstra']
_ALGORYTHM_TYPE = {
    ('labyrinth', 'dfs'): 'Рекурсивный лабиринт',
    ('labyrinth', 'prims'): 'Лабиринт Прима',
    ('labyrinth', 'eller'): 'Лабиринт Эллера',
    ('labyrinth', 'cicle_dfs'): 'Рекурсивный лабиринт с циклами',
    ('search', 'dfs'): 'Рекурсивный поиск в глубину',
    ('search', 'bfs'): 'Поиск в ширину',
    ('search', 'lee'): 'Алгоритм поиска Лии',
    ('search', 'dijkstra'): 'Алгоритм поиска Дейкстры',
}

Steps = Literal['left', 'right', 'top', 'bottom']
Names = Literal['dfs', 'prim', 'eller', 'cycle_dfs']
SearcherNames = Literal['dfs', 'bfs', 'lee', 'dijkstra']

Position = namedtuple('Position', ['x', 'y'])
Sizes = namedtuple('Sizes', ['width', 'height'])


def _get_absolut_way_len(matrix: list[list[int]]) -> int:
    total = 0

    for row in matrix:
        for column in row:
            if column == 4:
                total += 1

    return total


def _write_to_file(operation_name: _OPERATIONS_NAMES, answer: str):
    if operation_name == 'search':
        file_name = 'statistic_searcher_data.txt'
    else:
        file_name = 'statistic_labyrinth_data.txt'

    with open(f'labyrinth/statistic/{file_name}', 'a+', encoding='utf-8') as file:
        file.write(f'\n{answer}')


def _time_and_run(func: Callable, *args, **kwargs) -> tuple[list, Any]:
    result = []

    def wrapper():
        nonlocal result
        result = func(*args, **kwargs)

    exec_time = timeit.timeit(wrapper, number=1)

    return result, exec_time


def time_decorator(operation_name: _OPERATIONS_NAMES, object_type: Optional[_OBJECT_TYPES] = None) -> Callable:
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> list:

            result, algorythm_time = _time_and_run(func, *args, **kwargs)

            operation = _OPERATION_ANSWERS.get(operation_name)
            get_param = (operation_name, object_type)
            algorythm_type = _ALGORYTHM_TYPE.get(get_param)
            way_len = _get_absolut_way_len(result)

            len_string = f'. Длина пути - {way_len}' if operation_name == 'search' else ''

            answer_string = f'{operation}_{algorythm_type} - {algorythm_time}{len_string}'

            _write_to_file(operation_name, answer_string)

            print(answer_string)

            return result
        return wrapper
    return decorator
