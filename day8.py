from util import solve
import math

def process(data):
    movement_inputs = list(data[0].strip())
    directions = {}
    set_of_starting_pos = set()

    for row in data[2:]:
        tmp = row.split("=")
        src = tmp[0].strip()
        tmp = tmp[1].strip().strip("(").strip(")").split(",")
        left = tmp[0].strip()
        right = tmp[1].strip()

        if src.endswith("A"):
            set_of_starting_pos.add(src)
        
        directions[src] = {}
        directions[src]["L"] = left
        directions[src]["R"] = right
    
    return movement_inputs, directions, list(set_of_starting_pos)

def get_lcm(list_of_nums):
    if not list_of_nums: return 1

    curr = list_of_nums[0]
    for num in list_of_nums[1:]:
        curr = (curr * num) // math.gcd(curr, num)
    
    return curr

def solver(data):
    movements, directions, starting_pos = process(data)
    step_1 = step_2 = i = 0
    N = len(movements)

    # Part 1
    curr = "AAA"
    while curr != "ZZZ":
        curr = directions[curr][movements[i]]
        i = (i+1) % N
        step_1 += 1

    # Part 2
    list_of_steps_to_reach_Z = []

    for curr in starting_pos:
        i = steps = 0
        while True:
            curr = directions[curr][movements[i]]
            i = (i+1) % N
            steps += 1

            if curr.endswith("Z"):
                break
        list_of_steps_to_reach_Z.append(steps)

    step_2 = get_lcm(list_of_steps_to_reach_Z)
        
    return step_1, step_2

solve(solver, 8)