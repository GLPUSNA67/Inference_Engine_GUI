from abc import ABC, abstractmethod
# Updated 9/15/2024


class Problem(ABC):
    @abstractmethod
    def get_initial_state(self):
        pass

    @abstractmethod
    def is_goal_state(self, state):
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
