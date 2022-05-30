""" Sokoban Solver """
from typing import List, Tuple, Optional, Dict
from . import Sokoban, State
from .exceptions import *


class Solver:
    """
    Collection of methods to solve Sokoban
    """
    def __init__(self, initial_state: Sokoban):
        self.sokoban = sokoban

    def successors(self, state: State) -> List[Tuple[str, State]]:
        """
        renvoie les successeurs d'un état
        """
        return [
            (
                action,
                state.__copy__()
            )
            for action in self.sokoban.actions
            if self.sokoban.actions[action]()
        ]

    def solve(self, algorithm='bfs'):
        """
        solve the puzzle
        """
        if algorithm in self.solving_algorithms:
            return self.solving_algorithms[algorithm]()
        else:
            raise NotRecognizedAlgorithmException(
                f"Algorithme inconnu: {algorithm}\n"
                +
                ErrorHelpStrings.NOT_RECOGNIZED_ALGORITHM_HELP
            )

    def solve_bfs(self):
        """
        solve the puzzle using breadth-first search
        """
        queue = [self.current_state]
        while queue:
            state = queue.pop(0)
            if state.is_valid():
                return state
            else:
                queue.extend(state.successors())
        return None


    def reconstruct_path(self, state: State, precedents: Dict[State, Optional[Tuple[State, str]]]) -> str:
        """
        reconstruct the path from a state to the initial state
        """
        path = ""
        s = state
        while precedents[s]:
            path += precedents[s][1]
            s = precedents[s][0]
        return path[::-1]