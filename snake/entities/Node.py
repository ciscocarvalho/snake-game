from ..config import Defaults
import pygame as pg

defaults = Defaults()


class Node:
    next = None

    def __init__(self, display, color=defaults.snake_color, coords=(0, 0)):
        self.size = defaults.player_size
        self.display = display
        self.color = color
        self.coords = coords
        self.surface = pg.Surface(self.size).convert()
        self.surface.fill(self.color)
        self.next = self.previous = None
        self.direction = defaults.direction
        self.old_position = None

    def get_new_coords_by_current_direction(self):
        width, height = self.size
        x, y = self.coords
        dirs = {
            "left": (x - width, y),
            "right": (x + width, y),
            "up": (x, y - height),
            "down": (x, y + height),
        }
        coords = list(dirs[self.direction])
        display_size = self.display.get_size()
        for z in zip([0, 1], [width, height]):
            i, j = z
            if coords[i] >= display_size[i]:
                if defaults.teleport:
                    coords[i] = 0
                else:
                    return False
            elif coords[i] < 0:
                if defaults.teleport:
                    coords[i] = display_size[i] - j
                else:
                    return False
        return tuple(coords)

    def move(self):
        if self.is_tail():
            self.old_position = self.coords
        if self.is_head():
            self.coords = self.get_new_coords_by_current_direction()
        else:
            self.coords = self.previous.coords

    def update(self):
        self.display.blit(self.surface, self.coords)

    def get_rect(self):
        return self.surface.get_rect(topleft=self.coords)

    def is_tail(self):
        return self.next is None

    def is_head(self):
        return self.previous is None
