import heapq


class Puzzle:
    def __init__(self, n):
        self.N = n
        self.open_list = []
        self.closed_list = []

        # making open_list a priority Queue
        heapq.heapify(self.open_list)

    def input_puzzle(self):
        print("input the start state of puzzle like this pattern:")
        print("* * * ..."
              "* * * ..."
              "* * -1 ...")

        puzzle = []
        for i in range(self.N):
            puzz = list(map(int, input().split()))
            puzzle.append(puzz)

        return puzzle


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

    def blank_position(self, puzzle):
        pos = (0, 0)
        for i in range(self.N):
            for j in range(self.N):
                if puzzle[i][j] == -1:
                    pos = (i, j)
        return pos

# puzzle = [[1,2,3],[4,5,6],[7,8,-1]]

print()
