def char_to_cardinal(char, cardinal_dir):
    if char == 'L':
        return 'N' if cardinal_dir == 'W' else 'E'
    
    if char == 'F':
        return 'E' if cardinal_dir == 'N' else 'S'
    
    if char == 'J':
        return 'N' if cardinal_dir == 'E' else 'W'
    
    if char == '7':
        return 'S' if cardinal_dir == 'E' else 'W'
    
    if char == '|':
        return 'S' if cardinal_dir == 'S' else 'N'
    
    if char == '-':
        return 'E' if cardinal_dir == 'E' else 'W'
    
    assert False, f"Invalid char: {char}"

def cardinal_to_vec(cardinal_dir):
    if cardinal_dir == 'N':
        return (-1, 0)
    
    if cardinal_dir == 'S':
        return (1, 0)
    
    if cardinal_dir == 'E':
        return (0, 1)
    
    if cardinal_dir == 'W':
        return (0, -1)
    
    assert False, f"Invalid cardinal direction: {cardinal_dir}"

def vec_to_cardinal(delta):
    if delta == (-1, 0):
        return 'N'
    
    if delta == (1, 0):
        return 'S'
    
    if delta == (0, 1):
        return 'E'
    
    if delta == (0, -1):
        return 'W'
    
    assert False, f"Invalid delta: {delta}"

def valid_pos(pos, grid):
    return 0 <= pos[0] < len(grid) and 0 <= pos[1] < len(grid[0])


def can_connect(pos1, delta, grid):
    new_pos = (pos1[0] + delta[0], pos1[1] + delta[1])

    if not valid_pos(pos1, grid) or not valid_pos(new_pos, grid):
        return False
    
    new_pos_val = grid[new_pos[0]][new_pos[1]]
    if new_pos_val not in ['L', 'F', 'J', '7', '|', '-']:
        return False

    cardinal = vec_to_cardinal(delta)
    pair = f'{cardinal}{new_pos_val}'


    if pair in ['NF', 'N7', 'N|']:
        return True
    
    if pair in ['SL', 'SJ', 'S|']:
        return True
    
    if pair in ['EJ', 'E7', 'E-']:
        return True
    
    if pair in ['WL', 'WF', 'W-']:
        return True

    return False

def follow_path(grid, start, cardinal_dir):
    pos = start
    length = 0
    path = []

    while grid[pos[0]][pos[1]] != 'S':
        cardinal_dir = char_to_cardinal(grid[pos[0]][pos[1]], cardinal_dir)
        length += 1
        path.append(pos)

        delta = cardinal_to_vec(cardinal_dir)
        new_pos = (pos[0] + delta[0], pos[1] + delta[1])

        if not valid_pos(new_pos, grid):
            return -1, None
        
        pos = new_pos
    
    return (length + 1) // 2, path

def dir_pair_to_char(dir1, dir2):
    dir_pair = ''.join(sorted([dir1, dir2])) # [E, N, S, W]
    
    if dir_pair == 'EN':
        return 'L'
    
    if dir_pair == 'ES':
        return 'F'

    if dir_pair == 'EW':
        return '-'

    if dir_pair == 'NS':
        return '|'
    
    if dir_pair == 'NW':
        return 'J'
    
    if dir_pair == 'SW':
        return '7'


def parse(filename):
    with open(filename, 'r') as file:
        grid = [x.strip() for x in file.readlines()]
    
    start = None

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == 'S':
                start = (i, j)
    
    return grid, start
    
def part1(grid, start):
    lengths = []
    paths = []

    for cardinal_dir in ['N', 'S', 'E', 'W']:
        delta = cardinal_to_vec(cardinal_dir)
        new_pos = (start[0] + delta[0], start[1] + delta[1])

        if not valid_pos(new_pos, grid):
            continue

        if not can_connect(start, delta, grid):
            continue

        length, path = follow_path(grid, new_pos, cardinal_dir)

        if length != -1:
            paths.append(path)
            lengths.append(length)
    
    path_grid = [['.' for _ in range(len(grid[0]))] for _ in range(len(grid))]
    for pos in paths[0]:
        path_grid[pos[0]][pos[1]] = grid[pos[0]][pos[1]]

    return max(lengths)

def part2(grid, start):
    
    paths = []
    cardinal_dirs = []
    for cardinal_dir in ['N', 'S', 'E', 'W']:
        delta = cardinal_to_vec(cardinal_dir)
        new_pos = (start[0] + delta[0], start[1] + delta[1])

        if not valid_pos(new_pos, grid):
            continue

        if not can_connect(start, delta, grid):
            continue

        path = follow_path(grid, new_pos, cardinal_dir)[1]

        if path:
            paths.append(path)
            cardinal_dirs.append(cardinal_dir)
        
    
    path_grid = [['.' for _ in range(len(grid[0]))] for _ in range(len(grid))]
    for pos in paths[0]:
        path_grid[pos[0]][pos[1]] = grid[pos[0]][pos[1]]

    s_replacement = dir_pair_to_char(cardinal_dirs[0], cardinal_dirs[1])
    path_grid[start[0]][start[1]] = s_replacement

    verticals = 'LJ|'
    count = 0

    for i in range(len(path_grid)):
        vert_count = 0
        for j in range(len(path_grid[i])):
            if path_grid[i][j] in verticals:
                vert_count += 1
            elif path_grid[i][j] == '.' and vert_count % 2 == 1:
                count += 1

    return count        

if __name__ == '__main__':
    grid, start = parse('input.txt')
    print(f'Part 1: {part1(grid, start)}')
    print(f'Part 2: {part2(grid, start)}')
