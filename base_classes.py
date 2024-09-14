from abc import ABC, abstractmethod


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

    @abstractmethod
    def heuristic(self, state):
        pass
