import math
from puzzle import Puzzle

def ida_star_search(root: Puzzle):
    bound = root.compute_f_value()

    info = [(root.compute_heuristic_manhattan(), root.level, bound)]
    path = [root]
    while True:
        l = search(path, bound, info)
        if l == 'Found':
            return path, info
        elif l == math.inf:
            return 'Not Found'
        bound = l


def search(path, bound, info):
    node = path[-1]

    f = node.compute_f_value()
    if node.board == node.goal:
        return 'Found'
    if f > bound:
        return f

    min_ = math.inf
    successors = node.generate_children()
    for suc in successors:
        if suc not in path:
            path.append(suc)
            h = suc.compute_heuristic_manhattan()
            info.append((h, suc.level, h + suc.level))

            t = search(path, bound, info)
            if t == 'Found':
                return 'Found'
            if t < min_:
                min_ = t

            path.pop(-1)
            info.pop(-1)

    return min_

