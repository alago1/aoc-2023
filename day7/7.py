from collections import Counter

def parse(filename):
    with open(filename) as file:
        lines = [x.strip().split() for x in file.readlines()]

    hands = [x[0] for x in lines]
    bids = [int(x[1]) for x in lines]

    return hands, bids

def encode_by_type(hand):
    counts = Counter(hand).most_common(2)

    if len(counts) == 1:
        return counts[0][1]*10

    return counts[0][1]*10 + counts[1][1]

def encode_by_type_replace_joker(hand: str):
    j_count = len([x for x in hand if x == 'J'])

    if j_count == len(hand):
        return len(hand) * 10

    counts = Counter(hand.replace('J', '')).most_common(2)

    if len(counts) == 1:
        return (counts[0][1] + j_count)*10

    return (counts[0][1] + j_count)*10 + counts[1][1]

def encode_by_cards(hand, card_order):
    v = 0
    for card in hand:
        v = v*len(card_order) + card_order.index(card)
    
    return v

def encode_hand(hand, card_order, replace_joker=False):
    hand_type = encode_by_type(hand) if not replace_joker else encode_by_type_replace_joker(hand)
    card_encoding = encode_by_cards(hand, card_order)

    return hand_type, card_encoding

def part1(hands, bids):
    card_order = '23456789TJQKA'
    encodings = sorted((*encode_hand(hand, card_order), bid) for hand, bid in zip(hands, bids))

    return sum(
        (i + 1) * bid
        for i, (*_, bid) in enumerate(encodings)
    )

def part2(hands, bids):
    card_order = 'J23456789TQKA'
    encodings = sorted(
        (*encode_hand(hand, card_order, replace_joker=True), bid)
        for hand, bid in zip(hands, bids)
    )

    return sum(
        (i + 1) * bid
        for i, (*_, bid) in enumerate(encodings)
    )

if __name__ == '__main__':
    hands, bids = parse('input.txt')
    print(f"Part 1: {part1(hands, bids)}")
    print(f"Part 2: {part2(hands, bids)}")
