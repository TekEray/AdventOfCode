import numpy as np

# 1: rigth
# 2: left
# 3: up
# 4: down

# 0: empty space
# 6: |
# 7: -
# 8: /
# 9: \

# (direction, tile) = newDirection
mapping = {(1,0) : [1], (2,0) : [2], (3,0) : [3], (4,0) : [4],
           (1,6) : [3,4], (2,6) : [3,4], (3,6) : [3], (4,6) : [4],
           (1,7) : [1], (2,7) : [2], (3,7) : [1,2], (4,7) : [1,2],
           (1,8) : [3], (2,8) : [4], (3,8) : [1], (4,8) : [2],
           (1,9) : [4], (2,9) : [3], (3,9) : [2], (4,9) : [1]}

#(x,y)
dicToXY = {1: (1,0),
           2: (-1,0),
           3: (0,-1),
           4: (0,1)}


def readInput():
    input_list = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        if not line:
            break
        newLine = line.replace('.', '0').replace('|', '6').replace('-', '7').replace('/', '8').replace('\\', '9')
        input_list.append(list(newLine))
    return input_list


def energizedTiles(npPuzzle, startPoint,direction):
    energized = set()
    visited = set()
    queue = []
    yMax, xMax = npPuzzle.shape
    
    queue.append((startPoint, direction))

    while queue:
        point, direction = queue.pop()
        x,y = point
        if (x,y,direction) in visited:
            continue
        if not (x < xMax and x >= 0 and y < yMax and y >= 0):
            continue 
    
        visited.add((x,y,direction))
        energized.add((x,y))
        newDirection = mapping[(direction, npPuzzle[y][x])]
        for direct in newDirection:
            newX, newY = dicToXY[direct]
            newStartPoint = (point[0] + newX ,point[1] + newY )
            queue.append((newStartPoint, direct))
    return energized

def main():
    puzzleList = readInput()
    npPuzzle = np.array(puzzleList,dtype=int)
    energizedXY = energizedTiles(npPuzzle, (0,0), 1)
    print('A: ', len(energizedXY))

    yMax, xMax = npPuzzle.shape
    energizedXY = []
    energizedXY.extend([energizedTiles(npPuzzle, (x,0), 4) for x in range(xMax)])
    energizedXY.extend([energizedTiles(npPuzzle, (x,(yMax-1)), 3) for x in range(xMax)])
    energizedXY.extend([energizedTiles(npPuzzle, (0,y), 1) for y in range(yMax)])
    energizedXY.extend([energizedTiles(npPuzzle, ((xMax-1),(y)), 2) for y in range(yMax)])

    energizedXY_len = [len(i) for i in energizedXY]
    print('B: ', max(energizedXY_len))
    



if __name__ == '__main__':
    main()