from collections import defaultdict, deque
from itertools import combinations
from functools import lru_cache

def clean(line):
    crypt, counts = line.split()
    counts = [int(x) for x in counts.split(',')]
    return crypt, counts


def parse(filename):
    with open(filename, 'r') as file:
        return [clean(line.strip()) for line in file.readlines()]


@lru_cache(maxsize=None)
def count_valid_crypts(crypt, count, index_crypt=0, index_count=0, cumulative_count=0):
    if index_count == len(count):
        return cumulative_count == 0 and all(crypt[i] in '.?!' for i in range(index_crypt, len(crypt)))

    if cumulative_count > count[index_count]:
        return 0

    if crypt[index_crypt] == '!':
        return index_count == len(count) - 1 and cumulative_count == count[index_count]


    if crypt[index_crypt] == '.':
        if cumulative_count != 0 and cumulative_count != count[index_count]:
            return 0
        
        return count_valid_crypts(crypt, count, index_crypt+1, index_count + int(cumulative_count != 0), 0)

    if crypt[index_crypt] == '#':
        return count_valid_crypts(crypt, count, index_crypt+1, index_count, cumulative_count+1)
    
    if crypt[index_crypt] == '?':
        pound_count = count_valid_crypts(crypt, count, index_crypt+1, index_count, cumulative_count+1)
        period_count = 0

        if cumulative_count == 0 or cumulative_count == count[index_count]:
            period_count = count_valid_crypts(crypt, count, index_crypt+1, index_count + int(cumulative_count != 0), 0)

        return pound_count + period_count

    
def part1(crypt_counts):
    counts = [count_valid_crypts(crypt + '!', tuple(count)) for crypt, count in crypt_counts]
    return sum(counts)


def part2(crypt_counts):
    counts = [count_valid_crypts(((crypt + '?')*5)[:-1] + '!', tuple(count*5)) for crypt, count in crypt_counts]
    return sum(counts)

if __name__ == '__main__':
    x = parse('input.txt')
    print(f'Part 1: {part1(x)}')
    print(f'Part 2: {part2(x)}')
