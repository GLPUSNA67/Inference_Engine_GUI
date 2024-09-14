from inference_engine import InferenceEngine
from missionaries_cannibals import MCProblem
from blocks_world import BWProblem, BWState


def main():
    # Solve Missionaries and Cannibals Problem
    print("Solving Missionaries and Cannibals Problem:")
    mc_problem = MCProblem()
    mc_engine = InferenceEngine(mc_problem)
    mc_solution = mc_engine.solve()

    print("\n" + "="*50 + "\n")

    # Solve Blocks World Problem
    print("Solving Blocks World Problem:")
    initial_state = BWState({'A': ['a', 'b', 'c'], 'B': [], 'C': []})
    goal_state = BWState({'A': ['a'], 'B': ['b'], 'C': ['c']})
    bw_problem = BWProblem(initial_state, goal_state)
    bw_engine = InferenceEngine(bw_problem)
    bw_solution = bw_engine.solve()


if __name__ == "__main__":
    main()
