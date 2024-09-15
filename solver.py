from base_classes import State, Problem
from collections import deque
import heapq
import time


class InferenceEngine:
    def __init__(self, problem, max_moves=10000, timeout=120):
        self.problem = problem
        self.max_moves = max_moves
        self.timeout = timeout

    def solve(self):
        def a_star(initial_state):
            start_time = time.time()
            frontier = [(0, 0, initial_state, [])]
            visited = set()
            moves = 0

            while frontier and moves < self.max_moves and (time.time() - start_time) < self.timeout:
                _, cost, state, path = heapq.heappop(frontier)

                if state in visited:
                    continue
                visited.add(state)

                if state.is_goal(self.problem.get_goal_state()):
                    return path, moves, time.time() - start_time

                moves += 1
                for move in self.problem.get_possible_moves(state):
                    new_state = self.problem.apply_move(state, move)
                    if new_state not in visited:
                        new_cost = cost + 1
                        new_path = path + [move]
                        priority = new_cost + self.problem.heuristic(new_state)
                        heapq.heappush(
                            frontier, (priority, new_cost, new_state, new_path))

            return None, moves, time.time() - start_time

        solution, moves_explored, time_taken = a_star(
            self.problem.get_initial_state())
        return solution, moves_explored, time_taken
