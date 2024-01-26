from util import solve

def process(data):
    list_of_condition = []
    list_of_config = []

    for row in data:
        cond, conf = row.split(" ")
        list_of_condition.append(cond.strip())

        conf = conf.strip().split(",")
        config = []
        for raw_num in conf:
            config.append(int(raw_num.strip()))
        list_of_config.append(config)

    return list_of_condition, list_of_config

def process_unfolded(data):
    list_of_condition = []
    list_of_config = []

    for row in data:
        cond, conf = row.split(" ")
        tmp = [cond.strip()] * 5
        list_of_condition.append("?".join(tmp))

        conf = conf.strip().split(",")
        config = []
        for raw_num in conf:
            config.append(int(raw_num.strip()))
        config = config * 5
        list_of_config.append(config)

    return list_of_condition, list_of_config

def get_num_of_arrangements(condition, config: list) -> int:
    # print(condition, config)
    if not condition and not config: return 1
    if not condition and config: return 0

    if condition and not config:
        set_of_char = set(condition)
        if '#' in set_of_char: return 0
        else: return 1

    # if condition and config: do these
    if condition[0] == ".":
        return get_num_of_arrangements(condition[1:], config)
    else:
        total = 0
        if condition[0] == "?":
            total += get_num_of_arrangements(condition[1:], config) # place a '.'

    # or place a '#' and fill up according to config[0]
    # if can fill up, continue. Else, it is invalid
        num_to_place = config[0]
        for i in range(num_to_place):
            if i >= len(condition): break
            if condition[i] == '.': 
                i -= 1
                break
        
        if i == num_to_place-1:
            if num_to_place == len(condition): # reached the end of string
                total += get_num_of_arrangements("", config[1:])
            # if next character is not '#', leave a space and start from second character
            if i+1 < len(condition) and condition[i+1] != '#':
                total += get_num_of_arrangements(condition[num_to_place+1:], config[1:]) 
                
        return total


def solver(data):
    list_of_condition, list_of_config = process_unfolded(data)

    # list_of_condition = [
    #     '???.###',
    #     '.??..??...?##.',
    #     '?#?#?#?#?#?#?#?',
    #     '????.#...#...',
    #     '????.######..#####.',
    #     '?###????????'
    # ]
    # list_of_config = [
    #      [1,1,3],
    #      [1,1,3],
    #      [1,3,1,6],
    #      [4,1,1],
    #      [1,6,5],
    #      [3,2,1]
    # ]

    total = 0

    for condition, config in zip(list_of_condition, list_of_config):
        res = get_num_of_arrangements(condition, config)
        total += res
        print(res)
    
    return total

solve(solver, 12)
