def clean(s):
    winning, mine = s.split(': ')[1].split(' | ')

    return (
        {int(x) for x in winning.split(' ') if len(x) > 0},
        {int(x) for x in mine.split(' ') if len(x) > 0}
    )

def parse(filename):
    with open(filename) as file:
        return [clean(s.strip()) for s in file.readlines()]
    
def part1(nums):
    return sum(
        int(2**(len(winning & mine) - 1))
        for winning, mine in nums
    )

def part2(nums):
    card_count = [1 for _ in range(len(nums))]

    for i, (winning, mine) in enumerate(nums):
        matches_count = len(winning & mine)
        for j in range(matches_count):
            card_count[i + j + 1] += card_count[i]

    return sum(card_count)

if __name__ == '__main__':
    nums = parse('input.txt')
    print(f"Part 1: {part1(nums)}")
    print(f"Part 2: {part2(nums)}")
