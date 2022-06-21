import pygame
from pygame import gfxdraw

import config
from constants import *
from utils_functions import *


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
        if (
            self.position.collidepoint(pygame.mouse.get_pos())
            and self.can_move
            and is_turn
            and not self.selected
            and not config.is_piece_moving
            and not config.mouse_clicked
        ):
            config.change_to_button_cursor = True

            if pygame.mouse.get_pressed()[0]:
                self.selected = True
                config.mouse_clicked = True

        if not pygame.mouse.get_pressed()[0]:
            self.clicked = False

    def moved(self):
        if self.selected and self.move_amount == 0:
            self.selected = False
            config.is_piece_moving = False
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
                config.is_piece_moving = True

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
