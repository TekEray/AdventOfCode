import os

xMax, yMax = 0,0

def readInput():
    script_dir = os.path.dirname(__file__)
    rel_path = "inputs/input.txt"
    abs_file_path = os.path.join(script_dir, rel_path)
    with open(abs_file_path,'r') as f:
        puzzleOutput = [list(line) for line in f.read().splitlines()]
        return puzzleOutput

def getFullNumber(puzzle, row, col):
    xLeft = col
    xRight = col
    while 0 <= xLeft < xMax and puzzle[row][xLeft].isdigit():
        xLeft -= 1
    while 0 <= xRight < xMax and puzzle[row][xRight].isdigit():
        xRight += 1
    return int(''.join(puzzle[row][xLeft+1:xRight])), [(x, row)for x in range(xLeft+1,xRight)]

def find_adjacent_numbers(puzzle, row, col):
    adjacent_numbers = []
    adjacent_index = []
    for y in range(row - 1, row + 2):
        for x in range(col - 1, col + 2):
            if 0 <= row < yMax and 0 <= col < xMax and puzzle[y][x].isdigit() and (x,y) not in adjacent_index:
                num, indexList = getFullNumber(puzzle, y, x)
                adjacent_numbers.append(num)
                adjacent_index.extend(indexList)
    return adjacent_numbers

def sum_part_numbers(puzzle):
    part_numbers_sum = 0
    for y in range(len(puzzle)):
        for x in range(len(puzzle[y])):
            if puzzle[y][x] != '.' and not puzzle[y][x].isdigit():
                adjacent_numbers = find_adjacent_numbers(puzzle, y, x)
                part_numbers_sum += sum(adjacent_numbers)
    return part_numbers_sum

def multply_gear_numbers(puzzle):
    part_numbers_sum = 0
    for y in range(len(puzzle)):
        for x in range(len(puzzle[y])):
            if puzzle[y][x] == '*':
                adjacent_numbers = find_adjacent_numbers(puzzle, y, x)
                if len(adjacent_numbers) == 2:
                    part_numbers_sum += adjacent_numbers[0] * adjacent_numbers[1]           
    return part_numbers_sum

def main():
    global xMax, yMax
    puzzle_list = readInput()
    yMax, xMax = len(puzzle_list), len(puzzle_list[0])
    print('PART A:', sum_part_numbers(puzzle_list))
    print('PART B:', multply_gear_numbers(puzzle_list))

if __name__ == '__main__':
    main()