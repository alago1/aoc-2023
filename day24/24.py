from collections import defaultdict, Counter, deque
from itertools import combinations, cycle
from functools import lru_cache
from math import gcd
from copy import deepcopy
import re

from sympy.solvers import solve
from sympy import Symbol, symbols

def parse_triple(triple_str):
    return tuple(map(int, triple_str.split(',')))

def parse(filename):
    with open(filename) as file:
        lines = [tuple(map(parse_triple, line.strip().split('@'))) for line in file.readlines()]
    
    positions = tuple(map(lambda x: x[0], lines))
    velocities = tuple(map(lambda x: x[1], lines))

    return positions, velocities

def is_parallel(v1, v2):
    if any(vd1 == 0 and vd2 != 0 or vd1 != 0 and vd2 == 0 for vd1, vd2 in zip(v1, v2)):
        return False
    
    ratios = [vd1 / vd2 for vd1, vd2 in zip(v1, v2) if vd1 != 0 and vd2 != 0]
    return len(set(ratios)) in [0, 1]

def find_intersection2d(p1, p2, v1, v2):
    p1 = p1[:2]
    p2 = p2[:2]
    v1 = v1[:2]
    v2 = v2[:2]

    if is_parallel(v1, v2):
        return None
    
    p_diff = [pd1 - pd2 for pd1, pd2 in zip(p1, p2)]

    # | -v1[0]  v2[0] |
    # | -v1[1]  v2[1] |

    denominator = -v1[0]*v2[1] + v1[1]*v2[0]

    if denominator == 0:
        return None
    
    t1 = (p_diff[0]*v2[1] - p_diff[1]*v2[0]) / denominator
    t2 = (-v1[0]*p_diff[1] + v1[1]*p_diff[0]) / denominator

    if t1 < 0 or t2 < 0:
        return None

    x = t1 * v1[0] + p1[0]
    y = t1 * v1[1] + p1[1]

    return x, y

def part1(positions, velocities):
    valid_range = (200000000000000, 400000000000000)
    # valid_range = (7, 27)

    count = 0
    
    for (p1, v1), (p2, v2) in combinations(zip(positions, velocities), 2):
        xy = find_intersection2d(p1, p2, v1, v2)

        if xy is None:
            continue

        x, y = xy
        if valid_range[0] <= x <= valid_range[1] and valid_range[0] <= y <= valid_range[1]:
            count += 1
    
    return count

def part2(positions, velocities):
    num_eqs = 3  # we know the solution exists so we can just solve with the minimum amount of eqs

    x, y, z, vx, vy, vz = symbols('x, y, z, vx, vy, vz')
    ts = [Symbol(f't{i}') for i in range(len(positions))][:num_eqs]

    xs = [x + vx*t - p[0] - v[0]*t for t, p, v in zip(ts, positions, velocities)]
    ys = [y + vy*t - p[1] - v[1]*t for t, p, v in zip(ts, positions, velocities)]
    zs = [z + vz*t - p[2] - v[2]*t for t, p, v in zip(ts, positions, velocities)]

    # solve for x, y, z, vx, vy, vz
    sols = solve([*xs, *ys, *zs], [x, y, z, vx, vy, vz, *ts])

    return sum(sols[0][:3])


if __name__ == "__main__":
    positions, velocities = parse('input.txt')
    print(f"Part 1: {part1(positions, velocities)}")
    print(f"Part 2: {part2(positions, velocities)}")
