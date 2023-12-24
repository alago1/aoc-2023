def clean(lines):
    out = []
    for line in lines:
        if 'map:' in line:
            out.append([])
            continue
        
        out[-1].append([int(x) for x in line.split(' ')])
    
    return out

def parse(filename):
    with open(filename, 'r') as file:
        seeds = [int(x) for x in file.readline().strip().split(': ')[1].split(' ')]
        lines = [x.strip() for x in file.readlines() if len(x.strip()) > 0]

    map_ranges = clean(lines)
    return seeds, map_ranges

def map_seed(seed, single_map):
    for map_range in single_map:
        if map_range[1] <= seed < map_range[1] + map_range[2]:
            offset = seed - map_range[1]
            return map_range[0] + offset
    
    return seed

def find_range_intersection(range1, range2):
    # range is (start, length)
    firstRange, secondRange = sorted([range1, range2], key=lambda x: x[0])

    # no intersection, firstRange doesnt reach secondRange
    if firstRange[0] + firstRange[1] <= secondRange[0]:
        return None
    
    # firstRange ends before secondRange ends
    if firstRange[0] + firstRange[1] <= secondRange[0] + secondRange[1]:
        inter_length = firstRange[0] + firstRange[1] - secondRange[0]
        return secondRange[0], inter_length

    # firstRange encapsulates secondRange
    return secondRange

def split_range_from_intersection(seed_range, intersection_range):
    startRange = seed_range[0], intersection_range[0] - seed_range[0]
    endRange = intersection_range[0] + intersection_range[1], seed_range[0] + seed_range[1] - intersection_range[0] - intersection_range[1]

    return [x for x in [startRange, endRange] if x[1] > 0]

def map_seed_range(seed_range, single_map):
    for map_range in single_map:
        intersect_range = find_range_intersection(seed_range, map_range[1:])

        if intersect_range is None:
            continue

        remaining_ranges = split_range_from_intersection(seed_range, intersect_range)

        offset = intersect_range[0] - map_range[1]
        mapped_intersect_range = map_range[0] + offset, intersect_range[1]

        final_mapping = [mapped_intersect_range]

        for s_range in remaining_ranges:
            final_mapping.extend(map_seed_range(s_range, single_map))

        return final_mapping
    
    return [seed_range]

def part1(seeds, map_ranges):
    for single_map in map_ranges:
        seeds = [map_seed(s, single_map) for s in seeds]

    return min(seeds)

def part2(seeds, map_ranges):
    seed_ranges = list(zip(seeds[::2], seeds[1::2]))

    for single_map in map_ranges:
        new_seed_ranges = []
        for seed_range in seed_ranges:
            new_seed_ranges.extend(map_seed_range(seed_range, single_map))
        seed_ranges = new_seed_ranges

    return min(x[0] for x in seed_ranges)

if __name__ == '__main__':
    seeds, map_ranges = parse('input.txt')
    print(f'Part 1: {part1(seeds, map_ranges)}')
    print(f'Part 2: {part2(seeds, map_ranges)}')
