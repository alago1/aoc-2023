def parse(input_file):
    def parse_line(line):
        return [int(x) for x in line.split()]

    with open(input_file) as file:
        return [parse_line(line.strip()) for line in file.readlines()]
    
def seq_diff(seq):
    return [b - a for a, b in zip(seq, seq[1:])]

def next_val_in_seq(seq):
    endings = [seq[-1]]
    diff = seq_diff(seq)

    while any(d != 0 for d in diff):
        endings.append(diff[-1])
        diff = seq_diff(diff)

    if len(endings) == 0:
        return seq[-1]

    return sum(endings)  

def first_val_in_seq(seq):
    endings = [seq[0]]
    diff = seq_diff(seq)

    while any(d != 0 for d in diff):
        endings.append(diff[0] * (-1) ** len(endings))
        diff = seq_diff(diff)

    if len(endings) == 0:
        return seq[0]

    return sum(endings)

def part1(seqs):
    next_vals = [next_val_in_seq(seq) for seq in seqs]
    return sum(next_vals)


def part2(seqs):
    first_vals = [first_val_in_seq(seq) for seq in seqs]
    return sum(first_vals)

if __name__ == '__main__':
    x = parse('input.txt')
    print(f"Part 1: {part1(x)}")
    print(f"Part 2: {part2(x)}")
