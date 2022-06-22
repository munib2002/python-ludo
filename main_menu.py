import pygame, sys

import config
from constants import *
from button import Button
from utils_functions import *
from options_menu import options_menu


def main_menu(surface, resume):
    resume_btn = Button(
        SCREEN_WIDTH / 2, TILE_SIZE * 5, TILE_SIZE * 4.5, TILE_SIZE * 1.3, "Resume", 0.5
    )

    play_btn = Button(
        SCREEN_WIDTH / 2, TILE_SIZE * 7.5, TILE_SIZE * 3, TILE_SIZE * 1.3, "Play", 0.5
    )

    options_btn = Button(
        SCREEN_WIDTH / 2,
        TILE_SIZE * 10,
        TILE_SIZE * 4.5,
        TILE_SIZE * 1.3,
        "Options",
        0.5,
    )

    exit_btn = Button(
        SCREEN_WIDTH / 2, TILE_SIZE * 12.5, TILE_SIZE * 3, TILE_SIZE * 1.3, "Exit", 0.5
    )

    menu_buttons = [play_btn, options_btn, exit_btn]

    reset_board = False

    clock = pygame.time.Clock()

    run = True
    while run:
        clock.tick(FPS)

        surface.fill(LIGHT_BROWN)

        config.change_to_button_cursor = False

        draw_text(
            surface, "Main Menu", 0.5, 0.5, SCREEN_WIDTH / 2, TILE_SIZE, TILE_SIZE * 1.3
        )

        for btn in menu_buttons:
            btn.draw(surface)
            btn.update(selected=True)

        resume_btn.draw(surface)
        resume_btn.update(selected=True, disabled=not resume)

        draw_text(
            surface,
            "© 2022 Munib ur Rehman Qasim",
            0.5,
            0.5,
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT - TILE_SIZE / 2,
            TILE_SIZE * 0.4,
        )

        if resume_btn.get_pressed() and resume:
            reset_board = False
            run = False

        if play_btn.get_pressed():
            reset_board = True
            run = False

        if options_btn.get_pressed() and not config.mouse_clicked:
            options_menu(surface)

        if exit_btn.get_pressed():
            pygame.quit()
            sys.exit()

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

    return reset_board
