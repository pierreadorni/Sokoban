""" exceptions for Sokoban """


class ErrorHelpStrings:
    """ Collection of Help texts for exceptions"""
    UNDOABLE_ACTION_HELP = "Vérifiez que les préconditions de l'action sont réunies."
    NOT_RECOGNIZED_ACTION_HELP = "Les actions valides sont: g, G, d, D, h, H, b, B."
    NOT_RECOGNIZED_ALGORITHM_HELP = "Les algorithmes valides sont: bfs."


class UndoableActionException(Exception):
    """ Custom error thrown when an action is not possible in the current state """
    pass


class NotRecognizedActionException(Exception):
    """ Custom error thrown when an action is not recognized """
    pass


class NotRecognizedAlgorithmException(Exception):
    """ Custom error thrown when a solving algorithm is not recognized """
    pass
