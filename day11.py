from util import solve

class Lense:
    def __init__(self, num_row, num_col, empty_rows, empty_cols):
        empty_rows.sort()
        empty_cols.sort()
        self.lookup_new_row = self._init_new_lookup(empty_rows, num_row)
        self.lookup_new_col = self._init_new_lookup(empty_cols, num_col)
    
    def __call__(self, pos):
        row, col = pos
        return self.lookup_new_row[row], self.lookup_new_col[col]
    
    def _init_new_lookup(self, empty, dim_size):
        empty_idx = 0
        lookup = {}
        extra = 0

        for i in range(dim_size):
            if empty_idx < len(empty) and i == empty[empty_idx]:
                extra += 999_999
                empty_idx += 1
            lookup[i] = i + extra
        
        return lookup

def get_empty_cols(data):
    M = len(data)
    N = len(data[0])

    list_of_empty_cols = []
    for j in range(N):
        empty = True

        for i in range(M):
            if data[i][j] != '.':
                empty = False
                break
        
        if empty: list_of_empty_cols.append(j)
    return list_of_empty_cols

def get_empty_rows(data):
    M = len(data)
    N = len(data[0])

    list_of_empty_rows = []
    for i in range(M):
        empty = True

        for j in range(N):
            if data[i][j] != '.':
                empty = False
                break
        
        if empty: list_of_empty_rows.append(i)
    return list_of_empty_rows

def noop(input):
    return input

def process(data, lense=None):
    set_of_pos = set()
    if not lense:
        lense = noop
    
    for i in range(len(data)):
        for j in range(len(data[0])):
            if data[i][j] == '#':
                actual_pos = lense((i,j))
                set_of_pos.add(actual_pos)
    return set_of_pos

def solver(data):
    list_of_empty_rows = get_empty_rows(data)
    list_of_empty_cols = get_empty_cols(data)

    lense = Lense(len(data), len(data[0]), list_of_empty_rows, list_of_empty_cols)

    set_of_pos = process(data, lense)
    
    dist = 0
    for pos in set_of_pos:
        min_dist = get_dist_to_other_pos(set_of_pos, pos)
        #print(f"{pos}: {min_dist}")
        dist += min_dist
    
    return dist // 2 # since there is double-counting

def get_dist_to_other_pos(all_positions, pos):
    dist = 0

    for other_pos in all_positions:
        dist += abs(other_pos[0]-pos[0]) + abs(other_pos[1]-pos[1])
   
    return dist

solve(solver, 11)