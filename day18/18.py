from collections import defaultdict, deque, Counter
from itertools import combinations
from functools import lru_cache
import re
from math import gcd
from copy import deepcopy

def parse(filename):
    with open(filename, 'r') as file:
        lines = [line.strip().split(' ') for line in file.readlines()]
    
    return [(x[0], int(x[1]), x[2][2:-1]) for x in lines]

def get_dims(instructions):
    max_x, max_y = 0, 0
    min_x, min_y = 0, 0

    x, y = 0, 0

    for inst in instructions:
        if inst[0] in 'LR':
            x += inst[1] * (-1 if inst[0] == 'L' else 1)
        
        if inst[0] in 'UD':
            y += inst[1] * (-1 if inst[0] == 'D' else 1)
        
        max_x = max(max_x, x)
        max_y = max(max_y, y)
        min_x = min(min_x, x)
        min_y = min(min_y, y)

    dimensions = (max_y - min_y + 1, max_x - min_x + 1, )
    origin = (-min_y, -min_x)

    return dimensions, origin

def is_valid(grid, y, x):
    return 0 <= y < len(grid) and 0 <= x < len(grid[0])

def print_grid(grid):
    with open('grid.txt', 'w') as file:
        for row in grid:
            file.write(''.join(row) + '\n')

def part1(instructions):
    dimensions, origin = get_dims(instructions)
    dimensions = (dimensions[0] + 2, dimensions[1] + 2)
    origin = (origin[0] + 1, origin[1] + 1)

    seg_length = 0

    grid = [['.' for _ in range(dimensions[1])] for _ in range(dimensions[0])]
    y, x = origin
    for inst in instructions:
        ny, nx = y, x
        if inst[0] in 'LR':
            nx = x + inst[1] * (-1 if inst[0] == 'L' else 1)
        
        if inst[0] in 'UD':
            ny = y + inst[1] * (-1 if inst[0] == 'D' else 1)
        
        for i in range(min(x, nx), max(x, nx) + 1):
            for j in range(min(y, ny), max(y, ny) + 1):
                grid[j][i] = '#'
                seg_length += 1
        
        x, y = nx, ny
    
    found_outside = False
    for i in range(dimensions[0]):
        for j in range(dimensions[1]):
            if grid[i][j] == '.':
                y, x = i, j
                found_outside = True
                break
        
        if found_outside:
            break

    if not found_outside:
        return len(grid) * len(grid[0])

    outside_length = 1
    grid[y][x] = 'O'
    q = deque([(y, x)])

    while q:
        y, x = q.popleft()

        for dy in range(-1, 2):
            for dx in range(-1, 2):
                if dy == 0 and dx == 0:
                    continue
                
                ny, nx = y + dy, x + dx

                if is_valid(grid, ny, nx) and grid[ny][nx] not in '#O':
                    q.append((ny, nx))
                    grid[ny][nx] = 'O'
                    outside_length += 1
    
    print_grid(grid)

    return len(grid) * len(grid[0]) - outside_length


def shoelace(points):
    area = 0

    for (x1, y1), (x2, y2) in zip(points, points[1:] + [points[0]]):
        area += x1 * y2 - x2 * y1
    
    return abs(area) // 2

def part2(instructions):
    instructions = [('RDLU'[int(inst[2][-1])], int(inst[2][:-1], 16)) for inst in instructions]

    seg_length = 0
    points = [(0, 0)]
    for inst in instructions:
        seg_length += inst[1]
        if inst[0] == 'R':
            points.append((points[-1][0], points[-1][1] + inst[1]))
        elif inst[0] == 'D':
            points.append((points[-1][0] + inst[1], points[-1][1]))
        elif inst[0] == 'L':
            points.append((points[-1][0], points[-1][1] - inst[1]))
        elif inst[0] == 'U':
            points.append((points[-1][0] - inst[1], points[-1][1]))
    
    area = shoelace(points)
    return area + seg_length // 2 + 1

if __name__ == '__main__':
    instructions = parse('input.txt')
    print(f"Part 1: {part1(instructions)}")
    print(f"Part 2: {part2(instructions)}")
