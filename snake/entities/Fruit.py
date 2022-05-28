from .. import util
from ..config import Defaults
from random import choice
import pygame as pg

defaults = Defaults()


class Fruit:
    def __init__(self, display):
        self.size = defaults.fruit_size
        self.display = display
        self.color = defaults.fruit_color
        self.surface = pg.Surface(self.size).convert()
        self.surface.fill(self.color)
        self.coords = None
        self.move()

    def move(self, avoid_coords=[]):
        def _filter(coords):
            nonlocal avoid_coords
            if coords in avoid_coords:
                return False
            return True

        valid_coords = util.filter_display_coords(self.display, _filter)

        if len(valid_coords) > 1 and self.coords in valid_coords:
            valid_coords.remove(self.coords)

        if len(valid_coords) > 0:
            self.coords = choice(valid_coords)
            return False

        return True

    def update(self):
        self.display.blit(self.surface, self.coords)

    def get_rect(self):
        coords = self.coords

        if coords is not None:
            return self.surface.get_rect(topleft=coords)
        else:
            return self.surface.get_rect()
