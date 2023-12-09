from functools import reduce
import math
 
def lcm(numbers):
    return reduce(lambda x, y: x * y // math.gcd(x, y), numbers, 1)

rlDict = {'R':1, 'L':0}

def readInput():
    inputList = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        if not line:
            break
        inputList.append(line)
    return [tuple( i.split(' = ') ) for i in inputList] 

def findZZZPartA(puzzleDict, leftRight):
    startPoint = 'AAA'
    pointTemp = puzzleDict[startPoint]
    foundZZZ = False
    step = 0
    moduloLR = len(leftRight)
    while not foundZZZ:
        way = leftRight[step % moduloLR]
        startPoint = pointTemp[way]
        pointTemp = puzzleDict[startPoint]
        step = step + 1
        if startPoint == 'ZZZ':
            foundZZZ = True
        
    return step

def lcm(numbers):
    return reduce(lambda x, y: x * y // math.gcd(x, y), numbers, 1)

def findZZZPartB(puzzleDict, leftRight):
    startPoint = [key for key in puzzleDict.keys() if key.endswith('A')]
    endSteps = []
    pointTemp = set(puzzleDict[point] for point in startPoint)
    foundZZZ = False
    step = 0
    moduloLR = len(leftRight)
    while not foundZZZ:
        way = leftRight[step % moduloLR]
        startPoint = [point[way] for point in pointTemp]
        step = step + 1
        if any(point.endswith('Z') for point in startPoint):
            for point in startPoint:
                if point.endswith('Z'):
                    startPoint.remove(point)
                    endSteps.append(step)
        pointTemp = set(puzzleDict[point] for point in startPoint)
        if all(point.endswith('Z') for point in startPoint):
            foundZZZ = True
        
    return endSteps


def main():

    leftRight = list(readInput()[0][0])
    leftRight = [rlDict[way] for way in leftRight]
    puzzle = readInput()
    puzzleDict = {}

    puzzleDict = {key : tuple( value.replace('(', '').replace(')', '').split(', ') ) for key, value in puzzle}

    print(findZZZPartA(puzzleDict, leftRight))
    print(lcm(findZZZPartB(puzzleDict, leftRight)))



if __name__ == '__main__':
    main()
