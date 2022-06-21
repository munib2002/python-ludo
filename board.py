import pygame
from pygame import gfxdraw

import config
from constants import *
from utils_functions import *
from dice import Dice
from player import Player


class Board:
    def __init__(self, x, y, board_base_layout, players):
        self.x = x
        self.y = y
        self.board_base_layout = board_base_layout
        self.players = players
        self.turn = 0
        self.next_finish_position = 1
        self.finish_positions = {0: None, 1: None, 2: None, 3: None}
        self.turn_over = False
        self.game_over = False
        self.players_pieces_pos = []
        self.tiles_with_multiple_pieces = []
        self.captured_pieces_info = []
        self.safe_squares_coords = []

        for player in self.players:
            for piece in player.pieces:
                for key, val in piece.piece_path.items():
                    if key in SAFE_SQUARES:
                        self.safe_squares_coords.append(val.center)
                break
            if len(self.safe_squares_coords):
                break

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
        self.captured_pieces_info.clear()

        if not config.is_piece_moving:
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

    def draw_game_over(self, surface):
        if self.game_over:
            draw_text(
                surface,
                "GAME OVER!",
                0.5,
                0.5,
                SCREEN_WIDTH / 2,
                SCREEN_HEIGHT / 2,
                TILE_SIZE * 2,
            )

    def update_turn(self):
        if self.turn_over:
            self.turn += 1

            self.turn_over = False
            self.dice.reset()

            if self.turn >= len(self.players):
                self.turn = 0

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
        self.dice.draw(surface)
        self.draw_game_over(surface)

    def next_turn(self):
        self.turn_over = True

    def reset(self, config):
        return self.create_board(config)

    @classmethod
    def create_board(self, config):
        players = []

        for player_config in config.players_config["players"].values():

            player = Player(
                player_config["index"],
                player_config["base_color"],
                player_config["piece_color"],
                player_config["max_pieces"] if player_config["playing"] else 0,
            )

            players.append(player)

        return Board(BOARD_LEFT_X, BOARD_TOP_Y, BOARD_BASE_LAYOUT, players)

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
