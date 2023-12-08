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
    return [tuple( map(int,i.split()) ) for i in inputList] 

def preprocess_mapping(mapping):
    result = {}
    for dest_start, source_start, length in mapping:
        for i in range(length):
            result[source_start + i] = dest_start + i
    return result

def main():
    seedList = []

    allLists = []

    seedList = readInput('seeds: ')[0]
    allLists.append(readInput('seedToSoil: '))
    allLists.append(readInput('soilToFert: '))
    allLists.append(readInput('fertToWat: '))
    allLists.append(readInput('watToLight: '))
    allLists.append(readInput('lightToTemp: '))
    allLists.append(readInput('tempToHum: '))
    allLists.append(readInput('humToLoc: '))

    minLoc = 2**63 - 1
    for seed in seedList:
        temp = seed
        for listMap in allLists:
            for mapping in listMap:
                if temp >=  mapping[1] and temp < mapping[1] + mapping[2]:
                    temp = mapping[0] + (temp - mapping[1])
                    break     
        if minLoc > temp:
            minLoc = temp
    print('min: ', minLoc)

    #testMap = []
    #for listMap in allLists:
    #    testMap.append(preprocess_mapping (listMap))
    #print('MAPPING DONE')

    #result_dict = {}

    #for current_dict in testMap:
    #    result_dict.update({key: current_dict[val] if val in current_dict else val for key, val in result_dict.items()})
    #    result_dict.update({key: val for key, val in current_dict.items() if val not in result_dict})
    #print(result_dict)

    # minLocRange = 2**63 - 1
    # for idx in range(0,len(seedList),2):
    #     print ('TUPLE', idx)
    #     startSeed = seedList[idx]
    #     lengthSeed = seedList[idx+1]
    #     for seed in range(startSeed, startSeed + lengthSeed):
    #         temp = seed
    #         for dictMap in testMap:
    #             if temp in dictMap:
    #                 temp = dictMap[temp]   
    #         if minLocRange > temp:
    #             minLocRange = temp
    # print('minWithRange: ', minLocRange)


    minLocRange = 2**63 - 1
    for idx in range(0,len(seedList),2):
        print ('TUPLE', idx)
        startSeed = seedList[idx]
        lengthSeed = seedList[idx+1]
        for seed in range(startSeed, startSeed + lengthSeed):
            temp = seed
            for listMap in allLists:
                for destPoint, startPoint, lenPoint in listMap:
                    if temp >=  startPoint and temp < startPoint + lenPoint:
                        temp = destPoint + (temp - startPoint)
                        break     
            if minLocRange > temp:
                minLocRange = temp
    print('minWithRange: ', minLocRange)



if __name__ == '__main__':
    main()