import random, time, msvcrt
from enum import Enum
WAIT_SECONDS = 1 / 5
FIELD_WIDTH = 20
FIELD_HEIGHT = 20
BOAT_CHARACTER = "》"
BLANK_CHARACTER = "　"
score = 0

class INKB(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4
    SHOT = 5
    NONE = 6

class Ship:

    def __init__(self, character, x, y):
        self.character = character
        self.x = x
        self.y = y
    
    def move(self, x, y):
        self.x += x
        self.y += y

        if self.x < 0:
            self.x = 0
        elif self.x >= FIELD_WIDTH:
            self.x = FIELD_WIDTH - 1
        
        if self.y < 0:
            self.y = 0
        elif self.y >= FIELD_HEIGHT:
            self.y = FIELD_HEIGHT - 1
    
    def setPosition(self, x, y):
        self.x = x
        self.y = y
    
    def overlap(self, x, y):
        return self.x == x and self.y == y



def initTile(width, height):
    tile = []
    for y in range(height):
        row = [False] * width
        tile.append(row)
    return tile

def initBoats(length):
    boats = []
    for i in range(length):
        boats.append(Ship("》", 0, 0))
    return boats

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
            return INKB.SHOT
        else:
            return INKB.NONE
    else:
        return INKB.NONE

def tickMyShip(myShip, boats, tile, inkb):
    if inkb == INKB.UP:
        myShip.move(0, -1)
    elif inkb == INKB.DOWN:
        myShip.move(0, 1)
    elif inkb == INKB.LEFT:
        myShip.move(-1, 0)
    elif inkb == INKB.RIGHT:
        myShip.move(1, 0)
    elif inkb == INKB.SHOT and boats[0].x >= FIELD_WIDTH - 1:
        boats[0].setPosition(myShip.x, myShip.y)
        boats = boats[1:] + boats[:1]
    
    for boat in boats:
        if boat.x < FIELD_WIDTH - 2:
            if tile[boat.y][boat.x] == True:
                #score += 1
                tile[boat.y][boat.x] = False
                boat.move(FIELD_WIDTH, 0)
            elif tile[boat.y][boat.x - 1] == True:
                #score += 1
                tile[boat.y][boat.x - 1] = False
                boat.move(FIELD_WIDTH, 0)
        if boat.x <= FIELD_WIDTH:
            boat.move(1, 0)
    return boats, tile

def tickTile(tile):
    for y in range(FIELD_HEIGHT):
        row = tile[y]
        row = row[1:]
        row.append(random.randint(0, 4) == 0)
        tile[y] = row

def overlapBoats(boats, x, y):
    for boat in boats:
        if boat.x == x and boat.y == y:
            return True
    return False

def getTextTile(myShip, boats, tile):
    text = ""
    for y in range(FIELD_HEIGHT):
        for x in range(FIELD_WIDTH - 1):
            if myShip.overlap(x, y):
                text += myShip.character
            elif overlapBoats(boats, x, y):
                text += BOAT_CHARACTER
            elif tile[y][x] == True:
                text += "■"
            else:
                text += BLANK_CHARACTER
        text += "\n"
    text += "■" * FIELD_WIDTH
    return text

tick = 0
tile = initTile(FIELD_WIDTH, FIELD_HEIGHT)
myShip = Ship("＞", 0, 0)
boats = initBoats(20)
showText = getTextTile(myShip, boats, tile)
print(showText)
while True:
    inkb = getINKB()
    boats, tile = tickMyShip(myShip, boats, tile, inkb)
    if tick >= 1:
        tick -= 1
        tickTile(tile)
    text = getTextTile(myShip, boats, tile)
    if text != showText:
        showText = text
        print(showText)
    tick += WAIT_SECONDS
    time.sleep(WAIT_SECONDS)
