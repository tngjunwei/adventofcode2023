from util import solve

# Do not run this for Part 2, as it will take too long.
# Alternative algorithm is needed, such as search by ranges, etc.
# C# is used to speed up Part 2 algorithm.

def process_seeds(row):
    seed_list_str = row.split(":")[1].strip()

    list_of_seeds = [int(s) for s in seed_list_str.split(" ")]
    return list_of_seeds

def process_new_seeds(row):
    num_list_str = row.split(":")[1].strip()
    list_of_nums = [int(s) for s in num_list_str.split(" ")]

    list_of_intervals = []
    for i in range(0,len(list_of_nums), 2):
        list_of_intervals.append((list_of_nums[i], list_of_nums[i]+list_of_nums[i+1]-1))
    
    return merge_intervals(list_of_intervals)


def merge_intervals(list_of_intervals):
    new_list = sorted(list_of_intervals)
    tmp = []
    for interval in new_list:
        curr = interval
        if not tmp: 
            tmp.append(curr)
            continue

        while is_overlapping(tmp[-1], curr):
            start, end = tmp.pop()
            new_start = min(start, curr[0])
            new_end = max(end, curr[1])

            curr = (new_start, new_end)
        
        tmp.append(curr)
    return tmp

def is_overlapping(i1, i2):
    return i1[0] <= i2[1] and i1[1] >= i2[0]

def process_maps(data: list[str]) -> list[list[str]]:
    list_of_maps = []
    mappings = []
    
    for row in data:
        row = row.strip()
        if not row:
            list_of_maps.append(mappings)
            continue
        
        if row.endswith(":"):
            mappings = []
        else:
            tmp = row.split(" ")
            mapping = (int(tmp[0].strip()), int(tmp[1].strip()), int(tmp[2].strip()))
            mappings.append(mapping)
    
    if mappings:
        list_of_maps.append(mappings)

    return list_of_maps

class Mapping:
    def __init__(self, raw_maps):
        self.mappings = []

        for (dest, src, dist) in raw_maps:
            entry = (src, src+dist-1, dest)
            self.mappings.append(entry)
        self.mappings.sort()
    
    def convert(self, src_id):
        idx = self._binary_search(0, len(self.mappings)-1, src_id)

        if idx == -1:
            return src_id
        else:
            src, _, dest = self.mappings[idx]
            return dest + (src_id-src)
    
    def _binary_search(self, l, r, to_find):
        if l > r:
            return -1

        m = l + (r-l)//2

        start, end = self.mappings[m][0], self.mappings[m][1]
        if start <= to_find and to_find <= end:
            return m
        
        if to_find < start:
            return self._binary_search(l, m-1, to_find)
        elif to_find > end:
            return self._binary_search(m+1, r, to_find)


def solver(data):
    list_of_seeds = process_seeds(data[0])
    list_of_raw_maps = process_maps(data[2:])
    list_of_maps = [Mapping(raw_map) for raw_map in list_of_raw_maps]

    min_location = float("inf")
    for seed in list_of_seeds:
        curr = seed
        for map in list_of_maps:
            curr = map.convert(curr)
        min_location = min(curr, min_location)
    
    return min_location

from time import time
def solver_new(data):
    list_of_seeds = process_new_seeds(data[0])
    list_of_raw_maps = process_maps(data[2:])
    list_of_maps = [Mapping(raw_map) for raw_map in list_of_raw_maps]

    min_location = float("inf")
    list_of_seeds = [(0, 10_000_000)]
    for (start, end) in list_of_seeds:
        begin = time()
        for seed in range(start, end+1):
            curr = seed
            for map in list_of_maps:
                curr = map.convert(curr)
            min_location = min(curr, min_location)
        fin = time()
        print(f"{end-start} entries took {fin-begin} seconds")
    
    return min_location

solve(solver_new, 5)