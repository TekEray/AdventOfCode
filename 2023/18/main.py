import os
import numpy as np
from shapely.geometry import Point, Polygon

# dir: (x,y)
dirToXY = {'R': (1,0),
           'L': (-1,0),
           'U': (0,-1),
           'D': (0,1)}

dicToDir = {0: 'R',
           1: 'D',
           2: 'L',
           3: 'U'}

def readInput():
    script_dir = os.path.dirname(__file__)
    rel_path = "inputs/input.txt"
    abs_file_path = os.path.join(script_dir, rel_path)
    with open(abs_file_path,'r') as f:
        inputList = [tuple(row.split()) for row in f.read().splitlines()]
        return [(dir, int(count), color.replace('(','').replace(')','')) for dir, count, color in inputList]

#Erster Versuch
# def createArray(npArray, startPoint, commands):
#     currentX, currentY = startPoint
#     polyPointList = [Point(currentX,currentY)]
#     npArray[currentY][currentX] = 1

#     for dir, count, color in commands:
#         addX, addY = dirToXY[dir]
#         for i in range(count):
#             currentX = currentX + addX
#             currentY = currentY + addY
#             if startPoint == (currentX,currentY): 
#                 break
#             polyPointList.append(Point(currentX,currentY))
#             npArray[currentY][currentX] = 1
#     return polyPointList

# def calculateMaxArraySizeAndStart(commands):
#     max_x, min_x, max_y, min_y = 0, 0, 0, 0
#     current_x, current_y = 0, 0

#     for dir, count, color in commands:
#         add_x, add_y = dirToXY[dir]
#         current_x += count * add_x
#         current_y += count * add_y

#         max_x = max(max_x, current_x)
#         min_x = min(min_x, current_x)
#         max_y = max(max_y, current_y)
#         min_y = min(min_y, current_y)

#     array_size = (max(max_x - min_x + 1, 0), max(max_y - min_y + 1, 0))
#     start_point = (abs(min_x), abs(min_y))

#     return array_size, start_point

def createArray(startPoint, commands):
    currentX, currentY = startPoint
    polyPointList = [Point(currentX,currentY)]

    for dir, count, color in commands:
        addX, addY = dirToXY[dir]
        currentX = currentX + count * addX
        currentY = currentY + count * addY
        if (currentX, currentY) == startPoint:
            break
        polyPointList.append(Point(currentX,currentY))
    return polyPointList

def main():
    puzzleList = readInput()
    #arraySize, startPoint = calculateMaxArraySizeAndStart(puzzleList)
    #xMax, yMax = arraySize
    #npArray = np.zeros((yMax, xMax),dtype=bool)
    #polyPointList = createArray(npArray, startPoint, puzzleList)

    #indicesDots = np.where(npArray == 0)
    #dotsTuples = list(zip(indicesDots[0], indicesDots[1]))
    #polyDotsList  = [Point(x,y) for y,x in dotsTuples]
    #poly = Polygon([[p.x, p.y] for p in polyPointList])

    polyDotsListA = createArray((0,0), puzzleList)
    polyA = Polygon([[p.x, p.y] for p in polyDotsListA])
    tmpArea = polyA.area
    b = sum([count for dir, count, color in puzzleList])
    print('Part A: ', int(tmpArea - b/2 + 1 + b))
    
    puzzleList = [ (dicToDir[int(color[-1])], int(color[1:-1],16), color) for dir, count, color in puzzleList]  # PART B
    polyDotsListB = createArray((0,0), puzzleList)
    polyB = Polygon([[p.x, p.y] for p in polyDotsListB])
    tmpArea = polyB.area
    b = sum([count for dir, count, color in puzzleList])
    print('Part B: ', int(tmpArea - b/2 + 1 + b))



if __name__ == '__main__':
    main()