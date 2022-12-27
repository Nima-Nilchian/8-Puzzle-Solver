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
        str_ = "_"*13 + '\n'
        for i in range(len(self.board)):
            str_ += '|'
            if self.board[i] == -1:
                str_ += str(self.board[i]) + ' '
            else:
                str_ += ' ' + str(self.board[i]) + ' '
            if (i+1) % self.N == 0:
                str_ = str_ + '|' + '\n'

        str_ += "_"*13 + '\n'
        return str_

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


    def initial_phase(self):
        self.input_board()

        solvable = self.solvable(self.curr_puzzle)  # Check if the puzzle is Solvable
        if solvable is False:
            print('puzzle is not solvable!')
            self.initial_phase()

        stat = input('Play with the Algorithm or User (a/u)? ')
        if stat == 'a':
            self.process()
        elif stat == 'u':
            self.user_move()


    def process(self):
        puzzle = self.curr_puzzle
        path, info = self.ida_star_search(puzzle)

        for i in range(len(path)):
            print(path[i])
            self.print_info(info[i])

        return

    def print_info(self, info):
        print('*'*13)
        print('h value: ', info[0])
        print('g value: ', info[1])
        print('f value: ', info[2])
        print('*' * 13)


    def user_move(self):
        puz = self.curr_puzzle
        print(puz)
        print('Choose house number and the action to perform on it (up, down, left, right)')
        num = int(input('house: '))
        action = input('action: ')

        new_board = self.move_house(num, action)
        new_puzzle = Puzzle(self.N, new_board, level=puz.level + 1)
        self.curr_puzzle = new_puzzle

        if new_board == new_puzzle.goal:
            print(new_puzzle)
            print()
            print('YAY!! You Found the Goal!\n')

        status = input('Continue / Finish / Restart the Game? (c/f/r)')
        if status == 'f':
            return
        if status == 'r':
            self.initial_phase()
        else:
            self.user_move()

        return


    def input_board(self):
        print('initial state is:')
        board = [7, 1, 2, -1, 5, 4, 8, 6, 3]
        initial_puz = Puzzle(self.N, board, 0)
        print(initial_puz)

        state = input('Continue with initial state or input custom state (y/n)? ')
        board = []
        if state == 'n':
            print("input the start state of puzzle:")
            for i in range(self.N):
                puz = list(map(int, input().split()))
                board.extend(puz)

            initial_puz.board = board

        self.curr_puzzle = initial_puz
        return


    def move_house(self, num, action):
        board = self.curr_puzzle.board
        pos = board.index(num)
        if action == 'up' and pos - self.N >= 0:
            if board[pos - self.N] == -1:
                board[pos], board[pos - self.N] = board[pos - self.N], board[pos]
        elif action == 'down' and pos + self.N < len(board):
            if board[pos + self.N] == -1:
                board[pos], board[pos + self.N] = board[pos + self.N], board[pos]
        elif action == 'left' and pos - 1 >= 0:
            if board[pos - 1] == -1:
                board[pos], board[pos - 1] = board[pos - 1], board[pos]
        elif action == 'right' and pos + 1 < len(board):
            if board[pos + 1] == -1:
                board[pos], board[pos + 1] = board[pos + 1], board[pos]
        else:
            print('not valid!')

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

    def ida_star_search(self, root: Puzzle):

        bound = root.compute_f_value()

        info = [(root.compute_heuristic_manhattan(), root.level, bound)]
        path = [root]
        while True:
            l = self.search(path, bound, info)
            if l == 'Found':
                return path, info
            elif l == math.inf:
                return 'Not Found'
            bound = l

    def search(self, path, bound, info):
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
                info.append((h, suc.level, h+suc.level))

                t = self.search(path, bound, info)
                if t == 'Found':
                    return 'Found'
                if t < min_:
                    min_ = t

                path.pop(-1)
                info.pop(-1)

        return min_


# puzzle = [[1,2,3],[4,5,6],[7,8,-1]]
# print(puzzle[-1])
# print(puzzle)

b = [7, 1, 2, -1, 5, 4, 8, 6, 3]

# p = Puzzle(3, b, 0)
# print(p)
s = Solver(3)
s.initial_phase()

# actions = ['up', 'down', 'left', 'right']
# print(*actions)
