from util import solve
from collections import Counter

class HandType():
    HIGH_CARD = 1
    ONE_PAIR = 2
    TWO_PAIR = 3
    THREE_OF_A_KIND = 4
    FULL_HOUSE = 5
    FOUR_OF_A_KIND = 6
    FIVE_OF_A_KIND = 7

## Changed 'J' to 0 for Part 2
card_score = {
    'A': 14,
    'K': 13,
    'Q': 12,
    "J": 0,
    "T": 10,
    "9": 9,
    "8": 8,
    "7": 7,
    "6": 6,
    "5": 5,
    "4": 4,
    "3": 3,
    "2": 2
}

class Hand:
    def __init__(self, hand, bid):
        self.hand = tuple(hand.strip())
        self.hand_type = self._get_hand_type()
        self.bid = bid
    
    def __lt__(self, another_hand):
        if self.hand_type < another_hand.hand_type:
            return True
        elif self.hand_type > another_hand.hand_type:
            return False
        
        # same hand type
        for this_card, other_card in zip(self.hand, another_hand.hand):
            res = self._compare(this_card, other_card)
            if res == -1: return True
            if res == 1: return False
        
        return False
    
    # always want to match other card to get more duplicates = higher hand type score
    def _get_better_hand(self, original_counter: Counter, wildcard):
        num_of_wildcards = original_counter[wildcard]

        if num_of_wildcards == 0: return original_counter
        if num_of_wildcards == 5: return Counter('AAAAA')

        most_duplicates = ''
        max_duplicates = 1

        for card, num_cards in original_counter.items():
            if card != wildcard and num_cards >= max_duplicates:
                most_duplicates = card
                max_duplicates = num_cards

        original_counter[most_duplicates] += num_of_wildcards
        original_counter.pop(wildcard)
        return original_counter
            
    def _get_hand_type(self):
        count = Counter(self.hand)
        if 'J' in count:
            count = Counter(self._get_better_hand(count, wildcard='J'))

        set_of_values = set(count.values())

        if 5 in set_of_values:
            return HandType.FIVE_OF_A_KIND
        if 4 in set_of_values:
            return HandType.FOUR_OF_A_KIND
        if 3 in set_of_values:
            if 2 in set_of_values:
                return HandType.FULL_HOUSE
            elif 1 in set_of_values:
                return HandType.THREE_OF_A_KIND
        
        if 2 in set_of_values:
            num_of_unique_cards = len(count.keys())
            if num_of_unique_cards == 3:
                return HandType.TWO_PAIR
            elif num_of_unique_cards == 4:
                return HandType.ONE_PAIR
        
        return HandType.HIGH_CARD

    def _compare(self, this_card, other_card):
        this_score = card_score[this_card]
        other_score = card_score[other_card]

        if this_score > other_score:
            return 1
        elif this_score < other_score:
            return -1
        else:
            return 0


def process(row):
    tmp = row.split(" ")
    hand = tmp[0].strip()
    bid = int(tmp[1].strip())

    return hand, bid

def solver(data):
    list_of_hands = []

    for row in data:
        hand, bid = process(row)
        list_of_hands.append(Hand(hand, bid))
    
    list_of_hands.sort()

    total = 0
    for idx, hand in enumerate(list_of_hands):
        total += (idx+1) * hand.bid
        print(idx+1, hand.hand, hand.bid)
    return total

solve(solver, 7)