import random, time, msvcrt
from enum import Enum
WAIT_SECONDS = 1 / 60
FALL_COUNT = 1.0
MINOS = [
    [ # I
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [1, 1, 1, 1],
        [0, 0, 0, 0],
    ],
    [ # O
        [0, 0, 0, 0],
        [0, 1, 1, 0],
        [0, 1, 1, 0],
        [0, 0, 0, 0],
    ],
    [ # L
        [0, 1, 0, 0],
        [0, 1, 0, 0],
        [0, 1, 1, 0],
        [0, 0, 0, 0],
    ],
    [ # J
        [0, 0, 1, 0],
        [0, 0, 1, 0],
        [0, 1, 1, 0],
        [0, 0, 0, 0],
    ],
    [ # S
        [0, 1, 0, 0],
        [0, 1, 1, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 0],
    ],
    [ # Z
        [0, 0, 1, 0],
        [0, 1, 1, 0],
        [0, 1, 0, 0],
        [0, 0, 0, 0],
    ],
]

class INKB(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4
    CLOCK = 5
    REVCLOCK = 6
    NONE = 7

class Mino:
    id = 0
    angle = 0
    fallTimer = 0
    x = 0
    y = 0
    isHit = False

    def __init__(self):
        self.id = random.randrange(len(MINOS))
        self.angle = 0
        self.fallTimer = 0
        self.x = int((10 - 4) / 2)
        self.y = 0
        self.isHit = False
    
    def getHit(self, tile):
        myTile = self.getTile()
        width = len(tile[0])
        height = len(tile)
        for y in range(4):
            for x in range(4):
                if myTile[y][x] == 1:
                    px = self.x + x
                    py = self.y + y
                    if px < 0 or width <= px or py < 0 or height <= py:
                        return True
                    if tile[py][px] == 1:
                        return True
        return False
    
    def tick(self, tile, deltaTime: float, inkb: INKB):
        if inkb == INKB.DOWN:
            self.fallTimer = 0
            self.y += 1
            if self.getHit(tile):
                self.isHit = True
                self.y -= 1
        elif inkb == INKB.LEFT:
            self.x -= 1
            if self.getHit(tile):
                self.x += 1
        elif inkb == INKB.RIGHT:
            self.x += 1
            if self.getHit(tile):
                self.x -= 1
        elif inkb == INKB.CLOCK:
            self.angle = (self.angle + 1) % 4
            if self.getHit(tile):
                self.angle = (self.angle - 1 + 4) % 4
        elif inkb == INKB.REVCLOCK:
            self.angle = (self.angle - 1 + 4) % 4
            if self.getHit(tile):
                self.angle = (self.angle + 1) % 4

        self.fallTimer += deltaTime
        if self.fallTimer >= FALL_COUNT:
            self.fallTimer -= FALL_COUNT
            self.y += 1
            if self.getHit(tile):
                self.isHit = True
                self.y -= 1
    
    def getTile(self):
        tile = [0] * 4
        for i in range(4):
            row = [0] * 4
            for j in range(4):
                if self.angle == 0:
                    row[j] = MINOS[self.id][i][j]
                elif self.angle == 1:
                    row[j] = MINOS[self.id][j][3 - i]
                elif self.angle == 2:
                    row[j] = MINOS[self.id][3 - i][3 - j]
                elif self.angle == 3:
                    row[j] = MINOS[self.id][3 - j][i]
                else:
                    print("ERROR")
            tile[i] = row
        return tile
    
    def overlap(self, x: int, y: int):
        tile = self.getTile()
        left = self.x
        right = left + len(tile[0])
        up = self.y
        down = up + len(tile)
        if x < left or right <= x:
            return False
        elif y < up or down <= y:
            return False
        elif tile[y - self.y][x - self.x] != 1:
            return False
        else:
            return True

def initTile(width, height):
    tile = []
    for y in range(height):
        row = [0] * width
        tile.append(row)
    return tile

def getINKB():
    if msvcrt.kbhit():
        key0 = str(msvcrt.getch())
        if key0 == "b'\\xe0'":
            key1 = str(msvcrt.getch())
            if key1 == "b'H'":
                return INKB.UP
            elif key1 == "b'P'":
                return INKB.DOWN
            elif key1 == "b'K'":
                return INKB.LEFT
            elif key1 == "b'M'":
                return INKB.RIGHT
            else:
                return INKB.NONE
        elif key0 == "b'z'":
            return INKB.CLOCK
        elif key0 == "b'x'":
            return INKB.REVCLOCK
        else:
            return INKB.NONE
    else:
        return INKB.NONE

def putMino(tile, mino: Mino):
    width = len(tile[0])
    height = len(tile)
    for y in range(height):
        for x in range(width):
            if mino.overlap(x, y):
                tile[y][x] = 1
    
    for y in range(height):
        if sum(tile[y]) == width:
            tile.pop(y)
            tile.insert(0, [0] * width)

def getTextCell(cell):
    if cell == 0:
        return "　"
    elif cell == 1:
        return "■"
    else:
        return "Ｅ"

def getTextTile(tile, mino: Mino):
    text = ""
    width = len(tile[0])
    height = len(tile)
    for y in range(height):
        text += "■"
        for x in range(width):
            if mino.overlap(x, y):
                text += "■"
            else:
                text += getTextCell(tile[y][x])
        text += "■\n"
    text += "■" * (width + 2)
    return text

mino = Mino()
tile = initTile(10, 20)
showText = getTextTile(tile, mino)
print(showText)
while True:
    inkb = getINKB()
    mino.tick(tile, WAIT_SECONDS, inkb)
    if mino.isHit:
        putMino(tile, mino)
        mino = Mino()
    text = getTextTile(tile, mino)
    if text != showText:
        showText = text
        print(showText)
    time.sleep(WAIT_SECONDS)
