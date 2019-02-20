# -*- coding: utf8 -*-

import hashlib
import os
import sys
import platform

isPy3 = (sys.version_info.major == 3)

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