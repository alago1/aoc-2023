from collections import defaultdict, deque, Counter
from itertools import combinations, cycle
from functools import lru_cache
from math import gcd
from copy import deepcopy
import re

def parse(filename):
    with open(filename, 'r') as file:
        lines = [line.strip().split('~') for line in file.readlines()]
    
    bricks = [[tuple(map(int, a.split(','))), tuple(map(int, b.split(',')))] for a, b in lines]

    return bricks

def print_bricks(xy_to_brick, bricks):
    width = max(list(map(lambda x: max(x[0][0], x[1][0]), bricks)))
    height = max(list(map(lambda x: max(x[0][1], x[0][1]), bricks)))

    for y in range(height):
        for x in range(width):
            print(dict.get(xy_to_brick, (x, y), ('*', -1))[0], end='')
        print()

def part1(bricks):
    numbered_bricks = sorted(list(enumerate(bricks)), key=lambda x: min(x[1][0][2], x[1][1][2]))

    xy_to_brick = dict()
    dependencies = defaultdict(set) # who i depend on

    for index, (vertex_a, vertex_b) in numbered_bricks:
        x_range = [min(vertex_a[0], vertex_b[0]), max(vertex_a[0], vertex_b[0]) + 1]
        y_range = [min(vertex_a[1], vertex_b[1]), max(vertex_a[1], vertex_b[1]) + 1]

        highest_z = -1
        deps_with_high_z = []

        for x in range(*x_range):
            for y in range(*y_range):
                brick_index, brick_z = dict.get(xy_to_brick, (x, y), (None, -1))

                if highest_z != -1 and brick_z == highest_z:
                    deps_with_high_z.append(brick_index)

                if brick_z > highest_z:
                    highest_z = brick_z
                    deps_with_high_z = [brick_index]
        
        dz = abs(vertex_a[2] - vertex_b[2]) + 1

        for x in range(*x_range):
            for y in range(*y_range):
                xy_to_brick[(x, y)] = (index, highest_z + dz)

        for dep in deps_with_high_z:
            dependencies[index].add(dep)
    
    sole_dependencies = {list(v)[0] for _, v in dependencies.items() if len(v) == 1}
    return len(numbered_bricks) - len(sole_dependencies)


def search_who_falls(start, dependent, dependencies):
    dependencies = deepcopy(dependencies)

    num_fallen = 0

    q = deque([start])

    while q:
        node = q.popleft()
        num_fallen += 1
        for dep in dependent[node]:
            dependencies[dep].discard(node)
            if not dependencies[dep]:
                q.append(dep)

    return num_fallen

def part2(bricks):
    numbered_bricks = sorted(list(enumerate(bricks)), key=lambda x: min(x[1][0][2], x[1][1][2]))

    xy_to_brick = dict()
    dependencies = defaultdict(set) # who i depend on
    dependent = defaultdict(set) # who depends on me

    for index, (vertex_a, vertex_b) in numbered_bricks:
        x_range = [min(vertex_a[0], vertex_b[0]), max(vertex_a[0], vertex_b[0]) + 1]
        y_range = [min(vertex_a[1], vertex_b[1]), max(vertex_a[1], vertex_b[1]) + 1]

        highest_z = -1
        deps_with_high_z = []

        for x in range(*x_range):
            for y in range(*y_range):
                brick_index, brick_z = dict.get(xy_to_brick, (x, y), (None, -1))

                if highest_z != -1 and brick_z == highest_z:
                    deps_with_high_z.append(brick_index)

                if brick_z > highest_z:
                    highest_z = brick_z
                    deps_with_high_z = [brick_index]
        
        dz = abs(vertex_a[2] - vertex_b[2]) + 1

        for x in range(*x_range):
            for y in range(*y_range):
                xy_to_brick[(x, y)] = (index, highest_z + dz)

        for dep in deps_with_high_z:
            dependencies[index].add(dep)
            dependent[dep].add(index)

    
    sole_dependencies = {list(v)[0] for _, v in dependencies.items() if len(v) == 1}
    return sum(search_who_falls(dep, dependent, dependencies) - 1 for dep in sole_dependencies)


if __name__ == '__main__':
    bricks = parse('input.txt')
    print(f"Part 1: {part1(bricks)}")
    print(f"Part 2: {part2(bricks)}")
