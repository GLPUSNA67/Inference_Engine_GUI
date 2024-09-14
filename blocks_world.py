from base_classes import State, Problem


class BWState(State):
    def __init__(self, pegs):
        self.pegs = pegs

    def is_valid(self):
        return len(self.pegs) == 3 and all(isinstance(peg, list) for peg in self.pegs.values())

    def is_goal(self, goal_state):
        return self.pegs == goal_state.pegs

    def __eq__(self, other):
        return isinstance(other, BWState) and self.pegs == other.pegs

    def __hash__(self):
        return hash(tuple(tuple(peg) for peg in self.pegs.values()))

    def __str__(self):
        return " | ".join([f"{k}: {v}" for k, v in self.pegs.items()])


class BWProblem(Problem):
    def __init__(self, initial_state, goal_state):
        self._initial_state = initial_state
        self._goal_state = goal_state

    def get_initial_state(self):
        return self._initial_state

    def get_goal_state(self):
        return self._goal_state

    def get_possible_moves(self, state):
        moves = []
        for source in state.pegs:
            if state.pegs[source]:
                for destination in state.pegs:
                    if source != destination:
                        moves.append((source, destination))
        return moves

    def apply_move(self, state, move):
        source, destination = move
        new_pegs = {k: v[:] for k, v in state.pegs.items()}
        block = new_pegs[source].pop()
        new_pegs[destination].append(block)
        return BWState(new_pegs)

    def get_move_description(self, move, state):
        source, destination = move
        return f"Move top block from {source} to {destination}"

    def heuristic(self, state):
        misplaced = 0
        for peg in self._goal_state.pegs:
            for i, block in enumerate(self._goal_state.pegs[peg]):
                if i >= len(state.pegs[peg]) or state.pegs[peg][i] != block:
                    misplaced += 1
        return misplaced
