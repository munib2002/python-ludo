import pygame
from itertools import combinations, permutations, chain

from colors import *


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


def draw_text(
    surface,
    text,
    coord_offset_x,
    coord_offset_y,
    x,
    y,
    height,
    color=DARK_GREY,
    bg_color=None,
):
    font = pygame.font.SysFont("Futura", int(height))
    text_img = font.render(f"{text}", True, color)

    pygame.rect

    if bg_color:
        border_rect = pygame.Rect(
            (
                x - text_img.get_width() * coord_offset_x - 6,
                y - text_img.get_height() * coord_offset_y - 6,
                text_img.get_width() + 12,
                text_img.get_height() + 12,
            ),
        )

        pygame.draw.rect(surface, bg_color, border_rect)
        pygame.draw.rect(surface, DARK_BROWN, border_rect, 2)

    surface.blit(
        text_img,
        (
            x - text_img.get_width() * coord_offset_x,
            y - text_img.get_height() * coord_offset_y,
        ),
    )
