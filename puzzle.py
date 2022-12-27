
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

        str_ += "_"*13
        return str_



