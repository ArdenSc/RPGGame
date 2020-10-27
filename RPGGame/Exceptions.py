class StopGame(Exception):
    """Exception to be raised when the game should stop."""
    ...


class WinGame(Exception):
    """Exception to be raised when the game was won."""
    ...


class LoseGame(Exception):
    """Exception to be raised when the game was lost."""
    ...
