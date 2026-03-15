import copy
import sys

sys.setrecursionlimit(2000)


class BaseSearch:
    def __init__(self, labyrinth: list[list[int]], graph: dict[tuple[int, int]: tuple[int, tuple[int, int]]]):
        self._labyrinth = labyrinth
        self._graph = graph
        self._steps = copy.deepcopy(self._labyrinth)

        self._width = len(labyrinth[0])
        self._height = len(labyrinth)
