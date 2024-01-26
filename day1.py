from functools import reduce
import re

from util import solve

def process(raw_digit: str) -> int:
    digit_map = {
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9
    }

    if raw_digit in digit_map:
        return digit_map[raw_digit]
    else:
        return int(raw_digit)

def get_num_in_row(row: str):
    row = row.strip()
    dbl_pattern = r"(one|two|three|four|five|six|seven|eight|nine|[0-9]).*(one|two|three|four|five|six|seven|eight|nine|[0-9])"
    single_pattern = r"(one|two|three|four|five|six|seven|eight|nine|[0-9])"

    captured_grps = re.findall(dbl_pattern, row)
    if not captured_grps:
        captured_grp = re.findall(single_pattern, row)
        first = second = process(captured_grp[0][0])
    else:
        first = process(captured_grps[0][0])
        second = process(captured_grps[0][1])

    return first * 10 + second

def run(data):
    total = 0
    for row in data:
        total += get_num_in_row(row)
    return total

solve(run, 1)
