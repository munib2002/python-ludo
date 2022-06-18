import pygame
from pygame import gfxdraw
import random

# Initialize Pygame
pygame.init()

# Setup Clock
clock = pygame.time.Clock()

# Screen Size
SCREEN_WIDTH = 1300
SCREEN_HEIGHT = 1100

# Setup Game Window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Ludo")

# Ludo Board Start Coordinates
BOARD_LEFT_X = 200
BOARD_TOP_Y = 100

# Game Variables
FPS = 60
TILE_SIZE = 60

# Dice
diceImg = pygame.image.load("dice.png").convert_alpha()
diceRect = diceImg.get_rect()

# Colors
RED = (231, 76, 60)
DARK_RED = (192, 57, 43)
BLUE = (72, 219, 251)
DARK_BLUE = (10, 189, 227)
GREEN = (46, 204, 113)
DARK_GREEN = (30, 179, 100)
ORANGE = (253, 150, 68)
DARK_ORANGE = (239, 108, 0)
LIGHT_GREY = (223, 228, 234)
LIGHT_BROWN = (247, 241, 227)
DARK_GREY = (47, 53, 66)
WHITE = (255, 255, 255)

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


is_piece_moving = False
mouse_clicked = False


def rotate_2d_array_clockwise(arr):
    return list(zip(*reversed(arr)))


class Board:
    def __init__(self, x, y, board_base_layout, players):
        self.x = x
        self.y = y
        self.board_base_layout = board_base_layout
        self.players = players
        self.turn = 1
        self.rolls = []
        self.roll_index = 0
        self.rolled = False
        self.turn_over = False
        self.rolling = False
        self.last_roll = 0
        self.players_pieces_pos = []
        self.tiles_with_multiple_pieces = []
        self.captured_pieces_info = []
        self.safe_squares_coords = [
            val.center
            for key, val in players[0].pieces[0].piece_path.items()
            if key in SAFE_SQUARES
        ]

        self.pressed = False  # Temp

        # Board Rectangle
        self.rect = pygame.Rect(
            self.x - 2, self.y - 2, 15 * TILE_SIZE + 4, 15 * TILE_SIZE + 4
        )

        # Colors Corresponding to Board Layout Tile Aliases
        self.colors = {
            "TT": LIGHT_GREY,
            "CC": LIGHT_BROWN,
        }

        # Adds Player Colors to self.colors
        # self.players is a Tuple containing Player instances Created from the Player Class
        for player in self.players:
            # player.index will be values 0-3
            self.colors[f"P{player.index}"] = player.base_color

    def draw_base_board(self, surface):
        for i, row in enumerate(self.board_base_layout):
            for j, tile in enumerate(row.split(" ")):
                pygame.draw.rect(
                    surface,
                    self.colors[tile],
                    (
                        self.x + TILE_SIZE * j,
                        self.y + TILE_SIZE * i,
                        TILE_SIZE,
                        TILE_SIZE,
                    ),
                )

    def draw_board_grid(self, surface):
        # Draws Horizontal Lines
        for i in range(1, 15):
            start_x = self.x + TILE_SIZE * (0 if i in range(6, 10) else 6)
            end_x = self.x + TILE_SIZE * (15 if i in range(6, 10) else 9)
            start_y = self.y + TILE_SIZE * i
            end_y = start_y

            pygame.draw.line(surface, DARK_GREY, (start_x, start_y), (end_x, end_y))

        # Draws Vertical Lines
        for i in range(1, 15):
            start_x = self.x + TILE_SIZE * i
            end_x = start_x
            start_y = self.y + TILE_SIZE * (0 if i in range(6, 10) else 6)
            end_y = self.y + TILE_SIZE * (15 if i in range(6, 10) else 9)

            pygame.draw.line(surface, DARK_GREY, (start_x, start_y), (end_x, end_y))

        # Draws Border Around the Board
        self.rect = pygame.draw.rect(surface, DARK_GREY, self.rect, 2)

    def update_tiles_with_multiple_pieces(self):
        flat_list = [j for i in self.players_pieces_pos for j in set(i)]

        self.tiles_with_multiple_pieces = list(
            set([i for i in flat_list if flat_list.count(i) > 1])
        )

    def update_captured_pieces_info(self):
        global is_piece_moving

        self.captured_pieces_info.clear()

        if not is_piece_moving:
            self.captured_pieces_info = [
                (i, self.turn)
                for i in self.tiles_with_multiple_pieces
                if not i in self.safe_squares_coords
            ]

    def draw_board_center(self, surface):
        # Draws Triangles in the Board Center for Each Player
        for player in self.players:
            x1, y1, x2, y2 = CENTER_TRIANGLE_TILES_OFFSET[player.index]

            # pygame.draw.polygon(surface, player.base_color, [
            # (self.x + TILE_SIZE * x1, self.y + TILE_SIZE * y1), (self.x + TILE_SIZE * x2, self.y + TILE_SIZE * y2), self.rect.center])

            gfxdraw.aatrigon(
                surface,
                self.x + TILE_SIZE * x1,
                self.y + TILE_SIZE * y1,
                self.x + TILE_SIZE * x2,
                self.y + TILE_SIZE * y2,
                self.rect.centerx,
                self.rect.centery,
                player.base_color,
            )
            gfxdraw.filled_trigon(
                surface,
                self.x + TILE_SIZE * x1,
                self.y + TILE_SIZE * y1,
                self.x + TILE_SIZE * x2,
                self.y + TILE_SIZE * y2,
                self.rect.centerx,
                self.rect.centery,
                player.base_color,
            )
            # gfxdraw.aatrigon(surface, self.x + TILE_SIZE *
            #                  x1, self.y + TILE_SIZE * y1, self.x + TILE_SIZE * x2, self.y + TILE_SIZE * y2, self.rect.centerx, self.rect.centery, DARK_GREY)

    def draw_player_areas(self, surface):
        for player in self.players:
            player.draw_player_area(surface)

    def draw_players_pieces(self, surface):
        for player in self.players:
            player.draw_pieces(surface)

    def update_turn(self):
        if self.turn_over:
            self.turn += 1

            self.turn_over = False
            self.rolled = False
            self.roll_index = 0
            self.rolls = []

            if self.turn > 3:
                self.turn = 0

    def check_for_six(self):
        global is_piece_moving

        if self.rolled and len(self.rolls) and self.rolls[-1] == 6:
            self.rolled = False

    def draw_temp(self, surface):
        font = pygame.font.SysFont("Futura", 30)

        turnImg = font.render(f"Player {self.turn+1}'s Turn", True, DARK_GREY)
        rollImg = font.render(
            f"Dice Rolls: {' '.join(str(x) for x in self.rolls)}", True, DARK_GREY
        )
        lastRollImg = font.render(f"Last Roll: {self.last_roll}", True, DARK_GREY)
        surface.blit(turnImg, (150, 50))
        surface.blit(rollImg, (350, 50))
        surface.blit(lastRollImg, (50, 150))

    def draw(self, surface):
        self.draw_base_board(surface)
        self.draw_board_grid(surface)
        self.draw_board_center(surface)
        self.draw_player_areas(surface)
        self.draw_players_pieces(surface)
        self.draw_temp(surface)
        self.draw_temp_dice_roll_adder(surface)

    def draw_temp_dice_roll_adder(self, surface):

        for i in range(1, 7):
            r = pygame.draw.rect(surface, LIGHT_GREY, (500 + i * 50, 10, 30, 30))
            pygame.draw.rect(surface, DARK_GREY, (500 + i * 50, 10, 32, 32), 1)

            font = pygame.font.SysFont("Futura", 30)

            numImg = font.render(f"{i}", True, DARK_GREY)

            surface.blit(numImg, (r.x + 10, r.y + 8))

            if r.collidepoint(pygame.mouse.get_pos()) and not self.pressed:
                if pygame.mouse.get_pressed()[0]:
                    self.pressed = True
                    self.rolls.append(i)

            if not pygame.mouse.get_pressed()[0]:
                self.pressed = False

    def update(self):
        if (
            diceRect.collidepoint(pygame.mouse.get_pos())
            and not self.rolled
            and not is_piece_moving
            and not self.rolling
        ):
            if pygame.mouse.get_pressed()[0]:
                roll = random.randint(1, 6)
                self.last_roll = roll
                self.rolls.append(roll)

                self.rolling = True
                self.rolled = True

        if not pygame.mouse.get_pressed()[0]:
            self.rolling = False

        update_again = False

        self.players_pieces_pos.clear()
        for player in self.players:
            player_pieces_pos, update_again_ = player.update(
                self.turn,
                self.rolls,
                self.roll_index,
                self.rolled,
                self.tiles_with_multiple_pieces,
                self.captured_pieces_info,
            )

            update_again = True if update_again_ else update_again

            self.players_pieces_pos.append(player_pieces_pos)

        self.update_tiles_with_multiple_pieces()
        self.update_captured_pieces_info()

        if self.rolled and not is_piece_moving and len(self.rolls) == 0:
            self.turn_over = True

        self.check_for_six()
        self.update_turn()
        return update_again


class Piece:
    def __init__(self, index, color, position, piece_path, player_index):
        self.index = index
        self.player_index = player_index
        self.color = color
        self.initial_position = position
        self.position = self.initial_position
        self.playing = False
        self.promoted = False
        self.path_index = 0
        self.piece_path = piece_path
        self.move_amount = 0
        self.selected = False
        self.speed = 20
        self.speed_counter = self.speed
        self.piece_sizes = ((0.5, 0.5), (0.4, 0.35), (0.2, 0.18))
        self.piece_coords_offset = (
            (0.5, 0.5),
            (0.5, 0.5),
            PIECES_COORDS_OFFSET_FOR_MULTIPLE_PIECES[self.player_index],
        )
        self.piece_draw_index = 0
        self.captured = False

    def draw(self, surface):
        self.draw_piece(surface)

        return self.get_piece_pos_details()[1]

    def draw_piece(self, surface):
        size1, size2 = self.piece_sizes[self.piece_draw_index]
        x_offset, y_offset = self.piece_coords_offset[self.piece_draw_index]

        gfxdraw.aacircle(
            surface,
            int(self.position.x + TILE_SIZE * x_offset),
            int(self.position.y + TILE_SIZE * y_offset),
            int(self.position.height * size1),
            WHITE,
        )
        gfxdraw.filled_circle(
            surface,
            int(self.position.x + TILE_SIZE * x_offset),
            int(self.position.y + TILE_SIZE * y_offset),
            int(self.position.height * size1),
            WHITE,
        )

        gfxdraw.aacircle(
            surface,
            int(self.position.x + TILE_SIZE * x_offset),
            int(self.position.y + TILE_SIZE * y_offset),
            int(self.position.height * size2),
            self.color,
        )
        gfxdraw.filled_circle(
            surface,
            int(self.position.x + TILE_SIZE * x_offset),
            int(self.position.y + TILE_SIZE * y_offset),
            int(self.position.height * size2),
            self.color,
        )

    def get_piece_pos_details(self):
        _, size2 = self.piece_sizes[self.piece_draw_index]
        x_offset, y_offset = self.piece_coords_offset[self.piece_draw_index]

        return (
            self.position.center,
            (
                int(self.position.x + TILE_SIZE * x_offset),
                int(self.position.y + TILE_SIZE * y_offset),
                int(self.position.height * size2),
            ),
        )

    def move(self, rolls, roll_index, is_turn, rolled):
        if self.selected and is_turn and rolled and self.move_amount == 0:
            if self.playing:
                self.move_amount = 0 if len(rolls) == 0 else rolls.pop(roll_index)
            elif rolls[roll_index] == 6:
                rolls.pop(roll_index)
                self.playing = True

    def check_legal_moves(self, is_turn, rolls, rolled):

        return not is_turn or not rolled or self.playing or 6 in rolls

    def click(self, is_turn):
        global is_piece_moving, mouse_clicked

        if (
            self.position.collidepoint(pygame.mouse.get_pos())
            and is_turn
            and not self.selected
            and not is_piece_moving
            and not mouse_clicked
        ):
            if pygame.mouse.get_pressed()[0]:
                self.selected = True
                mouse_clicked = True

        if not pygame.mouse.get_pressed()[0]:
            self.clicked = False

    def moved(self):
        global is_piece_moving

        if self.selected and self.move_amount == 0:
            self.selected = False
            is_piece_moving = False
            self.speed_counter = self.speed

    def reset(self):
        self.position = self.initial_position
        self.path_index = 0
        self.captured = False
        self.playing = False
        self.selected = False

    def check_captured_pieces_info(self, captured_pieces_info):
        for i in captured_pieces_info:
            if i[1] != self.player_index and i[0] == self.position.center:
                self.captured = True

    def update(
        self,
        can_promote,
        is_turn,
        rolls,
        roll_index,
        rolled,
        tiles_with_multiple_pieces,
        captured_pieces_info,
    ):
        global is_piece_moving

        self.check_captured_pieces_info(captured_pieces_info)

        if self.captured:
            self.reset()

        if self.selected:
            self.speed_counter += 1

        self.moved()

        self.click(is_turn)
        self.move(rolls, roll_index, is_turn, rolled)

        self.piece_draw_index = (
            2
            if self.position.center in tiles_with_multiple_pieces
            else 1
            if self.playing
            else 0
        )

        if self.move_amount > 0:
            is_piece_moving = True

        if self.move_amount > 0 and self.speed_counter > self.speed:
            self.path_index += 1
            self.move_amount -= 1
            self.speed_counter = 0

        if not can_promote and self.path_index > 50:
            self.path_index = -1

        if self.path_index > 56:
            self.path_index = 56

        self.position = (
            self.piece_path[self.path_index] if self.playing else self.initial_position
        )

        return (
            self.check_legal_moves(is_turn, rolls, rolled),
            self.get_piece_pos_details()[0],
            self.speed_counter == 0,
        )


class Player:
    def __init__(self, index, base_color, piece_color, max_pieces):
        self.index = index
        self.base_color = base_color
        self.piece_color = piece_color
        self.max_pieces = max_pieces
        self.rect = self.get_player_area_rect()
        self.pieces = self.make_pieces()
        self.can_promote = True
        self.is_turn = False

    def draw_player_area(self, surface):
        pygame.draw.rect(surface, WHITE, self.rect, 0, 15)

    def get_pieces_initial_positions(self):
        # Tiles Offset of Pieces from the start of the Player Area
        tiles_offsets = [(0.4, 0.4), (2.1, 0.4), (0.4, 2.1), (2.1, 2.1)]

        pieces_positions = []

        for i in range(self.max_pieces):
            x1, y1 = tiles_offsets[i]

            piece_position = pygame.Rect(
                self.rect.x + TILE_SIZE * x1,
                self.rect.y + TILE_SIZE * y1,
                TILE_SIZE,
                TILE_SIZE,
            )

            pieces_positions.append(piece_position)

        return pieces_positions

    def draw_pieces(self, surface):
        pieces_pos_details = []

        for piece in self.pieces:
            piece_pos_details = piece.draw(surface)

            pieces_pos_details.append(piece_pos_details)

        for i in set(pieces_pos_details):
            piece_count_on_one_tile = pieces_pos_details.count(i)

            x, y, radius = i

            if piece_count_on_one_tile > 1:
                font = pygame.font.SysFont("Futura", radius * 2)
                textImg = font.render(f"{piece_count_on_one_tile}", True, DARK_GREY)

                surface.blit(
                    textImg,
                    (x - textImg.get_width() / 2 + 1, y - textImg.get_height() / 2 + 1),
                )

    def make_pieces(self):
        pieces = []
        initial_positions = self.get_pieces_initial_positions()
        pieces_path_coords = self.get_pieces_path_coords()

        for i in range(self.max_pieces):
            piece = Piece(
                i,
                self.piece_color,
                initial_positions[i],
                pieces_path_coords,
                self.index,
            )

            pieces.append(piece)

        return pieces

    def get_pieces_path_coords(self):
        pieces_path_2d_arr = [i.split(" ") for i in PIECES_GENERAL_PATH]

        for _ in range(self.index):
            pieces_path_2d_arr = rotate_2d_array_clockwise(pieces_path_2d_arr)

        pieces_path_coords = {}

        for i, row in enumerate(pieces_path_2d_arr):
            for j, tile in enumerate(row):
                if tile != "**":
                    pieces_path_coords[int(tile)] = pygame.Rect(
                        (
                            BOARD_LEFT_X + TILE_SIZE * j,
                            BOARD_TOP_Y + TILE_SIZE * i,
                            TILE_SIZE,
                            TILE_SIZE,
                        )
                    )
        return pieces_path_coords

    def get_player_area_rect(self):
        x1, y1 = PLAYERS_AREA_TILES_OFFSET[self.index]

        return pygame.Rect(
            BOARD_LEFT_X + TILE_SIZE * x1,
            BOARD_TOP_Y + TILE_SIZE * y1,
            TILE_SIZE * 3.5,
            TILE_SIZE * 3.5,
        )

    def update(
        self,
        turn,
        rolls,
        roll_index,
        rolled,
        tiles_with_multiple_pieces,
        captured_pieces_info,
    ):
        self.is_turn = self.index == turn

        if len(captured_pieces_info) and captured_pieces_info[0][1] == self.index:
            self.can_promote = True

        can_pieces_move = []
        pieces_pos = []

        update_again = False

        for piece in self.pieces:
            can_piece_move, piece_pos, update_again_ = piece.update(
                self.can_promote,
                self.is_turn,
                rolls,
                roll_index,
                rolled,
                tiles_with_multiple_pieces,
                captured_pieces_info,
            )

            update_again = True if update_again_ else update_again

            can_pieces_move.append(can_piece_move)
            pieces_pos.append(piece_pos)

        if all(not x for x in can_pieces_move):
            rolls.clear()

        return (pieces_pos, update_again)


player1 = Player(0, RED, DARK_RED, 4)
player2 = Player(1, BLUE, DARK_BLUE, 4)
player3 = Player(2, ORANGE, DARK_ORANGE, 4)
player4 = Player(3, GREEN, DARK_GREEN, 4)

players = (player1, player2, player3, player4)

board = Board(BOARD_LEFT_X, BOARD_TOP_Y, BOARD_BASE_LAYOUT, players)


run = True

while run:
    clock.tick(FPS)

    screen.fill(LIGHT_BROWN)

    diceRect = screen.blit(diceImg, (100, 50))

    update_again = board.update()
    if update_again:
        board.update()
        board.update()
        board.update()
    board.draw(screen)

    mouse_clicked = pygame.mouse.get_pressed()[0]

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Update Pygame Display
    pygame.display.update()

pygame.quit()
