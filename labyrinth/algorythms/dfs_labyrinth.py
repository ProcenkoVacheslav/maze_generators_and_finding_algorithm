import random
from typing import Optional

from labyrinth.annotations import Position, Steps, time_decorator
from labyrinth.base_labyrinth import BaseLabyrinth


class DFSLabyrinth(BaseLabyrinth):

    __labyrinth_name__ = 'dfs'

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def _dfs_generator(self, position: Position, from_step: Optional[Steps]) -> None:
        self._mark_current_position(position)
        self._mark_step_position(position, from_step)

        steps = self._generate_steps(position)
        steps_names = self._get_cur_steps_name(steps)

        while len(steps_names) > 0:
            cur_step = random.choice(steps_names)
            steps_names.pop(steps_names.index(cur_step))

            cur_size = self._get_cur_size(cur_step)
            cur_position = self._get_cur_position(cur_step, steps[cur_step])

            if cur_size > cur_position >= 0:
                new_position = steps[cur_step]

                if self._steps_map[new_position.y][new_position.x] != 1:
                    self._dfs_generator(new_position, cur_step)

    def _mark_current_position(self, position: Position) -> None:
        self._steps_map[position.y][position.x] = 1
        self._labyrinth[position.y][position.x] = 0
        if position.x == position.y == 0:
            self._labyrinth[position.x][position.y] = 3

    def _mark_step_position(self, position: Position, from_step: Optional[Steps]) -> None:
        steps_positions = self._generate_step_positions(position)

        if from_step is not None:
            from_step_cord = steps_positions[from_step]
            self._labyrinth[from_step_cord.y][from_step_cord.x] = 0

    def _get_cur_steps_name(self, steps):
        steps_name = []
        for step in steps:
            if step == 'left':
                if steps[step].x >= 0:
                    steps_name.append(step)
            elif step == 'right':
                if steps[step].x < self._width:
                    steps_name.append(step)
            elif step == 'top':
                if steps[step].y >= 0:
                    steps_name.append(step)
            elif step == 'bottom':
                if steps[step].y < self._height:
                    steps_name.append(step)

        return steps_name

    @staticmethod
    def _generate_step_positions(position: Position) -> dict[str: Position]:
        return {
            'left': Position(position.x + 1, position.y),
            'right': Position(position.x - 1, position.y),
            'top': Position(position.x, position.y + 1),
            'bottom': Position(position.x, position.y - 1),
        }

    @staticmethod
    def _generate_steps(position: Position) -> dict[str: int]:
        return {
            'left': Position(position.x - 2, position.y),
            'right': Position(position.x + 2, position.y),
            'top': Position(position.x, position.y - 2),
            'bottom': Position(position.x, position.y + 2),
        }

    def _get_cur_size(self, cur_step: Steps) -> int:
        return self._width if cur_step in ['left', 'right'] else self._height

    @staticmethod
    def _get_cur_position(cur_step: Steps, position: Position) -> int:
        return position.x if cur_step in ['left', 'right'] else position.y

    @time_decorator('labyrinth', 'dfs')
    def generate_labyrinth(self) -> list[list[int]]:
        self._dfs_generator(Position(0, 0), None)
        self._matrix_to_graph()

        return self._labyrinth
