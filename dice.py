import pygame, random

import config
from button import Button
from constants import *
from utils_functions import *


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
            0.5,
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
        # self.draw_temp_dice_roll_adder(surface)

    def check_rolled(self):
        if (
            self.rect.collidepoint(pygame.mouse.get_pos())
            and not self.rolled
            and not config.is_piece_moving
            and not self.rolling
        ):
            config.change_to_button_cursor = True

            if pygame.mouse.get_pressed()[0]:
                roll = random.randint(1, 6 if len(self.rolls) < 5 else 5)
                self.rolling = True

                self.last_roll = roll
                self.rolls.append(roll)

                self.rolls_updated = True

    # def draw_temp_dice_roll_adder(self, surface):

    #     for i in range(1, 7):
    #         button = Button(500 + i * 50, 10, 30, 30, i)
    #         button.update()
    #         button.draw(surface)

    #         if button.get_pressed():
    #             self.rolls.append(i)
    #             self.rolls_updated = True

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
