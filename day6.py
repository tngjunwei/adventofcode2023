from util import solve

def process(data):
    raw_time = _process(data[0])
    raw_dist = _process(data[1])

    return [(int(time_str), int(dist_str)) for time_str, dist_str in zip(raw_time, raw_dist)]

def process_new(data):
    raw_time = _process(data[0])
    raw_dist = _process(data[1])

    return int("".join(raw_time)), int("".join(raw_dist))

def _process(row):
    tmp = row.split(":")[1].strip().split(" ")
    return [s for s in tmp if s]

def get_ways(contest):
    max_time, dist_to_beat = contest
    total_ways = 0

    charging_time = 0

    while charging_time < max_time//2 + 1:
        if (max_time-charging_time) * charging_time > dist_to_beat:
            break
        charging_time += 1

    if charging_time >= max_time // 2:
        return 0
    
    total_ways = abs(charging_time - max_time//2) * 2

    if max_time+1 % 2 == 0: return total_ways+2
    else: return total_ways+1


def solver(data):
    contests = process(data)
    one_contest = process_new(data)

    res = 1
    for contest in contests:
        num_of_ways = get_ways(contest)
        res *= num_of_ways

    return res, get_ways(one_contest)

solve(solver, 6)

