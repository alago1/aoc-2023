from math import ceil, floor

def parse(filename):
    with open(filename) as file:
        times = [int(x) for x in file.readline().strip().split(' ')[1:] if len(x) > 0]
        distances = [int(x) for x in file.readline().strip().split(' ')[1:] if len(x) > 0]

    return times, distances

def quadratic_formula(t_m, d):
    disc = (t_m * t_m - 4 * d)**0.5
    
    x_0 = ceil((t_m - disc) / 2)
    x_1 = floor((t_m + disc) / 2)

    return x_0, x_1

def part1(times, distances):
    p = 1

    for time, dist in zip(times, distances):
        count = len([
            1 for t_p in range(1, time)
            if (time - t_p) * t_p > dist
        ])

        count = max(1, count)
        p *= count

    return p

def part2(times, distances):
    times = int(''.join(map(str, times)))
    distances = int(''.join(map(str, distances)))

    x_0, x_1 = quadratic_formula(times, distances)

    return x_1 - x_0 + 1

if __name__ == '__main__':
    times, distances = parse('input.txt')
    print(f"Part 1: {part1(times, distances)}")
    print(f"Part 2: {part2(times, distances)}")
