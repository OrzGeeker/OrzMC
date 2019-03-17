# -*- coding: utf8 -*-

import hashlib
import os
import sys
import platform

isPy3 = (sys.version_info.major >= 3)

def checkFileExist(filePath, hash):
    if not os.path.exists(filePath):
        return False
    
    with open(filePath, 'rb') as f:
        computeHash = hashlib.sha1(f.read()).hexdigest()
        ret = (computeHash == hash)
        if not ret:
            print('sha1 check failed: ' + filePath)
        return ret

def makedirs(path):
    if not os.path.exists(path):
        os.makedirs(path)


def platformType():
    '''OS type'''
    system = {
        'Linux':'linux',
        'Darwin':'osx',
        'Windows': 'windows'
    }
    return system[platform.system()]

def hint(msg):
    if isPy3:
        return input(msg)
    else:
        return raw_input(msg)

class ColorString:

    FG_BLACK = 30
    FG_RED = 31
    FG_GREEN = 32
    FG_YELLOW = 33
    FG_BLUE = 34
    FG_PURPLE = 35
    FG_CYAN = 36
    FG_WHITE = 37

    BG_BLACK = 40
    BG_RED = 41
    BG_GREEN = 42
    BG_YELLOW = 43
    BG_BLUE = 44
    BG_PURPLE = 45
    BG_CYAN = 46
    BG_WHITE = 47
    BG_DEFAULT = 0

    DEFUALT = 0
    HIGHLIGHT = 1
    UNDERLINE = 2
    TWINKLE = 3
    INVERSE = 4
    INVISIBLE = 5

    @classmethod
    def string(cls, str, fg = FG_WHITE, bg = BG_DEFAULT, displayMode = DEFUALT):
        if bg == ColorString.BG_DEFAULT:
            return '\033[%s;%sm%s\033[0m' % (displayMode, fg, str)
        else:
            return '\033[%s;%s;%sm%s\033[0m' % (displayMode, fg, bg, str)

    @classmethod
    def warn(cls, str):
        return ColorString.string(str, ColorString.FG_YELLOW, displayMode=ColorString.HIGHLIGHT)

    @classmethod
    def confirm(cls, str):
        return ColorString.string(str, ColorString.FG_GREEN, displayMode=ColorString.HIGHLIGHT)

    @classmethod
    def error(cls, str):
        return ColorString.string(str, ColorString.FG_RED, displayMode=ColorString.HIGHLIGHT)

    @classmethod
    def hint(cls, str):
        return ColorString.string(str, ColorString.FG_RED, displayMode=ColorString.HIGHLIGHT)