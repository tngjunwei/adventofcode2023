from util import solve
from collections import defaultdict

def process(data):
    words = data.strip().split(",")
    res = []
    action = []
    for word in words:
        if word[-1] == '-':
            res.append(word[:-1])
            action.append('-')
            continue
        else:
            tmp = word.split("=")
            res.append(tmp[0].strip())
            action.append(tmp[1].strip())
    
    assert len(words) == len(res)
    return res, action

def hash(some_str: str) -> int:
    total = 0
    for c in some_str:
        total += ord(c)
        total *= 17
        total %= 256
    return total

class Boxes:
    def __init__(self, hash_func):
        self.hash = hash_func
        self.boxes = defaultdict(list) # need to optimize

    def _search_index(self, some_list, word, element_idx=0) -> int:
        for i, element in enumerate(some_list):
            if word == element[element_idx]:
                return i
        return -1

    def remove(self, word):
        box_num = self.hash(word)
        word_idx = self._search_index(self.boxes[box_num], word)
        if word_idx != -1:
            self.boxes[box_num].pop(word_idx)
            return

    def update(self, word, new_focal_length):
        box_num = self.hash(word)
        word_idx = self._search_index(self.boxes[box_num], word)
        new_entry = (word, new_focal_length)
        if word_idx != -1:
            self.boxes[box_num][word_idx] = new_entry # replace value
        else:
            self.boxes[box_num].append(new_entry) # add new value

    def get_total_focal_power(self) -> int:
        total = 0
        for box_num, list_of_lenses in self.boxes.items():
            for idx, (_, focal_length) in enumerate(list_of_lenses):
                total += (box_num+1) * (idx+1) * focal_length
        
        return total

def solver(data):
    data = data[0]
    # data = "rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"
    words, actions = process(data)
    boxes = Boxes(hash)

    for word, action in zip(words, actions):
        if action == '-':
            boxes.remove(word)
        else:
            focal_length_to_update = int(action)
            boxes.update(word, focal_length_to_update)

    return boxes.get_total_focal_power()

solve(solver, 15)
