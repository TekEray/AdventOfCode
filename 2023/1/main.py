import os
from operator import itemgetter

digitDic = {
    'one' : '1',
    'two' : '2',
    'three' : '3',
    'four' : '4',
    'five' : '5',
    'six' : '6',
    'seven' : '7',
    'eight' : '8',
    'nine' : '9'
}

def readInput():
    script_dir = os.path.dirname(__file__)
    rel_path = "inputs/input.txt"
    abs_file_path = os.path.join(script_dir, rel_path)
    with open(abs_file_path,'r') as f:
        puzzleOutput = [line for line in f.read().splitlines()]
        return puzzleOutput

def replaceStr(str):
    newStr = str
    for spellDigit, digit in digitDic.items():
        newStr = newStr.replace(spellDigit, digit)
    return newStr

def main():
    puzzle_list = readInput()
    concatDigits = []
    for line in puzzle_list:
        tupleList = [(i, c) for i, c in enumerate(line) if c.isdigit()]
        concatDigits.append(int(min(tupleList, key=itemgetter(0))[1] + max(tupleList, key=itemgetter(0))[1]))
    print('PART A:', sum(concatDigits))
    
    newPuzzle_list = []
    for line in puzzle_list:
        newline = line
        i = 3
        while i <= len(newline):
            curPart = newline[:i]
            replace = replaceStr(curPart)
            tmpLine = replace + newline[i-1:]
            i += 1
            if replace != curPart:
                i = 3
                newline = tmpLine
        newPuzzle_list.append(newline)
    concatDigits = []
    for line in newPuzzle_list:
        tupleList = [(i, c) for i, c in enumerate(line) if c.isdigit()]
        concatDigits.append(int(min(tupleList, key=itemgetter(0))[1] + max(tupleList, key=itemgetter(0))[1]))
    print('PART B:', sum(concatDigits))
    

if __name__ == '__main__':
    main()