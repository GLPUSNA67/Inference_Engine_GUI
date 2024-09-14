from base_classes import State, Problem
from typing import List, Tuple


class TowerOfHanoiState(State):
    def __init__(self, pegs: List[List[int]]):
        self.pegs = pegs

    def is_valid(self):
        return len(self.pegs) == 3 and all(peg == sorted(peg, reverse=True) for peg in self.pegs)

    def is_goal(self, goal_state):
        return self.pegs == goal_state.pegs

    def __eq__(self, other):
        return isinstance(other, TowerOfHanoiState) and self.pegs == other.pegs

    def __hash__(self):
        return hash(tuple(tuple(peg) for peg in self.pegs))

    def __lt__(self, other):
        return self.heuristic() < other.heuristic()

    def __str__(self):
        return " | ".join([f"Peg {i}: {peg}" for i, peg in enumerate(self.pegs)])

    def heuristic(self):
        # Count the number of disks not on the target peg
        return sum(len(peg) for peg in self.pegs[:-1])


class TowerOfHanoiProblem(Problem):
    def __init__(self, num_disks: int):
        self.num_disks = num_disks
        self._initial_state = TowerOfHanoiState(
            [list(range(num_disks, 0, -1)), [], []])
        self._goal_state = TowerOfHanoiState(
            [[], [], list(range(num_disks, 0, -1))])

    def get_initial_state(self):
        return self._initial_state

    def get_goal_state(self):
        return self._goal_state

    def get_possible_moves(self, state: TowerOfHanoiState) -> List[Tuple[int, int]]:
        moves = []
        for source in range(3):
            for destination in range(3):
                if source != destination and state.pegs[source]:
                    if not state.pegs[destination] or state.pegs[source][-1] < state.pegs[destination][-1]:
                        moves.append((source, destination))
        return moves

    def apply_move(self, state: TowerOfHanoiState, move: Tuple[int, int]) -> TowerOfHanoiState:
        source, destination = move
        new_pegs = [peg[:] for peg in state.pegs]
        disk = new_pegs[source].pop()
        new_pegs[destination].append(disk)
        return TowerOfHanoiState(new_pegs)

    def get_move_description(self, move: Tuple[int, int], state: TowerOfHanoiState) -> str:
        source, destination = move
        disk = state.pegs[source][-1]
        return f"Move disk {disk} from peg {source} to peg {destination}"

    def heuristic(self, state: TowerOfHanoiState) -> int:
        return state.heuristic()
