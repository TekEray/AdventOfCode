import numpy as np
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

def findHorizontalMirror(puzzle,task):
    matches = []
    puzzle[puzzle == '.'] = 1
    puzzle[puzzle == '#'] = 2
    intPuzzle = puzzle.astype('i')
    for i in range(1,len(intPuzzle)):
        firstPart = intPuzzle[:i]
        secondPart = intPuzzle[i:]

        firstPart = firstPart[::-1]

        lenFirst = len(firstPart)
        lenSecond = len(secondPart)
        if lenFirst > lenSecond:
            firstPart = firstPart[:lenSecond]
        elif lenFirst < lenSecond:
            secondPart = secondPart[:lenFirst]
        
        resultArr = np.absolute(np.subtract(firstPart, secondPart))
        if np.sum(resultArr.sum(axis=1)) == 1 and task == 'B':
            matches.append(i)
        elif np.sum(resultArr.sum(axis=1)) == 0 and task == 'A':
            matches.append(i)
    if not matches:
        return 0
    halfLen = len(intPuzzle)/2
    return min(matches, key=lambda x:abs(x-halfLen))


def findVerticalMirror(puzzle,task):
    return findHorizontalMirror(puzzle.T,task)


def main():
    puzzle_list = readInput()
    sumPuzzleA = 0
    sumPuzzleB = 0
    for puzzle in puzzle_list:
        puzzle = np.array(puzzle)
        sumPuzzleA += findHorizontalMirror(puzzle,'A') * 100  + findVerticalMirror(puzzle,'A')
        sumPuzzleB += findHorizontalMirror(puzzle,'B') * 100  + findVerticalMirror(puzzle,'B')
    print('PART A: ', sumPuzzleA) 
    print('PART B: ', sumPuzzleB) 

if __name__ == '__main__':
    main()