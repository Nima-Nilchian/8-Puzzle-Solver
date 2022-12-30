import math
from puzzle import Puzzle

def ida_star_search(root: Puzzle):
    bound = root.compute_f_value()                              # initially bound is the f value of root

    info = [(bound - root.level, root.level, bound, bound)]     # ( h, g, f, bound )
    path = [root]                                               # the steps of ida* in optimal path
    mins = []                                                   # minimum out of fringe
    while True:
        l = search(path, bound, info, mins)
        if l == 'Found':
            return path, info, mins
        elif l == math.inf:
            return 'Not Found'
        mins.append(l)
        bound = l

def search(path, bound, info, mins):
    node = path[-1]

    f = node.compute_f_value()
    if node.board == node.goal:
        return 'Found'
    if f > bound:
        mins.append(f)
        return f

    min_ = math.inf
    successors = node.generate_children()
    for suc in successors:
        if suc not in path:
            path.append(suc)
            h = suc.compute_heuristic_manhattan()
            info.append((h, suc.level, h + suc.level, bound))

            t = search(path, bound, info, mins)
            if t == 'Found':
                return 'Found'
            if t < min_:
                min_ = t

            path.pop(-1)
            info.pop(-1)

    return min_


def recursive_best_first_search(root: Puzzle):
    path = [root]
    info = []

    res = RBFS(root, math.inf, path, info)
    h = res[0].compute_heuristic_manhattan()
    info = [h, res[0].level, h+res[0].level, res[1]]

    return res[0], info

def RBFS(node, f_limit, path, info):
    successors = []
    result = None
    if node.board == node.goal:
        return node, None

    children = node.generate_children()
    if not len(children):
        return None, f_limit

    compare = -1
    for child in children:
        if child not in path:
            f = child.compute_f_value()
            compare += 1
            successors.append((f, compare, child))
        else:
            return None, f_limit

    while len(successors):
        successors.sort()
        for suc in successors:
            path.append(suc[2])
            info.append((suc[0] - suc[2].level, suc[2].level, suc[0], f_limit))

        best_node = successors[0][2]
        f = successors[0][0]

        if f > f_limit:
            return None, f
        second_best_f = successors[1][0]        # Alternative

        result, best_f = RBFS(best_node, min(f_limit, second_best_f), path, info)
        successors[0] = (best_f, successors[0][1], best_node)

        if result is not None:
            break

        path.pop(0)
        info.pop(0)


    return result, None





