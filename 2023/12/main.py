def readInput():
    input_list = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        if not line:
            break
        input_list.append(tuple(line.split()))
    return [(s, list(map(int, group.split(',')))) for s, group in input_list]

def count_arrangements(row, groups, memo):
    key = (row, tuple(groups))
    if key in memo:
        return memo[key]

    if not groups:
        result = int(not any(s == '#' for s in row))
    elif not row:
        result = 0
    elif row[0] == '.':
        result = count_arrangements(row[1:], groups, memo)
    elif row[0] == '?':
        result = (
            count_arrangements(row.replace('?', '#', 1), groups, memo) +
            count_arrangements(row.replace('?', '.', 1), groups, memo)
        )
    else:
        len_hash = groups[0]
        if (
            not any(s == '.' for s in row[:len_hash]) and
            ((len(row) > len_hash and row[len_hash] != '#') or len(row) == len_hash)
        ):
            result = count_arrangements(row[len_hash + 1:], groups[1:], memo)
        else:
            result = 0

    memo[key] = result
    return result

def main():
    puzzle_list = readInput()
    print(sum(count_arrangements(i_str, group, {}) for i_str, group in puzzle_list))

    tmp_count = 0
    for i_str, group in puzzle_list:
        unfolded_i_str = '?'.join([i_str] * 5)
        unfolded_group = group * 5
        tmp_count += count_arrangements(unfolded_i_str, unfolded_group, {})
    print(tmp_count)

if __name__ == '__main__':
    main()