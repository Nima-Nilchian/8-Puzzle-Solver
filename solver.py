import heapq
import random

from search import *

class Solver:
    initial_puzzle = None
    curr_puzzle = None

    def __init__(self, n):
        self.N = n
        self.initial_phase()

    def initial_phase(self):
        self.input_board()                          # input random initial board or custom board

        solvable = self.solvable(self.curr_puzzle)  # Check if the puzzle is Solvable
        if solvable is False:
            print('puzzle is not solvable!')
            print()
            self.initial_phase()                    # if not solvable repeat again
        else:
            print('Puzzle is Solvable')
            Puzzle.goal_board(self.N)               # create the goal puzzle board

            stat = input('Play with the Algorithm or User or Race (a/u/r)? ')
            if stat == 'a':                         # Two options (ida* or rbfs)
                self.process()
            elif stat == 'u':                       # user can move houses and finish the game
                self.user_move()
            elif stat == 'r':                       # race between user and algorithm
                self.race()

        return

    def process(self, alg=None):
        puzzle = self.curr_puzzle

        if alg is None:
            alg = input('solve with witch algorithm (ida*, rbfs)? ')

        if alg == 'rbfs':
            res = recursive_best_first_search(puzzle)
            print(res[0])
            Solver.print_info(res[1])
        else:
            path, info, mins = ida_star_search(puzzle)
            mins = set(mins)
            print()
            print('min out of fringes in order:', mins)
            print('steps in last bound on optimal path: ')
            for i in range(len(path)):
                print(path[i])
                Solver.print_info(info[i])

        status = input('Finish / Restart the Game (f/r)? ')
        if status == 'f':
            return
        elif status == 'r':
            self.initial_phase()


    def user_move(self):
        puz = self.curr_puzzle
        print(puz)

        print('Choose house number and the action to perform on it (up, down, left, right)')
        num = int(input('house: '))
        action = input('action: ')

        # Move house with given action and create new puzzle
        new_board = self.move_house(num, action)
        new_puzzle = Puzzle(self.N, new_board, level=puz.level + 1)
        self.curr_puzzle = new_puzzle

        # Finish the game if its goal
        if new_board == new_puzzle.goal:
            print(new_puzzle)
            print()
            print('YAY!! You Found the Goal!\n')
            return True

        # decide the next action
        status = input('Continue / Finish / Restart the Game? (c/f/r)')
        if status == 'f':
            return
        if status == 'r':
            self.initial_phase()
        else:
            self.user_move()

        return False

    def race(self):
        self.user_move()                                # will return if user finished the game
        user_level = self.curr_puzzle.level

        initial_board = self.initial_puzzle.board       # reset to the initial board game
        self.curr_puzzle = Puzzle(self.N, initial_board, 0)
        self.process('ida*')                            # algorithm will start to solve the puzzle again
        alg_level = self.curr_puzzle.level

        if user_level < alg_level:
            print("User wins the game")
        elif alg_level < user_level:
            print('Algorithm wins the game')
        else:
            print('game is equal ( both wins :) )')

        return

    def input_board(self):
        print('initial random state is:')
        board = self.random_initiation()                # Random initiation of the puzzle board
        initial_puz = Puzzle(self.N, board, 0)
        print(initial_puz)

        state = input('Continue with random state or input custom state (y/n)? ')
        board = []
        if state == 'n':                                # custom initiation of puzzle board
            print("input the start state of puzzle:")
            for i in range(self.N):
                puz = list(map(int, input().split()))
                board.extend(puz)

            initial_puz.board = board

        # set the current_puzzle and initial_puzzle to this first puzzle
        self.curr_puzzle = initial_puz
        second = initial_puz.board.copy()
        self.initial_puzzle = Puzzle(self.N, second, 0)

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
        population = list(range(1, size))
        population.append(-1)
        rnd_board = random.sample(population, size)

        return rnd_board

    def solvable(self, puzzle: Puzzle):
        inversions = self.count_inversions(puzzle)

        # if N is odd --> Number of inversions should be even
        if self.N % 2 == 1:
            if inversions % 2 == 0:
                return True
        else:
            pos = puzzle.blank_position()
            pos = self.N - pos

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
        print('*' * 13)
        print('h value: ', info[0])
        print('g value: ', info[1])
        print('f value: ', info[2])
        print('bound: ', info[3])
        # print('min', info[4])
        print('*' * 13)
        print()

