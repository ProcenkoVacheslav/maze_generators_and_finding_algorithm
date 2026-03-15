from labyrinth.annotations import time_decorator
from labyrinth.searchers.base_search import BaseSearch

from collections import deque


class BFSSearcher(BaseSearch):

    __searcher_name__ = 'bfs'

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._is_find = False
        self._queue = deque()
        self._visited = dict()

    def _bfs_search(self, position: tuple) -> list[tuple[int, int]]:
        self._queue.append(position)
        self._visited[position] = None

        while self._queue:
            cur = self._queue.popleft()
            cur_x = cur[0]
            cur_y = cur[1]

            if self._labyrinth[cur_y][cur_x] == 2:
                return self._get_path(cur)

            for pos_x, pos_y in self._get_positions():
                neighbor = (cur[0] + pos_x, cur[1] + pos_y)
                self._check_neighbor(neighbor, cur)

    def _get_path(self, cur: tuple) -> list[tuple[int, int]]:
        path = []

        while cur:
            path.append(cur)
            cur = self._visited[cur]

        return path[::-1]

    @staticmethod
    def _get_positions() -> list[tuple[int, int]]:
        return [
            (-1, 0),
            (1, 0),
            (0, -1),
            (0, 1),
        ]

    def _check_neighbor(self, neighbor: tuple, cur: tuple) -> None:
        pos_x = neighbor[0]
        pos_y = neighbor[1]

        if 0 <= pos_x < self._width:
            if 0 <= pos_y < self._height:
                if self._labyrinth[pos_y][pos_x] != 1:
                    if neighbor not in self._visited:
                        self._add_neighbor(neighbor, cur)

    def _add_neighbor(self, neighbor: tuple, cur: tuple) -> None:
        self._queue.append(neighbor)
        self._visited[neighbor] = cur

    @time_decorator('search', 'bfs')
    def find_way(self) -> list[list[int]]:
        way = self._bfs_search((0, 0))

        if way:
            for cord_x, cord_y in way:
                if self._labyrinth[cord_y][cord_x] not in [2, 3]:
                    self._labyrinth[cord_y][cord_x] = 4

        return self._labyrinth
