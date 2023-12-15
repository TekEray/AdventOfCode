import os
from collections import defaultdict

def readInput():
    script_dir = os.path.dirname(__file__)
    rel_path = "inputs/input.txt"
    abs_file_path = os.path.join(script_dir, rel_path)
    f = open(abs_file_path, "r")
    line = f.read()
    return line.split(',')


def hashValue(val):
    curHash = 0
    for c in val:
        asciiCode = ord(c)
        curHash += asciiCode
        curHash *= 17
        curHash = curHash % 256
    return curHash

def labelToBox(tupleList):
    dictBoxes = defaultdict(list)
    for box, label, focal in tupleList:
        tmpBox = dictBoxes[box]
        if tmpBox:
            existList = [item for item in tmpBox if item[0] == label]
            if existList:
                if not focal:
                    dictBoxes[box] = list(filter(lambda x: x[0] != label, tmpBox))
                    continue
                dictBoxes[box] = [(label, focal) if oldLabel == label else (oldLabel, oldFocal) for oldLabel, oldFocal in tmpBox]
                continue
        if focal:
            dictBoxes[box].append((label, focal))
    return dictBoxes




def main():
    puzzleList = readInput()
    hashListA = list(map(hashValue, puzzleList))
    print(sum(hashListA))

    tupleList = [tuple(val.replace('-', '=').split('=')) for val in puzzleList]
    hashListB = [(hashValue(label), label, num) for label, num in tupleList]
    print(hashListB)
    dictLabelBox = labelToBox(hashListB)

    sumB = 0
    for box, valueList in dictLabelBox.items():
        for idx, val in enumerate(valueList):
            sumB += (box+1) * (idx+1) * int(val[1])
    print(sumB)

if __name__ == '__main__':
    main()