from util import solve

dir_map = {
    "U": (-1,0),
    "D": (1,0),
    "L": (0,-1),
    "R": (0,1)
}

def process(data):
    res = []

    for row in data:
        raw = row.strip().split(" ")
        direction = raw[0]
        units = int(raw[1])
        color = raw[2][1:-1] # remove parenthesis

        res.append((direction, units, color))
    
    return res

def get_dimensions_of_area(data):
    curr = [0,0]
    max_r, max_c = 0, 0

    for entry in data:
        direction = entry[0]
        units = entry[1]
        dr, dc = dir_map[direction]

        curr[0] += dr * units
        curr[1] += dc * units

        max_r = max(max_r, curr[0])
        max_c = max(max_c, curr[1])
    
    return max_r+1, max_c+1

def dig_area(grid, data):
    pass

def dig_inside(grid):
    pass

def get_dug_area(grid):
    total = 0
    for row in grid:
        for cell in row:
            if cell == '#':
                total += 1
    return total

def solver(data):

    data = [
        "R 6 (#70c710)",
        "D 5 (#0dc571)",
        "L 2 (#5713f0)",
        "D 2 (#d2c081)",
        "R 2 (#59c680)",
        "D 2 (#411b91)",
        "L 5 (#8ceee2)",
        "U 2 (#caa173)",
        "L 1 (#1b58a2)",
        "U 2 (#caa171)",
        "R 2 (#7807d2)",
        "U 3 (#a77fa3)",
        "L 2 (#015232)",
        "U 2 (#7a21e3)",
    ]
    
    data = process(data)

    M, N = get_dimensions_of_area(data)
    grid = [['.'] * N for _ in range(M)]
    dig_area(grid, data)
    dig_inside(grid)
    return get_dug_area(grid)

solve(solver, 18)