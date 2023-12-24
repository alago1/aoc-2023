try:
    from math import lcm
except ImportError:
    from math import gcd
    from functools import reduce

    def lcm(*args):
        lcm_ = reduce(lambda x, y: x * y // gcd(x, y), args)
        return abs(lcm_)

def parse_path(line):
    line = line.strip().replace(' ', '').replace('(', '').replace(')', '')

    source, dests = line.split('=')
    l, r = dests.split(',')

    return (source, (l, r))

def parse(filename):
    with open(filename) as file:
        insts = ['LR'.index(x) for x in file.readline().strip()]
        file.readline()
        paths = dict(parse_path(x) for x in file.readlines())

    return insts, paths

def get_path_length(start, instructions):
    step_count = 0

    while not start.endswith('Z'):
        for inst in instructions:
            if start.endswith('Z'):
                break

            step_count += 1
            start = paths[start][inst]
    
    return step_count

def part1(insts, paths):
    curr = 'AAA'
    step_count = 0

    while curr != 'ZZZ':
        for inst in insts:
            if curr == 'ZZZ':
                break

            curr = paths[curr][inst]
            step_count += 1

    return step_count

def part2(insts, paths):
    ghost_starts = [k for k in paths.keys() if k.endswith('A')]
    ghost_path_lengths = [get_path_length(start, insts) for start in ghost_starts]
    return lcm(*ghost_path_lengths)

if __name__ == '__main__':
    insts, paths = parse('input.txt')
    print(f"Part 1: {part1(insts, paths)}")
    print(f"Part 2: {part2(insts, paths)}")
