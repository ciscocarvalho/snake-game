from ..config import Defaults
import pygame as pg

defaults = Defaults()


class Endgame():
    def __init__(self, display, background, info):
        lines = []

        if info["win"]:
            lines.append("You win")
        else:
            lines.append("You lose")

        lines.append(f"Your score: {info['points']}")
        lines.append("Play again? [y/n]")

        font_size = 32
        font = pg.font.Font(defaults.font, font_size)

        display_width, display_height = display.get_size()

        line_height = font.get_linesize()
        lines_height = len(lines) * line_height
        initial_position = display_height / 2 - lines_height / 2

        display.blit(background, (0, 0))

        for idx, line in enumerate(lines):
            text = font.render(line, True, (255, 255, 255), (0, 0, 0))
            text_rect = text.get_rect()
            text_center_x = display_width // 2
            text_center_y = int(initial_position + idx * line_height)
            text_rect.center = (text_center_x, text_center_y)
            display.blit(text, text_rect)
