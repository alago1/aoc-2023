from collections import defaultdict, Counter, deque
from functools import lru_cache
from itertools import combinations
from copy import deepcopy
from math import gcd
import re
import heapq


def parse(filename):
    with open(filename) as file:
        grid = [list(line.strip()) for line in file.readlines()]

    return grid

# def print_grid(grid, filename='grid.txt'):
#     with open(filename, 'w') as file:
#         for line in grid:
#             file.write(''.join([f'|{'0' if x < 10 else ''}{x}|' if not type(x) is str else x for x in line]) + '\n')

UPWARDS = (-1, 0)
RIGHTWARDS = (0, 1)
DOWNWARDS = (1, 0)
LEFTWARDS = (0, -1)

def is_valid(r, c, grid):
    return 0 <= r < len(grid) and 0 <= c < len(grid[0]) and grid[r][c] != '#'

def char_to_dir(char):
    dirs = [UPWARDS, RIGHTWARDS, DOWNWARDS, LEFTWARDS]
    chars = '^>v<'

    assert char in chars, f"Invalid char: {char}"
    return dirs[chars.index(char)]

def dir_to_char(dir):
    dirs = [UPWARDS, RIGHTWARDS, DOWNWARDS, LEFTWARDS]
    chars = '^>v<'

    assert dir in dirs, f"Invalid dir: {dir}"
    return chars[dirs.index(dir)]

def part1(grid):
    start = (0, 1)
    end = (len(grid) - 1, len(grid[0]) - 2)

    max_steps = 0
    q = deque([(0, start, {start})]) # steps, position

    while q:
        steps, curr, visited = q.popleft()

        if curr == end:
            max_steps = max(max_steps, steps)
            continue

        for dir in [UPWARDS, RIGHTWARDS, DOWNWARDS, LEFTWARDS]:
            new_r, new_c = curr[0] + dir[0], curr[1] + dir[1]
            if not is_valid(new_r, new_c, grid):
                continue

            if grid[new_r][new_c] in '^>v<' and dir != char_to_dir(grid[new_r][new_c]):
                continue

            if (new_r, new_c) in visited:
                continue

            q.append((steps + 1, (new_r, new_c), visited | {(new_r, new_c)}))

    return max_steps

def part2_slow(grid):
    grid = [[grid[r][c] if grid[r][c] not in '^>v<' else '.' for c in range(len(grid[0]))] for r in range(len(grid))]

    start = (0, 1)
    end = (len(grid) - 1, len(grid[0]) - 2)

    max_steps = 0
    q = deque([(0, start, {start})]) # steps, position, visited

    c = 0

    while q:
        steps, curr, visited = q.popleft()
        c += 1

        if c % 100000 == 0:
            print(c, max_steps)

        if curr == end:
            max_steps = max(max_steps, steps)
            continue

        for dir in [UPWARDS, RIGHTWARDS, DOWNWARDS, LEFTWARDS]:
            new_r, new_c = curr[0] + dir[0], curr[1] + dir[1]
            if not is_valid(new_r, new_c, grid):
                continue

            if grid[new_r][new_c] in '^>v<' and dir != char_to_dir(grid[new_r][new_c]):
                continue

            if (new_r, new_c) in visited:
                continue

            q.append((steps + 1, (new_r, new_c), visited | {(new_r, new_c)}))

    return max_steps

def build_graph(grid):
    assert all(grid[r][c] in '.#' for r in range(len(grid)) for c in range(len(grid[0]))), "Unprocessed grid"

    # mark all intersections
    for r in range(1, len(grid) - 1):
        for c in range(1, len(grid[0]) - 1):
            if grid[r][c] == '.' and sum(grid[r + dir[0]][c + dir[1]] == '.' for dir in [UPWARDS, RIGHTWARDS, DOWNWARDS, LEFTWARDS]) > 2:
                grid[r][c] = 'O'
    
    grid[len(grid) - 1][len(grid[0]) - 2] = 'O' # mark end as intersection

    # build graph
    children = defaultdict(dict)

    visited = set()
    q = deque([(0, (0, 1), (0, 1))]) # steps, position, parent

    while q:
        steps, curr, parent = q.pop()

        if curr in visited:
            continue

        visited.add(curr)

        for dir in [UPWARDS, RIGHTWARDS, DOWNWARDS, LEFTWARDS]:
            new_r, new_c = curr[0] + dir[0], curr[1] + dir[1]
            if not is_valid(new_r, new_c, grid):
                continue

            if (new_r, new_c) == parent:
                continue

            if grid[new_r][new_c] == 'O':
                children[parent][(new_r, new_c)] = steps + 1
                children[(new_r, new_c)][parent] = steps + 1

                if (new_r, new_c) not in visited:
                    q.append((0, (new_r, new_c), (new_r, new_c)))
                    continue

            if (new_r, new_c) not in visited:
                q.append((steps + 1, (new_r, new_c), parent))
    
    return dict(children)

def part2(grid):
    grid = [[grid[r][c] if grid[r][c] not in '^>v<' else '.' for c in range(len(grid[0]))] for r in range(len(grid))]

    start = (0, 1)
    end = (len(grid) - 1, len(grid[0]) - 2)

    graph = build_graph(grid)

    max_steps = 0
    q = deque([(0, start, {start})]) # steps, position, visited

    while q:
        steps, curr, visited = q.popleft()

        if curr == end:
            max_steps = max(max_steps, steps)
            continue

        for next_node, cost in graph[curr].items():
            if next_node in visited:
                continue

            q.append((steps + cost, next_node, visited | {next_node}))

    return max_steps

if __name__ == "__main__":
    grid = parse('input.txt')
    print(f"Part 1: {part1(grid)}")
    print(f"Part 2: {part2(grid)}")
