from labyrinth.annotations import time_decorator, Position
from labyrinth.cycle_labyrinth import CycleLabyrinth
from labyrinth.algorythms.dfs_labyrinth import DFSLabyrinth


class CycleDFSLabyrinth(DFSLabyrinth, CycleLabyrinth):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    @time_decorator('labyrinth', 'cycle_dfs')
    def generate_labyrinth(self) -> list[list[int]]:
        self._dfs_generator(Position(0, 0), None)

        self._delete_walls()
        self._matrix_to_graph()

        return self._labyrinth
