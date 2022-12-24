import heapq
import math


class Puzzle:
    goal = [1, 2, 3, 4, 5, 6, 7, 8, -1]


    def __init__(self, n, board, level):
        self.N = n
        self.level = level  # g = 0 initially
        self.board = board  # initial board state

    def compute_heuristic_manhattan(self):
        heuristic = 0
        for num in range(1, 9):
            distance = abs(self.board.index(num) - self.goal.index(num))
            i = int(distance / 3)
            j = int(distance % 3)
            heuristic = heuristic + i + j

        return heuristic

    def compute_f_value(self):
        h = self.compute_heuristic_manhattan()

        return h + self.level

    def generate_children(self):
        actions = self.legal_actions()

        children = []
        for action in actions:
            new_board = self.generate_new_board(action)
            new_puzzle = Puzzle(self.N, new_board, level=self.level + 1)

            children.append(new_puzzle)

        return children

    def generate_new_board(self, action):
        blank_pos = self.blank_position()

        new_board = self.board.copy()
        if action == 'up':
            new_board[blank_pos], new_board[blank_pos - self.N] = new_board[blank_pos - self.N], new_board[blank_pos]
        elif action == 'down':
            new_board[blank_pos], new_board[blank_pos + self.N] = new_board[blank_pos + self.N], new_board[blank_pos]
        elif action == 'left':
            new_board[blank_pos], new_board[blank_pos - 1] = new_board[blank_pos - 1], new_board[blank_pos]
        elif action == 'right':
            new_board[blank_pos], new_board[blank_pos + 1] = new_board[blank_pos + 1], new_board[blank_pos]

        return new_board

    def legal_actions(self):
        blank_pos = self.blank_position()
        row, col = blank_pos // self.N, blank_pos % self.N

        actions = ['up', 'down', 'left', 'right']
        if row == 0:
            actions.remove('up')
        if row == self.N - 1:
            actions.remove('down')
        if col == 0:
            actions.remove('left')
        if col == self.N - 1:
            actions.remove('right')

        return actions

    def blank_position(self):
        pos = 0
        for i in range(self.N * self.N):
            if self.board[i] == -1:
                pos = i
                return pos

        return pos

    def __str__(self):
        return str(self.board[0:3]) + '\n' + str(self.board[3:6]) + '\n' + str(self.board[6:9]) + '\n'

    # def move_blank(self):
    #     actions, blank_pos = self.legal_actions()
    #     print('You can move in these directions: (', end=' ')
    #     print(*actions, end=')')
    #     print()
    #     action = input('Please choose one: ')
    #     new_board = self.generate_new_board(action)
    #     self.board = new_board


class Solver:
    curr_puzzle = None

    def __init__(self, n):
        self.N = n
        self.open_list = []
        self.closed_list = []

        heapq.heapify(self.open_list)  # making open_list a priority Queue

    def process(self):
        board = self.input_board()  # Get the initial board from user or default
        puzzle = Puzzle(self.N, board, level=0)  # Create the initial Puzzle
        self.curr_puzzle = puzzle

        solvable = self.solvable(puzzle)  # Check if the puzzle is Solvable
        if solvable is False:
            print('puzzle is not solvable!')
        else:
            res = self.ida_star_search(puzzle)
            print("Path to goal is:")
            print(*res)
            return

    def ida_star_search(self, root: Puzzle):
        bound = root.compute_f_value()

        path = [root]
        while True:
            l = self.search(path, bound)
            if l == 'Found':
                return path
            elif l == math.inf:
                return 'Not Found'
            bound = l

    def search(self, path, bound):
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

                t = self.search(path, bound)
                if t == 'Found':
                    return 'Found'
                if t < min_:
                    min_ = t

                path.pop(-1)

        return min_

    def input_board(self):
        print('initial state is:')
        print('7 1 2\n'
              '-1 5 4\n'
              '8 6 3\n')
        state = input('Continue with initial state or input custom state (y / n)? ')
        board = []
        if state == 'y':
            board = [7, 1, 2, -1, 5, 4, 8, 6, 3]
        else:
            print("input the start state of puzzle:")
            for i in range(self.N):
                puz = list(map(int, input().split()))
                board.extend(puz)

        return board

    def solvable(self, puzzle: Puzzle):
        inversions = self.count_inversions(puzzle)

        # if N is odd --> Number of inversions should be even
        if self.N % 2 == 1:
            if inversions % 2 == 0:
                return True
        else:
            pos = puzzle.blank_position()
            pos = self.N - pos[0]

            # the blank is on an even row counting from the bottom and number of inversions is odd
            if pos % 2 == 0 and inversions % 2 == 1:
                return True
            # the blank is on an odd row counting from the bottom and number of inversions is even
            elif pos % 2 == 1 and inversions % 2 == 0:
                return True

        return False

    def count_inversions(self, puzzle):
        puz = puzzle.board
        inv = 0
        dims = self.N * self.N

        for i in range(dims - 1):
            if puz[i] == -1:
                continue
            for j in range(i + 1, dims):
                if puz[j] != -1 and puz[i] > puz[j]:
                    inv += 1
        return inv


# puzzle = [[1,2,3],[4,5,6],[7,8,-1]]
# print(puzzle[-1])
# print(puzzle)
# b = [7, 1, 2, -1, 5, 4, 8, 6, 3]

s = Solver(3)
s.process()

# actions = ['up', 'down', 'left', 'right']
# print(*actions)
