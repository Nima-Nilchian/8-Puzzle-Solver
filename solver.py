import heapq
import random

from search import *

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
            print()
            self.initial_phase()

        stat = input('Play with the Algorithm or User (a/u)? ')
        if stat == 'a':
            self.process()
        elif stat == 'u':
            self.user_move()

    def process(self):
        puzzle = self.curr_puzzle
        path, info = ida_star_search(puzzle)

        for i in range(len(path)):
            print(path[i])
            Solver.print_info(info[i])

        return

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
        print('initial random state is:')
        # board = [7, 1, 2, -1, 5, 4, 8, 6, 3]
        board = self.random_initiation()
        initial_puz = Puzzle(self.N, board, 0)
        print(initial_puz)

        state = input('Continue with random state or input custom state (y/n)? ')
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

    def random_initiation(self):
        size = self.N * self.N
        pop = list(range(1, size))
        pop.append(-1)
        rnd_board = random.sample(pop, size)

        return rnd_board

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

    @staticmethod
    def print_info(info):
        print('*-^' * 5)
        print('h value: ', info[0])
        print('g value: ', info[1])
        print('f value: ', info[2])
        print('*-^' * 5)
        print()

