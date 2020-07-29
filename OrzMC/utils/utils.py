# -*- coding: utf8 -*-

import hashlib
import os
import sys
import platform
import zipfile
import re

def matchAndReplace(pattern, repl, string):

    if platformType() == 'windows':
        repl = repl.replace('\\', '@')

    ret = re.sub(pattern, repl, string)

    if platformType() == 'windows':
        ret = ret.replace('@', '\\')
        
    return ret

def checkFileExist(filePath, hash):
    if not os.path.exists(filePath):
        return False
    ret = (computeHash(filePath) == hash)   
    if not ret:
        # print('sha1 check failed: ' + filePath)
        pass
    return ret

def computeHash(filePath):
    if not os.path.exists(filePath):
        return None
    with open(filePath, 'rb') as f:
        computeHash = hashlib.sha1(f.read()).hexdigest()
        return computeHash

def writeContentToFile(content, filePath):
        if content != None:
            with open(filePath,'w',encoding='utf-8') as f:
                f.write(content)

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
    return input(msg)

def zip(srcPaths, dstPath):
    if len(srcPaths) <= 0:
        return

    with zipfile.ZipFile(dstPath, 'w', zipfile.ZIP_DEFLATED) as myzip:
        for srcPath in srcPaths:
            if os.path.exists(srcPath):
                if os.path.isdir(srcPath):
                    for dirpath, _, filenames in os.walk(srcPath):
                        dir_path = srcPath.replace(os.path.basename(srcPath), '')
                        fpath = dirpath.replace(dir_path, '')
                        fpath = fpath and fpath + os.sep or ''
                        for filename in filenames:
                            source = os.path.join(dirpath,filename)
                            destination = fpath + filename
                            myzip.write(source, destination)
                else:
                    myzip.write(srcPath)