import pygame

SCREEN_SIZE = [pygame.display.Info().current_w, pygame.display.Info().current_h]

# Game Variables
FPS = 60
TILE_SIZE = round(SCREEN_SIZE[1] / 22)

# Screen Size
SCREEN_HEIGHT = TILE_SIZE * 20
SCREEN_WIDTH = SCREEN_HEIGHT * (
    SCREEN_SIZE[0] / SCREEN_SIZE[1] * (0.8 if SCREEN_SIZE[0] > SCREEN_SIZE[1] else 1)
)

# Ludo Board Start Coordinates
BOARD_LEFT_X = round((SCREEN_WIDTH - 15 * TILE_SIZE) / 2)
BOARD_TOP_Y = round((SCREEN_HEIGHT - 15 * TILE_SIZE) / 2)


# Board Base Layout:
# 15 x 15 2D Board
# P0-P3 represents player colored tiles
# TT represents normal tiles
# CC Represents Center of the Board
BOARD_BASE_LAYOUT = [
    "P0 P0 P0 P0 P0 P0 TT TT TT P1 P1 P1 P1 P1 P1",
    "P0 P0 P0 P0 P0 P0 TT P1 P1 P1 P1 P1 P1 P1 P1",
    "P0 P0 P0 P0 P0 P0 P1 P1 TT P1 P1 P1 P1 P1 P1",
    "P0 P0 P0 P0 P0 P0 TT P1 TT P1 P1 P1 P1 P1 P1",
    "P0 P0 P0 P0 P0 P0 TT P1 TT P1 P1 P1 P1 P1 P1",
    "P0 P0 P0 P0 P0 P0 TT P1 TT P1 P1 P1 P1 P1 P1",
    "TT P0 TT TT TT TT CC CC CC TT TT TT P2 TT TT",
    "TT P0 P0 P0 P0 P0 CC CC CC P2 P2 P2 P2 P2 TT",
    "TT TT P0 TT TT TT CC CC CC TT TT TT TT P2 TT",
    "P3 P3 P3 P3 P3 P3 TT P3 TT P2 P2 P2 P2 P2 P2",
    "P3 P3 P3 P3 P3 P3 TT P3 TT P2 P2 P2 P2 P2 P2",
    "P3 P3 P3 P3 P3 P3 TT P3 TT P2 P2 P2 P2 P2 P2",
    "P3 P3 P3 P3 P3 P3 TT P3 P3 P2 P2 P2 P2 P2 P2",
    "P3 P3 P3 P3 P3 P3 P3 P3 TT P2 P2 P2 P2 P2 P2",
    "P3 P3 P3 P3 P3 P3 TT TT TT P2 P2 P2 P2 P2 P2",
]

# Marks out the general path of a Piece on the board (for 1st player)
PIECES_GENERAL_PATH = [
    "** ** ** ** ** ** 10 11 12 ** ** ** ** ** **",
    "** ** ** ** ** ** 09 ** 13 ** ** ** ** ** **",
    "** ** ** ** ** ** 08 ** 14 ** ** ** ** ** **",
    "** ** ** ** ** ** 07 ** 15 ** ** ** ** ** **",
    "** ** ** ** ** ** 06 ** 16 ** ** ** ** ** **",
    "** ** ** ** ** ** 05 ** 17 ** ** ** ** ** **",
    "-1 00 01 02 03 04 ** ** ** 18 19 20 21 22 23",
    "50 51 52 53 54 55 56 ** ** ** ** ** ** ** 24",
    "49 48 47 46 45 44 ** ** ** 30 29 28 27 26 25",
    "** ** ** ** ** ** 43 ** 31 ** ** ** ** ** **",
    "** ** ** ** ** ** 42 ** 32 ** ** ** ** ** **",
    "** ** ** ** ** ** 41 ** 33 ** ** ** ** ** **",
    "** ** ** ** ** ** 40 ** 34 ** ** ** ** ** **",
    "** ** ** ** ** ** 39 ** 35 ** ** ** ** ** **",
    "** ** ** ** ** ** 38 37 36 ** ** ** ** ** **",
]


SAFE_SQUARES = [0, 8, 13, 21, 26, 34, 39, 47]

# Tiles offset for center Triangle Coords
# (x1, y1, x2, y2) - P0-P3 respectively
CENTER_TRIANGLE_TILES_OFFSET = ((6, 6, 6, 9), (6, 6, 9, 6), (9, 6, 9, 9), (6, 9, 9, 9))

# (x1, y1)
PLAYERS_AREA_TILES_OFFSET = ((1.25, 1.25), (10.25, 1.25), (10.25, 10.25), (1.25, 10.25))

PIECES_COORDS_OFFSET_FOR_MULTIPLE_PIECES = (
    (0.25, 0.25),
    (0.75, 0.25),
    (0.75, 0.75),
    (0.25, 0.75),
)
