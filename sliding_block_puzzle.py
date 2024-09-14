from base_classes import State, Problem
import random


class SlidingBlockPuzzleState(State):
    def __init__(self, board, width, height):
        self.board = board
        self.width = width
        self.height = height

    def is_valid(self):
        return len(self.board) == self.width * self.height and set(self.board) == set(range(self.width * self.height))

    def is_goal(self, goal_state):
        return self.board == goal_state.board

    def __eq__(self, other):
        return isinstance(other, SlidingBlockPuzzleState) and self.board == other.board

    def __hash__(self):
        return hash(tuple(self.board))

    def __lt__(self, other):
        return self.heuristic() < other.heuristic()

    def __str__(self):
        return '\n'.join([' '.join(f'{self.board[i*self.width + j]:2d}' for j in range(self.width)) for i in range(self.height)])

    def get_tile_position(self, tile):
        index = self.board.index(tile)
        return (index // self.width, index % self.width)

    def heuristic(self):
        distance = 0
        for i in range(self.width * self.height):
            if i == 0:
                continue
            current_row, current_col = self.get_tile_position(i)
            goal_row, goal_col = divmod(i - 1, self.width)
            distance += abs(current_row - goal_row) + \
                abs(current_col - goal_col)
        return distance


class SlidingBlockPuzzleProblem(Problem):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self._goal_state = SlidingBlockPuzzleState(
            list(range(width * height)), width, height)
        self._initial_state = self._generate_solvable_state()
        print(f"Initial state:\n{self._initial_state}")
        print(f"Goal state:\n{self._goal_state}")

    def _generate_solvable_state(self):
        goal_board = list(range(self.width * self.height))
        num_moves = 20  # Reduced number of random moves
        current_state = SlidingBlockPuzzleState(
            goal_board[:], self.width, self.height)
        for i in range(num_moves):
            moves = self.get_possible_moves(current_state)
            move = random.choice(moves)
            current_state = self.apply_move(current_state, move)
            print(
                f"Move {i + 1}: {self.get_move_description(move, current_state)}")
            print(f"State after move:\n{current_state}\n")
        return current_state

    def _is_solvable(self, board):
        inversions = sum(1 for i in range(len(board)) for j in range(
            i + 1, len(board)) if board[i] and board[j] and board[i] > board[j])
        blank_row = board.index(0) // self.width
        if self.width % 2 == 1:
            return inversions % 2 == 0
        else:
            return (inversions % 2 == 0) == (blank_row % 2 == 1)

    def get_initial_state(self):
        return self._initial_state

    def get_goal_state(self):
        return self._goal_state

    def get_possible_moves(self, state):
        moves = []
        blank_index = state.board.index(0)
        row, col = divmod(blank_index, self.width)

        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < self.height and 0 <= new_col < self.width:
                moves.append(new_row * self.width + new_col)

        return moves

    def apply_move(self, state, move):
        new_board = state.board[:]
        blank_index = new_board.index(0)
        new_board[blank_index], new_board[move] = new_board[move], new_board[blank_index]
        return SlidingBlockPuzzleState(new_board, self.width, self.height)

    def get_move_description(self, move, state):
        return f"Move tile {state.board[move]} to empty space"

    def heuristic(self, state):
        return state.heuristic()
