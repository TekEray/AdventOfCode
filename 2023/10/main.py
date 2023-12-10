from shapely.geometry import Point, Polygon

# KOMMT VON : GEHT ZU (X, Y)
mapFromTo = {'|':{'N': (0,1), 'S': (0,-1)}, '-':{'E': (-1,0), 'W': (1,0)}, 'L':{'N': (1,0), 'E': (0,-1)}, 'J':{'N': (-1,0), 'W': (0,-1)}, 
             '7':{'S': (-1,0), 'W': (0,1)}, 'F':{'S': (1,0), 'E': (0,1)}, 'S':{'N': (0,-1), 'E': (1,0), 'S': (0,1), 'W': (-1,0)}}

mapDictChange = {'N' : 'S',
                'S' : 'N',
                'E' : 'W',
                'W' : 'E'}

class Tile:
    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.type = type
    def __repr__(self):
        return repr((self.x, self.y, self.type))

def readInput():
    inputList = []
    y = 0
    while True:
        try:
            line = input()
        except EOFError:
            break
        if not line:
            break
        tileList = []
        for x, tile in enumerate(line):
            tileList.append(Tile(x, y, tile))
        inputList.append(tileList)
        y += 1
    return inputList


def findStart(puzzle):
    maxY = len(puzzle)
    maxX = len(puzzle[0])
    for x in range(maxX):
        for y in range(maxY):
            if puzzle[y][x].type == 'S':
                return puzzle[y][x]


def findLoop(startPoint, puzzle):
    curPoint = startPoint
    maxX = len(puzzle[0])
    maxY = len(puzzle)
    for curFrom, value in mapFromTo[startPoint.type].items():
        way = [startPoint]
        newX = startPoint.x + value[0]
        newY = startPoint.y + value[1]
        curFrom = mapDictChange[curFrom]
        while True:
            if not (newX > -1 and newY > -1 and newX < maxX and newY < maxY):
                break
            curPoint = puzzle[newY][newX]
            if curPoint.type == 'S':
                return way
            if curPoint.type == '.':
                break
            curWays = mapFromTo[curPoint.type]
            if curFrom not in curWays:
                break
            way.append(curPoint)

            tmp = (curWays.keys() - set(curFrom)).pop()
            curX, curY = curWays[curFrom]
            curFrom = mapDictChange[tmp]
            newX = curPoint.x + curX
            newY = curPoint.y + curY


def findDots(puzzle, loopList):
    maxY = len(puzzle)
    maxX = len(puzzle[0])
    dotList = []
    for x in range(maxX):
        for y in range(maxY):
            if puzzle[y][x] not in loopList:
                dotList.append(puzzle[y][x])
    return dotList


def main():
    
    puzzleList = readInput()
    startPoint = findStart(puzzleList)
    loopList = findLoop(startPoint,puzzleList)
    #part A
    print(int(len(loopList)/2))

    dotsList = findDots(puzzleList, loopList)
    polyDotsList = [Point(p.x,p.y) for p in dotsList]
    polyPointList  = [Point(p.x,p.y) for p in loopList]
    poly = Polygon([[p.x, p.y] for p in polyPointList])
    cointainList = [poly.contains(dot) for dot in polyDotsList]
    #part B
    print(sum(cointainList))


if __name__ == '__main__':
    main()