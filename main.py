import heapq

class Solver:
    def __init__(self):
        return


class Puzzle:
    def __init__(self, n):
        self.N = n
        self.board = [7, 1, 2, -1, 5, 4, 8, 6, 3]      # Default initial board state

        self.open_list = []
        self.closed_list = []
        # making open_list a priority Queue
        heapq.heapify(self.open_list)


    def generate_children(self):
        actions, blank_pos = self.legal_actions()

        children = []
        for action in actions:
            new_board = self.generate_new_board(action)
            children.append(new_board)

        return children

    def move_blank(self):
        actions, blank_pos = self.legal_actions()

        print('You can move in these directions: (', end=' ')
        print(*actions, end=')')
        print()
        action = input('Please choose one: ')

        new_board = self.generate_new_board(action)
        self.board = new_board


    def legal_actions(self):
        blank_pos = self.blank_position()
        row, col = blank_pos / self.N, blank_pos % self.N

        actions = ['up', 'down', 'left', 'right']
        if row == 0:
            actions.remove('up')
        if row == self.N:
            actions.remove('down')
        if col == 0:
            actions.remove('left')
        if col == self.N:
            actions.remove('right')

        return actions, blank_pos


    def generate_new_board(self, action):
        actions, blank_pos = self.legal_actions()

        new_board = self.board.copy()
        if action == 'up':
            new_board[blank_pos], new_board[blank_pos - self.N] = new_board[blank_pos - self.N], new_board[blank_pos]
        if action == 'down':
            new_board[blank_pos], new_board[blank_pos + self.N] = new_board[blank_pos + self.N], new_board[blank_pos]
        if action == 'left':
            new_board[blank_pos], new_board[blank_pos - 1] = new_board[blank_pos - 1], new_board[blank_pos]
        if action == 'right':
            new_board[blank_pos], new_board[blank_pos + 1] = new_board[blank_pos + 1], new_board[blank_pos]

        return new_board

    def input_puzzle(self):
        print("input the start state of puzzle like this pattern:")
        print("* * * ..."
              "* * * ..."
              "* * -1 ...")

        puzzle = []
        for i in range(self.N):
            puzz = list(map(int, input().split()))
            puzzle.extend(puzz)

        self.board = puzzle

        return

    def solvable(self, puzzle):
        inversions = self.count_inversions(puzzle)

        # if N is odd --> Number of inversions should be even
        if self.N % 2 == 1:
            if inversions % 2 == 0:
                return True
        else:
            pos = self.blank_position(puzzle)
            pos = self.N - pos[0]

            # the blank is on an even row counting from the bottom and number of inversions is odd
            if pos % 2 == 0 and inversions % 2 == 1:
                return True
            # the blank is on an odd row counting from the bottom and number of inversions is even
            elif pos % 2 == 1 and inversions % 2 == 0:
                return True

        return False

    def count_inversions(self, puzzle):
        d1_puzz = []
        [d1_puzz.extend(puzzle[i]) for i in range(len(puzzle))]

        inv = 0
        dims = self.N * self.N

        for i in range(dims - 1):
            if d1_puzz[i] == -1:
                continue

            for j in range(i+1, dims):
                if d1_puzz[j] != -1 and d1_puzz[i] > d1_puzz[j]:
                    inv += 1
        return inv

    def blank_position(self):
        pos = 0
        for i in range(self.N * self.N):
            if self.board[i] == -1:
                return pos

        return pos

# puzzle = [[1,2,3],[4,5,6],[7,8,-1]]


# actions = ['up', 'down', 'left', 'right']
# print(*actions)
