""" exceptions for Sokoban """


class ErrorHelpStrings:
    """ Collection of Help texts for exceptions"""
    UNDOABLE_ACTION_HELP = "Vérifiez que les préconditions de l'action sont réunies."
    NOT_RECOGNIZED_ACTION_HELP = "Les actions valides sont: g, G, d, D, h, H, b, B."


class UndoableActionException(Exception):
    """ Custom error thrown when an action is not possible in the current state """
    pass


class NotRecognizedActionException(Exception):
    """ Custom error thrown when an action is not recognized """
    pass
