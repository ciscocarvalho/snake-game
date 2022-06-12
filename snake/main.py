from . import util
from . import menus
from . import entities
from .config import Defaults
import pygame as pg

defaults = Defaults()


def main():
    while True:
        pg.init()

        clock = pg.time.Clock()

        point_up_sound = util.get_sound(defaults.pointup_sound)
        win_sound = util.get_sound(defaults.win_sound)

        display = pg.display.set_mode(defaults.display_size)

        background = pg.Surface(display.get_size(), pg.SCALED).convert()
        background.fill(defaults.background_color)

        display.blit(background, (0, 0))

        player = entities.Snake(display, 1)
        fruit = entities.Fruit(display)
        player.update()
        fruit.update()

        force_quit = False

        dirs = {
            pg.K_DOWN: "down",
            pg.K_UP: "up",
            pg.K_LEFT: "left",
            pg.K_RIGHT: "right",
        }

        fruit_cooldown = util.Cooldown(defaults.fruit_cooldown)
        player_cooldown = util.Cooldown(defaults.player_cooldown)

        first_time = True
        won = False

        new_direction = player.get_direction()

        while True:
            clock.tick(60)

            for e in pg.event.get():
                if e.type == pg.KEYDOWN:
                    if e.key in [pg.K_ESCAPE, pg.K_q]:
                        force_quit = True
                        break
                    elif e.key in dirs:
                        current_direction = player.get_direction()
                        opposite_direction = util.get_opposite_direction(
                            current_direction
                        )
                        if dirs[e.key] != opposite_direction:
                            new_direction = dirs[e.key]

            if force_quit:
                break

            display.blit(background, (0, 0))

            if fruit_cooldown.passed():
                won = fruit.move(player.get_node_coords())
                fruit_cooldown.tick()

            if player_cooldown.passed() or first_time:
                if not first_time:
                    player.set_direction(new_direction)
                    valid_move = player.move()
                    if not valid_move:
                        break
                fruit_rect = fruit.get_rect()
                player_head_rect = player.get_head().get_rect()
                if player_head_rect.colliderect(fruit_rect):
                    player.add_node()
                    player.points += 1
                    point_up_sound.play()
                    won = fruit.move(player.get_node_coords())
                    fruit_cooldown.tick()
                player_cooldown.tick()

            fruit.update()
            player.update()
            pg.display.flip()

            first_time = False

            if won:
                win_sound.play()

        if force_quit:
            pg.quit()
            break

        endgame_info = {"points": player.points, "win": won}
        menus.Endgame(display, background, endgame_info)

        pg.display.flip()

        waiting_answer = True

        while waiting_answer:
            for e in pg.event.get():
                if e.type != pg.KEYDOWN or e.key not in [pg.K_n, pg.K_y]:
                    continue

                play_again = e.key == pg.K_y

                if play_again:
                    first_time = True
                else:
                    pg.quit()

                waiting_answer = False
                break

        if not play_again:
            break


if __name__ == "__main__":
    main()
