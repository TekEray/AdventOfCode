import numpy as np

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
    return [np.array(i.split(), dtype=int) for i in inputList]

def extrapolateToZero(line):

    extrapolateList = [line]
    while np.any(extrapolateList[-1]):
        extrapolateList.append(np.diff(extrapolateList[-1]))
    return extrapolateList

def predictTopLast(line):
    line = extrapolateToZero(line)
    calc = 0
    for arr in reversed(line[:-1]):
        topPredict = arr[-1] + calc
        arr = np.append(arr, topPredict)
        calc = arr[-1]
    return topPredict

def predictTopFirst(line):
    line = extrapolateToZero(line)
    calc = 0
    for arr in reversed(line[:-1]):
        topPredict = arr[0] - calc
        arr = np.append(topPredict, arr)
        calc = arr[0]
    return topPredict

def main():

    dataset = readInput()
    predicts = [predictTopLast(arr) for arr in dataset]
    print('A: ', sum(predicts))
    predicts = [predictTopFirst(arr) for arr in dataset]
    print('B: ', sum(predicts))




if __name__ == '__main__':
    main()
