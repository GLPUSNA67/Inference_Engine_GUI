# Updated 9/15/2024
import tkinter as tk
from tkinter import ttk
import threading
from solver import InferenceEngine
from missionaries_cannibals import MCProblem
from blocks_world import BWProblem, BWState
from fifteen_puzzle import FifteenPuzzleProblem
from sliding_block_puzzle import SlidingBlockPuzzleProblem
from tower_of_hanoi import TowerOfHanoiProblem
from abc import ABC, abstractmethod
from main import *


class State(ABC):
    @abstractmethod
    def is_valid(self):
        pass

    @abstractmethod
    def is_goal(self, goal_state):
        pass

    @abstractmethod
    def __eq__(self, other):
        pass

    @abstractmethod
    def __hash__(self):
        pass


class Problem(ABC):
    @abstractmethod
    def get_initial_state(self):
        pass

    @abstractmethod
    def get_goal_state(self):
        pass

    @abstractmethod
    def get_possible_moves(self, state):
        pass

    @abstractmethod
    def apply_move(self, state, move):
        pass

    @abstractmethod
    def get_move_description(self, move):
        pass


class InferenceEngine:
    def __init__(self, problem):
        self.problem = problem

    def solve(self):
        def dfs(state, path, visited):
            if state.is_goal(self.problem.get_goal_state()):
                return path

            for move in self.problem.get_possible_moves(state):
                new_state = self.problem.apply_move(state, move)

                print("\nConsidering move:")
                print(self.problem.get_move_description(move, state))
                print("Current state: {}".format(state))
                print("Resulting state: {}".format(new_state))

                if not new_state.is_valid():
                    print("Move rejected: Invalid state")
                    continue

                if new_state in visited:
                    print("Move rejected: State already visited")
                    continue

                print("Move accepted: Valid state")
                visited.add(new_state)
                result = dfs(new_state, path + [move], visited)
                if result:
                    return result
                visited.remove(new_state)
                print("Backtracking from state:")
                print(str(new_state))

            return None

        initial_state = self.problem.get_initial_state()
        solution = dfs(initial_state, [], set())

        if solution:
            print("\nSolution found:")
            current_state = initial_state
            for i, move in enumerate(solution):
                print("Step {}:".format(i))
                print(self.problem.get_move_description(move, current_state))
                print("Before: {}".format(current_state))
                current_state = self.problem.apply_move(current_state, move)
                print("After:  {}".format(current_state))
                print()
        else:
            print("No solution found.")

        return solution


# Example usage
if __name__ == "__main__":
    from missionaries_cannibals import MCProblem
    from blocks_world import BWProblem, BWState

    # Solve Missionaries and Cannibals Problem
    mc_problem = MCProblem()
    mc_engine = InferenceEngine(mc_problem)
    mc_solution = mc_engine.solve()

    # Solve Blocks World Problem
    initial_state = BWState({'A': ['a', 'b', 'c'], 'B': [], 'C': []})
    goal_state = BWState({'A': ['a'], 'B': ['b'], 'C': ['c']})
    bw_problem = BWProblem(initial_state, goal_state)
    bw_engine = InferenceEngine(bw_problem)
    bw_solution = bw_engine.solve()
