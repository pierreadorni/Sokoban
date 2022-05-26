""" Classe State """
from typing import Tuple, List


def load_from_string(state_string: str) -> \
        [
            List[Tuple[int, int]],
            List[Tuple[int, int]],
            List[Tuple[int, int]],
            Tuple[int, int],
        ]:
    """
    Charge un état à partir d'une chaîne de caractères.
    """
    murs, buts, caisses, personnage_pos = [], [], [], (0, 0)
    lines = [l for l in state_string.split('\n') if l != '']
    w, h = len(lines[0]), len(lines)
    for y in range(h):
        for x in range(w):
            if lines[y][x] == '%':
                murs.append((x, y))
            elif lines[y][x] == 'b':
                buts.append((x, y))
            elif lines[y][x] == 'c':
                caisses.append((x, y))
            elif lines[y][x] == 'p':
                personnage_pos = (x, y)
            elif lines[y][x] == 'v':
                buts.append((x, y))
                caisses.append((x, y))
            elif lines[y][x] == 'q':
                personnage_pos = (x, y)
                buts.append((x, y))
    return murs, buts, caisses, personnage_pos, (w, h)


class State:
    """
    Classe de représentation d'un état de jeu.
    Doit être initialisée avec une chaîne de caractères correspondant à l'état.
    """

    def __init__(self, state_string: str) -> None:
        self.murs, self.buts, self.caisses, self.personnage_pos, self.map_size = load_from_string(state_string)

    def __copy__(self) -> 'State':
        return State(self.__string__())

    def personnage(self, x: int, y: int) -> bool:
        """
        Renvoie True si le personnage se trouve à la position (x, y).
        """
        return (x, y) == self.personnage_pos

    def but(self, x: int, y: int) -> bool:
        """
        Renvoie True si la case (x, y) est un but.
        """
        return (x, y) in self.buts

    def mur(self, x: int, y: int) -> bool:
        """
        Renvoie True si la case (x, y) est un mur.
        """
        return (x, y) in self.murs

    def caisse(self, x: int, y: int) -> bool:
        """
        Renvoie True si la case (x, y) contient une caisse.
        """
        return (x, y) in self.caisses

    def is_valid(self) -> bool:
        """
        Renvoie True si l'état est valide (toutes les caisses sont sur un but).
        """
        for caisse in self.caisses:
            if caisse not in self.buts:
                return False
        return True

    def __string__(self) -> str:
        text = ''
        for y in range(self.map_size[1]):
            line = ''
            for x in range(self.map_size[0]):
                if self.personnage(x, y) and self.but(x, y):
                    line += 'q'
                elif self.caisse(x, y) and self.but(x, y):
                    line += 'v'
                elif self.personnage(x, y):
                    line += 'p'
                elif self.caisse(x, y):
                    line += 'c'
                elif self.but(x, y):
                    line += 'b'
                elif self.mur(x, y):
                    line += '%'
                else:
                    line += ' '
            text += line + '\n'
        return text

    def __repr__(self) -> str:
        return self.__string__()
