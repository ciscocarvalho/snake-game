from .. import util
from ..config import Defaults
from random import randint
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
        valid_coords_length = len(valid_coords)

        if valid_coords_length > 1 and self.coords in valid_coords:
            valid_coords.remove(self.coords)
            valid_coords_length = len(valid_coords)

        if valid_coords_length > 0:
            random_idx = randint(0, valid_coords_length - 1)
            self.coords = valid_coords[random_idx]
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
