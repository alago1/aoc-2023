from collections import defaultdict, deque
from itertools import combinations
from functools import lru_cache

def parse(filename):
    with open(filename, 'r') as f:
        lines = [x.strip() for x in f.readlines()]
    
    grids = [[]]
    for line in lines:
        if line == '':
            grids.append([])
            continue
        
        grids[-1].append(line)
    
    return grids

def transpose(grid):
    return [*zip(*grid)]

def convert_to_int(grid_line):
    grid_line = ''.join(grid_line).replace('.', '0').replace('#', '1')
    return int(grid_line, 2)

def find_reflection(grid):
    encoded_grid = [convert_to_int(line) for line in grid]

    for i in range(1, len(grid)):
        left = encoded_grid[:i][::-1]
        right = encoded_grid[i:]

        length = min(len(left), len(right))
        left = left[:length]
        right = right[:length]

        if left == right:
            return i

    return -1

def is_power_of_two(n):
    return (n & (n-1) == 0) and n != 0

def find_smudge(grid):
    encoded_grid = [convert_to_int(line) for line in grid]

    for i in range(1, len(grid)):
        left = encoded_grid[:i][::-1]
        right = encoded_grid[i:]

        length = min(len(left), len(right))
        left = left[:length]
        right = right[:length]

        diff = [l ^ r for l, r in zip(left, right) if l != r]
        if len(diff) == 1 and is_power_of_two(diff[0]):
            return i

    return -1


def part1(grids):
    s = 0

    for grid in grids:
        guess1 = find_reflection(grid) # rows
        guess2 = find_reflection(transpose(grid)) # cols

        if guess1 != -1:
            s += guess1 * 100
        
        if guess2 != -1:
            s += guess2
        
    return s

def part2(grids):
    s = 0

    for grid in grids:
        guess1 = find_smudge(grid) # rows
        guess2 = find_smudge(transpose(grid)) # cols

        if guess1 != -1:
            s += guess1 * 100
        
        if guess2 != -1:
            s += guess2
        
    return s

if __name__ == '__main__':
    grids = parse('input.txt')
    print(f"Part 1: {part1(grids)}")
    print(f"Part 2: {part2(grids)}")
