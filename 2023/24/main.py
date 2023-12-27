import os
import itertools
from sympy import symbols, Eq, solve

def readInput():
    script_dir = os.path.dirname(__file__)
    rel_path = "inputs/input.txt"
    abs_file_path = os.path.join(script_dir, rel_path)
    with open(abs_file_path,'r') as f:
        puzzleOutput = [line.replace(' @ ', ', ').split(', ') for line in f.read().splitlines()]
        puzzleOutput = [ list(map(int, line)) for line in puzzleOutput]
        return puzzleOutput
    
def line_intersection(point1, point2, xdiff, ydiff):
    line1 = (point1, (point1[0] + xdiff[0], point1[1] + ydiff[0]))
    line2 = (point2, (point2[0] + xdiff[1], point2[1] + ydiff[1]))

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
       return #raise Exception('lines do not intersect')

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div * -1
    y = det(d, ydiff) / div * -1

    if (xdiff[0] < 0 and x > point1[0]) or (xdiff[0] > 0 and x < point1[0]) or (xdiff[1] < 0 and x > point2[0]) or (xdiff[1] > 0 and x < point2[0]):
        return
    return x, y

# https://en.wikipedia.org/wiki/Line%E2%80%93line_intersection -> 'Given two points on each line segment'
def line_intersectionVec(point1, point2, xdiff, ydiff):
    if ((xdiff[0] * ydiff[1]) - (xdiff[1]*ydiff[0])) == 0:
        return
    t = (((point1[0] - point2[0]) * ydiff[1]) - ((point1[1] - point2[1]) * xdiff[1])) / ((xdiff[0] * ydiff[1]) - (xdiff[1]*ydiff[0])) * -1

    r = (((point1[0] - point2[0]) * ydiff[0]) - ((point1[1] - point2[1]) * xdiff[0])) / ((xdiff[0] * ydiff[1]) - (xdiff[1]*ydiff[0])) * -1

    x = point1[0] + t*xdiff[0]
    y = point1[1] + t*ydiff[0]

    if t < 0 or r < 0:
        return
    return x, y

def main():
    puzzle_list = readInput()
    xyMin, xyMax = 200000000000000, 400000000000000
    crossList = []
    # for pair in itertools.combinations(puzzle_list,2):
    #     point1, point2 = pair
    #     cross = line_intersection((point1[0], point1[1]), (point2[0], point2[1]), (point1[3], point2[3]), (point1[4], point2[4]))
    #     if cross is not None and xyMin <= cross[0] <=xyMax and xyMin <= cross[1] <=xyMax:
    #         crossList.append(cross)
    # print(len(crossList))

    for pair in itertools.combinations(puzzle_list,2):
        point1, point2 = pair
        cross = line_intersectionVec((point1[0], point1[1]), (point2[0], point2[1]), (point1[3], point2[3]), (point1[4], point2[4]))
        if cross is not None and xyMin <= cross[0] <=xyMax and xyMin <= cross[1] <=xyMax:
            crossList.append(cross)
    print(len(crossList))

    # Part A mit sympy
    # for pair in itertools.combinations(puzzle_list,2):
    #     point1, point2 = pair
    #     # Symbole für die Unbekannten
    #     a, b, x, y = symbols('a b x y')

    #     # Beispielgleichung: 2x + 3y = 7, 4x - 5y = -3
    #     eq1 = Eq(point1[0] + a*point1[3], point2[0] + b*point2[3])
    #     eq2 = Eq(point1[1] + a*point1[4], point2[1] + b*point2[4])
    #     eq3 = Eq(point1[0] + a*point1[3],x)
    #     eq4 = Eq(point1[1] + a*point1[4],y)

    #     # Lösen des Gleichungssystems
    #     solution = solve((eq1, eq2), (a, b))
    #     if solution:
    #         equation1_result = solve(eq3.subs({a: solution[a]}),x)
    #         print(float(equation1_result[0]))
    #     print(solution)


    point1, point2, point3 = puzzle_list[0], puzzle_list[1], puzzle_list[2]

    # Symbole für die Unbekannten
    s, t, r, x, y, z, a, b, c = symbols('s t r x y z a b c')

    eq1 = Eq(point1[0] + s*point1[3], x + s*a)
    eq2 = Eq(point1[1] + s*point1[4], y + s*b)
    eq3 = Eq(point1[2] + s*point1[5], z + s*c)

    eq4 = Eq(point2[0] + t*point2[3], x + t*a)
    eq5 = Eq(point2[1] + t*point2[4], y + t*b)
    eq6 = Eq(point2[2] + t*point2[5], z + t*c)

    eq7 = Eq(point3[0] + r*point3[3], x + r*a)
    eq8 = Eq(point3[1] + r*point3[4], y + r*b)
    eq9 = Eq(point3[2] + r*point3[5], z + r*c)

    # Lösen des Gleichungssystems
    solution = solve((eq1, eq2, eq3, eq4, eq5, eq6, eq7, eq8, eq9), (x, y, z, a, b, c, s, t, r))
    print(sum(solution[0][:3]))

if __name__ == '__main__':
    main()