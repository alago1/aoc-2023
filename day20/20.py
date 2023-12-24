from collections import defaultdict, Counter, deque
from itertools import combinations, takewhile
from functools import lru_cache, reduce
from math import gcd, prod
from copy import deepcopy
import re

try:
    from math import lcm
except ImportError:
    def lcm(*args):
        return reduce(lambda x, y: abs(x * y) // gcd(x, y), args)

# types: % flipflop, & conjunction, broadcast

def parse(filename):
    with open(filename) as file:
        lines = [line.strip() for line in file]
    
    types = {}
    dests = {}

    for line in lines:
        module, destinations = line.split(' -> ')

        module_type = module[0]
        module_name = module[1:]

        if module == 'broadcaster':
            module_name = module
            module_type = module
        
        types[module_name] = module_type
        dests[module_name] = tuple(destinations.split(', '))
    
    return types, dests

def part1(types: dict[str, str], dests: dict[str, tuple[str]]) -> int:
    flipflops = {name: 0 for name, mod_type in types.items() if mod_type == '%'}
    conjunction_inputs = {name: [] for name, mod_type in types.items() if mod_type == '&'}
    conjunction_memory = {}

    for name, destinations in dests.items():
        for dest in destinations:
            if dest in types and types[dest] == '&':
                conjunction_inputs[dest].append(name)
                conjunction_memory[(dest, name)] = 0

    pulse_count = [0, 0]
    for _ in range(1000):
        pulse_q = deque([('broadcaster', 0, 'button')]) # module, pulse, source

        while pulse_q:
            module, pulse, source = pulse_q.popleft()

            pulse_count[pulse] += 1

            if module not in types:
                continue

            if types[module] == 'broadcaster':
                for dest in dests[module]:
                    pulse_q.append((dest, pulse, module))
                continue
            
            if types[module] == '%' and pulse == 0:
                flipflops[module] = 1 - flipflops[module]
                for dest in dests[module]:
                    pulse_q.append((dest, flipflops[module], module))
                continue

            if types[module] == '&':
                conjunction_memory[(module, source)] = pulse
                out_pulse = not all(conjunction_memory[(module, name)] for name in conjunction_inputs[module])
                for dest in dests[module]:
                    pulse_q.append((dest, out_pulse, module))
                continue

    return prod(pulse_count)

def part2(types, dests):
    flipflops = {name: 0 for name, mod_type in types.items() if mod_type == '%'}
    conjunction_inputs = {name: [] for name, mod_type in types.items() if mod_type == '&'}
    conjunction_memory = {}

    for name, destinations in dests.items():
        for dest in destinations:
            if dest in types and types[dest] == '&':
                conjunction_inputs[dest].append(name)
                conjunction_memory[(dest, name)] = 0

    rx_conj = list([name for name, mod_type in types.items() if mod_type == '&' and 'rx' in dests[name]])[0]
    key_modules = [mod_name for mod_name, _ in dests.items() if rx_conj in dests[mod_name]]

    cycles = {name: set() for name in key_modules}

    press_count = 0
    while True:
        pulse_count = [0, 0]
        press_count += 1

        pulse_q = deque([('broadcaster', 0, 'button')]) # module, pulse, source

        while pulse_q:
            module, pulse, source = pulse_q.popleft()

            pulse_count[pulse] += 1

            if module == 'rx':
                if pulse == 0:
                    return press_count
                continue

            if types[module] == 'broadcaster':
                for dest in dests[module]:
                    pulse_q.append((dest, pulse, module))
                continue
            
            if types[module] == '%' and pulse == 0:
                flipflops[module] = 1 - flipflops[module]
                for dest in dests[module]:
                    pulse_q.append((dest, flipflops[module], module))
                continue

            if types[module] == '&':
                conjunction_memory[(module, source)] = pulse
                out_pulse = not all(conjunction_memory[(module, name)] for name in conjunction_inputs[module])
                for dest in dests[module]:
                    pulse_q.append((dest, out_pulse, module))

                if module in key_modules and out_pulse == 1:
                    cycles[module].add((sum(pulse_count), press_count))
                continue
                
        if press_count > int(1e4):
            break

    cycle_sizes = set()

    for k in cycles:
        pulses = set(v[0] for v in cycles[k])

        for pulse in pulses:
            subset = sorted([v[1] for v in cycles[k] if v[0] == pulse])
            diff = [v1 - v0 for v0, v1 in zip(subset, subset[1:])]
            assert len(set(diff)) == 1, diff

            cycle_sizes.add(diff[0])
    
    return lcm(*cycle_sizes)

if __name__ == '__main__':
    types, dests = parse('input.txt')
    print(f"Part 1: {part1(types, dests)}")
    print(f"Part 2: {part2(types, dests)}")
