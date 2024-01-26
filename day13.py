from util import solve

def process(data):
    list_of_grid = []
    grid = []
    for row in data:
        row = row.strip()
        if not row and grid:
            list_of_grid.append(grid)
            grid = []
        else:
            grid.append(row)
    
    if grid:
        list_of_grid.append(grid)
    return list_of_grid

def get_vertical_sep(grid):
    M = len(grid)
    N = len(grid[0])
    list_of_line = []

    # start with vertical line between col 0 and 1, till N-1 and N
    for j in range(N-1):
        opposite = True
        first = True
        for k in range(min(N-j-1, j+1)):
            for i in range(M):
                if grid[i][j-k] != grid[i][j+k+1]:
                    if not first:
                        opposite = False
                        break
                    else:
                        first = False
            if not opposite:
                break

        if not first and opposite:
            list_of_line.append(j)
            return list_of_line

    return list_of_line


def get_horizontal_sep(grid):
    M = len(grid)
    N = len(grid[0])
    list_of_line = []

    # start with horizontal line between col 0 and 1, till N-1 and N
    for i in range(M-1):
        opposite = True
        first = True
        for k in range(min(M-i-1, i+1)):
            for j in range(N):
                if grid[i-k][j] != grid[i+k+1][j]:
                    if not first:
                        opposite = False
                        break
                    else:
                        first = False
            if not opposite:
                break

        if not first and opposite:
            list_of_line.append(i)
            return list_of_line
            
    return list_of_line

def solver(data):
    list_of_grid = process(data)

    total = 0
    for grid in list_of_grid:
        list_of_vert_sep = get_vertical_sep(grid)
        list_of_hor_sep = get_horizontal_sep(grid)

        # print(list_of_hor_sep, list_of_vert_sep)
        res = 100 * (sum(list_of_hor_sep) + len(list_of_hor_sep))
        res += (sum(list_of_vert_sep) + len(list_of_vert_sep))

        total += res
        # print(res)

    return total


solve(solver, 13)