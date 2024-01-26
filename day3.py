from util import solve

def make_grid(data):
    R = len(data)
    C = len(data[0])

    grid = [[-1] * C for _ in range(R)]
    return grid

def solver(data):
    grid = make_grid(data)
    gear_ratio = dfs(data, grid, visited=set())
    res = process(grid)
    return res, gear_ratio

def process_gear_ratio(list_of_digit_set, grid, N):
    gear_ratio = 1

    for digit_set in list_of_digit_set:
        i, j = min(digit_set)
        num = 0

        while j < N and grid[i][j] != -1:
            num  = num * 10 + grid[i][j]
            j += 1
        gear_ratio *= num

    return gear_ratio


def dfs(data, grid, visited):
    R = len(data)
    C = len(data[0])
    total_gear_ratio = 0

    directions = [(1,1), (1,-1), (-1,1), (-1,-1), # diagonal
                (0,1), (0,-1), (1,0), (-1,0)]  # vert/horz
    
    def is_symbol(char):
        return not char.isdigit()
    
    def _dfs(i, j, visited_digits:set):
        if i < 0 or i >= R:
            return
        if j < 0 or j >= C:
            return
        if (i, j) in visited:
            return

        visited.add((i, j))

        if data[i][j].isdigit():
            grid[i][j] = int(data[i][j])
            visited_digits.add((i, j))
        else:
            return
        
        # visit horz
        _dfs(i, j-1, visited_digits)
        _dfs(i, j+1, visited_digits)
        
    for r, row in enumerate(data):
        for c, char in enumerate(row):
            if char != "." and is_symbol(char):
                list_of_digit_set = []

                for (dr, dc) in directions:
                    visited_digits = set()
                    _dfs(r+dr, c+dc, visited_digits)
                    if visited_digits:
                        list_of_digit_set.append(visited_digits)
                
                if char == "*" and len(list_of_digit_set) == 2:
                    total_gear_ratio += process_gear_ratio(list_of_digit_set, grid, C)

    return total_gear_ratio


def process(grid):
    total = 0
    curr = 0
    for row in grid:
        for digit in row:
            if digit != -1:
                if curr == 0: curr += digit
                else: curr = curr * 10 + digit
            else:
                if curr != 0:
                    total += curr
                    curr = 0

        if curr != 0:
            total += curr
            curr = 0
    
    return total

solve(solver, 3)