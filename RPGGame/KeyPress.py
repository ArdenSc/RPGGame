# Implementation of a cross platform keyboard listener,
# adapted to the game.
# Credits to someone on StackOverflow, I can't find the post.

from RPGGame.Game import StopGame


class GetKeyPress:
    def __init__(self):
        try:
            self.impl = _GetKeyPressWindows()
        except ImportError:
            self.impl = _GetKeyPressUnix()

    def __call__(self):
        ch = self.impl()
        if ch == '\x03':
            raise KeyboardInterrupt
        elif ch == '\x04':
            raise EOFError
        elif ch == 'q':
            raise StopGame
        return ch


class _GetKeyPressWindows:
    def __init__(self):
        from msvcrt import getch
        self.getch = getch

    def __call__(self):
        ch = b''
        while not ch:
            ch = self.getch()
        try:
            return bytes.decode(ch)
        except:
            if ch == b'\x03':
                return '\x03'
            elif ch == b'\x04':
                return '\x04'
            else:
                raise AttributeError('Error getting keypress from Windows')


class _GetKeyPressUnix:
    def __init__(self):
        from sys import stdin
        self.stdin = stdin
        from tty import setraw
        self.setraw = setraw
        from termios import tcgetattr, tcsetattr, TCSADRAIN
        self.tcgetattr, self.tcsetattr = tcgetattr, tcsetattr
        self.TCSADRAIN = TCSADRAIN

    def __call__(self):
        fd = self.stdin.fileno()
        old_settings = self.tcgetattr(fd)
        try:
            self.setraw(fd)
            raw_settings = self.tcgetattr(fd)
            raw_settings[1] = old_settings[1]
            self.tcsetattr(fd, self.TCSADRAIN, raw_settings)
            ch = self.stdin.read(1)
        finally:
            self.tcsetattr(fd, self.TCSADRAIN, old_settings)
        return ch
