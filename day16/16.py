from collections import defaultdict, Counter, deque
from functools import lru_cache
from itertools import combinations, permutations, product
from copy import deepcopy
from math import gcd
import re

def parse(filename):
    with open(filename) as file:
        return [list(line.strip()) for line in file.readlines()]

UPWARD = (-1, 0)
DOWNWARD = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)

def is_valid(position, grid):
    return 0 <= position[0] < len(grid) and 0 <= position[1] < len(grid[0])

def interact(direction, pos, grid):
    if not is_valid(pos, grid):
        return None

    char = grid[pos[0]][pos[1]]

    if char == '.':
        return [direction]
    
    if char == '|':
        if direction == UPWARD or direction == DOWNWARD:
            return [direction]
        else:
            return [UPWARD, DOWNWARD]
    
    if char == '-':
        if direction == LEFT or direction == RIGHT:
            return [direction]
        else:
            return [LEFT, RIGHT]
    
    if char == '/':
        if direction == UPWARD:
            return [RIGHT]
        if direction == DOWNWARD:
            return [LEFT]
        if direction == LEFT:
            return [DOWNWARD]
        if direction == RIGHT:
            return [UPWARD]
    
    if char == '\\':
        if direction == UPWARD:
            return [LEFT]
        if direction == DOWNWARD:
            return [RIGHT]
        if direction == LEFT:
            return [UPWARD]
        if direction == RIGHT:
            return [DOWNWARD]
    
    raise Exception(f"Unknown character {char}")

def move(direction, pos):
    return (pos[0] + direction[0], pos[1] + direction[1])

def part1(grid, start=(0, 0, RIGHT)):
    seen = set()
    seen_with_dir = set()
    q = [start]

    while q:
        *pos, direction = q.pop(0)
        seen.add(tuple(pos))
        seen_with_dir.add((*pos, direction))

        next_dir = interact(direction, pos, grid)
        if next_dir is None:
            continue

        for d in next_dir:
            next_pos = move(d, pos)
            if not is_valid(next_pos, grid):
                continue

            if (*next_pos, d) in seen_with_dir:
                continue

            q.append((*next_pos, d))
    
    return len(seen)


def part2(grid):
    starts = []
    starts.extend([(0, i, DOWNWARD) for i in range(len(grid[0]))])
    starts.extend([(i, 0, RIGHT) for i in range(len(grid))])
    starts.extend([(len(grid) - 1, i, UPWARD) for i in range(len(grid[0]))])
    starts.extend([(i, len(grid[0]) - 1, LEFT) for i in range(len(grid))])

    return max(part1(grid, start) for start in starts)

if __name__ == '__main__':
    grid = parse('input.txt')
    print(f"Part 1: {part1(grid)}")
    print(f"Part 2: {part2(grid)}")
