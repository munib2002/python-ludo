import pygame

import config
from constants import *
from utils_functions import *
from piece import Piece


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
        self.total_possible_moves = []
        self.possible_move_combos = []
        self.can_pieces_move = [False for _ in range(self.max_pieces)]
        self.won = False
        self.playing = len(self.pieces) > 0
        self.finish_position = None

    def draw_player_area(self, surface):
        draw_text(
            surface,
            f"Player {self.index + 1}",
            0.5,
            0.5,
            self.rect.centerx,
            self.rect.centery + TILE_SIZE * 3.4 * (-1 if self.index < 2 else 1),
            TILE_SIZE * 0.7,
            self.piece_color if self.is_turn else GREY,
            bg_color=LIME_GREEN if self.is_turn else DISABLED_GREY,
        )

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
                0.5,
                self.rect.centerx,
                self.rect.centery - TILE_SIZE / 2,
                TILE_SIZE,
            )

            draw_text(
                surface,
                finish_pos_texts[self.finish_position],
                0.5,
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
        if dice.rolled and self.is_turn and not config.is_piece_moving and dice.rolls_updated:
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
            config.is_piece_playing = [False for _ in range(self.max_pieces)]

            for piece in self.pieces:
                config.is_piece_playing[piece.index] = piece.playing

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
                            and (config.is_piece_playing[i] or z[i][0] == "6")
                            for i, v in enumerate(invalid_moves)
                        ]
                    )
                    and any(a != 0 for a in z)
                )
            )

            dice.reset_rolls_updated()

    def update_can_pieces_move(self, dice):
        if dice.rolled and self.is_turn and not config.is_piece_moving and len(dice.rolls):

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
                and not config.is_piece_moving
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
