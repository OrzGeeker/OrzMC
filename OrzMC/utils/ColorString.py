# -*- coding: utf8 -*-

from .utils import platformType

from enum import IntEnum

class BGColor(IntEnum):
    BLACK = 40
    RED = 41
    GREEN = 42
    YELLOW = 43
    BLUE = 44
    PURPLE = 45
    CYAN = 46
    WHITE = 47
    DEFAULT = 0
class FGColor(IntEnum):
    BLACK = 30
    RED = 31
    GREEN = 32
    YELLOW = 33
    BLUE = 34
    PURPLE = 35
    CYAN = 36
    WHITE = 37
class DisplayMode(IntEnum):
    DEFUALT = 0
    HIGHLIGHT = 1
    UNDERLINE = 2
    TWINKLE = 3
    INVERSE = 4
    INVISIBLE = 5

class ColorString:

    @classmethod
    def string(cls, str, fg = FGColor.WHITE, bg = BGColor.DEFAULT, displayMode = DisplayMode.DEFUALT):
        if bg == BGColor.DEFAULT:
            return '\033[%s;%sm%s\033[0m' % (displayMode.value, fg.value, str) if platformType() != 'windows' else str
        else:
            return '\033[%s;%s;%sm%s\033[0m' % (displayMode.value, fg.value, bg.value, str) if platformType() != 'windows' else str

    @classmethod
    def warn(cls, str):
        return ColorString.string(str, FGColor.YELLOW, displayMode=DisplayMode.HIGHLIGHT)

    @classmethod
    def confirm(cls, str):
        return ColorString.string(str, FGColor.GREEN, displayMode=DisplayMode.HIGHLIGHT)

    @classmethod
    def error(cls, str):
        return ColorString.string(str, FGColor.RED, displayMode=DisplayMode.HIGHLIGHT)

    @classmethod
    def hint(cls, str):
        return ColorString.string(str, FGColor.YELLOW, displayMode=DisplayMode.HIGHLIGHT)