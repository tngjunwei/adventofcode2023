from util import solve

# iterate from 0 (south) to N-1 (north)
def get_load(column: list[str]):
    num_of_rocks = 0
    total = 0
    for row_num, obj in enumerate(column):
        if obj == '.': continue
        if obj == 'O': 
            num_of_rocks += 1 
            continue

        for i in range(num_of_rocks):
            total += row_num - i
        num_of_rocks = 0
    
    if num_of_rocks > 0:
        N = len(column)
        for i in range(num_of_rocks):
            total += N - i
    return total
        
def get_column(data, col_num):
    M, N = len(data), len(data[0])
    col = []
    for i in range(M-1, -1, -1):
        col.append(data[i][col_num])

    return col


def solver(data):
    total = 0

    for i in range(len(data[0])):
        col = get_column(data, i)
        total += get_load(col)
    
    return total

solve(solver, 14)