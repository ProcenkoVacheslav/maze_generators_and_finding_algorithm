from labyrinth.annotations import time_decorator
from labyrinth.searchers.annotations import Position
from labyrinth.searchers.base_search import BaseSearch


class DFSSearcher(BaseSearch):

    __searcher_name__ = 'dfs'

    _WIDTH_POSITIONS = ['left', 'right']
    _HEIGHT_POSITIONS = ['top', 'bottom']
    _POSITIONS_NAME = [*_WIDTH_POSITIONS, *_HEIGHT_POSITIONS]

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._is_find = False

    def _dfs_search(self, position: Position) -> None:
        pos_x = position.x
        pos_y = position.y

        steps_position = self._get_positions(position)
        self._steps[pos_y][pos_x] = 1
        self._is_finish(pos_x, pos_y)

        for cur_step in self._POSITIONS_NAME:
            new_position = steps_position[cur_step]

            if not self._is_find:
                if cur_step in self._WIDTH_POSITIONS:
                    self._start_horysontal(new_position)
                else:
                    self._start_vertical(new_position)
            else:
                break

        self._mark_way(pos_x, pos_y)

    @staticmethod
    def _get_positions(position: Position) -> dict[str: Position]:
        pos_x = position.x
        pos_y = position.y

        return {
            'left': Position(pos_x - 1, pos_y),
            'right': Position(pos_x + 1, pos_y),
            'top': Position(pos_x, pos_y - 1),
            'bottom': Position(pos_x, pos_y + 1),
        }

    def _is_finish(self, pos_x: int, pos_y: int) -> None:
        if self._labyrinth[pos_y][pos_x] == 2:
            self._is_find = True

    def _mark_way(self, pos_x: int, pos_y: int) -> None:
        if self._is_find:
            if self._labyrinth[pos_y][pos_x] not in [2, 3]:
                self._labyrinth[pos_y][pos_x] = 4

    def _start_horysontal(self, new_position: Position) -> None:
        new_pos_x = new_position.x
        new_pos_y = new_position.y

        if 0 <= new_pos_x < self._width:
            if self._steps[new_pos_y][new_pos_x] != 1:
                self._dfs_search(new_position)

    def _start_vertical(self, new_position: Position) -> None:
        new_pos_x = new_position.x
        new_pos_y = new_position.y

        if 0 <= new_pos_y < self._height:
            if self._steps[new_pos_y][new_pos_x] != 1:
                self._dfs_search(new_position)

    @time_decorator('search', 'dfs')
    def find_way(self) -> list[list[int]]:
        self._is_find = False
        self._dfs_search(Position(0, 0))

        return self._labyrinth
