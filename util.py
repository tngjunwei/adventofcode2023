def _read_input(filename: str) -> list[str]:
    with open(filename, "r") as f:
        data = f.readlines()
    
    return data

def solve(solver, day):
    data = _read_input(f"inputs/day{day}")
    data = [row.strip() for row in data]  # impt -> causes bug in day 3 already :(
    res = solver(data)
    print(res)
