import numpy as np
from collections import defaultdict

def readInput():
    input_list = []
    output_list = []
    while True:
        try:
            line = input()
        except EOFError:
            output_list.append(input_list)
            break
        if not line:
            output_list.append(input_list)
            input_list = []
            continue
        input_list.append(list(line))
    return output_list


def tiltPuzzle(puzzle):
    if puzzle.tobytes() in tiltPuzzle.cache:
        return tiltPuzzle.cache[puzzle.tobytes()]
    intPuzzle = np.copy(puzzle)

    for i in range(len(intPuzzle)-1,0,-1):
        iRow = intPuzzle[i]
        calcPuzzle = intPuzzle[:i] - iRow
        idxRound , = np.where(iRow == 5)
        for roundRock in idxRound:
            iCol = calcPuzzle[:, roundRock]
            idxPosibleRound = 0
            if -3 in iCol:
                idxPosibleRound = len(iCol) - np.argmax(iCol[::-1]==-3)
            while idxPosibleRound < i:
                if intPuzzle[idxPosibleRound][roundRock] == 1:
                    intPuzzle[idxPosibleRound][roundRock] = 5
                    intPuzzle[i][roundRock] = 1
                    break
                idxPosibleRound += 1
    tiltPuzzle.cache[puzzle.tobytes()] = intPuzzle
    return intPuzzle

tiltPuzzle.cache = {}

def calcTotalLoad(puzzle):
    intPuzzle = np.zeros_like(puzzle, dtype=int)
    intPuzzle[puzzle == '.'] = 1
    intPuzzle[puzzle == '#'] = 2
    intPuzzle[puzzle == 'O'] = 5
    
    tiltedPuzzle =  tiltPuzzle(intPuzzle)
    sumTilted = 0
    lenArray = len(tiltedPuzzle)
    for i in range(lenArray):
        sumTilted += np.count_nonzero(tiltedPuzzle[i] == 5) * abs(i-lenArray)
    return sumTilted

def calcTotalLoadCycle(puzzle):
    intPuzzle = np.zeros_like(puzzle, dtype=int)
    intPuzzle[puzzle == '.'] = 1
    intPuzzle[puzzle == '#'] = 2
    intPuzzle[puzzle == 'O'] = 5

    tiltedPuzzle =  intPuzzle
    sumTilted = 0
    lenArray = len(tiltedPuzzle) 
    dictTilts = defaultdict(list)
    maxLoop = 1000000000
    i = 0
    speedUp = True
    checkAfter = 1000
    while i < maxLoop:
        tiltedPuzzle =  tiltPuzzle(tiltedPuzzle)                                            # North
        tiltedPuzzle =  tiltPuzzle(tiltedPuzzle.T).T                                        # West
        tiltedPuzzle =  np.flip(tiltPuzzle(np.flip(tiltedPuzzle, axis=0)), axis=0)          #South
        tiltedPuzzle =  np.flip(tiltPuzzle(np.flip(tiltedPuzzle.T, axis=0)), axis=0).T      #East
        if tiltedPuzzle.tobytes() in dictTilts and i >= checkAfter and speedUp:
            tiltList = dictTilts[tiltedPuzzle.tobytes()]
            diffList = [j-i for i, j in zip(tiltList[:-1], tiltList[1:])]
            tmpDif = max(set(diffList), key=diffList.count)
            multi = (maxLoop - i) // tmpDif
            if (tmpDif * multi) + i == maxLoop-1:
                break
        dictTilts[tiltedPuzzle.tobytes()].append(i)
        i += 1

    for j in range(lenArray):
        sumTilted += np.count_nonzero(tiltedPuzzle[j] == 5) * abs(j-lenArray)
    return sumTilted


def main():
    puzzle_list = readInput()
    for puzzle in puzzle_list:
        puzzle = np.array(puzzle)
        print(calcTotalLoadCycle(puzzle))

if __name__ == '__main__':
    main()