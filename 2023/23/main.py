import numpy as np
import os
import sys
from collections import deque

class recursionlimit:
    def __init__(self, limit):
        self.limit = limit

    def __enter__(self):
        self.old_limit = sys.getrecursionlimit()
        sys.setrecursionlimit(self.limit)

    def __exit__(self, type, value, tb):
        sys.setrecursionlimit(self.old_limit)

arrayMap = {
    '.' : 0,
    '#' : 1,
    '>' : 5,
    '<' : 6,
    '^' : 7,
    'v' : 8
}

dirMap = {
    5 : (1,0),
    6 : (-1,0),
    7 : (0,-1),
    8: (0,1)
}

xMax, yMax = 0,0

def readInput():
    script_dir = os.path.dirname(__file__)
    rel_path = "inputs/input.txt"
    abs_file_path = os.path.join(script_dir, rel_path)
    with open(abs_file_path,'r') as f:
        puzzleInput = f.read()
        puzzleOutput = [list(line) for line in puzzleInput.splitlines()]
        puzzleOutput = [list(map(arrayMap.get, line)) for line in puzzleOutput]
        return puzzleOutput

def isNotValidPoint(point, puzzle, visited):
    curX, curY = point
    return point in visited or curX < 0 or curX >= xMax or curY < 0 or curY >= yMax or puzzle[curY][curX] == 1

def recWaySearch(puzzle, curPoint, target, visited, outputList):
    curX, curY = curPoint
    if isNotValidPoint(curPoint, puzzle, visited):
        return
    visitedSet = set(visited)
    visitedSet.add(curPoint)
    if curPoint == target:
        outputList.append(len(visitedSet)-1)
        return
    curValue = puzzle[curY][curX]
    if curValue == 0:
        recWaySearch(puzzle, (curX + 1, curY), target, visitedSet, outputList)
        recWaySearch(puzzle, (curX - 1, curY), target, visitedSet, outputList)
        recWaySearch(puzzle, (curX, curY + 1), target, visitedSet, outputList)
        recWaySearch(puzzle, (curX, curY - 1), target, visitedSet, outputList)
    else:
        addX, addY = dirMap[curValue]
        recWaySearch(puzzle, (curX + addX, curY + addY), target, visitedSet, outputList)



def isCrossing(x, y, puzzle):
    return puzzle[y][x] != 1 and sum(1 for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)] if 0 <= x + dx < xMax and 0 <= y + dy < yMax and puzzle[y + dy][x + dx] != 1) > 2

def findEdges(point, puzzle, crossNodes):
    queue = deque([(point, set(), 0)])
    outputList = []

    while queue:
        curPoint, visited, weight = queue.popleft()
        curX, curY = curPoint
        
        if curPoint in crossNodes and curPoint != point:
            outputList.append((curPoint, weight))
            continue
        
        visitedSet = set(visited)
        visitedSet.add(curPoint)
        
        neighbors = [(curX + 1, curY), (curX - 1, curY), (curX, curY + 1), (curX, curY - 1)]
        for neighbor in neighbors:
            if not isNotValidPoint(neighbor, puzzle, visitedSet):
                queue.append((neighbor, visitedSet, weight+1))
    return outputList

def iterWaySearchB(start, target, weightDict):
    queue = deque([(start, set(), 0)])
    outputList = []
    
    while queue:
        curPoint, visited, dist = queue.popleft()
        
        visitedSet = set(visited)
        visitedSet.add(curPoint)
        
        if curPoint == target:
            outputList.append(dist)
        
        neighborsWeightList = weightDict[curPoint]
        for neighbor, weight in neighborsWeightList:
            if neighbor not in visitedSet:
                queue.append((neighbor, visitedSet, dist+weight))
    return outputList

def main():
    global xMax,yMax
    puzzle_list = readInput()
    puzzleArray = np.array(puzzle_list, dtype=int)
    yMax, xMax = puzzleArray.shape
    startX = np.where(puzzleArray[0,:] == 0)[0][0]
    startPoint = (startX, 0)
    targetX = np.where(puzzleArray[yMax-1,:] == 0)[0][0]
    targetPoint = (targetX, yMax-1)

    outputList = []
    with recursionlimit(3000):
        recWaySearch(puzzleArray, startPoint, targetPoint, set(), outputList)
    print('PART A:', max(outputList))

    crossNodes = {startPoint, targetPoint}
    for y in range(yMax):
        for x in range(xMax):
            if isCrossing(x,y, puzzleArray):
                crossNodes.add((x,y))
    weightDict = {}
    for cross in crossNodes:
        weightDict[cross] = findEdges(cross, puzzleArray, crossNodes)
    outputList = iterWaySearchB(startPoint, targetPoint, weightDict)
    print('PART B:', max(outputList))

if __name__ == '__main__':
    main()