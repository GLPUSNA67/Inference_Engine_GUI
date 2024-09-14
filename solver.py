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
        def heuristic(state):
            return self.problem.heuristic(state) if hasattr(self.problem, 'heuristic') else 0

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
                    print(f"Solution found in {moves} moves and ")
                    print(f"{time.time() - start_time:.2f} seconds")
                    return path

                moves += 1
                if moves % 1000 == 0:
                    print(f"Explored {moves} moves, current state:\n{state}")

                for move in self.problem.get_possible_moves(state):
                    new_state = self.problem.apply_move(state, move)
                    if new_state not in visited:
                        new_cost = cost + 1
                        new_path = path + [move]
                        priority = new_cost + heuristic(new_state)
                        heapq.heappush(
                            frontier, (priority, new_cost, new_state, new_path))

            print(f"Search terminated after {moves} moves ")
            print(f"and {time.time() - start_time:.2f} seconds")
            return None

        return a_star(self.problem.get_initial_state())

    def print_solution(self, solution):
        if solution:
            print("\nSolution found:")
            current_state = self.problem.get_initial_state()
            for i, move in enumerate(solution):
                print(f"Step {i}:")
                print(self.problem.get_move_description(move))
                print("Before:", current_state)
                current_state = self.problem.apply_move(current_state, move)
                print("After:", current_state)
                print()
        else:
            print("No solution found within the given constraints.")
