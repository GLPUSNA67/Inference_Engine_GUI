from base_classes import State, Problem
import random
# Updated 9/15/2024


class FifteenPuzzleState(State):
    def __init__(self, board):
        self.board = board
        self.size = 4

    def is_valid(self):
        return len(self.board) == self.size * self.size and set(self.board) == set(range(16))

    def is_goal(self, goal_state):
        return self.board == goal_state.board

    def __eq__(self, other):
        return isinstance(other, FifteenPuzzleState) and self.board == other.board

    def __hash__(self):
        return hash(tuple(self.board))

    def __lt__(self, other):
        return self.heuristic() < other.heuristic()

    def __str__(self):
        return '\n'.join([' '.join(f'{self.board[i*4 + j]:2d}' for j in range(4)) for i in range(4)])

    def get_tile_position(self, tile):
        index = self.board.index(tile)
        return (index // 4, index % 4)

    def heuristic(self):
        distance = 0
        for i in range(16):
            if i == 0:
                continue
            current_row, current_col = self.get_tile_position(i)
            goal_row, goal_col = divmod(i - 1, 4)
            distance += abs(current_row - goal_row) + \
                abs(current_col - goal_col)
        return distance

    def manhattan_distance(self):
        distance = 0
        for i in range(16):
            if i == 0:
                continue
            current_row, current_col = self.get_tile_position(i)
            goal_row, goal_col = divmod(i - 1, 4)
            distance += abs(current_row - goal_row) + \
                abs(current_col - goal_col)
        return distance

    def linear_conflicts(self):
        conflicts = 0
        for row in range(4):
            conflicts += self._count_conflicts_in_row(row)
        for col in range(4):
            conflicts += self._count_conflicts_in_column(col)
        return conflicts * 2

    def _count_conflicts_in_row(self, row):
        conflicts = 0
        tiles_in_row = [self.board[row * 4 + i]
                        for i in range(4) if self.board[row * 4 + i] != 0]
        for i in range(len(tiles_in_row)):
            for j in range(i + 1, len(tiles_in_row)):
                if tiles_in_row[i] > tiles_in_row[j] and (tiles_in_row[i] - 1) // 4 == row and (tiles_in_row[j] - 1) // 4 == row:
                    conflicts += 1
        return conflicts

    def _count_conflicts_in_column(self, col):
        conflicts = 0
        tiles_in_col = [self.board[col + 4 * i]
                        for i in range(4) if self.board[col + 4 * i] != 0]
        for i in range(len(tiles_in_col)):
            for j in range(i + 1, len(tiles_in_col)):
                if tiles_in_col[i] > tiles_in_col[j] and (tiles_in_col[i] - 1) % 4 == col and (tiles_in_col[j] - 1) % 4 == col:
                    conflicts += 1
        return conflicts

    def heuristic(self):
        return self.manhattan_distance() + self.linear_conflicts()


class FifteenPuzzleProblem(Problem):
    def __init__(self):
        self._goal_state = FifteenPuzzleState(list(range(16)))
        self._initial_state = self._generate_solvable_state()
        print(f"Initial state:\n{self._initial_state}")
        print(f"Goal state:\n{self._goal_state}")

    def _generate_solvable_state(self):
        goal_board = list(range(16))
        num_moves = 10  # Reduced number of random moves
        current_state = FifteenPuzzleState(goal_board[:])
        for i in range(num_moves):
            moves = self.get_possible_moves(current_state)
            move = random.choice(moves)
            current_state = self.apply_move(current_state, move)
            print(
                f"Move {i + 1}: {self.get_move_description(move, current_state)}")
            print(f"State after move:\n{current_state}\n")
        return current_state

    def get_initial_state(self):
        return self._initial_state

    def get_goal_state(self):
        return self._goal_state

    def get_possible_moves(self, state):
        moves = []
        blank_index = state.board.index(0)
        row, col = divmod(blank_index, 4)

        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < 4 and 0 <= new_col < 4:
                moves.append(new_row * 4 + new_col)

        return moves

    def apply_move(self, state, move):
        new_board = state.board[:]
        blank_index = new_board.index(0)
        new_board[blank_index], new_board[move] = new_board[move], new_board[blank_index]
        return FifteenPuzzleState(new_board)

    def get_move_description(self, move, state):
        return f"Move tile {state.board[move]} to empty space"

    def heuristic(self, state):
        return state.heuristic()
