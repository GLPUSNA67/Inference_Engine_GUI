import tkinter as tk
from tkinter import ttk
import threading
from solver import InferenceEngine
from missionaries_cannibals import MCProblem
from blocks_world import BWProblem, BWState
from fifteen_puzzle import FifteenPuzzleProblem
from sliding_block_puzzle import SlidingBlockPuzzleProblem
from tower_of_hanoi import TowerOfHanoiProblem


class SolverGUI:
    def __init__(self, master):
        self.master = master
        master.title("Problem Solver")

        self.problem_var = tk.StringVar(value="Missionaries and Cannibals")
        self.problem_dropdown = ttk.Combobox(master, textvariable=self.problem_var,
                                             values=["Missionaries and Cannibals", "Blocks World",
                                                     "15 Puzzle", "Sliding Block Puzzle", "Tower of Hanoi"])
        self.problem_dropdown.grid(row=0, column=0, padx=5, pady=5)
        self.problem_dropdown.bind(
            "<<ComboboxSelected>>", self.on_problem_select)

        self.solve_button = tk.Button(
            master, text="Solve", command=self.start_solve_thread)
        self.solve_button.grid(row=0, column=1, padx=5, pady=5)

        self.clear_button = tk.Button(
            master, text="Clear", command=self.clear_output)
        self.clear_button.grid(row=0, column=2, padx=5, pady=5)

        self.copy_button = tk.Button(
            master, text="Copy", command=self.copy_output)
        self.copy_button.grid(row=0, column=3, padx=5, pady=5)

        self.step_button = tk.Button(
            master, text="Next Step", command=self.show_next_step, state=tk.DISABLED)
        self.step_button.grid(row=1, column=0, padx=5, pady=5)

        self.reset_button = tk.Button(
            master, text="Reset", command=self.reset_solution, state=tk.DISABLED)
        self.reset_button.grid(row=1, column=1, padx=5, pady=5)

        self.width_label = tk.Label(master, text="Width:")
        self.width_entry = tk.Entry(master, width=5)
        self.width_entry.insert(0, "3")  # Default width
        self.height_label = tk.Label(master, text="Height:")
        self.height_entry = tk.Entry(master, width=5)
        self.height_entry.insert(0, "3")  # Default height

        self.num_disks_label = tk.Label(master, text="Number of Disks:")
        self.num_disks_entry = tk.Entry(master, width=5)
        self.num_disks_entry.insert(0, "3")  # Default number of disks

        self.output_text = tk.Text(master, wrap=tk.WORD, width=60, height=20)
        self.output_text.grid(row=2, column=0, columnspan=4, padx=5, pady=5)

        self.scrollbar = tk.Scrollbar(master, command=self.output_text.yview)
        self.scrollbar.grid(row=2, column=4, sticky='nsew')
        self.output_text['yscrollcommand'] = self.scrollbar.set

        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            master, variable=self.progress_var, maximum=100)
        self.progress_bar.grid(
            row=3, column=0, columnspan=4, sticky='ew', padx=5, pady=5)

        self.solution = None
        self.current_step = 0
        self.problem = None

    def on_problem_select(self, event):
        problem = self.problem_var.get()
        self.width_label.grid_remove()
        self.width_entry.grid_remove()
        self.height_label.grid_remove()
        self.height_entry.grid_remove()
        self.num_disks_label.grid_remove()
        self.num_disks_entry.grid_remove()

        if problem == "Sliding Block Puzzle":
            self.width_label.grid(row=1, column=2)
            self.width_entry.grid(row=1, column=3)
            self.height_label.grid(row=1, column=4)
            self.height_entry.grid(row=1, column=5)
        elif problem == "Tower of Hanoi":
            self.num_disks_label.grid(row=1, column=2)
            self.num_disks_entry.grid(row=1, column=3)

    def start_solve_thread(self):
        self.solve_button.config(state=tk.DISABLED)
        self.output_text.delete(1.0, tk.END)
        self.progress_var.set(0)
        threading.Thread(target=self.solve_problem, daemon=True).start()

    def solve_problem(self):
        problem_type = self.problem_var.get()
        self.output_text.delete(1.0, tk.END)

        try:
            if problem_type == "Missionaries and Cannibals":
                self.problem = MCProblem()
            elif problem_type == "Blocks World":
                initial_state = BWState(
                    {'A': ['a', 'b', 'c'], 'B': [], 'C': []})
                goal_state = BWState({'A': ['a'], 'B': ['b'], 'C': ['c']})
                self.problem = BWProblem(initial_state, goal_state)
            elif problem_type == "15 Puzzle":
                self.problem = FifteenPuzzleProblem()
            elif problem_type == "Sliding Block Puzzle":
                try:
                    width = int(self.width_entry.get() or "3")
                    height = int(self.height_entry.get() or "3")
                    self.problem = SlidingBlockPuzzleProblem(width, height)
                except ValueError:
                    raise ValueError(
                        "Invalid width or height. Please enter positive integers.")
            elif problem_type == "Tower of Hanoi":
                num_disks = int(self.num_disks_entry.get() or "3")
                self.problem = TowerOfHanoiProblem(num_disks)
            else:
                raise ValueError("Invalid problem type selected.")

            engine = InferenceEngine(self.problem)
            self.solution, moves_explored, time_taken = engine.solve()

            if self.solution:
                t_out = f"Solution found in {moves_explored} moves and "
                t_out = t_out + f"{time_taken:.2f} seconds.\n\n"
                is_out = f"Initial state:\n{self.problem.get_initial_state()}"
                is_out = is_out + f"\n\n"
                self.output_text.insert(tk.END, t_out)
                self.output_text.insert(tk.END, is_out)
                self.step_button.config(state=tk.NORMAL)
                self.reset_button.config(state=tk.NORMAL)
                self.current_step = 0
            else:
                self.output_text.insert(
                    tk.END, "No solution found within the given constraints.")

        except Exception as e:
            self.output_text.insert(tk.END, f"An error occurred: {str(e)}")

        self.solve_button.config(state=tk.NORMAL)

    def show_next_step(self):
        if self.solution and self.current_step < len(self.solution):
            move = self.solution[self.current_step]
            current_state = self.problem.get_initial_state()
            for i in range(self.current_step):
                current_state = self.problem.apply_move(
                    current_state, self.solution[i])

            self.output_text.insert(tk.END, f"Step {self.current_step + 1}:\n")
            self.output_text.insert(
                tk.END, self.problem.get_move_description(move, current_state) + "\n")
            new_state = self.problem.apply_move(current_state, move)
            self.output_text.insert(tk.END, f"After move:\n{new_state}\n\n")

            self.current_step += 1

            if self.current_step == len(self.solution):
                self.step_button.config(state=tk.DISABLED)
                self.output_text.insert(tk.END, "Solution complete!\n")

        self.output_text.see(tk.END)

    def reset_solution(self):
        self.current_step = 0
        self.output_text.delete(1.0, tk.END)
        is_out = f"Initial state:\n{self.problem.get_initial_state()}"
        is_out = is_out + f"\n\n"
        self.output_text.insert(tk.END, is_out)
        self.step_button.config(state=tk.NORMAL)

    def clear_output(self):
        self.output_text.delete(1.0, tk.END)

    def copy_output(self):
        self.master.clipboard_clear()
        self.master.clipboard_append(self.output_text.get(1.0, tk.END))


def main():
    root = tk.Tk()
    gui = SolverGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
