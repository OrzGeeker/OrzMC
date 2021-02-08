# -*- coding: utf8 -*-

import hashlib
import os
import platform
import zipfile
import re
import json
import time
from urllib.parse import urlparse, urlunparse

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
    try:
        with zipfile.ZipFile(dstPath, 'w', zipfile.ZIP_DEFLATED, allowZip64=True) as myzip:
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
    except Exception as e:
        print(e)


def loadJSON(filePath):
    with open(filePath) as json_data:
        jsonObj = json.load(json_data)
        return jsonObj

from .CleanUp import CleanUp
def is_sigint_up():
    return CleanUp.is_sigint_up

def convertOggToMap3(source_file_path, target_file_path):
    cmd = 'ffmpeg -i ' + source_file_path + ' ' + target_file_path + ' -y'
    os.system(cmd)  

def changeUrlDomain(url,content):

    parse_result = urlparse(url)
    if parse_result:
        new_url = urlunparse(parse_result._replace(netloc = content))
        return new_url

    return url

def getUrlDomain(url):
    return urlparse(url).netloc

def sleep(seconds):
    time.sleep(seconds)