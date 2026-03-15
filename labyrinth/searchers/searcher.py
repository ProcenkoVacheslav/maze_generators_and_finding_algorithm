from labyrinth.searchers.annotations import Names
from labyrinth.searchers.base_search import BaseSearch
from labyrinth.searchers.bfs_searcher import BFSSearcher
from labyrinth.searchers.dfs_searcher import DFSSearcher
from labyrinth.searchers.dijkstra_searcher import DijkstraSearcher
from labyrinth.searchers.lee_searcher import LeeSearcher


class Searcher:
    def __init__(self, name: Names, labyrinth: list[list[int]],
                 graph: dict[tuple[int, int]: tuple[int, tuple[int, int]]]):

        self._name = name
        self._labyrinth = labyrinth
        self._graph = graph

        self._search_object = self._get_generators()[self._name](self._labyrinth, self._graph)

    @staticmethod
    def _get_generators() -> dict[str: BaseSearch]:
        return {
            'dfs': DFSSearcher,
            'bfs': BFSSearcher,
            'lee': LeeSearcher,
            'dijkstra': DijkstraSearcher,
        }

    def find_way(self):
        new_labyrinth = self._search_object.find_way()

        return new_labyrinth
