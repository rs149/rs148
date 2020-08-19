import random
class Color:
    RED       = ''
    GREEN     = ''
    YELLOW    = ''
    BLUE      = ''
    END       = ''

def initTile(width, height, ratio):
    tile = []
    for y in range(height):
        row = []
        tile.append(row)
        for x in range(width):
            row.append(random.randint(0, ratio))
    return tile

def contains(tile, x, y):
    width = len(tile[0])
    height = len(tile)
    if x < 0 or width <= x: return False
    if y < 0 or height <= y: return False
    return True

def isMine(cell):
    return cell in {0, -1}

def mines(tile, x, y):
    count = 0
    for dy in range(-1, 2):
        for dx in range(-1, 2):
            if contains(tile, x + dx, y + dy):
                if isMine(tile[y + dy][x + dx]):
                    count += 1
    return count

def openTile(tile, x, y):
    if contains(tile, x, y):
        cell = tile[y][x]
        if cell < 0:
            return 1
        elif isMine(cell):
            tile[y][x] = -1
        else:
            mineCount = mines(tile, x, y)
            tile[y][x] = -mineCount - 2
            if mineCount == 0:
                for dy in range(-1, 2):
                    for dx in range(-1, 2):
                        openTile(tile, x + dx, y + dy)

def allOpenTile(tile):
    width = len(tile[0])
    height = len(tile)
    for y in range(height):
        for x in range(width):
            openTile(tile, x, y)

def printCell(cell):
    if cell >= 0:
        return "■"
    elif cell == -1:
        return Color.RED + "Ⅹ" + Color.END
    elif cell == -2:
        return "．"
    elif cell == -3:
        return Color.BLUE + "１" + Color.END
    elif cell == -4:
        return Color.GREEN + "２" + Color.END
    elif cell == -5:
        return Color.YELLOW + "３" + Color.END
    elif cell == -6:
        return Color.YELLOW + "４" + Color.END
    elif cell == -7:
        return Color.YELLOW + "５" + Color.END
    elif cell == -8:
        return Color.YELLOW + "６" + Color.END
    elif cell == -9:
        return Color.YELLOW + "７" + Color.END
    elif cell == -10:
        return Color.YELLOW + "８" + Color.END
    else:
        return "Ｅ"

def printTile(tile):
    text = ""
    width = len(tile[0])
    height = len(tile)

    text += "　"
    for x in range(width):
        text += '{:>2}'.format(x)
    text += "\n"

    for y in range(height):
        row = tile[y]
        text += '{:>2}'.format(y)
        for x in range(width):
            cell = row[x]
            text += printCell(cell)
        text += '{:>2}'.format(y)
        text += "\n"
    
    text += "　"
    for x in range(width):
        text += '{:>2}'.format(x)
    text += "\n"
    
    print(text)

tile = initTile(20, 20, 7)
while True:
    printTile(tile)
    print("x,yで開く qで終了")
    keys = input('>>').split(",")
    if keys[0] == "q":
        allOpenTile(tile)
        printTile(tile)
        break
    if len(keys) != 2: continue
    x = int(keys[0])
    y = int(keys[1])
    openTile(tile, x, y)

input('enter to exit')
