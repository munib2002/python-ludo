import pygame, sys

import config
from constants import *
from button import Button
from utils_functions import *
from player_config_options import Player_Config


def options_menu(surface):
    back_button = Button(
        SCREEN_WIDTH / 2, TILE_SIZE * 16, TILE_SIZE * 3, TILE_SIZE * 1.3, "Back", 0.5
    )

    players_config = []

    for i, val in enumerate([(1, 1), (0, 1), (0, 0), (1, 0)]):
        player_config = Player_Config(
            SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - TILE_SIZE, i, *val
        )

        players_config.append(player_config)

    clock = pygame.time.Clock()

    run = True

    while run:
        clock.tick(FPS)

        surface.fill(LIGHT_BROWN)

        config.change_to_button_cursor = False

        draw_text(
            surface, "Options", 0.5, 0.5, SCREEN_WIDTH / 2, TILE_SIZE, TILE_SIZE * 1.3
        )

        for player_config in players_config:
            player_config.update()
            player_config.draw(surface)

        back_button.draw(surface)
        back_button.update(selected=True)

        if back_button.get_pressed():
            run = False

        config.mouse_clicked = pygame.mouse.get_pressed()[0]

        if config.change_to_button_cursor:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Update Pygame Display
        pygame.display.update()
