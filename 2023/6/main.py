import math
math.ceil(1.1)

def readInput(inputText):
    inputList = []
    while True:
        try:
            line = input(inputText)
        except EOFError:
            break
        if not line:
            break
        inputList.append(line)
    return [list( map(int,i.split()) ) for i in inputList] 


def rootPoints(time, dist):
    return ((1/2)*(time - (time**2 - 4*dist)**0.5) , (1/2) * (time + (time**2 - 4*dist)**0.5))


def calculateRange(start, end):
    if start % 1 == 0:
        start = start + 1
    else:
        start = math.ceil(start)
    if end % 1 == 0:
        end = end - 1
    else:
        end = math.floor(end)
    return int(end - start + 1)




def main():

    timeList = readInput('time: ')[0]
    distList = readInput('distance: ')[0]

    waysMulti = 1

    for idx, time in enumerate(timeList):
        start, end =  (rootPoints(time, distList[idx]))
        waysMulti = waysMulti * calculateRange(start, end)
    print(waysMulti)





if __name__ == '__main__':
    main()