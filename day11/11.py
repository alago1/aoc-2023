from itertools import combinations

def parse(filename):
    with open(filename) as file:
        return [x.strip() for x in file.readlines()]

def transposed(grid):
    t_grid = []
    for c in range(len(grid[0])):
        t_grid.append([])
        for r in range(len(grid)):
            t_grid[c].append(grid[r][c])
    
    return t_grid

def find_folds(grid):
    folded_rows = [
        i
        for i, row in enumerate(grid)
        if all(c == '.' for c in row)
    ]

    folded_cols = [
        i
        for i, col in enumerate(transposed(grid))
        if all(c == '.' for c in col)
    ]

    return folded_rows, folded_cols


def unfold_grid(grid):
    folded_rows, folded_cols = [set(x) for x in find_folds(grid)]

    unfolded_grid = []
    for r in range(len(grid)):
        unfolded_grid.append([])
        for c in range(len(grid[r])):
            unfolded_grid[-1].append(grid[r][c])
            if c in folded_cols:
                unfolded_grid[-1].append(grid[r][c])
        
        if r in folded_rows:
            unfolded_grid.append([])
            for c in range(len(grid[r])):
                unfolded_grid[-1].append(grid[r][c])
                if c in folded_cols:
                    unfolded_grid[-1].append(grid[r][c])
    
    return unfolded_grid
    
def write_grid(grid, filename='grid.txt'):
    with open('grid.txt', 'w') as grid_file:
        for r in range(len(grid)):
            grid_file.write(''.join(grid[r]) + '\n')

def part1(grid):
    unfolded_grid = unfold_grid(grid)

    locs = {
        (r, c)
        for r in range(len(unfolded_grid))
        for c in range(len(unfolded_grid[r]))
        if unfolded_grid[r][c] == '#'
    }

    return sum(
        abs(a[0] - b[0]) + abs(a[1] - b[1])
        for a, b in combinations(locs, r=2)
    )

def count_folds_between(folded_rows, folded_cols, a, b):
    row_range = (min(a[0], b[0]), max(a[0], b[0]))
    col_range = (min(a[1], b[1]), max(a[1], b[1]))

    row_crosses = sum([1 for r in folded_rows if row_range[0] < r < row_range[1]])
    col_crosses = sum([1 for c in folded_cols if col_range[0] < c < col_range[1]])

    return row_crosses + col_crosses


def part2(grid):
    folded_rows, folded_cols = find_folds(grid)

    locs = {
        (r, c)
        for r in range(len(grid))
        for c in range(len(grid[r]))
        if grid[r][c] == '#'
    }

    return sum(
        abs(a[0] - b[0]) + abs(a[1] - b[1])
        + int(1e6 - 1) * count_folds_between(folded_rows, folded_cols, a, b)
        for a, b in combinations(locs, r=2)
    )

if __name__ == '__main__':
    x = parse('input.txt')
    print(f"Part 1: {part1(x)}")
    print(f"Part 2: {part2(x)}")