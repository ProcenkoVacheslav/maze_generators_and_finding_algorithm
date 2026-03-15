from heapq import heappush, heappop

from labyrinth.annotations import time_decorator
from labyrinth.searchers.base_search import BaseSearch


class DijkstraSearcher(BaseSearch):

    __searcher_name__ = 'dijkstra'

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._start = (0, 0)
        self._queue = []
        heappush(self._queue, (0, self._start))
        self._cost_visited = {self._start: 0}
        self._visited = {self._start: None}

        self._finish = self._get_finish()

    def _get_finish(self) -> tuple[int, int]:
        for row_number, row in enumerate(self._labyrinth):
            for column_number, column in enumerate(row):
                if column == 2:
                    finish_pos = (column_number, row_number)
                    return finish_pos

    def _dijkstra(self) -> dict[tuple[int, int]: tuple[int, int]]:
        while self._queue:
            cur_cost, cur_node = heappop(self._queue)
            if self._labyrinth[cur_node[1]][cur_node[0]] == 2:
                self._finish = cur_node
                break

            next_nodes = self._graph[cur_node]
            for next_node in next_nodes:
                neigh_cost, neigh_node = next_node
                new_cost = self._cost_visited[cur_node] + neigh_cost

                if neigh_node not in self._cost_visited or new_cost < self._cost_visited[neigh_node]:
                    heappush(self._queue, (new_cost, neigh_node))
                    self._cost_visited[neigh_node] = new_cost
                    self._visited[neigh_node] = cur_node

        return self._visited

    def _get_path(self) -> list[tuple[int, int]]:
        visited = self._dijkstra()
        path = []

        cur_node = self._finish
        while cur_node != self._start:
            cur_node = visited[cur_node]
            path.append(cur_node)

        return path

    @time_decorator('search', 'dijkstra')
    def find_way(self) -> list[list[int]]:
        way = self._get_path()

        if way:
            for cord_x, cord_y in way:
                if self._labyrinth[cord_y][cord_x] not in [2, 3]:
                    self._labyrinth[cord_y][cord_x] = 4

        return self._labyrinth
