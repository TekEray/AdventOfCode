import numpy as np
import os
from operator import itemgetter
import collections

xMax, yMax = 0,0

def readInput():
    script_dir = os.path.dirname(__file__)
    rel_path = "inputs/input.txt"
    abs_file_path = os.path.join(script_dir, rel_path)
    with open(abs_file_path,'r') as f:
        puzzleInput = f.read()
        puzzleOutput = [(line.split('~')[0], line.split('~')[1] ) for line in puzzleInput.splitlines()]
        puzzleOutput = [(int(first.split(',')[0]), int(first.split(',')[1]), int(first.split(',')[2]), int(sec.split(',')[0]), int(sec.split(',')[1]), int(sec.split(',')[2])) for first, sec in puzzleOutput]
        return puzzleOutput

def fillMatrix(matrix, puzzleList):
    i = 1
    newPuzzleList = []
    tupleToIdx = {}
    for tupleIn in puzzleList:
        xFrom, yFrom, zFrom, xTo, yTo, zTo = tupleIn
        for j in range(zFrom, 0,-1):
            if matrix[yFrom:yTo+1, xFrom:xTo+1, j].any():
                j += 1
                break
        diff = zFrom - j
        matrix[yFrom:yTo+1, xFrom:xTo+1, j:zTo-diff+1] = i
        newPuzzleList.append((xFrom, yFrom, j, xTo, yTo, zTo-diff))
        tupleToIdx[(xFrom, yFrom, j, xTo, yTo, zTo-diff)] = i
        i += 1
    return newPuzzleList, tupleToIdx

def findHolds(matrix, puzzleList, tupleToIdx):
    holds = {}
    holdedBy = {}
    for tupleIn in puzzleList:
        xFrom, yFrom, zFrom, xTo, yTo, zTo = tupleIn
        if matrix[yFrom:yTo+1, xFrom:xTo+1, zTo+1].any():
            tmp = matrix[yFrom:yTo+1, xFrom:xTo+1, zTo+1]
            holdsSet = set(tmp[tmp>0])
            holds[tupleToIdx[tupleIn]] = holdsSet
            for point in holdsSet:                                  #holdedBy erstellen Part B 
                if point in holdedBy:
                    holdedBy[point].add(tupleToIdx[tupleIn])
                else:
                    newSet = set()
                    newSet.add(tupleToIdx[tupleIn])
                    holdedBy[point] = newSet
        else:
            holds[tupleToIdx[tupleIn]] = []
    return holds, holdedBy

def countSafe(holdDict):
    holded = [point for listVal in holdDict.values() for point in listVal]
    count = 0
    safeList = []
    for holdKey, listVal in holdDict.items():
        if all([holded.count(point) > 1 for point in listVal]) or len(listVal) == 0:
            count += 1
            safeList.append(holdKey)
    return safeList


def countFall(holdDict, holdedByDict, safeList):
    safeSet = set(safeList)
    count = 0
    for holdKey, listVal in holdDict.items():
        if holdKey not in safeSet:
            q = collections.deque()
            fallSet = set()
            fallSet.add(holdKey)
            for holdPoint in listVal:
                q.append(holdPoint)
            while q:
                cur = q.popleft()
                holdedBySet = holdedByDict[cur]
                if holdedBySet.issubset(fallSet):   # alle die ihn halten sind auch gefallen 
                    count += 1
                    fallSet.add(cur)
                    for holdPoint in holdDict[cur]:
                        if holdPoint not in q:
                            q.append(holdPoint)
    return count


def main():
    puzzle_list = readInput()
    puzzle_list.sort(key=itemgetter(2))
    xMax = max(max(puzzle_list, key=itemgetter(0))[0] +1, max(puzzle_list, key=itemgetter(3))[3] +1)    #xFrom, xTo
    yMax = max(max(puzzle_list, key=itemgetter(1))[1] +1, max(puzzle_list, key=itemgetter(4))[4] +1)    #yFrom, yTo
    zMax = max(max(puzzle_list, key=itemgetter(2))[2] +1, max(puzzle_list, key=itemgetter(5))[5] +1)    #zFrom, zTo
    puzzle = np.zeros((yMax,xMax,zMax), dtype=int)

    puzzle_list, tupleToIdx = fillMatrix(puzzle, puzzle_list)
    #print(puzzle)
    puzzle_list.sort(key=itemgetter(2))
    holdDict, holdedBy = findHolds(puzzle, puzzle_list, tupleToIdx)
    #print(holdedBy)
    safeList = countSafe(holdDict)
    print('PART A:', len(safeList))

    print('PART B:', countFall(holdDict, holdedBy, safeList))


if __name__ == '__main__':
    main()