from collections import deque
from typing import Optional

from labyrinth.annotations import time_decorator
from labyrinth.searchers.base_search import BaseSearch

from copy import deepcopy


class LeeSearcher(BaseSearch):

    __searcher_name__ = 'lee'

    _TRANSLATE_VALUES = {
        2: -1,
        0: -1,
        1: -7,
        3: 0,
    }

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._finish_cords = tuple()
        self._restructure_steps_matrix()
        self._queue = deque()

    def _restructure_steps_matrix(self) -> None:
        labyrinth_copy = deepcopy(self._steps)
        for pos_y, row in enumerate(self._steps):
            for pos_x, column in enumerate(row):
                labyrinth_copy[pos_y][pos_x] = self._TRANSLATE_VALUES[column]

                if column == 2:
                    self._finish_cords = (pos_x, pos_y)

        self._steps = labyrinth_copy

    def _lee_search(self, position: tuple[int, int]) -> Optional[list[tuple[int, int]]]:
        self._queue.append(position)

        while self._queue:
            cur = self._queue.popleft()
            cur_x = cur[0]
            cur_y = cur[1]

            if cur == self._finish_cords:
                return self._get_path(cur)

            for pos_x, pos_y in self._get_positions():
                neighbor = (cur_x + pos_x, cur_y + pos_y)
                self._check_neighbor(neighbor, cur)

    def _get_path(self, cur: tuple) -> list[tuple[int, int]]:
        path = []

        while cur:
            neighbors_pos, neighbors_values = self._get_neighbors_pos_values(cur)

            min_value = min(neighbors_values)
            min_value_pos = neighbors_pos[neighbors_values.index(min_value)]

            path.append(min_value_pos)

            cur = min_value_pos

            if cur == (0, 0):
                break

        return path[::-1]

    def _get_neighbors_pos_values(self, cur) -> tuple[list[tuple[int, int]], list[int]]:
        neighbors = []
        values = []

        for pos_x, pos_y in self._get_positions():
            neighbor_pos = (cur[0] + pos_x, cur[1] + pos_y)
            if 0 <= neighbor_pos[0] < self._width:
                if 0 <= neighbor_pos[1] < self._height:
                    if self._steps[neighbor_pos[1]][neighbor_pos[0]] >= 0:
                        neighbors.append(neighbor_pos)
                        values.append(self._steps[neighbor_pos[1]][neighbor_pos[0]])

        response = (neighbors, values)

        return response

    def _check_neighbor(self, neighbor: tuple, cur: tuple) -> None:
        pos_x = neighbor[0]
        pos_y = neighbor[1]

        if 0 <= pos_x < self._width:
            if 0 <= pos_y < self._height:
                if self._steps[pos_y][pos_x] == -1:
                    self._steps[pos_y][pos_x] = self._steps[cur[1]][cur[0]] + 1
                    self._queue.append(neighbor)

    @staticmethod
    def _get_positions() -> list[tuple[int, int]]:
        return [
            (-1, 0),
            (1, 0),
            (0, -1),
            (0, 1),
        ]

    @time_decorator('search', 'lee')
    def find_way(self) -> list[list[int]]:
        way = self._lee_search((0, 0))

        if way:
            for cord_x, cord_y in way:
                if self._labyrinth[cord_y][cord_x] not in [2, 3]:
                    self._labyrinth[cord_y][cord_x] = 4

        return self._labyrinth
