import pygame
from pygame import gfxdraw
import random
from itertools import combinations, permutations, chain

# Initialize Pygame
pygame.init()

# Setup Clock
clock = pygame.time.Clock()

# Game Variables
FPS = 60
TILE_SIZE = 60

# Screen Size
SCREEN_WIDTH = TILE_SIZE * 22
SCREEN_HEIGHT = SCREEN_WIDTH * 0.9

# Ludo Board Start Coordinates
BOARD_LEFT_X = int((SCREEN_WIDTH - 15 * TILE_SIZE) / 2)
BOARD_TOP_Y = int((SCREEN_HEIGHT - 15 * TILE_SIZE) / 2)


# Colors
RED = (231, 76, 60)
DARK_RED = (192, 57, 43)
BLUE = (72, 219, 251)
DARK_BLUE = (10, 189, 227)
LIGHT_GREEN = (0, 230, 118)
GREEN = (46, 204, 113)
DARK_GREEN = (30, 179, 100)
ORANGE = (253, 150, 68)
DARK_ORANGE = (239, 108, 0)
DEEP_ORANGE = (255, 87, 34)
LIGHT_GREY = (223, 228, 234)
GREY = (117, 117, 117)
BROWN = (109, 76, 65)
LIGHT_BROWN = (247, 241, 227)
DARK_GREY = (47, 53, 66)
WHITE = (255, 255, 255)
DARK_BROWN = (62, 39, 35)

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
change_to_button_cursor = False


def rotate_2d_array_clockwise(arr):
    return list(zip(*reversed(arr)))


def splits_r(str, current, res, max_splits):

    if len(str) == 0:
        if len(current) <= max_splits:
            res += [sorted(current, key=int)]
    else:
        for i in range(len(str)):
            splits_r(str[i + 1 :], current + [str[0 : i + 1]], res, max_splits)


def splits(str, max_splits):

    res = []

    splits_r(str, [], res, max_splits)

    return res


def unique_powerset_of_string(iterable):
    s = list(iterable)
    return list(
        set(
            "".join(sorted(x))
            for x in chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))
            if x
        )
    )


def permutate_string(string):
    return list(set("".join(x) for x in permutations(string)))


def draw_text(surface, text, coord_pos_offset, x, y, height, color=DARK_GREY):
    font = pygame.font.SysFont("Futura", int(height))
    text_img = font.render(f"{text}", True, color)

    pygame.rect

    surface.blit(
        text_img,
        (
            x - text_img.get_width() * coord_pos_offset,
            y - text_img.get_height() / 2 + 1,
        ),
    )


class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect((x, y, width, height))
        self.rect_border = pygame.Rect((x, y, width + 2, height + 2))

        self.rect_border.center = self.rect.center

        self.text = text
        self.pressed = False
        self.selected = False

    def draw(self, surface, color=LIGHT_GREY):
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(
            surface,
            BROWN if self.selected else GREY,
            self.get_border_rect(),
            1 + self.selected,
        )

        font = pygame.font.SysFont("Futura", self.rect.height)

        text_img = font.render(f"{self.text}", True, DARK_GREY)

        surface.blit(
            text_img,
            (
                self.rect.centerx - text_img.get_width() / 2 + 1,
                self.rect.centery - text_img.get_height() / 2 + 1,
            ),
        )

    def get_border_rect(self):
        rect = pygame.Rect(
            (
                0,
                0,
                self.rect.h + 1 + self.selected * 2,
                self.rect.w + 1 + self.selected * 2,
            )
        )
        rect.center = self.rect.center

        return rect

    def update(self, selected=False):
        global change_to_button_cursor

        if (
            self.rect.collidepoint(pygame.mouse.get_pos())
            and not self.pressed
            and not mouse_clicked
        ):
            change_to_button_cursor = True

            if pygame.mouse.get_pressed()[0]:
                self.pressed = True

        if not pygame.mouse.get_pressed()[0]:
            self.pressed = False

        self.selected = selected

    def get_pressed(self):
        return self.pressed


class Dice:
    def __init__(self, x, y, width, height):
        self.all_dice = []

        self.rect = pygame.Rect((x, y, width + 1, height + 1))
        self.rect.center = (x, y)

        self.dice_img_index = 0
        self.last_role = 1
        self.rolls = []
        self.roll_index = 0
        self.rolling = False
        self.rolled = False
        self.rolls_updated = False
        self.rolls_buttons = []

        self.rolling_time = 80
        self.rolling_time_counter = 0
        self.rolling_speed = 4
        self.rolling_speed_counter = 0

        for i in range(1, 7):
            img = pygame.image.load(f"images/dice/dice-{i}.png").convert_alpha()
            img = pygame.transform.scale(img, (width, height)).convert_alpha()
            self.all_dice.append(img)

    def update_rolls_buttons(self):
        self.rolls_buttons = []
        for i, val in enumerate(self.rolls):
            button = Button(
                BOARD_LEFT_X + i * TILE_SIZE * 0.8,
                BOARD_TOP_Y / 2 - TILE_SIZE / 4 + 1,
                TILE_SIZE / 2,
                TILE_SIZE / 2,
                val,
            )

            self.rolls_buttons.append(button)

            is_button_selected = self.roll_index == i

            button.update(is_button_selected)

            if button.get_pressed():
                self.roll_index = i

    def draw_rolls_buttons(self, surface):
        draw_text(
            surface,
            "Dice Rolls: ",
            1,
            BOARD_LEFT_X,
            BOARD_TOP_Y / 2,
            TILE_SIZE / 2,
        )

        for button in self.rolls_buttons[:-1] if self.rolling else self.rolls_buttons:
            button.draw(surface)

    def draw(self, surface):
        surface.blit(
            self.all_dice[self.dice_img_index],
            self.rect,
        )

        pygame.draw.rect(
            surface, GREY if self.rolled or self.rolling else BROWN, self.rect, 4, 8
        )

        self.draw_rolls_buttons(surface)
        self.draw_temp_dice_roll_adder(surface)

    def check_rolled(self):
        global change_to_button_cursor

        if (
            self.rect.collidepoint(pygame.mouse.get_pos())
            and not self.rolled
            and not is_piece_moving
            and not self.rolling
        ):
            change_to_button_cursor = True

            if pygame.mouse.get_pressed()[0]:
                roll = random.randint(1, 6 if len(self.rolls) < 6 else 5)
                self.rolling = True

                self.last_roll = roll
                self.rolls.append(roll)

                self.rolls_updated = True

    def draw_temp_dice_roll_adder(self, surface):

        for i in range(1, 7):
            button = Button(500 + i * 50, 10, 30, 30, i)
            button.update()
            button.draw(surface)

            if button.get_pressed():
                self.rolls.append(i)
                self.rolls_updated = True

    def reset(self):
        self.rolls.clear()
        self.rolled = False
        self.rolling = False
        self.roll_index = 0

    def reset_rolls_updated(self):
        self.rolls_updated = False

    def update_rolls(self):
        roll = self.rolls.pop(self.roll_index)
        self.roll_index = 0

        self.rolls_updated = True

        return roll

    def update(self):
        self.check_rolled()

        if self.rolling:
            if self.rolling_speed_counter >= self.rolling_speed:
                roll_img_options = list(range(6))
                del roll_img_options[self.dice_img_index]

                self.dice_img_index = random.choice(roll_img_options)

                self.rolling_speed_counter = 0

            self.rolling_speed_counter += 1
            self.rolling_time_counter += 1

        if (
            self.rolling_time_counter >= self.rolling_time
            and not pygame.mouse.get_pressed()[0]
        ):
            if self.last_roll != 6:
                self.rolled = True
                if len(self.rolls) == 4:
                    self.rolls = self.rolls[-1:]

            self.rolling = False
            self.dice_img_index = self.last_roll - 1
            self.rolling_speed_counter = 0
            self.rolling_time_counter = 0


class Board:
    def __init__(self, x, y, board_base_layout, players):
        self.x = x
        self.y = y
        self.board_base_layout = board_base_layout
        self.players = players
        self.turn = 1
        self.next_finish_position = 1
        self.finish_positions = {0: None, 1: None, 2: None, 3: None}
        self.turn_over = False
        self.game_over = False
        self.players_pieces_pos = []
        self.tiles_with_multiple_pieces = []
        self.captured_pieces_info = []
        self.safe_squares_coords = [
            val.center
            for key, val in players[0].pieces[0].piece_path.items()
            if key in SAFE_SQUARES
        ]

        # Board Rectangle
        self.rect = pygame.Rect(
            self.x - 2, self.y - 2, 15 * TILE_SIZE + 4, 15 * TILE_SIZE + 4
        )

        self.dice = Dice(*self.rect.center, TILE_SIZE, TILE_SIZE)

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
            self.dice.reset()

            if self.turn >= len(self.players):
                self.turn = 0

    def draw_temp(self, surface):
        font = pygame.font.SysFont("Futura", 30)

        turnImg = font.render(f"Player {self.turn+1}'s Turn", True, DARK_GREY)
        surface.blit(turnImg, (40, 120))

    def check_game_over(self):
        if (
            len([True for player in self.players if player.playing])
            <= self.next_finish_position
        ):
            self.game_over = True

    def draw(self, surface):
        self.draw_base_board(surface)
        self.draw_board_grid(surface)
        self.draw_board_center(surface)
        self.draw_player_areas(surface)
        self.draw_players_pieces(surface)
        self.draw_temp(surface)
        self.dice.draw(surface)

    def next_turn(self):
        self.turn_over = True

    def update(self):
        if not self.game_over:
            self.check_game_over()
            self.dice.update()

            update_again = False

            self.players_pieces_pos.clear()
            for player in self.players:
                player_pieces_pos, update_again_ = player.update(
                    self.turn,
                    self.dice,
                    self.tiles_with_multiple_pieces,
                    self.captured_pieces_info,
                    self.next_turn,
                    self.finish_positions,
                )

                if player.won and not self.finish_positions[player.index]:
                    self.finish_positions[player.index] = self.next_finish_position

                    self.next_finish_position += 1

                update_again = True if update_again_ else update_again

                self.players_pieces_pos.append(player_pieces_pos)

            self.update_tiles_with_multiple_pieces()
            self.update_captured_pieces_info()

            self.update_turn()
            self.dice.update_rolls_buttons()

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
        self.speed = 15
        self.speed_counter = self.speed
        self.piece_sizes = ((0.58, 0.5), (0.4, 0.35), (0.2, 0.18))
        self.piece_coords_offset = (
            (0.5, 0.5),
            (0.5, 0.5),
            PIECES_COORDS_OFFSET_FOR_MULTIPLE_PIECES[self.player_index],
        )
        self.piece_draw_index = 0
        self.captured = False
        self.can_move = False

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
            DARK_BROWN if self.can_move else WHITE,
        )
        gfxdraw.filled_circle(
            surface,
            int(self.position.x + TILE_SIZE * x_offset),
            int(self.position.y + TILE_SIZE * y_offset),
            int(self.position.height * size1),
            DARK_BROWN if self.can_move else WHITE,
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

    def move(self, is_turn, dice):
        if self.selected and is_turn and dice.rolled and self.move_amount == 0:
            if self.playing:
                self.move_amount = 0 if len(dice.rolls) == 0 else dice.update_rolls()
            elif dice.rolls[dice.roll_index] == 6:
                dice.update_rolls()
                self.playing = True
                return True

    def click(self, is_turn):
        global is_piece_moving, mouse_clicked, change_to_button_cursor

        if (
            self.position.collidepoint(pygame.mouse.get_pos())
            and self.can_move
            and is_turn
            and not self.selected
            and not is_piece_moving
            and not mouse_clicked
        ):
            change_to_button_cursor = True

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

    def check_promoted(self):
        if self.path_index == 56:
            self.promoted = True

    def update(
        self,
        can_promote,
        is_turn,
        dice,
        tiles_with_multiple_pieces,
        captured_pieces_info,
        can_piece_move,
    ):
        update_again_ = False

        if not self.promoted:
            global is_piece_moving

            self.check_promoted()

            self.can_move = can_piece_move

            self.check_captured_pieces_info(captured_pieces_info)

            if self.captured:
                self.reset()

            if self.selected:
                self.speed_counter += 1

            self.moved()

            self.click(is_turn)
            update_again_ = self.move(is_turn, dice)

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

            self.position = (
                self.piece_path[self.path_index]
                if self.playing
                else self.initial_position
            )

        return (
            self.get_piece_pos_details()[0],
            self.speed_counter == 0 or update_again_,
        )


class Player:
    def __init__(self, index, base_color, piece_color, max_pieces):
        self.index = index
        self.base_color = base_color
        self.piece_color = piece_color
        self.max_pieces = max_pieces
        self.rect = self.get_player_area_rect()
        self.pieces = self.make_pieces()
        self.pieces_pos = []
        self.can_promote = True
        self.is_turn = False
        # self.total_move_combos = []
        self.total_possible_moves = []
        self.possible_move_combos = []
        self.can_pieces_move = [False for _ in range(self.max_pieces)]
        self.won = False
        self.playing = len(self.pieces) > 0
        self.finish_position = None

    def draw_player_area(self, surface):
        pygame.draw.rect(surface, WHITE, self.rect, 0, 15)

        if self.playing and not self.won:
            pygame.draw.rect(
                surface, DARK_BROWN if self.is_turn else WHITE, self.rect, 5, 15
            )

        if self.won and self.finish_position:
            finish_pos_texts = {1: "1st", 2: "2nd", 3: "3rd", 4: "4th"}

            draw_text(
                surface,
                "FINISHED!",
                0.5,
                self.rect.centerx,
                self.rect.centery - TILE_SIZE / 2,
                TILE_SIZE,
            )

            draw_text(
                surface,
                finish_pos_texts[self.finish_position],
                0.5,
                self.rect.centerx,
                self.rect.centery + TILE_SIZE / 2,
                TILE_SIZE,
            )

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

    def update_move_combos(self, dice):
        if dice.rolled and self.is_turn and not is_piece_moving and dice.rolls_updated:
            rolls_str = "".join(str(x) for x in dice.rolls)

            moves_permutation = permutate_string(rolls_str)

            move_combos_for_1_order = [
                list(move_combo) + [0 for _ in range(self.max_pieces - len(move_combo))]
                for move_combo in set(
                    tuple(move_combo)
                    for move_order in moves_permutation
                    for move_combo in splits(move_order, self.max_pieces)
                )
            ]

            self.total_possible_moves = unique_powerset_of_string(rolls_str)

            invalid_moves = [[] for _ in range(self.max_pieces)]
            is_piece_playing = [False for _ in range(self.max_pieces)]

            for piece in self.pieces:
                is_piece_playing[piece.index] = piece.playing

                move_limit = 56 - piece.path_index + (6 if not piece.playing else 0)

                for moves in self.total_possible_moves:
                    moves_sum = sum([int(x) for x in moves])
                    if moves_sum > move_limit:
                        invalid_moves[piece.index].append(moves)

            self.possible_move_combos = list(
                set(
                    z
                    for x in list(
                        list(set(permutations(x))) for x in move_combos_for_1_order
                    )
                    for z in x
                    if all(
                        [
                            z[i] == 0
                            or "".join(sorted(list(z[i]), key=int)) not in v
                            and (is_piece_playing[i] or z[i][0] == "6")
                            for i, v in enumerate(invalid_moves)
                        ]
                    )
                    and any(a != 0 for a in z)
                )
            )

            dice.reset_rolls_updated()

    def update_can_pieces_move(self, dice):
        if dice.rolled and self.is_turn and not is_piece_moving and len(dice.rolls):

            roll = dice.rolls[dice.roll_index]

            for piece in self.pieces:
                self.can_pieces_move[piece.index] = any(
                    int(x[piece.index][0]) == roll
                    for x in self.possible_move_combos
                    if x[piece.index]
                )

        else:
            self.can_pieces_move = [False for _ in range(self.max_pieces)]

    def get_player_area_rect(self):
        x1, y1 = PLAYERS_AREA_TILES_OFFSET[self.index]

        return pygame.Rect(
            BOARD_LEFT_X + TILE_SIZE * x1,
            BOARD_TOP_Y + TILE_SIZE * y1,
            TILE_SIZE * 3.5,
            TILE_SIZE * 3.5,
        )

    def check_win(self):
        if all(piece.promoted for piece in self.pieces):
            self.won = True

    def update(
        self,
        turn,
        dice,
        tiles_with_multiple_pieces,
        captured_pieces_info,
        next_turn,
        finish_positions,
    ):
        self.is_turn = self.index == turn

        if not self.won and self.playing:
            self.check_win()

            if len(captured_pieces_info) and captured_pieces_info[0][1] == self.index:
                self.can_promote = True

            pieces_pos = []

            update_again = False

            self.update_move_combos(dice)
            self.update_can_pieces_move(dice)

            if (
                self.is_turn
                and not is_piece_moving
                and len(self.possible_move_combos) == 0
                and dice.rolled
                and not dice.rolling
            ):
                next_turn()

            for piece in self.pieces:
                piece_pos, update_again_ = piece.update(
                    self.can_promote,
                    self.is_turn,
                    dice,
                    tiles_with_multiple_pieces,
                    captured_pieces_info,
                    self.can_pieces_move[piece.index],
                )

                update_again = True if update_again_ else update_again

                pieces_pos.append(piece_pos)

            return (pieces_pos, update_again)
        else:
            if self.is_turn:
                next_turn()

            if self.won:
                self.finish_position = finish_positions[self.index]

            return (self.pieces_pos, False)


def play_ludo():
    global change_to_button_cursor, mouse_clicked

    # Setup Game Window
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Ludo")

    player1 = Player(0, RED, DARK_RED, 2)
    player2 = Player(1, BLUE, DARK_BLUE, 1)
    player3 = Player(2, ORANGE, DARK_ORANGE, 0)
    player4 = Player(3, GREEN, DARK_GREEN, 0)

    players = (player1, player2, player3, player4)

    board = Board(BOARD_LEFT_X, BOARD_TOP_Y, BOARD_BASE_LAYOUT, players)

    run = True

    while run:
        clock.tick(FPS)

        screen.fill(LIGHT_BROWN)

        change_to_button_cursor = False

        update_again = board.update()
        if update_again:
            board.update()
            board.update()
            board.update()

        board.draw(screen)

        mouse_clicked = pygame.mouse.get_pressed()[0]

        if change_to_button_cursor:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # Update Pygame Display
        pygame.display.update()

    pygame.quit()


play_ludo()
