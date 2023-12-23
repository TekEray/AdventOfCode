import os
from functools import reduce

bag_config = {'red': 12, 'green': 13, 'blue': 14}

def readInput():
    script_dir = os.path.dirname(__file__)
    rel_path = "inputs/input.txt"
    abs_file_path = os.path.join(script_dir, rel_path)
    with open(abs_file_path,'r') as f:
        tmpList = f.read()
        possible_game_ids = []
        gameMax = {}
        i = 0
        for row in tmpList.splitlines():
            gameIn = True
            game_id, revealed_subsets = row.split(":")
            game_id = int(game_id.replace('Game ', ''))
            gameDict = {'red' : 0, 'green': 0, 'blue' : 0}
            for newSubset in revealed_subsets.split(';'):
                setDict = {'red' : 0, 'green': 0, 'blue' : 0}
                for subset in newSubset.split(','):
                    count, color = subset.strip().split()
                    setDict[color] = setDict[color] + int(count)
                    gameDict[color] = max(gameDict[color], setDict[color])
                    if bag_config[color] < setDict[color]:
                        gameIn = False
            if gameIn:
                possible_game_ids.append(game_id)
            gameMax[i] = list(gameDict.values())
            i += 1
        return possible_game_ids, gameMax

def main():
    partA, partB = readInput()
    print('PART A:', sum(partA))
    print('PART B:', sum([reduce(lambda x, y: x*y, game) for game in partB.values()]))



if __name__ == '__main__':
    main()