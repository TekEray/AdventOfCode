import numpy as np
import os

xMax, yMax = 0,0

def readInput():
    script_dir = os.path.dirname(__file__)
    rel_path = "inputs/input.txt"
    abs_file_path = os.path.join(script_dir, rel_path)
    with open(abs_file_path,'r') as f:
        puzzleInput = f.read()
        puzzleOutput = [list(line.replace('S','2').replace('.', '0').replace('#','1')) for line in puzzleInput.splitlines()]
        return puzzleOutput

def findWays(point):
    x, y = point
    return [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)] #[tuple(map(operator.add, point, way)) for way in wayMap]


def isValidPoint(point, rockList):
    x,y = point
    return 0 <= x < xMax and 0 <= y < yMax and point not in rockList


def stepFinder(puzzle, steps):
    dictWays = {}
    ways = set()
    rockList = np.where(puzzle == 1)
    rockList = set(zip(rockList[1],rockList[0]))
    startList = np.where(puzzle == 2)
    startPoint = set(zip(startList[1],startList[0]))
    ways.update(startPoint)
    for i in range(steps):
        if tuple(ways) in dictWays:
            ways = dictWays[tuple(ways)]
            continue
        #ways = {point for mapPoint in map(findWays, ways) for point in mapPoint if isValidPoint(point, rockList)}
        newWays = {point for current_point in ways for point in findWays(current_point) if isValidPoint(point, rockList)}
        dictWays[tuple(ways)] = newWays
        ways = newWays
    return ways

def isValidPointB(point, rockList):
    x,y = point
    return (x%xMax, y%yMax) not in rockList

def stepFinderB(puzzle, steps):
    ways = set()
    rockList = np.where(puzzle == 1)
    rockList = set(zip(rockList[1],rockList[0]))
    startList = np.where(puzzle == 2)
    startPoint = set(zip(startList[1],startList[0]))
    ways.update(startPoint)
    for _ in range(steps):
        ways = {point for current_point in ways for point in findWays(current_point) if isValidPointB(point, rockList)}
    return ways

def g(x):
    return x*131+65

def main():
    global xMax, yMax
    puzzle_list = readInput()
    puzzle = np.array(puzzle_list, dtype=int)
    yMax, xMax = puzzle.shape
    ways = stepFinder(puzzle, 1000)
    print('PART A: ', len(ways))

    x = []
    y = []
    for i in range(3):
        newX = g(i)
        setWays = stepFinderB(puzzle, newX)
        x.append(newX)
        y.append(len(setWays))
    x = np.array(x)
    y = np.array(y)

    pol = np.polyfit(x,y,len(x)-1)
    resultB = np.polyval(pol,26501365)
    print('PART B: ', int(resultB))

if __name__ == '__main__':
    main()