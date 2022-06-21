import pygame

import config
from constants import *
from button import Button
from utils_functions import *


class Player_Config:
    def __init__(self, x, y, player_index, coord_offset_x, coord_offset_y):
        self.rect = pygame.Rect((x, y, TILE_SIZE * 6, TILE_SIZE * 5))

        self.rect.center = (
            self.rect.centerx - self.rect.w * coord_offset_x,
            self.rect.centery - self.rect.h * coord_offset_y,
        )

        player_config = config.players_config["players"][f"player-{player_index+1}"]

        self.player_playing = player_config["playing"]
        self.buttons = []
        self.selected_btn_index = player_config["max_pieces"] - 1
        self.player_index = player_index
        self.select_button = Button(
            self.rect.centerx + TILE_SIZE * 0.4,
            self.rect.y + TILE_SIZE * 1.9,
            TILE_SIZE * 0.5,
            TILE_SIZE * 0.5,
            "",
        )

        self.total_players_playing = 4

        self.select_img = pygame.image.load("images/tick.png").convert_alpha()
        self.select_img = pygame.transform.scale(
            self.select_img, (TILE_SIZE / 2, TILE_SIZE / 2)
        )

        self.make_buttons()

    def make_buttons(self):
        for i in range(4):
            btn = Button(
                self.rect.centerx + TILE_SIZE * (i * 0.7 - 1.35),
                self.rect.y + TILE_SIZE * 3.2,
                TILE_SIZE * 0.5,
                TILE_SIZE * 0.5,
                i + 1,
            )
            self.buttons.append(btn)

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 204, 188), self.rect)
        pygame.draw.rect(surface, DARK_BROWN, self.rect, 3)

        draw_text(
            surface,
            f"Player {self.player_index + 1}",
            0.5,
            0,
            self.rect.centerx,
            self.rect.y + TILE_SIZE / 2,
            TILE_SIZE,
        )

        draw_text(
            surface,
            f"Select: ",
            0.5,
            0,
            self.rect.centerx - TILE_SIZE * 0.7,
            self.rect.y + TILE_SIZE * 2,
            TILE_SIZE / 2,
        )
        draw_text(
            surface,
            f"No. of Pieces: ",
            0.5,
            0,
            self.rect.centerx - TILE_SIZE * 0.2,
            self.rect.y + TILE_SIZE * 2.7,
            TILE_SIZE / 2,
        )

        for btn in self.buttons:
            btn.draw(surface)

        self.select_button.draw(surface)

        if self.player_playing:
            surface.blit(self.select_img, self.select_button.rect)

    def update(self):
        self.total_players_playing = len(
            [True for x in config.players_config["players"].values() if x["playing"]]
        )

        for i, btn in enumerate(self.buttons):
            btn_selected = i == self.selected_btn_index
            btn.update(btn_selected)

            if btn.get_pressed():
                self.selected_btn_index = i

        self.select_button.update(
            selected=self.player_playing,
            disabled=self.total_players_playing < 3 and self.player_playing,
        )

        if self.select_button.get_pressed() and not config.mouse_clicked:
            self.player_playing = not self.player_playing

        config.players_config["players"][f"player-{self.player_index+1}"][
            "max_pieces"
        ] = (self.selected_btn_index + 1)
        config.players_config["players"][f"player-{self.player_index+1}"][
            "playing"
        ] = self.player_playing
