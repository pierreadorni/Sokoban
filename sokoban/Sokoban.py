""" Classe Sokoban """
from typing import Tuple, List, Union, Dict, Optional

from .State import State
from .exceptions import *


class Sokoban:
    """
    classe de représentation d'un jeu de Sokoban.
    Doit être initialisée avec un objet State.
    """

    def __init__(self, initial_state: State):
        self.states = [initial_state]

        self.actions = {
            'g': self.aller_a_gauche,
            'G': self.pousser_a_gauche,
            'd': self.aller_a_droite,
            'D': self.pousser_a_droite,
            'h': self.aller_en_haut,
            'H': self.pousser_en_haut,
            'b': self.aller_en_bas,
            'B': self.pousser_en_bas
        }

        self. solving_algorithms = {
            'bfs': self.solve_bfs,
        }

    @property
    def current_state(self) -> State:
        """
        retourne l'état courant
        """
        return self.states[-1]

    def rollback(self) -> bool:
        """
        retourne à l'état précédent s'il existe
        """
        if self.states[-1] == self.states[0]:
            return False
        self.states.pop()
        return True

    def reset(self) -> None:
        """
        remet le jeu à l'état initial
        """
        self.states = [self.states[0]]

    def aller_a_gauche(self):
        """
        déplace le personnage d'une case à gauche si possible
        """
        x = self.current_state.personnage_pos[0]
        y = self.current_state.personnage_pos[1]
        if self.current_state.mur(x - 1, y) or \
                self.current_state.caisse(x - 1, y) or not \
                self.current_state.personnage(x, y):
            return False

        new_state = self.current_state.__copy__()
        new_state.personnage_pos = (x - 1, y)
        self.states.append(new_state)
        return True

    def aller_a_droite(self) -> bool:
        """
        déplace le personnage d'une case à droite si possible
        """
        x = self.current_state.personnage_pos[0]
        y = self.current_state.personnage_pos[1]
        if self.current_state.mur(x + 1, y) or \
                self.current_state.caisse(x + 1, y) or \
                not self.current_state.personnage(x, y):
            return False

        new_state = self.current_state.__copy__()
        new_state.personnage_pos = (x + 1, y)
        self.states.append(new_state)
        return True

    def aller_en_haut(self) -> bool:
        """
        déplace le personnage d'une case en haut si possible
        """
        x = self.current_state.personnage_pos[0]
        y = self.current_state.personnage_pos[1]
        if self.current_state.mur(x, y - 1) \
                or self.current_state.caisse(x, y - 1) \
                or not self.current_state.personnage(x, y):
            return False

        new_state = self.current_state.__copy__()
        new_state.personnage_pos = (x, y - 1)
        self.states.append(new_state)
        return True

    def aller_en_bas(self) -> bool:
        """
        déplace le personnage d'une case en bas si possible
        """
        x = self.current_state.personnage_pos[0]
        y = self.current_state.personnage_pos[1]
        if self.current_state.mur(x, y + 1) \
                or self.current_state.caisse(x, y + 1) \
                or not self.current_state.personnage(x, y):
            return False

        new_state = self.current_state.__copy__()
        new_state.personnage_pos = (x, y + 1)
        self.states.append(new_state)
        return True

    def pousser_a_gauche(self) -> bool:
        """
        pousse la caisse d'une case à gauche si possible
        """
        x = self.current_state.personnage_pos[0]
        y = self.current_state.personnage_pos[1]
        if self.current_state.mur(x - 1, y) \
                or not self.current_state.caisse(x - 1, y) \
                or self.current_state.mur(x - 2, y) \
                or self.current_state.caisse(x - 2, y) \
                or not self.current_state.personnage(x, y):
            return False

        new_state = self.current_state.__copy__()
        new_state.caisses.remove((x - 1, y))
        new_state.caisses.append((x - 2, y))
        new_state.personnage_pos = (x - 1, y)
        self.states.append(new_state)
        return True

    def pousser_a_droite(self) -> bool:
        """
        pousse la caisse d'une case à droite si possible
        """
        x = self.current_state.personnage_pos[0]
        y = self.current_state.personnage_pos[1]
        if self.current_state.mur(x + 1, y) \
                or not self.current_state.caisse(x + 1, y) \
                or self.current_state.mur(x + 2, y) \
                or self.current_state.caisse(x + 2, y) \
                or not self.current_state.personnage(x, y):
            return False

        new_state = self.current_state.__copy__()
        new_state.caisses.remove((x + 1, y))
        new_state.caisses.append((x + 2, y))
        new_state.personnage_pos = (x + 1, y)
        self.states.append(new_state)
        return True

    def pousser_en_haut(self) -> bool:
        """
        pousse la caisse d'une case en haut si possible
        """
        x = self.current_state.personnage_pos[0]
        y = self.current_state.personnage_pos[1]
        if self.current_state.mur(x, y - 1) \
                or not self.current_state.caisse(x, y - 1) \
                or self.current_state.mur(x, y - 2) \
                or self.current_state.caisse(x, y - 2) \
                or not self.current_state.personnage(x, y):
            return False

        new_state = self.current_state.__copy__()
        new_state.caisses.remove((x, y - 1))
        new_state.caisses.append((x, y - 2))
        new_state.personnage_pos = (x, y - 1)
        self.states.append(new_state)
        return True

    def pousser_en_bas(self) -> bool:
        """
        pousse la caisse d'une case en bas si possible
        """
        x = self.current_state.personnage_pos[0]
        y = self.current_state.personnage_pos[1]
        if self.current_state.mur(x, y + 1) \
                or not self.current_state.caisse(x, y + 1) \
                or self.current_state.mur(x, y + 2) \
                or self.current_state.caisse(x, y + 2) \
                or not self.current_state.personnage(x, y):
            return False

        new_state = self.current_state.__copy__()
        new_state.caisses.remove((x, y + 1))
        new_state.caisses.append((x, y + 2))
        new_state.personnage_pos = (x, y + 1)
        self.states.append(new_state)
        return True

    def execute(self, actions: str) -> bool:
        """
        exécute une liste d'actions
        """
        for action in actions:
            try:
                res = self.actions[action]()
            except KeyError:
                raise NotRecognizedActionException(
                    f"Action inconnue: {action}\n"
                    +
                    ErrorHelpStrings.NOT_RECOGNIZED_ACTION_HELP
                )
            finally:
                if not res:
                    raise UndoableActionException(
                        f"action {action} at position {self.current_state.personnage_pos} impossible\n"
                        +
                        ErrorHelpStrings.UNDOABLE_ACTION_HELP
                    )
        return True

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

    def solve_bfs(self) -> Optional[str]:
        """
        solve the puzzle using breadth-first search
        """
        self.states = [self.current_state]
        predecessors = {}
        while self.states:
            state = self.states.pop(0)
            if state.is_valid():
                states, actions = self.reconstruct_path(state, predecessors)
                self.states = states
                return actions
            for action in self.actions:
                if self.actions[action]():
                    predecessors[self.current_state] = (state, action)
        return None

    def reconstruct_path(self, state: State, predecessors: Dict[State, Optional[Tuple[State, str]]]) -> Tuple[List[State], str]:
        """
        reconstruct the path from a state to the initial state
        """
        path = ""
        s = state
        states = [s]
        while predecessors[s]:
            path += predecessors[s][1]
            states.append(predecessors[s][0])
            s = predecessors[s][0]
        return states[::-1], path[::-1]
