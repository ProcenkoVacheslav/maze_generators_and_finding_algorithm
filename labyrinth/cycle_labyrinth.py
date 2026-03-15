import random

from labyrinth.base_labyrinth import BaseLabyrinth


class CycleLabyrinth(BaseLabyrinth):
    _MAX_COUNTER = 100
    _MAX_X, _MAX_Y = 50, 40

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def _delete_walls(self) -> None:
        counter = 0

        while counter != self._MAX_COUNTER:
            pos_x = random.randrange(0, self._MAX_X)
            pos_y = random.randrange(0, self._MAX_Y)

            if self._labyrinth[pos_y][pos_x] == 1:
                self._labyrinth[pos_y][pos_x] = 0
                counter += 1
