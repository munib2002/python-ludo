import pygame, sys

# Initialize Pygame
pygame.init()

# Import local modules
import config

from board import Board
from button import *
from constants import *
from main_menu import main_menu

# Setup Clock
clock = pygame.time.Clock()


def play_ludo():
    # Setup Game Window
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Ludo")
    icon = pygame.image.load("images/ludo.png").convert_alpha()
    pygame.display.set_icon(icon)

    menu_button = Button(
        SCREEN_WIDTH / 2,
        BOARD_TOP_Y / 2,
        TILE_SIZE * 4,
        TILE_SIZE,
        "Main Menu",
        0.5,
        0.5,
    )

    board = None

    open_main_menu = True

    run = True

    while run:
        clock.tick(FPS)

        if open_main_menu:
            reset = main_menu(screen, board != None)
            open_main_menu = False

            if reset:
                board = Board.create_board(config)

        screen.fill(LIGHT_BROWN)

        menu_button.update(selected=True)
        menu_button.draw(screen)

        if menu_button.get_pressed() and not config.mouse_clicked:
            open_main_menu = True

        update_again = board.update()
        if update_again:
            board.update()
            board.update()
            board.update()

        board.draw(screen)

        config.mouse_clicked = pygame.mouse.get_pressed()[0]

        if config.change_to_button_cursor:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        config.change_to_button_cursor = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # Update Pygame Display
        pygame.display.update()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    play_ludo()
