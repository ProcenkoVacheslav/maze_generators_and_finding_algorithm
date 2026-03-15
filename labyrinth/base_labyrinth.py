from collections import deque
from typing import Optional

import pygame as pg

from .labyrinth_settings import TILE_HEIGHT, TILE_WIDTH
from .annotations import Position, SearcherNames
from .searchers.searcher import Searcher


class BaseLabyrinth:
    _WAYS_CORDS = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    def __init__(self, size: tuple, searcher_name: SearcherNames) -> None:
        self._size = size
        self._width = self._size[0]
        self._height = self._size[1]

        self._labyrinth = self._generate_number_matrix(1)
        self._steps_map = self._generate_number_matrix(0)

        self._find_way_object: Optional[Searcher] = None
        self._searcher_name = searcher_name

        self._start = (0, 0)
        self._graph = dict()

    def _matrix_to_graph(self) -> None:
        start_node = self._start
        queue = deque([start_node])
        visited = {start_node}

        while queue:
            x, y = queue.popleft()
            node = (x, y)

            if node not in self._graph:
                self._graph[node] = []

            for dx, dy in self._WAYS_CORDS:
                nx, ny = x + dx, y + dy

                if 0 <= nx < self._width:
                    if 0 <= ny < self._height:
                        if self._labyrinth[ny][nx] == 0:
                            neighbor = (nx, ny)

                            if neighbor not in visited:
                                visited.add(neighbor)
                                queue.append(neighbor)
                                self._graph[node].append((1, neighbor))

    def _generate_number_matrix(self, value: int) -> list[list[int]]:
        matrix = []
        for row in range(self._height):
            row = []
            for column in range(self._width):
                row.append(value)
            matrix.append(row)

        return matrix

    def event(self, event: pg.event) -> None:
        if event.type == pg.MOUSEBUTTONDOWN:
            position = self._get_event_pos(event.pos)
            if position:
                self._to_null_ways()
                self._labyrinth[position.y][position.x] = 2

                self._find_way_object = Searcher(self._searcher_name, self._labyrinth, self._graph)
                self._find_way()

    def _find_way(self) -> None:
        self._labyrinth = self._find_way_object.find_way()

    def change_find_way_object(self, new_name: SearcherNames) -> None:
        self._searcher_name = new_name

    def _get_event_pos(self, position: tuple[int, int]) -> Position | None:
        pos_x = position[0] // TILE_WIDTH
        pos_y = position[1] // TILE_HEIGHT

        new_pos = Position(pos_x, pos_y)

        if pos_x >= self._width:
            return None

        if self._is_not_wall(new_pos):
            return new_pos

    def _is_not_wall(self, position: Position) -> bool:
        if self._labyrinth[position.y][position.x] in [0, 4, 2]:
            return True

        return False

    def _to_null_ways(self) -> None:
        for row in range(len(self._labyrinth)):
            for column in range(len(self._labyrinth[row])):
                if self._labyrinth[row][column] in [2, 4]:
                    self._labyrinth[row][column] = 0
