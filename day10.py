from util import solve
from collections import deque

direction_map = {
    "-": [(0,-1), (0,1)],
    "|": [(-1,0), (1,0)],
    "F": [(0,1), (1,0)],
    "7": [(0,-1), (1,0)],
    "J": [(-1,0), (0,-1)],
    "L": [(-1,0), (0,1)]
}

def find_start(data):
    for i, row in enumerate(data):
        for j, cell in enumerate(row):
            if cell == "S": return (i, j)
    return (-1,-1)

def get_pipe_connected_to_start(data, start_pos):
    M, N = len(data), len(data[0])
    res = []

    constraints = {
        (-1,0): ["|", "7", "F"],
        (1, 0): ["|", "J", "L"],
        (0,-1): ["-", "L", "F"],
        (0, 1): ["-", "J", "7"]
    }

    r, c = start_pos

    for (dr, dc), check_list in constraints.items():
        new_r, new_c = r+dr, c+dc

        if 0 <= new_r < M and 0 <= new_c < N:
            if data[new_r][new_c] in check_list: 
                res.append((new_r, new_c))
    
    return res[0], res[1] # guaranteed

def solver(data):
    M, N = len(data), len(data[0])
    start_pos = find_start(data)
    pipe1, pipe2 = get_pipe_connected_to_start(data, start_pos)
    
    visited = set()
    step = 1
    memory = deque([pipe1, pipe2])
    visited.add(start_pos)

    while True:
        for i in range(len(memory)):
            r, c = memory.popleft()
            pipe = data[r][c]
            visited.add((r, c))

            for dr, dc in direction_map[pipe]:
                new_r, new_c = r+dr, c+dc
                if 0 <= new_r < M and 0 <= new_c < N and (new_r, new_c) not in visited:
                    memory.append((new_r, new_c))
        
        if not memory:
            break
        else:
            step += 1
    
    return step


def solver(data):
    M, N = len(data), len(data[0])
    start_pos = find_start(data) # find 'S'
    pipe1, pipe2 = get_pipe_connected_to_start(data, start_pos)

    start_pos_symbol = get_connector(pipe1, pipe2) # get symbol for 'S'
    data[start_pos[0]][start_pos[1]] = start_pos_symbol

    # always most left or most top, dfs_vector tells which direction to start dfs for enclosed area
    start_pos, dfs_vector = get_new_start_pos(data, pipe1, start_pos, pipe2) 
    
    
    pipelines = set()
    enclosed = set()
    step = 1

    visited.add(start_pos)

    while True:
        for i in range(len(memory)):
            r, c = memory.popleft()
            pipe = data[r][c]
            visited.add((r, c))

            for dr, dc in direction_map[pipe]:
                new_r, new_c = r+dr, c+dc
                if 0 <= new_r < M and 0 <= new_c < N and (new_r, new_c) not in visited:
                    memory.append((new_r, new_c))
        
        if not memory:
            break
        else:
            step += 1
    
    return step

solve(solver, 10)