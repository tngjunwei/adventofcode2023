from util import solve
from collections import deque

reflection_map = {
    "/": {
        (0,1): (-1,0),
        (1,0): (0,-1),
        (0,-1): (1,0),
        (-1,0): (0,1)
    },
    "\\": {
        (0,1): (1,0),
        (1,0): (0,1),
        (0,-1): (-1,0),
        (-1,0): (0,-1)
    }
}

class Ray:
    def __init__(self, pos, dir_vector):
        self.pos = pos
        self.dir_vector = dir_vector
        self.dead = False

    def _get_next_state(self, grid, pos, dir_vector):
        dr, dc = dir_vector
        r,c = pos
        symbol = grid[r][c]

        new_dir_vector = dir_vector
        new_ray = None

        if symbol == '.': 
            new_dir_vector = dir_vector
        elif symbol == '-':
            if dr != 0: # move vertically
                new_ray = Ray(pos, (0,-1)) # new ray moves left
                new_dir_vector = (0,1) # original ray moves right
        elif symbol == '|':
            if dc != 0: # move horizontally
                new_ray = Ray(pos, (-1,0)) # new ray moves up
                new_dir_vector = (1,0) # original ray moves down
        else: # reflection
            new_dir_vector = reflection_map[symbol][dir_vector]

        return new_dir_vector, new_ray

    
    def move(self, grid, energised_set):
        M, N = len(grid), len(grid[0])
        r,c = self.pos
        dr, dc = self.dir_vector

        new_ray = None
        new_r, new_c = r+dr, c+dc
        if 0 <= new_r < M and 0 <= new_c < N:
            pos = new_r, new_c
            self.pos = pos
            energised_set.add(pos)
            self.dir_vector, new_ray = self._get_next_state(grid, pos, self.dir_vector)
        else:
            self.dead = True
        
        return new_ray
    
def simulate(data, start_pos, init_dir):
    ray = Ray(start_pos, init_dir)

    queue_of_rays = deque([ray]) # process ray by time ticks
    energised_set = set()

    same_num_limit = 10
    count = 0

    while queue_of_rays:
        before = len(energised_set)
        
        for _ in range(len(queue_of_rays)):
            curr_ray = queue_of_rays.popleft()
            new_ray = curr_ray.move(data, energised_set)
            
            if new_ray is not None: queue_of_rays.append(new_ray)
            if not curr_ray.dead: queue_of_rays.append(curr_ray)
        
        after = len(energised_set)
        
        if after == before:
            count += 1
        else:
            count = 0
        if count > same_num_limit:
            break
    
    return len(energised_set)

def solver(data):
    # start outside the grid, facing right
    # start_pos = (0, -1) 
    # init_dir = (0, 1) # means the ray will travel one unit right after a tick
    list_of_res = []
    list_of_start_pos = []
    list_of_init_dirs = []
    M, N = len(data), len(data[0])
    for i in range(M):
        list_of_start_pos.append((i,-1))
        list_of_init_dirs.append((0, 1))
        list_of_start_pos.append((i, M))
        list_of_init_dirs.append((0,-1))
    
    for i in range(N):
        list_of_start_pos.append((-1,i))
        list_of_init_dirs.append((1, 0))
        list_of_start_pos.append((M, i))
        list_of_init_dirs.append((-1,0))

    for start_pos, init_dir in zip(list_of_start_pos, list_of_init_dirs):
        res = simulate(data, start_pos, init_dir)
        list_of_res.append(res)
        print(res)
    
    return max(list_of_res)

solve(solver, 16)