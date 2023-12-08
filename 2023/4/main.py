def main():
    scratchcards = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        scratchcards.append(line)

    scratchcards = [i.split(': ', 1)[1] for i in scratchcards]
    winningNumbers = [i.split(' | ', 1)[0] for i in scratchcards]
    haveNumbers = [i.split(' | ', 1)[1] for i in scratchcards]

    winningNumbers = [i.split() for i in winningNumbers]
    haveNumbers = [i.split() for i in haveNumbers]

    winningNumbers = [list( map(int,i) ) for i in winningNumbers]
    haveNumbers = [list( map(int,i) ) for i in haveNumbers]

    winningNumbers = [set(i) for i in winningNumbers]
    haveNumbers = [set(i) for i in haveNumbers]

    matches = []
    for idx, x in enumerate(winningNumbers):
        matches.append(len(x.intersection(haveNumbers[idx])))

    sumMatches = 0
    for x in matches:
        if x == 1:
            sumMatches = sumMatches + 1
        elif x > 1:
            sumMatches = sumMatches + pow(2, x-1)
    
    print(sumMatches)

    some_dict = {}
    for idx, x in enumerate(matches):
        some_dict[idx] = 1

    for idx, x in enumerate(matches):
        for z in range(1, x+1):
            some_dict[idx+z] = some_dict[idx+z] + some_dict[idx]

    print(sum(some_dict.values()))

if __name__ == '__main__':
    main()