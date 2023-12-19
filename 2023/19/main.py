import os
import copy

def readInput():
    script_dir = os.path.dirname(__file__)
    rel_path = "inputs/input.txt"
    abs_file_path = os.path.join(script_dir, rel_path)
    with open(abs_file_path,'r') as f:
        tmpList = f.read().split("\n\n")
        rulesDict = {record.split('{')[0]: record.split('{')[1][:-1] for record in tmpList[0].splitlines()
}
        puzzleList = [{key: int(value) for key, value in (item.split("=") for item in record[1:-1].split(","))} for record in tmpList[1].splitlines()]
        return rulesDict, puzzleList


def checkRule(puzzlePart, ruleStr):
    ruleList = ruleStr.split(',')
    for rule in ruleList:
        if ':' in rule:
            category = rule[0]
            condition = rule[1]
            number, newRule = rule[2:].split(':')
            if condition == '>' and puzzlePart[category] > int(number):
                return newRule
            if condition == '<' and puzzlePart[category] < int(number):
                return newRule
        else:
            return rule
        
def recCheck(puzzlePart, rule, rulesDict):
    if rule == 'A':
        return True
    if rule == 'R':
        return False
    newRule = checkRule(puzzlePart, rulesDict[rule])
    return recCheck(puzzlePart, newRule, rulesDict)


def checkRuleRange(rangePart, ruleStr):
    currentDict = copy.deepcopy(rangePart)
    ruleList = ruleStr.split(',')
    #rules = {} # wird ueberschrieben wenn A oefter vorkommt als exit
    rules = []
    for rule in ruleList:
        newRangePart = copy.deepcopy(currentDict)
        if ':' in rule:
            category = rule[0]
            condition = rule[1]
            number, newRule = rule[2:].split(':')
            if condition == '>':
                newRangePart[category][0] = int(number) + 1
                currentDict[category][1] = int(number)
            if condition == '<':
                newRangePart[category][1] = int(number) -1
                currentDict[category][0] = int(number)
            if newRangePart[category][0] > newRangePart[category][1]:
                break
            rules.append((newRule, newRangePart))
        else:
            rules.append((rule,newRangePart))
    return rules

def recCheckRange(ruleRangePart, rulesDict):
    rangeList = []
    for rule, range in ruleRangePart:
        if rule == 'A':
            rangeList.append(range)
            continue
        if rule == 'R':
            continue
        newRuleRangePart = checkRuleRange(range, rulesDict[rule])
        rangeList.extend(recCheckRange(newRuleRangePart, rulesDict))
    return rangeList

def main():
    rulesDict, puzzleList = readInput()
    sumValues = 0
    for puzzle in puzzleList:
        if  recCheck(puzzle, 'in', rulesDict):
            sumValues += sum(puzzle.values())
    print('Part A: ', sumValues)

    rangePart = {'x': [1,4000], 'm': [1,4000], 'a': [1,4000], 's': [1,4000]}
    rangeDict = recCheckRange(checkRuleRange(rangePart, rulesDict['in']), rulesDict)

    sumTest = 0
    for range in rangeDict:
        x = range['x'][1] - range['x'][0] + 1
        m = range['m'][1] - range['m'][0] + 1
        a = range['a'][1] - range['a'][0] + 1
        s = range['s'][1] - range['s'][0] + 1
        sumTest += x*m*a*s
    
    print('Part B: ', sumTest)


if __name__ == '__main__':
    main()