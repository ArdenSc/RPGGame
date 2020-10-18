from os import system
from sys import platform


def clear():
    if platform == 'win32':
        system('cls')
    else:
        system('clear')
