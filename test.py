import pygame
from pygame import gfxdraw

pygame.init()

clock = pygame.time.Clock()

SX = 1300
SY = 1100

TILE_SIZE = 60

BOARD = [
    'RRRRRRTTTBBBBBB',
    'RRRRRRTBBBBBBBB',
    'RRRRRRBBTBBBBBB',
    'RRRRRRTBTBBBBBB',
    'RRRRRRTBTBBBBBB',
    'RRRRRRTBTBBBBBB',
    'TRTTTTCCCTTTGTT',
    'TRRRRRCCCGGGGGT',
    'TTRTTTCCCTTTTGT',
    'OOOOOOTOTGGGGGG',
    'OOOOOOTOTGGGGGG',
    'OOOOOOTOTGGGGGG',
    'OOOOOOTOOGGGGGG',
    'OOOOOOOOTGGGGGG',
    'OOOOOOTTTGGGGGG',
]

PATHS = {
    "RED": [
        '* * * * * * 10 11 12 * * * * * *',
        '* * * * * * 9 * 13 * * * * * *',
        '* * * * * * 8 * 14 * * * * * *',
        '* * * * * * 7 * 15 * * * * * *',
        '* * * * * * 6 * 16 * * * * * *',
        '* * * * * * 5 * 17 * * * * * *',
        '-1 0 1 2 3 4 * * * 18 19 20 21 22 23',
        '50 51 52 53 54 55 56 * * * * * * * 24',
        '49 48 47 46 45 44 * * * 30 29 28 27 26 25',
        '* * * * * * 43 * 31 * * * * * *',
        '* * * * * * 42 * 32 * * * * * *',
        '* * * * * * 41 * 33 * * * * * *',
        '* * * * * * 40 * 34 * * * * * *',
        '* * * * * * 39 * 35 * * * * * *',
        '* * * * * * 38 37 36 * * * * * *',
    ],
    "BLUE": [
        '* * * * * * 49 50 -1 * * * * * *',
        '* * * * * * 48 51 0 * * * * * *',
        '* * * * * * 47 52 1 * * * * * *',
        '* * * * * * 46 53 2 * * * * * *',
        '* * * * * * 45 54 3 * * * * * *',
        '* * * * * * 44 55 4 * * * * * *',
        '38 39 40 41 42 43 * 56 * 5 6 7 8 9 10',
        '37 * * * * * * * * * * * * * 11',
        '36 35 34 33 32 31 * * * 17 16 15 14 13 12',
        '* * * * * * 30 * 18 * * * * * *',
        '* * * * * * 29 * 19 * * * * * *',
        '* * * * * * 28 * 20 * * * * * *',
        '* * * * * * 27 * 21 * * * * * *',
        '* * * * * * 26 * 22 * * * * * *',
        '* * * * * * 25 24 23 * * * * * *',
    ],
    "GREEN": [
        '* * * * * * 36 37 38 * * * * * *',
        '* * * * * * 35 * 39 * * * * * *',
        '* * * * * * 34 * 40 * * * * * *',
        '* * * * * * 33 * 41 * * * * * *',
        '* * * * * * 32 * 42 * * * * * *',
        '* * * * * * 31 * 43 * * * * * *',
        '25 26 27 28 29 30 * * * 44 45 46 47 48 49',
        '24 * * * * * * * 56 55 54 53 52 51 50',
        '23 22 21 20 19 18 * * * 4 3 2 1 0 -1',
        '* * * * * * 17 * 5 * * * * * *',
        '* * * * * * 16 * 6 * * * * * *',
        '* * * * * * 15 * 7 * * * * * *',
        '* * * * * * 14 * 8 * * * * * *',
        '* * * * * * 13 * 9 * * * * * *',
        '* * * * * * 12 11 10 * * * * * *',
    ],
    "ORANGE": [
        '* * * * * * 23 24 25 * * * * * *',
        '* * * * * * 22 * 26 * * * * * *',
        '* * * * * * 21 * 27 * * * * * *',
        '* * * * * * 20 * 28 * * * * * *',
        '* * * * * * 19 * 29 * * * * * *',
        '* * * * * * 18 * 30 * * * * * *',
        '12 13 14 15 16 17 * * * 31 32 33 34 35 36',
        '11 * * * * * * * * * * * * * 37',
        '10 9 8 7 6 5 * 56 * 43 42 41 40 39 38',
        '* * * * * * 4 55 44 * * * * * *',
        '* * * * * * 3 54 45 * * * * * *',
        '* * * * * * 2 53 46 * * * * * *',
        '* * * * * * 1 52 47 * * * * * *',
        '* * * * * * 0 51 48 * * * * * *',
        '* * * * * * -1 50 49 * * * * * *',
    ]
}

RED = (231, 76, 60)
GREEN = (46, 204, 113)
BLUE = (72, 219, 251)
ORANGE = (253, 150, 68)
TILE = (223, 228, 234)
BG = (247, 241, 227)
LINE = (47, 53, 66)
CENTER = (109, 76, 65)
WHITE = (255, 255, 255)

RED_P = (192, 57, 43)
BLUE_P = (10, 189, 227)
GREEN_P = (30, 179, 100)
ORANGE_P = (239, 108, 0)

COLORS = {
    "R": RED,
    "G": GREEN,
    "B": BLUE,
    "O": ORANGE,
    "C": TILE,
    "T": TILE,
    "W": WHITE,
    "P_R": RED_P,
    "P_B": BLUE_P,
    "P_G": GREEN_P,
    "P_O": ORANGE_P
}

screen = pygame.display.set_mode((SX, SY))

posR = 0
posB = 0
posG = 0
posO = 0
pR = {}
pB = {}
pG = {}
pO = {}
pR1 = True
pB1 = False
pG1 = False
pO1 = True


def drawPiece(p, pos, color):
    gfxdraw.aacircle(screen,  int(p[pos].centerx),
                     int(p[pos].centery), int(TILE_SIZE * 0.4), WHITE)
    gfxdraw.filled_circle(screen,  int(p[pos].centerx),
                          int(p[pos].centery), int(TILE_SIZE * 0.4), WHITE)

    gfxdraw.aacircle(screen,  int(p[pos].centerx),
                     int(p[pos].centery), int(TILE_SIZE * 0.35), color)
    gfxdraw.filled_circle(screen,  int(p[pos].centerx),
                          int(p[pos].centery), int(TILE_SIZE * 0.35), color)


for i, row in enumerate(PATHS['RED']):
    for j, tile in enumerate(row.split(' ')):
        if tile != '*':
            pR[int(tile)] = pygame.Rect((200 + TILE_SIZE * j,
                                        100 + TILE_SIZE * i, TILE_SIZE, TILE_SIZE))
for i, row in enumerate(PATHS['BLUE']):
    for j, tile in enumerate(row.split(' ')):
        if tile != '*':
            pB[int(tile)] = pygame.Rect((200 + TILE_SIZE * j,
                                        100 + TILE_SIZE * i, TILE_SIZE, TILE_SIZE))

for i, row in enumerate(PATHS['GREEN']):
    for j, tile in enumerate(row.split(' ')):
        if tile != '*':
            pG[int(tile)] = pygame.Rect((200 + TILE_SIZE * j,
                                        100 + TILE_SIZE * i, TILE_SIZE, TILE_SIZE))
for i, row in enumerate(PATHS['ORANGE']):
    for j, tile in enumerate(row.split(' ')):
        if tile != '*':
            pO[int(tile)] = pygame.Rect((200 + TILE_SIZE * j,
                                        100 + TILE_SIZE * i, TILE_SIZE, TILE_SIZE))

run = True
while run:

    screen.fill(BG)

    clock.tick(5)

    re = []

    for i, row in enumerate(BOARD):
        for j, tile in enumerate(row):
            print(i, j, row, tile)
            re.append(pygame.draw.rect(
                screen, COLORS[tile], (200 + TILE_SIZE * j, 100 + TILE_SIZE * i, TILE_SIZE, TILE_SIZE)))

    for i in range(1, len(BOARD)+1):
        s = 0 if i > 5 and i < 10 else 6
        e = 9 if s else 15
        pygame.draw.line(screen, LINE, (200 + TILE_SIZE * s, 100 +
                         i * TILE_SIZE), (200 + e*TILE_SIZE, 100 + i * TILE_SIZE))

    for i in range(1, len(BOARD[0])+1):
        s = 0 if i > 5 and i < 10 else 6
        e = 9 if s else 15
        pygame.draw.line(screen, LINE, (200+i*TILE_SIZE, 100 + TILE_SIZE * s),
                         (200+i*TILE_SIZE, 100+e*TILE_SIZE))

    pygame.draw.rect(screen, LINE, (200 - 2, 100 - 2, 15 *
                     TILE_SIZE + 4, 15 * TILE_SIZE + 4), 2)

    for val in [("B", (6, 6, 9, 6)), ("R", (6, 6, 6, 9)), ("G", (9, 6, 9, 9)), ("O", (6, 9, 9, 9))]:
        pygame.draw.polygon(screen, COLORS[val[0]], [
            (200 + TILE_SIZE * val[1][0], 100 + TILE_SIZE * val[1][1]), (200 + TILE_SIZE * val[1][2], 100 + TILE_SIZE * val[1][3]), (200 + TILE_SIZE * 7 + TILE_SIZE/2, 100 + TILE_SIZE * 7 + TILE_SIZE/2)])

    r = []

    for val in [(0, 0), (9, 0), (0, 9), (9, 9)]:
        z = pygame.draw.rect(screen, WHITE, (200 + TILE_SIZE * (1.25 + val[0]), 100 + TILE_SIZE * (
            1.25 + val[1]), TILE_SIZE*3.5, TILE_SIZE*3.5), 0, 15)
        r.append(z)

    for i, val in enumerate(r):
        temp_colors = ["P_R", "P_B", "P_O", "P_G"]
        for c in [(0.5, 0.5), (1.5, 0.5), (0.5, 1.5), (1.5, 1.5)]:
            gfxdraw.aacircle(screen,  int(val.topleft[0] + (val.centerx-val.topleft[0])*c[0]),
                             int(val.topleft[1] + (val.centery-val.topleft[1])*c[1]), int(TILE_SIZE/2), COLORS[temp_colors[i]])
            gfxdraw.filled_circle(screen,  int(val.topleft[0] + (val.centerx-val.topleft[0])*c[0]),
                                  int(val.topleft[1] + (val.centery-val.topleft[1])*c[1]), int(TILE_SIZE/2), COLORS[temp_colors[i]])
            

    drawPiece(pR, posR, RED_P)
    drawPiece(pB, posB, BLUE_P)
    drawPiece(pG, posG, GREEN_P)
    drawPiece(pO, posO, ORANGE_P)

    posR += 1

    if not pR1 and posR > 50:
        posR = -1
    if posR > 56:
        posR = 56

    posB += 1

    if not pB1 and posB > 50:
        posB = -1
    if posB > 56:
        posB = 56

    posG += 1

    if not pG1 and posG > 50:
        posG = -1
    if posG > 56:
        posG = 56

    posO += 1

    if not pO1 and posO > 50:
        posO = -1
    if posO > 56:
        posO = 56

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False


pygame.quit()
