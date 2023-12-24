def clean(s):
    color_indices = {
        'red': 0,
        'green': 1,
        'blue': 2,
    }

    subsets = s.split(':')[1].split(';')
    clean_subsets = []

    for subset in subsets:
        clean_subset = [0, 0, 0]
        colors = subset.split(',')

        for color in colors:
            v, c = color.strip().split(' ')
            v = int(v)
            clean_subset[color_indices[c]] = v
        
        clean_subsets.append(clean_subset)
    
    return clean_subsets

def parse(filename):
    with open(filename) as file:
        return [clean(s.strip()) for s in file.readlines()]

def part1(sets):
    max_vals = [12, 13, 14]
    valid_games = []

    for game_num, game in enumerate(sets):
        valid = True
        for subset in game:
            if not valid:
                break

            for i, val in enumerate(subset):
                if val > max_vals[i]:
                    valid = False
                    break
            
        if valid:
            valid_games.append(game_num + 1)
    
    return sum(valid_games)

def part2(sets):
    powers = []

    for game in sets:
        min_dice = game[0]
        for subset in game:
            for i, val in enumerate(subset):
                min_dice[i] = max(min_dice[i], val)
        
        powers.append(min_dice[0] * min_dice[1] * min_dice[2])

    return sum(powers)

if __name__ == '__main__':
    sets = parse('input.txt')
    print(f"Part 1: {part1(sets)}")
    print(f"Part 2: {part2(sets)}")
