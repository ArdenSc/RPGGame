from os import system
from sys import platform


def clear():
    """Cross platform method for clearing the terminal."""
    if platform == 'win32':
        system('cls')
    else:
        system('clear')
