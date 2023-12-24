from collections import defaultdict, Counter, deque
from itertools import combinations
from functools import lru_cache
from math import gcd, prod
from copy import deepcopy
import re

Range = tuple[int, int]
XMASRange = tuple[Range, Range, Range, Range]

def parse_workflow(workflow):
    bracket_index = workflow.index('{')
    name = workflow[:bracket_index]

    rules = workflow[bracket_index+1:-1].split(',')
    rules = tuple(x if len(x:=rule.split(':')) > 1 else ('True', x[0]) for rule in rules)

    return name, rules

def parse(filename):
    with open(filename) as file:
        lines = [line.strip() for line in file.readlines()]
    
    workflows = {name: rules for name, rules in map(parse_workflow, lines[:lines.index('')])}
    parts = [eval(x.replace("=", "':").replace("{", "{'").replace(",", ",'")) for x in lines[lines.index('')+1:]]

    return workflows, parts

def part1(workflows, parts):
    sum_parts = 0

    for part in parts:
        next_step = 'in'
        x, m, a, s = part.values()

        while next_step not in 'AR':
            for condition, direction in workflows[next_step]:
                if eval(condition):
                    next_step = direction
                    break
        
        if next_step == 'A':
            sum_parts += sum(part.values())
    
    return sum_parts

def split_branch_ranges(char, op, num, xmas_ranges: XMASRange):
    thresh = num + 1 if op == '>' else num

    passing_ranges = list(xmas_ranges)
    failing_ranges = list(xmas_ranges)
    
    char_index = 'xmas'.index(char)
    passing_ranges[char_index] = (thresh, passing_ranges[char_index][1])
    failing_ranges[char_index] = (failing_ranges[char_index][0], thresh)

    if op == '<':
        passing_ranges[char_index], failing_ranges[char_index] = failing_ranges[char_index], passing_ranges[char_index]

    return tuple(passing_ranges), tuple(failing_ranges)

def count_range_combs(x_range, m_range, a_range, s_range):
    return (x_range[1] - x_range[0]) * (m_range[1] - m_range[0]) * (a_range[1] - a_range[0]) * (s_range[1] - s_range[0])

def count_workflow_combs(workflows, wkflw, xmas_ranges: XMASRange):
    if wkflw == 'R':
        return 0
    
    if wkflw == 'A':
        return count_range_combs(*xmas_ranges)

    wkflw_combs = 0
    for condition, direction in workflows[wkflw]:
        if condition == 'True':
            wkflw_combs += count_workflow_combs(workflows, direction, xmas_ranges)
            continue

        char, op, *num = condition
        num = int(''.join(num))

        passing_ranges, failing_ranges = split_branch_ranges(char, op, num, xmas_ranges)
        wkflw_combs += count_workflow_combs(workflows, direction, passing_ranges)

        xmas_ranges = failing_ranges
    
    return wkflw_combs

def part2(workflows, _):
    x_range = (1, 4001) # [1, 4001)
    m_range = (1, 4001)
    a_range = (1, 4001)
    s_range = (1, 4001)

    return count_workflow_combs(workflows, 'in', (x_range, m_range, a_range, s_range))


if __name__ == '__main__':
    workflows, parts = parse('input.txt')
    print(f"Part 1: {part1(workflows, parts)}")
    print(f"Part 2: {part2(workflows, parts)}")
