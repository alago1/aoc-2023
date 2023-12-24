def parse(filename):
    with open(filename) as file:
        return [s.strip() for s in file.readlines()]

def parse_digs(s):
    digs = [int(x) for x in s if x.isdigit()]
    return int(str(digs[0]) + str(digs[-1]))

def part1(nums_str):
    return sum([parse_digs(s) for s in nums_str])

def foil_num_str(num_str):
    valid_digs = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
    for i, valid_dig in enumerate(valid_digs):
        num_str = num_str.replace(valid_dig, f"{valid_dig}{i+1}{valid_dig}")

    return num_str

def part2(nums_str):
    return sum(parse_digs(foil_num_str(s)) for s in nums_str)

if __name__ == '__main__':
    nums_str = parse('input.txt')
    print(f"Part 1: {part1(nums_str)}")
    print(f"Part 2: {part2(nums_str)}")