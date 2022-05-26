""" Classe Sokoban """
from . import State
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

    def execute(self, actions: str):
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
