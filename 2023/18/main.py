import os

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

#Shoelace Formula
def calcAreaPolygon(startPoint, commands):
    currentX, currentY = startPoint
    area = 0
    for dir, count, color in commands:
        addX, addY = dirToXY[dir]
        newX = currentX + count * addX
        newY = currentY + count * addY
        area += currentX * newY - newX * currentY
        currentX = newX
        currentY = newY
    return area/2

def main():
    puzzleList = readInput()

    areaA = calcAreaPolygon((0,0), puzzleList)
    #Picks Theorem
    b = sum([count for dir, count, color in puzzleList])
    print('Part A: ', int(areaA - b/2 + 1 + b))
    
    puzzleList = [ (dicToDir[int(color[-1])], int(color[1:-1],16), color) for dir, count, color in puzzleList]  # PART B
    areaB = calcAreaPolygon((0,0), puzzleList)
    b = sum([count for dir, count, color in puzzleList])
    print('Part B: ', int(areaB - b/2 + 1 + b))

if __name__ == '__main__':
    main()