from collections import defaultdict, deque, Counter
from itertools import combinations
from functools import lru_cache
from copy import deepcopy
import re

def parse(filename):
    with open(filename, 'r') as file:
        return [list(x.strip()) for x in file.readlines()]

def transpose(grid):
    return [*zip(*grid)]

def compute_total_load(grid):
    s = 0
    for c in range(len(grid[0])):
        for r in range(len(grid)):
            if grid[r][c] == 'O':
                s += len(grid) - r
    
    return s

def part1(grid):
    s = 0

    for c in range(len(grid[0])):
        pivot = -1
        pivot_count = 0
        for r in range(len(grid)):
            if grid[r][c] == '#':
                pivot_count = 0
                pivot = r
            
            if grid[r][c] == 'O':
                s += len(grid) - pivot_count - pivot - 1
                pivot_count += 1

    return s

def part1_slow(grid):
    g = deepcopy(grid)
    tilt_north(g)
    return compute_total_load(g)

def clockwise_rotation(grid):
    return [list(reversed(x)) for x in transpose(grid)]

def tilt_north(grid):
    for c in range(len(grid[0])):
        rock_count = 0
        for r in range(len(grid) - 1, -1 , -1):
            if grid[r][c] == 'O':
                rock_count += 1
                grid[r][c] = '.'
            
            if grid[r][c] == '#':
                for k in range(1, rock_count + 1):
                    grid[r + k][c] = 'O'

                rock_count = 0
        
        if rock_count > 0:
            for k in range(rock_count):
                grid[k][c] = 'O'

def tuple_grid(grid):
    return tuple(tuple(x) for x in grid)

def single_cycle(grid):
    for _ in range(4):
        tilt_north(grid)
        grid = clockwise_rotation(grid)

    return grid

ONE_BILLION = int(1e9)

def part2(grid, num_steps = ONE_BILLION):
    grid_cycle_count = dict()
    step = 0

    while step < num_steps:
        if tuple_grid(grid) not in grid_cycle_count:
            grid_cycle_count[tuple_grid(grid)] = step

        grid = single_cycle(grid)
        step += 1

        if tuple_grid(grid) in grid_cycle_count:
            cycle_step_count = step - grid_cycle_count[tuple_grid(grid)]
            remaining_steps = num_steps - step
            step += (remaining_steps // cycle_step_count) * cycle_step_count

    return compute_total_load(grid)


if __name__ == '__main__':
    grid = parse('input.txt')

    print(f"Part 1: {part1(grid)}")
    print(f"Part 2: {part2(grid)}")
