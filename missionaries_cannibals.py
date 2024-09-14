from base_classes import State, Problem


class MCState(State):
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

    def is_goal(self, goal_state):
        return self.left_m == 0 and self.left_c == 0

    def __eq__(self, other):
        if not isinstance(other, MCState):
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

    def __lt__(self, other):
        # Compare based on the number of missionaries and cannibals on the left bank
        return (self.left_m + self.left_c) < (other.left_m + other.left_c)


class MCProblem(Problem):
    def __init__(self):
        self._initial_state = MCState(3, 3, True)
        self._goal_state = MCState(0, 0, False)
        self.moves = [(1, 0), (2, 0), (0, 1), (0, 2), (1, 1)]

    def get_initial_state(self):
        return self._initial_state

    def get_goal_state(self):
        return self._goal_state

    def get_possible_moves(self, state):
        possible_moves = []
        for m, c in self.moves:
            if state.boat_left:
                if m <= state.left_m and c <= state.left_c:
                    possible_moves.append((m, c, True))
            else:
                if m <= state.right_m and c <= state.right_c:
                    possible_moves.append((m, c, False))
        return possible_moves

    def apply_move(self, state, move):
        m, c, from_left = move
        if from_left:
            return MCState(state.left_m - m, state.left_c - c, False)
        else:
            return MCState(state.left_m + m, state.left_c + c, True)

    def get_move_description(self, move, state=None):
        m, c, from_left = move
        direction = "from left to right" if from_left else "from right to left"
        return "{}M {}C {}".format(m, c, direction)

    def heuristic(self, state):
        # Simple heuristic: number of people on the left bank
        return state.left_m + state.left_c

    def is_mc_problem(self):
        return True
