from .labyrinth_generator import Labyrinth
from .labyrinth_settings import TILE_WIDTH, TILE_HEIGHT

import pygame as pg


class DrawLabyrinth:

    COLORS = {
        0: pg.Color('green'),
        1: pg.Color('blue'),
        2: pg.Color('red'),
        3: pg.Color('orange'),
        4: pg.Color('white'),
    }

    def __init__(self) -> None:
        self._labyrinth_object = Labyrinth('dfs', (50, 40))
        self._labyrinth = self._labyrinth_object.generate_labyrinth()

    def draw_labyrinth(self, screen) -> None:
        for row_number, row in enumerate(self._labyrinth):
            for column_number, column in enumerate(row):
                rect = pg.Rect(
                    column_number * TILE_WIDTH,
                    row_number * TILE_HEIGHT,
                    TILE_WIDTH,
                    TILE_HEIGHT,
                )

                color = self.COLORS[column]

                pg.draw.rect(
                    screen,
                    color,
                    rect
                )

    def event(self, event: pg.event) -> None:
        self._labyrinth_object.event(event)
