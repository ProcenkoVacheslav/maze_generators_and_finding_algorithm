import pygame as pg

from .window_settings import SCREEN_SIZE, FPS
from labyrinth.draw_labyrinth import DrawLabyrinth


class Window:
    def __init__(self):
        self._screen = pg.display.set_mode(SCREEN_SIZE)
        self._clock = pg.time.Clock()
        self._FPS = FPS
        self._runner = True
        self._labyrinth = DrawLabyrinth()

    def _events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self._runner = False

            self._labyrinth.event(event)

    def _fill(self):
        self._screen.fill(pg.Color('red'))

    def _update(self):
        self._clock.tick(self._FPS)
        pg.display.flip()

    def run(self):
        while self._runner:
            self._events()
            self._fill()

            self._labyrinth.draw_labyrinth(self._screen)

            self._update()
