import pygame

from colors import *
import config


class Button:
    def __init__(
        self, x, y, width, height, text, coord_offset_x=0, coord_offset_y=0, menu=False
    ):
        self.rect = pygame.Rect(
            (x - width * coord_offset_x, y - height * coord_offset_y, width, height)
        )

        self.rect_border = pygame.Rect((x, y, width + 2, height + 2))

        self.rect_border.center = self.rect.center

        self.disabled = False

        self.text = text
        self.pressed = False
        self.selected = False
        self.menu = menu

    def draw(self, surface, color="#EFEBE9"):
        pygame.draw.rect(
            surface,
            DISABLED_GREY if self.disabled else color,
            self.rect,
        )
        pygame.draw.rect(
            surface,
            DARK_BROWN if self.selected and not self.disabled else GREY,
            self.get_border_rect(),
            1 + self.selected,
        )

        font = pygame.font.SysFont("Futura", self.rect.height)

        text_img = font.render(
            f"{self.text}", True, GREY if self.disabled else DARK_GREY
        )

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
                self.rect.w + 1 + self.selected * 2,
                self.rect.h + 1 + self.selected * 2,
            )
        )
        rect.center = self.rect.center

        return rect

    def update(self, selected=False, disabled=False):
        self.disabled = disabled

        if (
            self.rect.collidepoint(pygame.mouse.get_pos())
            and not self.pressed
            and not config.mouse_clicked
            and not disabled
        ):
            config.change_to_button_cursor = True

            if pygame.mouse.get_pressed()[0]:
                self.pressed = True

        if not pygame.mouse.get_pressed()[0]:
            self.pressed = False

        self.selected = selected

    def get_pressed(self):
        return self.pressed
