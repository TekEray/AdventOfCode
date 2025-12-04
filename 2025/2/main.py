import os

REL_PATH = "inputs/input.txt"

def readInput():
    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, REL_PATH)
    with open(abs_file_path,'r') as f:
        puzzle = [tuple(line.split('-')) for line in f.read().split(',')]
        puzzle = [(int(x),int(y)) for x,y in puzzle]
        return puzzle


def main():
    puzzle = readInput()
    valid = 0
    for (rangeL, rangeR) in puzzle:
        while rangeL <= rangeR:
            tmp = len(str(rangeL)) 
            faktor = 10 ** (tmp // 2)

            x = rangeL // faktor
            y = rangeL % faktor
            if x == y:
                valid += rangeL
            rangeL +=1
    print('PART A:', valid)

    valid=0
    for (rangeL, rangeR) in puzzle:
        ids = set()
        while rangeL <= rangeR:
            rangeL_str = str(rangeL)
            mitte = len(rangeL_str) // 2
            for i in range(mitte+1):
                tmp = rangeL_str[:i]
                tmp_len = i
                tmp_occ = rangeL_str.count(tmp)
                if tmp_len*tmp_occ == len(rangeL_str):
                    ids.add(rangeL)
                    break
            rangeL +=1
        valid += sum(ids)
    print('PART B:', valid)




if __name__ == '__main__':
    main()