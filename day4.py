from util import solve

def process(row):
    num_data = row.split(":")[1]

    tmp = num_data.split("|")
    winning_nums_data, card_nums_data = tmp[0].strip(), tmp[1].strip()

    set_of_winning_nums = collect_nums(winning_nums_data)
    set_of_card_nums = collect_nums(card_nums_data)

    return set_of_winning_nums, set_of_card_nums

def collect_nums(nums_data):
    nums_data = nums_data.strip()
    list_of_num_str = nums_data.split(" ")

    res = set()
    for num_str in list_of_num_str:
        if num_str:
            res.add(int(num_str.strip()))
    
    return res

def score_card(winning_nums, card_nums):
    score = 0

    for num in card_nums:
        if num in winning_nums:
            score += 1

    return score

def calculate_final_num_cards(list_matched):
    N = len(list_matched)
    list_num_of_cards = [1] * N

    for i, num_matched in enumerate(list_matched):
        curr = list_num_of_cards[i]

        for j in range(1, num_matched+1):
            if i+j >= N: break

            list_num_of_cards[i+j] += curr
    
    return list_num_of_cards

def solver(data):
    total = 0
    list_num_matched = []

    for row in data:
        winning_nums, card_nums = process(row)
        num_of_winning_nums = score_card(winning_nums, card_nums)
        list_num_matched.append(num_of_winning_nums)

        if(num_of_winning_nums > 0):
            total += 2 ** (num_of_winning_nums - 1)
    
    final_num_cards = calculate_final_num_cards(list_num_matched)

    return total, sum(final_num_cards)

solve(solver, 4)