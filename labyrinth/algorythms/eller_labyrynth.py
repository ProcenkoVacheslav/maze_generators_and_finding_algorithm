import random

from labyrinth.annotations import time_decorator
from labyrinth.base_labyrinth import BaseLabyrinth


class EllersLabyrinth(BaseLabyrinth):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._matrix_to_graph()

        self._target_width = self._width
        self._target_height = self._height

        self._cells_in_row = self._width // 2
        self._rows_count = self._height // 2

        if self._cells_in_row < 1:
            self._cells_in_row = 1
        if self._rows_count < 1:
            self._rows_count = 1

        self._sets = list(range(self._cells_in_row))
        self._next_set_id = self._cells_in_row

    def _generate(self) -> list[list[int]]:
        self._labyrinth = [[1 for _ in range(self._target_width)] for _ in range(self._target_height)]
        self._sets = list(range(self._cells_in_row))

        for y in range(self._rows_count):
            grid_y = 2 * y + 1
            if grid_y >= self._target_height:
                break

            for x in range(self._cells_in_row):
                grid_x = 2 * x + 1
                if grid_x < self._target_width:
                    self._labyrinth[grid_y][grid_x] = 0

            for x in range(self._cells_in_row - 1):
                grid_x_wall = 2 * x + 2
                if grid_x_wall >= self._target_width:
                    break

                is_last_row = (y == self._rows_count - 1)
                if self._sets[x] != self._sets[x + 1]:
                    if random.choice([True, False]) or is_last_row:
                        self._merge_sets(self._sets[x + 1], self._sets[x])
                        self._labyrinth[grid_y][grid_x_wall] = 0

            if y < self._rows_count - 1:
                grid_y_wall = 2 * y + 2
                if grid_y_wall >= self._target_height:
                    continue

                next_row_sets = [-1] * self._cells_in_row
                sets_map = {}
                for x, s_id in enumerate(self._sets):
                    sets_map.setdefault(s_id, []).append(x)

                for s_id, indices in sets_map.items():
                    random.shuffle(indices)
                    num_drops = random.randint(1, len(indices))
                    for i in range(num_drops):
                        x = indices[i]
                        next_row_sets[x] = s_id
                        if grid_y_wall < self._target_height:
                            self._labyrinth[grid_y_wall][2 * x + 1] = 0

                for x in range(self._cells_in_row):
                    if next_row_sets[x] == -1:
                        self._sets[x] = self._next_set_id
                        self._next_set_id += 1
                    else:
                        self._sets[x] = next_row_sets[x]

        return self._labyrinth

    def _merge_sets(self, old_set, new_set) -> None:
        for i in range(len(self._sets)):
            if self._sets[i] == old_set:
                self._sets[i] = new_set

    def _mark_start_pos(self) -> None:
        self._labyrinth[0][0] = 3
        self._labyrinth[1][0] = 0

    @time_decorator('labyrinth', 'eller')
    def generate_labyrinth(self) -> list[list[int]]:
        self._generate()
        self._mark_start_pos()
        self._matrix_to_graph()

        return self._labyrinth
