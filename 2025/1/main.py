import os

REL_PATH = "inputs/input.txt"

def readInput():
    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, REL_PATH)
    with open(abs_file_path,'r') as f:
        puzzle = [(line[0:1],int(line[1:])) for line in f.read().splitlines()]
        return puzzle

def main():
    puzzle = readInput()

    dial = 50
    count = 0
    #a
    for (rotation, distance) in puzzle:
        if rotation == 'L':
            dial = (dial - distance) % 100
        else:
            dial = (dial + distance) % 100
        if dial == 0:
            count += 1
    print('A:' , count)


    dial = 50
    count = 0
    #b
    for (rotation, distance) in puzzle:
        if rotation == 'L':
            t_dial = dial - distance
            if t_dial <= 0:
                count = count + abs(int(t_dial / 100)) + 1
                if dial == 0: count -= 1
            dial = t_dial % 100
        else:
            t_dial = dial + distance
            if t_dial >= 100:
                count = count + int(t_dial / 100)
            dial = t_dial % 100
    print('B:' , count)

if __name__ == '__main__':
    main()