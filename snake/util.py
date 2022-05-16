from .config import Defaults
from os import path
import pygame as pg

main_dir = path.abspath(path.join(__file__, "../.."))
assets_dir = path.join(main_dir, "assets")

defaults = Defaults()


class Cooldown:
    now = last = pg.time.get_ticks()

    def __init__(self, cooldown):
        self.cooldown = cooldown

    def passed(self):
        return pg.time.get_ticks() - self.last >= self.cooldown

    def tick(self):
        self.last = pg.time.get_ticks()


def get_opposite_direction(dir):
    dirs = {
        "left": "right",
        "right": "left",
        "up": "down",
        "down": "up",
    }
    return dirs[dir]


def get_image(name, convert=True):
    filepath = path.join(assets_dir, name)
    image = pg.image.load(filepath)
    if convert:
        image.convert()
    return image


def get_sound(name=None):
    if not pg.mixer or name is None:

        class NoneSound:
            def play(self):
                pass

        return NoneSound()
    filepath = path.join(assets_dir, name)
    sound = pg.mixer.Sound(filepath)
    return sound


def filter_display_coords(display, _filter):
    width, height = display.get_size()
    display_unit = defaults.display_unit
    filtered_coords = []
    for y in range(0, height, display_unit):
        for x in range(0, width, display_unit):
            coords = (x, y)
            if _filter(coords):
                filtered_coords.append(coords)
    return filtered_coords
