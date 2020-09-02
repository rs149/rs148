import random, time, msvcrt, numpy, math
from enum import Enum
WAIT_SECONDS = 1 / 30
TEXT_WIDTH = 45
TEXT_HEIGHT = 25
BOAT_CHARACTER = "》"
BLANK_CHARACTER = "　"

class INKB(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4
    NONE = 5

class Car:
    character = ""
    position = numpy.array([0.0, 0.0])
    degree = 0.0
    velocity = numpy.array([0.0, 0.0])
    angularVelocity = 0.0
    isCrash = False
    isGoal = False

    def __init__(self, character: str, x: float, y: float, degree: float):
        self.character = character
        self.position = numpy.array([x, y])
        self.degree = degree

    def addVelocity(self, x: float, y: float):
        self.velocity += numpy.array([x, y])
    
    def addAngularVelocity(self, deltaAngularVelocity: float):
        self.angularVelocity += deltaAngularVelocity
    
    def tick(self, field, deltaTime: float, inkb: INKB):
        if inkb == INKB.UP:
            self.addVelocity(1.0, 0.0)
        elif inkb == INKB.LEFT:
            self.degree += 10.0
        elif inkb == INKB.RIGHT:
            self.degree -= 10.0
        #self.position += self.velocity * deltaTime
        rad = math.radians(self.degree)
        x = 0 * deltaTime
        y = 25 * deltaTime
        self.position[0] += x * math.cos(rad) - y * math.sin(rad)
        self.position[1] += x * math.sin(rad) + y * math.cos(rad)
        if field.getCrash(self.position[0] * 0.1, self.position[1] * 0.1):
            self.isCrash = True
        if field.getGoal(self.position[0] * 0.1, self.position[1] * 0.1):
            self.isGoal = True

class Field:
    characters = []
    charactersOdd = []
    tile = []

    def __init__(self, characters, charactersOdd, tile):
        self.characters = characters
        self.charactersOdd = charactersOdd
        self.tile = tile
    
    def contains(self, x: int, y: int):
        width = len(self.tile[0])
        height = len(self.tile)
        if x < 0 or width <= x:
            return False
        if y < 0 or height <= y:
            return False
        return True

    def getText(self, x: float, y: float):
        odd = round((x * 10) % 2 + (y * 10) % 2) == 1
        x = round(x)
        y = round(y)
        if self.contains(x, y):
            if odd:
                return self.characters[self.tile[y][x]]
            else:
                return self.charactersOdd[self.tile[y][x]]
        else:
            return self.characters[0]
    
    def getCrash(self, x: float, y: float):
        x = round(x)
        y = round(y)
        if self.contains(x, y):
            return self.tile[y][x] == 1
        else:
            return False
    
    def getGoal(self, x: float, y: float):
        x = round(x)
        y = round(y)
        if self.contains(x, y):
            return self.tile[y][x] == 2
        else:
            return False

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
        else:
            return INKB.NONE
    else:
        return INKB.NONE

def getTextTile(field: Field, myCar: Car):
    text = ""
    for y in range(int(TEXT_HEIGHT * 3 / 4), int(-TEXT_HEIGHT * 1 / 4), -1):
        for x in range(int(-TEXT_WIDTH / 2), int(TEXT_WIDTH / 2)):
            if x == 0 and y == 0:
                if myCar.isCrash:
                    text += "Ⅹ"
                elif myCar.isGoal:
                    text += "▲"
                else:
                    text += "△"
                continue
            rad = math.radians(myCar.degree)
            rx = x * math.cos(rad) - y * math.sin(rad)
            ry = x * math.sin(rad) + y * math.cos(rad)
            tx = myCar.position[0] + rx
            ty = myCar.position[1] + ry
            text += field.getText(tx * 0.1, ty * 0.1)
        text += "\n"
    return text

myCar = Car("@", 20.0, 20.0, 0.0)
field = Field(["　", "■", "　"], ["　", "■", "□"],
[
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
    [1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
    [1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
    [1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
    [1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
    [1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
    [1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
    [1, 1, 0, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
    [1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
    [1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
    [1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
    [1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
])

showText = getTextTile(field, myCar)
print(showText)
while True:
    inkb = getINKB()
    myCar.tick(field, WAIT_SECONDS, inkb)
    if myCar.isCrash:
        print(getTextTile(field, myCar))
        print("CRASH!")
        break
    elif myCar.isGoal:
        print(getTextTile(field, myCar))
        print("GOAL!")
        break
    text = getTextTile(field, myCar)
    if text != showText:
        showText = text
        print(showText)
    time.sleep(WAIT_SECONDS)
