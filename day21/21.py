from collections import deque
from copy import deepcopy
from functools import lru_cache

def parse(filename):
    with open(filename) as file:
        grid = [list(line.strip()) for line in file.readlines()]
    
    start = [(r, c) for r in range(len(grid)) for c in range(len(grid[0])) if grid[r][c] == 'S'][0]

    grid = tuple(tuple(row) for row in grid)

    return start, grid

def print_grid(grid, visited):
    ng = deepcopy(grid)

    print(visited)

    for r, c in visited:
        # print(r, c)
        if ng[r][c] == '.':
            ng[r][c] = 'O'
    
    with open('grid.txt', 'w') as file:
        for row in ng:
            file.write(''.join(row) + '\n')

def is_valid(pos, grid):
    r, c = pos
    return 0 <= r < len(grid) and 0 <= c < len(grid[0]) and grid[r][c] != '#'

def floodfill(start, grid, max_steps=None):
    counts = [0, 0]
    steps_needed = 0

    q = deque([(start, 0)])
    visited = {start}

    while q:
        pos, steps = q.popleft()

        counts[steps % 2] += 1
        steps_needed = max(steps_needed, steps)
        if max_steps is not None and steps == max_steps:
            continue

        for dr, dc in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            new_pos = (pos[0] + dr, pos[1] + dc)

            if not is_valid(new_pos, grid) or new_pos in visited:
                continue

            q.append((new_pos, steps + 1))
            visited.add(new_pos)
    
    return counts, steps_needed

def get_cached_floodfill(grid):
    @lru_cache(maxsize=None)
    def cached_floodfill(start, max_steps=None):
        return floodfill(start, grid, max_steps)
    
    return cached_floodfill

def get_grid_positions(grid):
    return {
        'top_middle': (0, len(grid[0]) // 2),
        'top_right': (0, len(grid[0]) - 1),
        'middle_right': (len(grid) // 2, len(grid[0]) - 1),
        'bottom_right': (len(grid) - 1, len(grid[0]) - 1),
        'bottom_middle': (len(grid) - 1, len(grid[0]) // 2),
        'bottom_left': (len(grid) - 1, 0),
        'middle_left': (len(grid) // 2, 0),
        'top_left': (0, 0)
    }

dir_offset = {
    'top_middle': (-1, 0),
    'top_right': (-1, 1),
    'middle_right': (0, 1),
    'bottom_right': (1, 1),
    'bottom_middle': (1, 0),
    'bottom_left': (1, -1),
    'middle_left': (0, -1),
    'top_left': (-1, -1)
}

opposite_dir = {
    'top_middle': 'bottom_middle',
    'top_right': 'bottom_left',
    'middle_right': 'middle_left',
    'bottom_right': 'top_left',
    'bottom_middle': 'top_middle',
    'bottom_left': 'top_right',
    'middle_left': 'middle_right',
    'top_left': 'bottom_right'
}

directions = list(dir_offset.keys())

def cost_to_move_grids(start, direction, gridpos):
    if 'middle' not in direction:
        return abs(start[0] - gridpos[direction][0]) + abs(start[1] - gridpos[direction][1])
    
    if 'top' in direction or 'bottom' in direction:
        return abs(start[0] - gridpos[direction][0])
    
    if 'left' in direction or 'right' in direction:
        return abs(start[1] - gridpos[direction][1])

    assert False, f"Invalid direction: {direction}"

def torus_floodfill(start, grid, max_steps):
    start = (0, 0, *start) # (R, C, r, c)
    gridpos = get_grid_positions(grid)

    filled_grid_count, steps_needed_per_grid = floodfill(start, grid)

    counts = [0, 0]
    q = deque([(start, 0)])
    visited_grids = {(0, 0)}

    highest_step = 0
    
    while q:
        (R, C, r, c), steps = q.popleft()

        if max_steps - steps > steps_needed_per_grid:
            counts[0] += filled_grid_count[0]
            counts[1] += filled_grid_count[1]

            for direction, (dR, dC) in dir_offset.items():
                new_grid_offset = (R + dR, C + dC)

                if new_grid_offset in visited_grids:
                    continue

                start_pos = gridpos[opposite_dir[direction]]
                new_pos = (*new_grid_offset, *start_pos)

                q.append((new_pos, steps + cost_to_move_grids((r, c), direction, gridpos)))
                visited_grids.add(new_grid_offset)

            continue

        grid_q = deque([((r, c), steps)])
        visited = {(r, c)}
        
        while grid_q:
            pos, steps = grid_q.popleft()

            counts[steps % 2] += 1
            if max_steps is not None and steps == max_steps:
                continue

            for dr, dc in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                new_pos = (pos[0] + dr, pos[1] + dc)

                if new_pos in visited:
                    continue

                if not is_valid(new_pos, grid):
                    if new_pos[0] < 0 and (R-1, C) not in visited_grids:
                        q.append(((R-1, C, *new_pos), steps + 1))
                        visited_grids.add((R-1, C))
                    if new_pos[0] >= len(grid) and (R+1, C) not in visited_grids:
                        q.append(((R+1, C, *new_pos), steps + 1))
                        visited_grids.add((R+1, C))
                    if new_pos[1] < 0 and (R, C-1) not in visited_grids:
                        q.append(((R, C-1, *new_pos), steps + 1))
                        visited_grids.add((R, C-1))
                    if new_pos[1] >= len(grid[0]) and (R, C+1) not in visited_grids:
                        q.append(((R, C+1, *new_pos), steps + 1))
                        visited_grids.add((R, C+1))
                    continue

                if grid[new_pos[0]][new_pos[1]] == '#':
                    continue

                grid_q.append((new_pos, steps + 1))
                visited.add(new_pos)
    
    return counts

def torus_floodfill2(start, grid, max_steps):
    gridpos = get_grid_positions(grid)
    floodfill = get_cached_floodfill(grid)

    steps_needed_per_grid = {
        'cardinal': floodfill(gridpos['middle_left'])[1],
        'diagonal': floodfill(gridpos['top_left'])[1]
    }

    counts = [0, 0]

    filled_grid_count = floodfill(start)[0]

    num_filled_grids = 0

    grids_right = (max_steps - len(grid) // 2 - 1) // steps_needed_per_grid['cardinal']

    for x in range(-grids_right, grids_right + 1):
        steps_left = max_steps - abs(x) * len(grid[0])
        if x != 0:
            steps_left -= len(grid[0]) // 2 + 1 # x offset
        
        steps_left -= len(grid) // 2 + 1 # y offset

        grids_above = steps_left // steps_needed_per_grid['diagonal']

        steps_left -= grids_above * len(grid)
        num_filled_grids += 2*grids_above + 1

        steps_left_below = steps_left

        # upper
        while steps_left > 0:
            print(steps_left)
            pos = gridpos['bottom_right'] if x < 0 else gridpos['bottom_left']
            c = floodfill(pos, steps_left)[0]
            counts = (counts[0] + c[0], counts[1] + c[1])
            steps_left -= len(grid)
        
        # lower
        while steps_left_below > 0:
            pos = gridpos['top_right'] if x < 0 else gridpos['top_left']
            c = floodfill(pos, steps_left_below)[0]
            counts = (counts[0] + c[0], counts[1] + c[1])
            steps_left_below -= len(grid)
        
    # left
    steps_left = max_steps - len(grid[0]) // 2 - 1 - grids_right * len(grid[0])
    steps_left_right = steps_left
    while steps_left > 0:
        c = floodfill(gridpos['middle_right'], steps_left)[0]
        counts = (counts[0] + c[0], counts[1] + c[1])
        steps_left -= len(grid[0])
    
    # right
    while steps_left_right > 0:
        c = floodfill(gridpos['middle_left'], steps_left_right)[0]
        counts = (counts[0] + c[0], counts[1] + c[1])
        steps_left_right -= len(grid[0])

    counts = (counts[0] + filled_grid_count[0]*num_filled_grids, counts[1] + filled_grid_count[1]*num_filled_grids)

    return counts

def torus_floodfill_slow(start, grid, max_steps=None):
    assert max_steps is not None

    counts = [0, 0]

    q = deque([(start, 0)])
    visited = {start}

    while q:
        pos, steps = q.popleft()

        counts[steps % 2] += 1
        if max_steps is not None and steps == max_steps:
            continue

        for dr, dc in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            new_pos = (pos[0] + dr, pos[1] + dc)

            if grid[new_pos[0] % len(grid)][new_pos[1] % len(grid[0])] == '#':
                continue

            if new_pos in visited:
                continue

            q.append((new_pos, steps + 1))
            visited.add(new_pos)
    
    return counts

def part1(start, grid):
    num_steps = 64
    counts, _ = floodfill(start, grid, num_steps)
    return counts[num_steps % 2]

def part2_fail(start, grid):
    num_steps = 26501365

    counts = torus_floodfill2(start, grid, num_steps)
    print(counts)
    return counts[num_steps % 2]

def part2(start, grid):
    num_steps = 26501365
    q, r = divmod(num_steps, len(grid))

    r1 = torus_floodfill_slow(start, grid, r)[r % 2]
    r2 = torus_floodfill_slow(start, grid, r + len(grid))[(r + len(grid)) % 2]
    r3 = torus_floodfill_slow(start, grid, r + 2*len(grid))[r % 2]

    a = (r3 + r1 -2*r2) / 2
    b = (4*r2 -3 * r1 - r3) / 2
    c = r1

    return int(a*q**2 + b*q + c)

if __name__ == '__main__':
    start, grid = parse('input.txt')
    print(f"Part 1: {part1(start, grid)}")
    print(f"Part 2: {part2(start, grid)}")
