from collections import defaultdict, deque
from itertools import combinations
from functools import lru_cache
from copy import deepcopy
import re

def parse(filename):
    with open(filename, 'r') as file:
        return file.readline().strip().split(',')

def parse_instruction(instruction):
    eq_index = instruction.find('=')
    dash_index = instruction.find('-')

    index = max(eq_index, dash_index)

    label = instruction[:index]
    op = instruction[index]
    focal_length = None

    if op == '=':
        focal_length = int(instruction[index+1:])

    return label, op, focal_length

def hash(s):
    val = 0
    for c in s:
        val += ord(c)
        val = (val * 17) % 256
    return val

def part1(steps):
    return sum(map(hash, steps))

def part2(steps):
    boxes = [dict() for _ in range(256)]

    for s in steps:
        label, op, focal_length = parse_instruction(s)
        loc = hash(label)

        if op == '-':
            boxes[loc].pop(label, None)
        
        if op == '=':
            boxes[loc][label] = focal_length

    power = 0
    for bn, box in enumerate(boxes):
        for ln, k in enumerate(box.keys()):
            power += (bn + 1) * (ln + 1) * box[k]

    return power

if __name__ == '__main__':
    x = parse('input.txt')
    print(f"Part 1: {part1(x)}")
    print(f"Part 2: {part2(x)}")
