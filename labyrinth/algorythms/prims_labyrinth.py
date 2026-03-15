import random

from labyrinth.annotations import time_decorator
from labyrinth.base_labyrinth import BaseLabyrinth


class PrimsLabyrinth(BaseLabyrinth):

    __labyrinth_name__ = 'prim'

    _DIRECTIONS = [
        (0, -1, 0, -2),
        (0, 1, 0, 2),
        (-1, 0, -2, 0),
        (1, 0, 2, 0),
    ]

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._matrix_to_graph()

    def _generate(self) -> list[list[int]]:
        start_x = 1
        start_y = 1

        gx, gy = start_x, start_y
        self._labyrinth[gy][gx] = 0

        walls = []
        self._add_walls(gx, gy, walls)

        while walls:
            wall_x, wall_y, direction = walls.pop(random.randint(0, len(walls) - 1))

            nx, ny = wall_x + direction[0], wall_y + direction[1]

            if 0 < nx < self._width and 0 < ny < self._height:
                if self._labyrinth[ny][nx] == 1:
                    self._labyrinth[wall_y][wall_x] = 0
                    self._labyrinth[ny][nx] = 0

                    self._add_walls(nx, ny, walls)

        self._mark_start_pos()
        
        return self._labyrinth

    def _add_walls(self, x: int, y: int, walls: list):
        for dx_w, dy_w, dx_c, dy_c in self._DIRECTIONS:
            wx, wy = x + dx_w, y + dy_w
            cx, cy = x + dx_c, y + dy_c

            if 0 < cx < self._width and 0 < cy < self._height:
                if self._labyrinth[cy][cx] == 1:
                    walls.append((wx, wy, (dx_w, dy_w)))

    def _mark_start_pos(self) -> None:
        self._labyrinth[0][0] = 3
        self._labyrinth[1][0] = 0

    @time_decorator('labyrinth', 'prims')
    def generate_labyrinth(self) -> list[list[int]]:
        self._generate()
        self._matrix_to_graph()

        return self._labyrinth
