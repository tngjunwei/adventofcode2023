from util import solve
from collections import defaultdict

def process(raw_color):
    raw_color = raw_color.strip()
    tmp = raw_color.split(' ')
    return int(tmp[0]), tmp[1]

def process_games(row):
    max_color = defaultdict(int)
    tmp = row.split(':')

    game_id = int(tmp[0].split(' ')[1])
    game_info = tmp[1]

    rounds = game_info.split(';')

    for round in rounds:
        colors = round.split(',')

        for raw_color in colors:
            raw_color = raw_color.strip()
            num, color_str = process(raw_color)

            max_color[color_str] = max(max_color[color_str], num)
    
    res = 1
    for v in max_color.values():
        res *= v
    return res

def solver(data):
    res = 0
    for row in data:
        ans = process_games(row)
        res += ans
    return res

solve(solver, 2)
