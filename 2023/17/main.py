import numpy as np
import heapq
import math
import os

mapping = {'R' : ('R','U','D'), 'L' : ('L','U','D'), 'U' : ('U','L','R'), 'D' : ('D','L','R'), 'S' : ('R', 'D')}

dirToXY = {'R': (1,0),
           'L': (-1,0),
           'U': (0,-1),
           'D': (0,1)}

def readInput():
    script_dir = os.path.dirname(__file__)
    rel_path = "inputs/input.txt"
    abs_file_path = os.path.join(script_dir, rel_path)
    with open(abs_file_path,'r') as f:
        return [list(row) for row in f.read().splitlines()]

def getNeighborListA(point, direction, streak):
    posDirection = mapping[direction]
    neighborList = []
    for newDirection in posDirection:
        newStreak = 1
        if newDirection == direction:
            newStreak = streak + 1
        if newStreak <= 3:
            addX, addY = dirToXY[newDirection]
            neighbor = (point[0] + addX, point[1] + addY)
            neighborList.append((neighbor, newDirection, newStreak))
    return neighborList


def dijkstra(aGraph, start, target):
    yMax, xMax = aGraph.shape
    distance = {start : 0}
    queue = [(0, start)]    # tuple (cost, (Vertex, direction, streak))

    while len(queue):

        cost, current  = heapq.heappop(queue)
        posCurrent, direction, streak = current

        if posCurrent == target:
            return cost

        neighborList = getNeighborListA(posCurrent, direction, streak)
        for posNeighbor, newDirection, newStreak in neighborList:
            x,y = posNeighbor
            neighbor = (posNeighbor, newDirection, newStreak)
            if 0 <= x < xMax and 0 <= y < yMax:
                newCost = cost + aGraph[y][x]
                if newCost < distance.get(neighbor, math.inf):
                    distance[neighbor] = newCost
                    heapq.heappush(queue, (newCost, neighbor))



def getNeighborListB(point, direction, streak):
    posDirection = mapping[direction]
    neighborList = []
    for newDirection in posDirection:
        newStreak = 4
        addX, addY = dirToXY[newDirection]
        if newDirection == direction:
            if streak < 10:
                newStreak = streak + 1
                neighbor = (point[0] + addX, point[1] + addY)
                neighborList.append((neighbor, newDirection, newStreak))
            continue
        neighbor = (point[0] + 4*addX, point[1] + 4*addY)
        neighborList.append((neighbor, newDirection, newStreak))
    return neighborList


def dijkstraB(aGraph, start, target):
    yMax, xMax = aGraph.shape
    distance = {start : 0}
    queue = [(0, start)]    # tuple (cost, (Vertex, direction, streak))
    while len(queue):
        cost, current  = heapq.heappop(queue)
        posCurrent, direction, streak = current

        if posCurrent == target:
            return cost

        neighborList = getNeighborListB(posCurrent, direction, streak)
        for posNeighbor, newDirection, newStreak in neighborList:
            x,y = posNeighbor
            neighbor = (posNeighbor, newDirection, newStreak)
            if 0 <= x < xMax and 0 <= y < yMax:
                tmpCost = aGraph[y][x]
                if direction != newDirection:
                    match newDirection:
                        case 'R': tmpCost = aGraph[y][x] + aGraph[y][x-1] + aGraph[y][x-2] + aGraph[y][x-3]
                        case 'L': tmpCost = aGraph[y][x] + aGraph[y][x+1] + aGraph[y][x+2] + aGraph[y][x+3]
                        case 'U': tmpCost = aGraph[y][x] + aGraph[y+1][x] + aGraph[y+2][x] + aGraph[y+3][x]
                        case 'D': tmpCost = aGraph[y][x] + aGraph[y-1][x] + aGraph[y-2][x] + aGraph[y-3][x]

                newCost = cost + tmpCost
                if newCost < distance.get(neighbor, math.inf):
                    distance[neighbor] = newCost
                    heapq.heappush(queue, (newCost, neighbor))

def main():
    puzzleList = readInput()
    npPuzzle = np.array(puzzleList,dtype=int)
    yMax, xMax = npPuzzle.shape
    distance = dijkstra(npPuzzle, ((0,0),'S', 0), (xMax-1,yMax-1))
    print('PART A: ', distance)

    distance = dijkstraB(npPuzzle, ((0,0),'S', 0), (xMax-1,yMax-1))
    print('PART B: ', distance)


if __name__ == '__main__':
    main()