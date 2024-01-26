from util import solve
from collections import deque

def process(data):
    list_of_sequences = []

    for row in data:
        values = row.split(" ")
        sequence = [int(raw_val.strip()) for raw_val in values]
        list_of_sequences.append(sequence)
    
    return list_of_sequences

# Wrong, as the last number can be 0, but not the rest
#example:[8, 12, 33, 75, 140, 233, 365, 558, 861, 1399, 2506, 5042, 11071, 25209, 57205, 126827, 273118, 571922, 1168779, 2339573, 4599646]
def extrapolate_wrong(sequence):
    last_nums = []
    queue = deque()
    next_queue = deque()

    for i in range(-1, -len(sequence)-1, -1):
        diff = sequence[i] - sequence[i-1]
        next_queue.append(diff)

        j = 0
        while queue:
            curr = queue.popleft()
            next_queue.append(curr-next_queue[j])
            j += 1

        queue = next_queue
        next_queue = deque()

        last_nums.append(queue[-1])
        if queue[-1] == 0:
            break
    
    return sum(last_nums) + sequence[-1]

def extrapolate(row):
    list_of_res = [row]
    i = 0
    while True:
        tmp = []
        curr = list_of_res[i]
        for j in range(1,len(curr)):
            tmp.append(curr[j]-curr[j-1])
        list_of_res.append(tmp)
        if len(set(tmp)) == 1:
            break
        else: i += 1
    
    forward = sum([r[-1] for r in list_of_res])
    
    backward = 0
    factor = 1
    for i in range(len(list_of_res)):
        backward += factor * list_of_res[i][0]
        factor *= -1

    return forward, backward


def solver(data):
    list_of_sequences = process(data)

    total_for = total_back = 0
    for sequence in list_of_sequences:
        forward, backward = extrapolate(sequence)

        total_for += forward
        total_back += backward
    
    return total_for, total_back

solve(solver, 9)