from labyrinth.annotations import Names
from .base_labyrinth import BaseLabyrinth
from labyrinth.algorythms.cycle_dfs_labyrinth import CycleDFSLabyrinth

from labyrinth.algorythms.dfs_labyrinth import DFSLabyrinth

import pygame as pg

from labyrinth.algorythms.eller_labyrynth import EllersLabyrinth
from labyrinth.algorythms.prims_labyrinth import PrimsLabyrinth


class Labyrinth:
    def __init__(self, name: Names, size: tuple) -> None:
        self._name = name
        self._size = size
        self._width = self._size[0]
        self._height = self._size[1]

        self._labyrinth_object = self._get_generators()[self._name](self._size, 'dijkstra')
        pg.display.set_caption('dijkstra')

    @staticmethod
    def _get_generators() -> dict[str: BaseLabyrinth]:
        return {
            'dfs': DFSLabyrinth,
            'prim': PrimsLabyrinth,
            'eller': EllersLabyrinth,
            'cycle_dfs': CycleDFSLabyrinth,
        }

    def generate_labyrinth(self) -> list[list]:
        labyrinth = self._labyrinth_object.generate_labyrinth()

        return labyrinth

    def event(self, event: pg.event):
        self._labyrinth_object.event(event)

        keys = pg.key.get_pressed()

        if keys[pg.K_1]:
            pg.display.set_caption('dfs')
            self._labyrinth_object.change_find_way_object('dfs')
        if keys[pg.K_2]:
            pg.display.set_caption('bfs')
            self._labyrinth_object.change_find_way_object('bfs')
        if keys[pg.K_3]:
            pg.display.set_caption('lee')
            self._labyrinth_object.change_find_way_object('lee')
