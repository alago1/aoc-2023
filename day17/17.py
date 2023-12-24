from collections import defaultdict, Counter, deque
from functools import lru_cache
from itertools import combinations
from copy import deepcopy
from math import gcd
import re
import heapq

def parse(filename):
    with open(filename) as file:
        return [[int(x) for x in line.strip()] for line in file.readlines()]

UPWARDS = (-1, 0)
DOWNWARDS = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)

def is_valid(grid, y, x):
    return 0 <= y < len(grid) and 0 <= x < len(grid[0])

def move(y, x, direction):
    dy, dx = direction
    return y + dy, x + dx

def possible_dirs(grid, y, x, incoming_dir, step_streak, ultra=False):    
    if ultra and step_streak < 4:
        return [incoming_dir] if is_valid(grid, *move(y, x, incoming_dir)) else []

    dirs = [UPWARDS, DOWNWARDS, LEFT, RIGHT]

    # cant go backwards
    opposites = [DOWNWARDS, UPWARDS, RIGHT, LEFT]
    dirs.remove(opposites[dirs.index(incoming_dir)])

    max_step = 10 if ultra else 3
    if step_streak >= max_step:
        dirs.remove(incoming_dir)

    for direction in deepcopy(dirs):
        new_y, new_x = move(y, x, direction)
        if not is_valid(grid, new_y, new_x):
            dirs.remove(deepcopy(direction))

    return dirs

def dir_to_char(direction):
    if direction == UPWARDS:
        return '^'
    elif direction == DOWNWARDS:
        return 'v'
    elif direction == LEFT:
        return '<'
    elif direction == RIGHT:
        return '>'

def build_path(prev, start):
    path = []
    curr = start

    while curr[:-1] in prev:
        dir, y, x, _, loss = curr
        path.append((y, x, dir_to_char(dir), loss))
        curr = prev[curr[:-1]]

    path.reverse()
    return path

def print_grid_path(grid, path):
    ng = [['.' for _ in range(len(grid[0]))] for _ in range(len(grid))]

    for y, x, dir, _ in path:
        ng[y][x] = dir
    
    with open('grid.txt', 'w') as file:
        for row in ng:
            file.write(''.join(row) + '\n')

def part1(grid):
    q = [(-grid[0][0], RIGHT, 0, 0, 0)]
    seen = set()

    while len(q) > 0:
        curr = heapq.heappop(q)
        loss, incoming_dir, y, x, step_streak = curr

        loss += grid[y][x]

        if (y, x) == (len(grid) - 1, len(grid[0]) - 1):
            return loss

        dirs = possible_dirs(grid, y, x, incoming_dir, step_streak)

        for direction in dirs:
            new_y, new_x = move(y, x, direction)
            new_streak = step_streak + 1 if direction == incoming_dir else 1

            if (direction, new_y, new_x, new_streak) not in seen:
                heapq.heappush(q, (loss, direction, new_y, new_x, new_streak))
                seen.add((direction, new_y, new_x, new_streak))

    assert False, "No path found"

def part2(grid):
    q = [(-grid[0][0], RIGHT, 0, 0, 0)]
    seen = set()

    while len(q) > 0:
        curr = heapq.heappop(q)
        loss, incoming_dir, y, x, step_streak = curr

        loss += grid[y][x]

        if (y, x) == (len(grid) - 1, len(grid[0]) - 1):
            return loss

        dirs = possible_dirs(grid, y, x, incoming_dir, step_streak, ultra=True)

        for direction in dirs:
            new_y, new_x = move(y, x, direction)
            new_streak = step_streak + 1 if direction == incoming_dir else 1

            if (direction, new_y, new_x, new_streak) not in seen:
                heapq.heappush(q, (loss, direction, new_y, new_x, new_streak))
                seen.add((direction, new_y, new_x, new_streak))

    assert False, "No path found"

if __name__ == '__main__':
    grid = parse('input.txt')
    print(f"Part 1: {part1(grid)}")
    print(f"Part 2: {part2(grid)}")
