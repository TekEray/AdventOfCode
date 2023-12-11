import numpy as np
from itertools import combinations

class Galaxy:
    def __init__(self, x, y, number):
        self.x = x
        self.y = y
        self.number = number
    def __repr__(self):
        return repr((self.x, self.y, self.number))

def readInput():
    inputList = []
    counter  = 1
    while True:
        try:
            line = input()
        except EOFError:
            break
        if not line:
            break
        imageList = []
        for obj in line:
            num1 = 0
            if obj == '#':
                num1 = counter
                counter += 1
            imageList.append(num1)
        inputList.append(imageList)
    return inputList

def distImage(imageArray):
    xList = []
    yList = []

    # Zeilen distanz
    for i in range(imageArray.shape[0]):
        if np.all(imageArray[i] == 0):
            xList.append(i)          

    # Spalten distanz
    for j in range(imageArray.shape[1]):  
        if np.all(imageArray[:, j] == 0):
            yList.append(j)

    return xList, yList

def findGalaxy(imageArray):
    galaxyList = []
    for iy, ix in np.ndindex(imageArray.shape):
        if imageArray[iy, ix] > 0:
            galaxyList.append(Galaxy(ix,iy,imageArray[iy, ix]))
    return galaxyList

def calcDistance(tupleGalaxy,xList, yList, expansion):
    sumAll = 0
    for val1, val2 in tupleGalaxy:
        wallY = [i for i in yList if (i > val1.x and i < val2.x) or (i > val2.x and i < val1.x)]
        wallX = [i for i in xList if (i > val1.y and i < val2.y) or (i > val2.y and i < val1.y)]
        sumAll = sumAll + abs(val2.x - val1.x) + abs(val2.y - val1.y) + ((len(wallY) + len(wallX)) * (expansion - 1))
    return sumAll


def main():
    imageList = readInput()
    imageArray = np.array(imageList)
    galaxyList = findGalaxy(imageArray)
    tupleGalaxy = list(combinations(galaxyList, 2))
    xList, yList = distImage(imageArray)

    #Part A
    print('PART A: ', calcDistance(tupleGalaxy, xList, yList, 2))
    #Part B
    print('PART B: ',calcDistance(tupleGalaxy, xList, yList, 1000000))

if __name__ == '__main__':
    main()