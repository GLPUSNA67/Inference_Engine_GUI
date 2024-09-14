# Simple Inference Engine

from collections import deque


class State:
    def __init__(self, left_m, left_c, boat_left):
        self.left_m = max(0, min(3, left_m))
        self.left_c = max(0, min(3, left_c))
        self.boat_left = boat_left
        self.right_m = 3 - self.left_m
        self.right_c = 3 - self.left_c

    def is_valid(self):
        if self.left_m < 0 or self.left_c < 0 or self.right_m < 0 or self.right_c < 0:
            return False
        if (self.left_m < self.left_c and self.left_m > 0) or \
           (self.right_m < self.right_c and self.right_m > 0):
            return False
        return True

    def is_goal(self):
        return self.left_m == 0 and self.left_c == 0

    def __eq__(self, other):
        if other is None:
            return False
        return self.left_m == other.left_m and self.left_c == other.left_c and \
            self.boat_left == other.boat_left

    def __hash__(self):
        return hash((self.left_m, self.left_c, self.boat_left))

    def __str__(self):
        left_bank = "M" * self.left_m + "C" * self.left_c
        right_bank = "M" * self.right_m + "C" * self.right_c
        boat = "<" if self.boat_left else ">"
        return "({0}){1}~~~{2}({3})".format(
            left_bank.ljust(6),
            boat if self.boat_left else " ",
            " " if self.boat_left else boat,
            right_bank.ljust(6)
        )


class InferenceEngine:
    def __init__(self):
        self.initial_state = State(3, 3, True)
        self.moves = [(1, 0), (2, 0), (0, 1), (0, 2), (1, 1)]

    def get_possible_moves(self, state):
        possible_moves = []
        for m, c in self.moves:
            if state.boat_left:
                if m <= state.left_m and c <= state.left_c:
                    possible_moves.append((m, c))
            else:
                if m <= state.right_m and c <= state.right_c:
                    possible_moves.append((m, c))
        return possible_moves

    def apply_move(self, state, move):
        m, c = move
        if state.boat_left:
            return State(state.left_m - m, state.left_c - c, False)
        else:
            return State(state.left_m + m, state.left_c + c, True)

    def remove_redundant_steps(self, solution):
        i = 0
        while i < len(solution) - 1:
            if solution[i] == (solution[i+1][1], solution[i+1][0]):
                solution.pop(i)
                solution.pop(i)
            else:
                i += 1
        return solution

    def solve(self):
        def dfs(state, path, visited):
            if state.is_goal():
                return [path]

            solutions = []
            for move in self.get_possible_moves(state):
                new_state = self.apply_move(state, move)
                if not new_state.is_valid() or new_state in visited:
                    continue
                visited.add(new_state)
                result = dfs(new_state, path + [move], visited)
                if result:
                    solutions.extend(result)
                visited.remove(new_state)

            return solutions

        all_solutions = dfs(self.initial_state, [], set())

        if all_solutions:
            print(f"\nFound {len(all_solutions)} solutions:")
            for i, solution in enumerate(all_solutions):
                print(f"\nSolution {i + 1}:")
                # Print the steps of this solution
        else:
            print("No solution found.")


# Run the solver
engine = InferenceEngine()
engine.solve()
