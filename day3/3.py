def parse(filename):
    with open(filename) as file:
        return [list(s.strip()) for s in file.readlines()]

def is_valid(grid, x, y):
    return 0 <= y < len(grid) and 0 <= x < len(grid[y])

def neighbors_symbol(grid, x, y):
    return any(
        not grid[y+dy][x+dx].isdigit()
        for dy in range(-1, 2)
        for dx in range(-1, 2)
        if is_valid(grid, x+dx, y+dy) and (dy, dx) != (0, 0) and grid[y+dy][x+dx] != '.'
    )

def try_parse(grid, x, y):
    if not is_valid(grid, x, y) or not grid[y][x].isdigit():
        return -1

    while x >= 0 and grid[y][x].isdigit():
        x -= 1
    x += 1
    
    num_buf = []
    while x < len(grid[y]) and grid[y][x].isdigit():
        num_buf.append(grid[y][x])
        x += 1
    
    return int(''.join(num_buf))

def count_number_neighbors(grid, x, y):
    vals = []

    if is_valid(grid, x, y-1):
        if not grid[y-1][x].isdigit():
            vals.append(try_parse(grid, x-1, y-1))
            vals.append(try_parse(grid, x+1, y-1))
        else:
            vals.append(try_parse(grid, x, y-1))
    
    vals.append(try_parse(grid, x-1, y))    
    vals.append(try_parse(grid, x+1, y))

    if is_valid(grid, x, y+1):
        if not grid[y+1][x].isdigit():
            vals.append(try_parse(grid, x-1, y+1))
            vals.append(try_parse(grid, x+1, y+1))
        else:
            vals.append(try_parse(grid, x, y+1))

    return [v for v in vals if v != -1]

def part1(grid):
    added_nums = []

    for y, row in enumerate(grid):
        num_buf = []
        is_near_symbol = False

        for x, char in enumerate(row):
            if not char.isdigit():
                if is_near_symbol:
                    added_nums.append(int(''.join(num_buf)))
                
                num_buf = []
                is_near_symbol = False
                continue

            num_buf.append(char)
            is_near_symbol |= neighbors_symbol(grid, x, y)

        if is_near_symbol:
            added_nums.append(int(''.join(num_buf)))
                
        num_buf = []
        is_near_symbol = False

    if is_near_symbol:
        added_nums.append(int(''.join(num_buf)))
            
        num_buf = []
        is_near_symbol = False
    
    return sum(added_nums)

def part2(grid):
    added_nums = []

    for y, row in enumerate(grid):
        for x, char in enumerate(row):
            if char == '*':
                vals = count_number_neighbors(grid, x, y)
                if len(vals) == 2:
                    added_nums.append(vals[0] * vals[1])

    return sum(added_nums)

if __name__ == '__main__':
    grid = parse('input.txt')
    print(f"Part 1: {part1(grid)}")
    print(f"Part 2: {part2(grid)}")
